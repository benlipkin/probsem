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
            parts = [self._pretext, example["text"], self._posttext, self._queries[i]]
            parts = [p for p in parts if p != ""]
            return "\n".join(parts)

        for example in self._context:
            index = example["expected"]
            samples = [_sample(i) for i in range(len(self._queries))]
            yield index, samples

    @property
    def n_examples(self) -> int:
        return len(self._context)

    @property
    def n_queries(self) -> int:
        return len(self._queries)

    @property
    def _pretext(self) -> str:
        assert "pretext" in self._suite
        assert isinstance(self._suite["pretext"], str)
        return self._suite["pretext"]

    @property
    def _context(self) -> typing.List[typing.Dict[str, typing.Any]]:
        assert "context" in self._suite
        assert isinstance(self._suite["context"], list)
        assert len(self._suite["context"]) > 0
        assert all(isinstance(c, dict) for c in self._suite["context"])
        assert all(("text" in c) and ("expected" in c) for c in self._suite["context"])
        assert all(isinstance(c["text"], str) for c in self._suite["context"])
        assert all(isinstance(c["expected"], int) for c in self._suite["context"])
        return self._suite["context"]

    @property
    def _posttext(self) -> str:
        assert "posttext" in self._suite
        assert isinstance(self._suite["posttext"], str)
        return self._suite["posttext"]

    @property
    def _queries(self) -> list[str]:
        assert "queries" in self._suite
        assert isinstance(self._suite["queries"], list)
        assert all(isinstance(p, str) for p in self._suite["queries"])
        return self._suite["queries"]

    def _load(self, prompt: str, suite: str) -> dict:
        suite_file = (
            pathlib.Path(__file__).parents[1] / "inputs" / f"{prompt}_{suite}.json"
        )
        with open(suite_file, "r", encoding="utf-8") as fstream:
            return json.load(fstream)
