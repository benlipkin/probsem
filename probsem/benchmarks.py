import json
import pathlib
import typing

from probsem.abstract import Object


class Prompt(Object):
    def __init__(self, prompt: str) -> None:
        super().__init__()
        self._text = self._load(prompt)

    @property
    def text(self) -> str:
        return self._text

    def _load(self, prompt: str) -> str:
        prompt_file = pathlib.Path(__file__).parents[1] / "inputs" / f"{prompt}.txt"
        with open(prompt_file, "r", encoding="utf-8") as fstream:
            return fstream.read()


class TestSuite(Object):
    def __init__(self, prompt: str, suite: str) -> None:
        super().__init__()
        self._suite = self._load(prompt, suite)

    @property
    def samples(self) -> typing.Iterator[typing.Tuple[int, typing.List[str]]]:
        def _sample(i: int) -> str:
            if self._query == ";;":
                parts = [self._premise, example["text"], self._programs[i]]
            else:
                parts = [self._premise, example["text"], self._query, self._programs[i]]
            return "\n".join(parts)

        for example in self._context:
            index = example["expected"]
            samples = [_sample(i) for i in range(len(self._programs))]
            yield index, samples

    @property
    def n_examples(self) -> int:
        return len(self._context)

    @property
    def n_programs(self) -> int:
        return len(self._programs)

    @property
    def _premise(self) -> str:
        assert "premise" in self._suite
        assert isinstance(self._suite["premise"], str)
        assert self._suite["premise"][:2] == ";;"
        return self._suite["premise"]

    @property
    def _context(self) -> typing.List[typing.Dict[str, typing.Any]]:
        assert "context" in self._suite
        assert isinstance(self._suite["context"], list)
        assert len(self._suite["context"]) > 0
        assert all(isinstance(c, dict) for c in self._suite["context"])
        assert all(("text" in c) and ("expected" in c) for c in self._suite["context"])
        assert all(isinstance(c["text"], str) for c in self._suite["context"])
        assert all(c["text"][:2] == ";;" for c in self._suite["context"])
        assert all(isinstance(c["expected"], int) for c in self._suite["context"])
        return self._suite["context"]

    @property
    def _query(self) -> str:
        assert "query" in self._suite
        assert isinstance(self._suite["query"], str)
        assert self._suite["query"][:2] == ";;"
        return self._suite["query"]

    @property
    def _programs(self) -> list[str]:
        assert "programs" in self._suite
        assert isinstance(self._suite["programs"], list)
        assert all(isinstance(p, str) for p in self._suite["programs"])
        assert all((p[0] == "(") and (p[-1] == ")") for p in self._suite["programs"])
        return self._suite["programs"]

    def _load(self, prompt: str, suite: str) -> dict:
        suite_file = (
            pathlib.Path(__file__).parents[1] / "inputs" / f"{prompt}_{suite}.json"
        )
        with open(suite_file, "r", encoding="utf-8") as fstream:
            return json.load(fstream)
