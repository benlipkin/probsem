import typing

import numpy as np
from tqdm import tqdm

from probsem.abstract import Object
from probsem.benchmarks import Prompt, TestSuite
from probsem.models import Model
from probsem.utils import normalize, pretty_print


class ProbSem(Object):
    def __init__(self, prompt: str, suite: str, model: str) -> None:
        super().__init__()
        self._prompt = Prompt(prompt)
        self._suite = TestSuite(prompt, suite)
        self._model = Model(model)

    @property
    def _samples(self) -> typing.Iterable[typing.Dict[str, typing.Any]]:
        for pos_sample, neg_sample in self._suite.samples:
            yield {
                "text": "\n".join(pos_sample.split("\n")[:-1]),
                "pos_full": "\n".join([self._prompt.text, pos_sample]),
                "neg_full": "\n".join([self._prompt.text, neg_sample]),
                "pos_eval": pos_sample.split("\n")[-1],
                "neg_eval": neg_sample.split("\n")[-1],
            }

    @staticmethod
    def _normalize_weights(sample):
        sample["pos_score"], sample["neg_score"] = normalize(
            np.array([sample["pos_weight"], sample["neg_weight"]])
        )

    def run(self) -> None:
        for sample in tqdm(self._samples, total=self._suite.n_examples):
            sample["pos_weight"] = self._model.score(
                sample["pos_full"], sample["pos_eval"]
            )
            sample["neg_weight"] = self._model.score(
                sample["neg_full"], sample["neg_eval"]
            )
            self._normalize_weights(sample)
            self.info(pretty_print(sample))
