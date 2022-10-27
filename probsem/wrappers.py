import json
import pathlib

from probsem.abstract import Object


class Prompt(Object):
    def __init__(self, prompt: str) -> None:
        super().__init__()
        self._gen_prompt = self._load_prompt(prompt, "gen")
        self._sum_prompt = self._load_prompt(prompt, "sum")

    @staticmethod
    def _load_prompt(prompt: str, version: str) -> str:
        prompt_file = (
            pathlib.Path(__file__).parents[1] / "inputs" / f"{prompt}_{version}.txt"
        )
        with open(prompt_file, "r") as f:
            return f.read()

    @property
    def generator(self) -> str:
        return self._gen_prompt

    @property
    def summarizer(self) -> str:
        return self._sum_prompt


class TestSample(Object):
    def __init__(self, sample: str) -> None:
        super().__init__()
        sample_file = pathlib.Path(__file__).parents[1] / "inputs" / f"{sample}.json"
        with open(sample_file, "r") as f:
            self._sample = json.loads(f.read())

    @property
    def query(self) -> str:
        return self._sample["query"]

    @property
    def programs(self) -> list:
        return self._sample["programs"]
