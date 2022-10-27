import numpy as np

from probsem.wrappers import TestSample


def pretty_print(query: str, programs: list, probs: np.ndarray) -> None:
    assert len(programs) == len(probs)
    ostream = []
    ostream.append(f"Query:\t{query}")
    for i, (program, prob) in enumerate(zip(programs, probs)):
        ostream.append(f"Program {i + 1}:\t{program}")
        ostream.append(f"Probability:\t{prob}")
    return "\n".join(ostream)
