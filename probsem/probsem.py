import multiprocessing
import typing

import joblib
import numpy as np
import numpy.typing as npt
from tqdm import tqdm

from probsem.abstract import Object
from probsem.models import Model
from probsem.utils import pretty_print
from probsem.wrappers import Prompt, TestSample


class ProbSem(Object):
    def __init__(
        self,
        prompt: str,
        sample: str,
        model: str,
    ) -> None:
        super().__init__()
        self._prompt = Prompt(prompt)
        self._sample = TestSample(sample)
        self._model = Model(model)
        if len(self.programs) == 0:
            self._generate_programs()
        assert len(self.programs) > 0

    @property
    def generator(self) -> str:
        return self._prompt.generator

    @property
    def summarizer(self) -> str:
        return self._prompt.summarizer

    @property
    def query(self) -> str:
        return self._sample.query

    @property
    def programs(self) -> typing.List[str]:
        return self._sample.programs

    @property
    def model(self) -> Model:
        return self._model

    def _generate_programs(self) -> None:
        self.info("Generating programs...")
        context = "\n".join([self.generator, self.query, ""])
        with joblib.parallel_backend("loky", n_jobs=multiprocessing.cpu_count()):
            programs = joblib.Parallel()(
                joblib.delayed(self._model.generate)(context, bool(i))
                for i in tqdm(list(range(self._sample.samples)))
            )
        for program in programs:
            self._sample.add_program(program)

    def _score(self, mode: str, program: str, i: int) -> typing.Tuple[int, np.float64]:
        if mode == "prior":
            full_text = "\n".join([self.generator, self.query, program])
            score = self.model.score(full_text, program, temperature=0.1)
        elif mode == "likelihood":
            full_text = "\n".join([self.summarizer, program, self.query])
            score = self.model.score(full_text, self.query, temperature=0.5)
        else:
            raise ValueError(f"Unknown mode: {mode}")
        return i, score

    def evaluate(self, mode: str) -> npt.NDArray[np.float64]:
        weights = np.zeros(len(self.programs))
        self.info(f"Evaluating {mode}...")
        with joblib.parallel_backend("loky", n_jobs=multiprocessing.cpu_count()):
            scores = joblib.Parallel()(
                joblib.delayed(self._score)(mode, program, i)
                for i, program in tqdm(enumerate(list(self.programs)))
            )
        for i, score in scores:
            weights[i] = score
        return weights

    def _log_results(self, mode: str, results: npt.NDArray[np.float64]) -> None:
        self.info(pretty_print(self.query, self.programs, results, mode))

    def run(self) -> None:
        prior = self.evaluate("prior")
        self._log_results("prior", prior)
        likelihood = self.evaluate("likelihood")
        self._log_results("likelihood", likelihood)
        self.info("Calculating posterior...")
        posterior = prior + likelihood
        self._log_results("posterior", posterior)
