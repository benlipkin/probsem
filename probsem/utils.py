import re
import typing

import nltk
import numpy as np
import numpy.typing as npt


def sanitize_filename(text: str) -> str:
    return re.sub(r"^[ .]|[/<>:\"\\|?*]+|[ .]$", "-", text)


def tokenize(text: str) -> typing.List[str]:
    text = text.replace("\n", " NEWLINE ").replace("'", " ` ")
    tokens = nltk.tokenize.treebank.TreebankWordTokenizer().tokenize(text)
    tokens = [t.replace("NEWLINE", "\n").replace("`", "'") for t in tokens]
    return tokens


def normalize(weights: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    return np.exp(weights) / np.sum(np.exp(weights))


def print_sample(sample: typing.Dict[str, typing.Any]) -> str:
    ostream = []
    ostream.append("\nText:")
    ostream.append(f"{sample['text'][0]}")
    ostream.append("\nScores:")
    for _, (query, score) in enumerate(zip(sample["queries"], sample["scores"])):
        ostream.append(f"{score:.3f}\t{query}")
    if sample["correct"] == -1:
        ostream.append("")
    elif np.argmax(sample["scores"]) == sample["correct"]:
        ostream.append("\n" + "TEST SAMPLE PASSED." + "\n")
    else:
        ostream.append("\n" + "TEST SAMPLE FAILED." + "\n")
    return "\n".join([30 * "_"] + ostream + [30 * "_"])


def print_summary(samples: typing.List[typing.Dict[str, typing.Any]]) -> str:
    scores = np.array([s["scores"] for s in samples])
    indices = np.array([s["correct"] for s in samples])
    if -1 in indices:
        accuracy = np.float64(np.nan)
    else:
        correct = scores[np.arange(indices.size), indices] == scores.max(axis=1)
        accuracy = correct.mean()
    ostream = []
    ostream.append(f"TEST SUITE ACCURACY:\t{accuracy:.3f}")
    return "\n".join([30 * "_"] + ostream + [30 * "_"])
