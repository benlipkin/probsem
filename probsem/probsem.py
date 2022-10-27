import numpy as np

from probsem.abstract import Object
from probsem.models import Model
from probsem.utils import pretty_print
from probsem.wrappers import Prompt, TestSample


class ProbSem(Object):
    def __init__(
        self,
        prompt: str,
        sample: str,
        model: str = "Salesforce/codegen-350M-multi",
    ) -> None:
        super().__init__()
        self._prompt = Prompt(prompt)
        self._sample = TestSample(sample)
        self._model = Model(model)

    @property
    def prompt(self) -> Prompt:
        return self._prompt

    @property
    def query(self) -> str:
        return self._sample.query

    @property
    def programs(self) -> list:
        return self._sample.programs

    def evaluate(self, mode: str) -> np.ndarray:
        assert mode in ["prior", "likelihood"]
        weights = np.zeros(len(self.programs))
        for i, eval in enumerate(self.programs):
            if mode == "prior":
                input = "\n".join([self.prompt.generator, self.query, eval])
                weights[i] = self._model.score(input, eval)
            elif mode == "likelihood":
                input = "\n".join([self.prompt.summarizer, eval, self.query])
                weights[i] = self._model.score(input, self.query)
            else:
                raise ValueError(f"Unknown mode: {mode}")
        return weights

    def marginalize(self, weights: np.ndarray) -> np.ndarray:
        return np.exp(weights) / np.sum(np.exp(weights))

    def run(self) -> None:
        prior = self.evaluate("prior")
        likelihood = self.evaluate("likelihood")
        posterior_weights = prior + likelihood
        posterior_probs = self.marginalize(posterior_weights)
        self.info(pretty_print(self.query, self.programs, posterior_probs))
