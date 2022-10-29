import typing

import numpy as np
import numpy.typing as npt


def normalize(weights: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    return np.exp(weights) / np.sum(np.exp(weights))


def pretty_print(
    query: str, programs: typing.List[str], results: npt.NDArray[np.float64], mode: str
) -> str:
    assert len(programs) == len(results)
    ostream = []
    ostream.append(f"Query:\t{query}")
    for i, (program, logit, prob) in enumerate(
        zip(programs, results, normalize(results))
    ):
        ostream.append(f"Program {i + 1}:\t{program}")
        ostream.append(f"{mode.title()}:\t{prob:.3f} ({logit:.3f})")
    if mode == "posterior":
        ostream.append(f"MAP Program:\t{programs[np.argmax(results)]}")
    return "\n".join(ostream + [""])
