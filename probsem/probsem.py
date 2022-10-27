import typing

import numpy as np
import numpy.typing as npt

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
    def programs(self) -> typing.List[str]:
        return self._sample.programs

    def evaluate(self, mode: str) -> npt.NDArray[np.float64]:
        assert mode in ["prior", "likelihood"]
        weights = np.zeros(len(self.programs))
        for i, program in enumerate(self.programs):
            if mode == "prior":
                full_text = "\n".join([self.prompt.generator, self.query, program])
                weights[i] = self._model.score(full_text, program)
            elif mode == "likelihood":
                full_text = "\n".join([self.prompt.summarizer, program, self.query])
                weights[i] = self._model.score(full_text, self.query)
            else:
                raise ValueError(f"Unknown mode: {mode}")
        return weights

    def marginalize(self, weights: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        return np.exp(weights) / np.sum(np.exp(weights))

    def run(self) -> None:
        prior = self.evaluate("prior")
        likelihood = self.evaluate("likelihood")
        posterior_weights = prior + likelihood
        posterior_probs = self.marginalize(posterior_weights)
        self.info(pretty_print(self.query, self.programs, posterior_probs))
