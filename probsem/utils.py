import typing

import numpy as np
import numpy.typing as npt


def pretty_print(
    query: str, programs: typing.List[str], probs: npt.NDArray[np.float64]
) -> str:
    assert len(programs) == len(probs)
    ostream = []
    ostream.append(f"Query:\t{query}")
    for i, (program, prob) in enumerate(zip(programs, probs)):
        ostream.append(f"Program {i + 1}:\t{program}")
        ostream.append(f"Probability:\t{prob}")
    ostream.append(f"MAP Program:\t{programs[np.argmax(probs)]}")
    return "\n".join(ostream)
