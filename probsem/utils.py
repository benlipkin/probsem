import typing

import nltk
import numpy as np
import numpy.typing as npt


def tokenize(text: str) -> typing.List[str]:
    text = text.replace("\n", " NEWLINE ").replace("'", " ` ")
    tokens = nltk.tokenize.treebank.TreebankWordTokenizer().tokenize(text)
    tokens = [t.replace("NEWLINE", "\n").replace("`", "'") for t in tokens]
    return tokens


def detokenize(text: str) -> str:
    return text.replace("; ;", ";;").replace("( ", "(").replace(" )", ")")


def normalize(weights: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    return np.exp(weights) / np.sum(np.exp(weights))


def pretty_print_sample(sample: typing.Dict[str, typing.Any]) -> str:
    ostream = []
    ostream.append("\nText:")
    ostream.append(f"{sample['text'][0]}")
    ostream.append("\nScores:")
    for _, (program, score) in enumerate(zip(sample["programs"], sample["scores"])):
        ostream.append(f"{score:.3f}\t{program}")
    result = (
        "TEST SAMPLE PASSED."
        if np.argmax(sample["scores"]) == sample["correct"]
        else "TEST SAMPLE FAILED."
    )
    ostream.append("\n" + result + "\n")
    return "\n".join([30 * "_"] + ostream + [30 * "_"])


def pretty_print_summary(accuracy: np.float64) -> str:
    ostream = []
    ostream.append(f"TEST SUITE ACCURACY:\t{accuracy:.3f}")
    return "\n".join([30 * "_"] + ostream + [30 * "_"])
