import functools
import hashlib
import pathlib
import time
import typing
import warnings

import diskcache
import numpy as np
import openai
import torch

from transformers import AutoConfig, AutoTokenizer, AutoModelForCausalLM

from probsem.abstract import Object, IModel

openai.api_key_path = str(pathlib.Path.home() / ".openai_api_key")


class Model(Object):
    def __init__(
        self, model_id: str, norm: bool, temp: float, cache_dir: pathlib.Path
    ) -> None:
        super().__init__()
        self._id = model_id
        self._norm = norm
        if temp <= 0:
            raise ValueError("Temperature must be positive.")
        self._temp = temp
        self._model: IModel
        openai_engines = [engine["id"] for engine in openai.Engine.list()["data"]]
        if self._id in openai_engines:
            self.info("Model ID found in OpenAI engines.")
            setattr(self, "_model", OpenAIModel(self._id))
        else:
            self.info("Model ID not found in OpenAI engines. Checking HuggingFace.")
            setattr(self, "_model", HuggingFaceModel(self._id))
        self._cache = diskcache.Cache(cache_dir)

    def score(
        self,
        full_text: str,
        eval_text: str,
    ) -> np.float64:
        key_id = "_".join([self._id, full_text, eval_text])
        key = hashlib.sha256(key_id.encode("utf-8")).hexdigest()
        if key in self._cache:
            logp, num_eval = self._cache[key]
        else:
            logp, num_eval = self._model.score(full_text, eval_text)
            self._cache[key] = logp, num_eval
        if self._norm:
            logp /= num_eval
        return logp / self._temp


class OpenAIModel(Object, IModel):
    def __init__(self, model_id: str) -> None:
        super().__init__()
        self._id = model_id
        self.info(f"Selected OpenAI {self._id} model.")

    def _get_response(
        self, text: str, retry_after=10
    ) -> openai.openai_object.OpenAIObject:
        try:
            return openai.Completion.create(
                engine=self._id,
                prompt=text,
                max_tokens=0,
                logprobs=0,
                echo=True,
            )
        except (openai.error.RateLimitError, openai.error.APIError) as e:
            self.warn(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
            time.sleep(retry_after)
            return self._get_response(text, retry_after * 2)

    def score(self, full_text: str, eval_text: str) -> typing.Tuple[np.float64, int]:
        full_resp = self._get_response(full_text)
        try:
            eval_resp = self._get_response(eval_text)
            num_eval = eval_resp["usage"]["total_tokens"]
        except openai.error.InvalidRequestError:
            num_eval = 1 if eval_text else 0
        logp = np.sum(full_resp["choices"][0]["logprobs"]["token_logprobs"][-num_eval:])
        return logp, num_eval


class HuggingFaceModel(Object, IModel):
    def __init__(self, model_id: str) -> None:
        super().__init__()
        self._id = model_id
        self.info(f"Attempting to load HuggingFace {self._id} model...")
        try:
            self._config = AutoConfig.from_pretrained(self._id)
            self._tokenizer = AutoTokenizer.from_pretrained(
                self._id, add_prefix_space=True
            )
            self._model = AutoModelForCausalLM.from_pretrained(
                self._id, torch_dtype=torch.float32, low_cpu_mem_usage=True
            )
            self._model.eval()
        except Exception as invalid_id:
            raise ValueError(
                "model must be valid HuggingFace CausalLM."
            ) from invalid_id
        self._set_torch_device()
        self.info(f"Successfully loaded pretrained {self._id} model on {self._device}.")

    def _set_torch_device(self) -> None:
        if torch.cuda.is_available():
            self._device = torch.device("cuda")
            torch.set_default_tensor_type(torch.cuda.FloatTensor)  # type: ignore
            try:
                self._model = self._model.to(self._device)
                return
            except RuntimeError:
                self._device = torch.device("cpu")
                torch.set_default_tensor_type(torch.FloatTensor)
                self._model = self._model.to(self._device)
        else:
            self._device = torch.device("cpu")
            torch.set_default_tensor_type(torch.FloatTensor)
            self._model = self._model.to(self._device)

    @functools.lru_cache(maxsize=128)
    def _encode_text(self, text: str) -> typing.Dict[str, torch.Tensor]:
        return self._tokenizer(text, return_tensors="pt").to(self._device)

    def _decode_text(self, tokens: torch.Tensor) -> str:
        return self._tokenizer.decode(tokens, skip_special_tokens=True)

    def score(self, full_text: str, eval_text: str) -> typing.Tuple[np.float64, int]:
        with torch.no_grad():
            inputs = self._encode_text(full_text)
            num_eval = self._encode_text(eval_text)["input_ids"].shape[1]
            tokens = inputs["input_ids"]
            mask = inputs["attention_mask"]
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                outputs = self._model(input_ids=tokens, attention_mask=mask)
            loss = torch.nn.CrossEntropyLoss(reduction="none")(
                outputs.logits[..., :-1, :]
                .contiguous()
                .view(-1, outputs.logits.size(-1)),
                tokens[..., 1:].contiguous().view(-1),
            ).view(tokens.size(0), tokens.size(-1) - 1)
            loss = loss * mask[..., 1:].contiguous()
            loss = loss[:, -num_eval:].sum(dim=1)
            logp = -loss.cpu().detach().item()
            return logp, num_eval
