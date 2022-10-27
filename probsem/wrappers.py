import json
import pathlib

from probsem.abstract import Object


class Prompt(Object):
    def __init__(self, prompt: str) -> None:
        super().__init__()
        prompt_file = pathlib.Path(__file__).parents[1] / "inputs" / f"{prompt}.txt"
        with open(prompt_file, "r") as f:
            self._prompt = f.read()

    @property
    def text(self) -> str:
        return self._prompt


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
