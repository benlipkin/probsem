import typing

import nltk
import numpy as np
import numpy.typing as npt


def tokenize(text: str) -> typing.List[str]:
    text = text.replace("\n", " NEWLINE ").replace("'", " ` ")
    tokens = nltk.tokenize.treebank.TreebankWordTokenizer().tokenize(text)
    tokens = [token.replace("NEWLINE", "\n") for token in tokens]
    return tokens


def detokenize(text: str) -> str:
    text = text.replace("` ", "'").replace("; ;", ";;")
    text = text.replace("( ", "(").replace(" )", ")")
    return text


def strip_program(program: str) -> str:
    program = program.strip()
    count = 0
    for i, char in enumerate(program):
        if char == "(":
            count += 1
        elif char == ")":
            count -= 1
        if count == 0:
            return program[: i + 1]
    return "INVALID PROGRAM"


def normalize(weights: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    return np.exp(weights) / np.sum(np.exp(weights))


def pretty_print(
    query: str, programs: typing.List[str], logits: npt.NDArray[np.float64], mode: str
) -> str:
    assert len(programs) == len(logits)
    ostream = []
    ostream.append(f"Query:\t{query}")
    for i, (program, prob) in enumerate(zip(programs, normalize(logits))):
        ostream.append(f"Program {i + 1}:\t{program}")
        ostream.append(f"{mode.title()}:\tp={prob:.2f}")
    if mode == "posterior":
        ostream.append(f"MAP Program:\t{programs[np.argmax(logits)]}")
    return "\n".join([30 * "_"] + ostream + [30 * "_"])
