import pytest

from probsem.probsem import ProbSem


@pytest.mark.parametrize(
    "prompt, benchmark, model",
    [pytest.param("test", "A", "Salesforce/codegen-350M-mono")],
)
def test_run(prompt, benchmark, model):
    ProbSem(prompt=prompt, test=benchmark, model=model).run()
