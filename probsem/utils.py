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


def normalize(weights: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    return np.exp(weights) / np.sum(np.exp(weights))


def pretty_print_sample(sample: typing.Dict[str, typing.Any]) -> str:
    ostream = []
    ostream.append("Text:")
    ostream.append(f"{sample['text']}")
    ostream.append("Scores:")
    ostream.append(f"{sample['pos_score']:.3f}\t{sample['pos_eval']}")
    ostream.append(f"{sample['neg_score']:.3f}\t{sample['neg_eval']}")
    return "\n".join([30 * "_"] + ostream + [30 * "_"])


def pretty_print_summary(mean_accuracy: np.float64, mean_score: np.float64) -> str:
    ostream = []
    ostream.append(f"TEST SUITE ACCURACY:\t{mean_accuracy:.3f}")
    ostream.append(f"TEST SUITE SCORE:\t{mean_score:.3f}")
    return "\n".join([30 * "_"] + ostream + [30 * "_"])
