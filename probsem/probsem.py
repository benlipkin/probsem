import numpy as np

from probsem.abstract import Object
from probsem.models import Model
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
    def prompt(self) -> str:
        return self._prompt.text

    @property
    def query(self) -> str:
        return self._sample.query

    @property
    def programs(self) -> list:
        return self._sample.programs

    def run(self) -> None:
        program_weights = np.zeros(len(self.programs))
        for i, eval in enumerate(self.programs):
            input = "\n".join([self.prompt, self.query, eval])
            program_weights[i] = self._model.score(input, eval)
        program_dist = np.exp(program_weights) / np.sum(np.exp(program_weights))
        self.info(f"Program distribution: {program_dist}")
