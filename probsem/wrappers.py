import json
import pathlib
import typing

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
        with open(prompt_file, "r", encoding="utf-8") as fstream:
            return fstream.read()

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
        with open(sample_file, "r", encoding="utf-8") as fstream:
            self._sample = json.loads(fstream.read())
        assert "query" in self._sample.keys()
        if not ("programs" in self._sample.keys() or "samples" in self._sample.keys()):
            raise RuntimeError(
                'Test sample must specify "programs" or number of "samples".'
            )
        if "samples" in self._sample.keys():
            assert isinstance(self._sample["samples"], int)
            assert self._sample["samples"] > 0
            self._sample["programs"] = []
        else:
            assert "programs" in self._sample.keys()
            assert isinstance(self._sample["programs"], list)
            assert len(self._sample["programs"]) > 0
            self._sample["samples"] = 0

    @property
    def query(self) -> str:
        return self._sample["query"]

    @property
    def programs(self) -> typing.List[str]:
        return self._sample["programs"]

    @property
    def samples(self) -> int:
        return self._sample["samples"]

    def add_program(self, program: str) -> None:
        self._sample["programs"].append(program)
