import pytest

from probsem.probsem import ProbSem


@pytest.mark.parametrize(
    "prompt, suite, model",
    [
        pytest.param("test", "A", "Salesforce/codegen-350M-mono"),
    ],
)
def test_run(prompt, suite, model):
    ProbSem(
        prompt=prompt,
        suite=suite,
        model=model,
    ).run()
