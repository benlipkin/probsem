import typing

import numpy as np
from tqdm import tqdm

from probsem.abstract import Object
from probsem.benchmarks import Prompt, TestSuite
from probsem.models import Model
from probsem.utils import normalize, pretty_print_sample, pretty_print_summary


class ProbSem(Object):
    def __init__(self, prompt: str, suite: str, model: str) -> None:
        super().__init__()
        self._prompt = Prompt(prompt)
        self._suite = TestSuite(prompt, suite)
        self._model = Model(model)

    @property
    def _samples(self) -> typing.Iterable[typing.Dict[str, typing.Any]]:
        for index, samples in self._suite.samples:
            iterator = range(len(samples))
            yield {
                "prompt": [self._prompt.text for _ in iterator],
                "text": ["\n".join(samples[i].split("\n")[:-1]) for i in iterator],
                "programs": [samples[i].split("\n")[-1] for i in iterator],
                "correct": index,
            }

    def _score(self, prompt: str, text: str, program: str) -> np.float64:
        full_text = "\n".join([prompt, text, program])
        return self._model.score(full_text, program)

    @staticmethod
    def _summarize(samples: typing.List[typing.Dict[str, typing.Any]]) -> np.float64:
        scores = np.array([s["scores"] for s in samples])
        indices = np.array([s["correct"] for s in samples])
        if -1 in indices:
            return np.float64(np.nan)
        correct = scores[np.arange(indices.size), indices] == scores.max(axis=1)
        accuracy = correct.mean()
        return accuracy

    def run(self) -> None:
        samples = []
        for sample in tqdm(self._samples, total=self._suite.n_examples):
            assert len(set(sample["prompt"])) == 1
            assert len(set(sample["text"])) == 1
            assert len(set(sample["programs"])) == self._suite.n_programs
            sample["weights"] = []
            for prompt, text, program in zip(
                sample["prompt"], sample["text"], sample["programs"]
            ):
                sample["weights"].append(self._score(prompt, text, program))
            sample["weights"] = np.array(sample["weights"])
            sample["scores"] = normalize(sample["weights"])
            samples.append(sample)
            self.info(pretty_print_sample(sample))
        self.info(pretty_print_summary(self._summarize(samples)))
