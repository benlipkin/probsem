import pytest

from probsem.probsem import ProbSem


@pytest.mark.parametrize(
    "prompt, suite, model, rerank",
    [
        pytest.param("test", "A", "Salesforce/codegen-350M-mono",True),
    ],
)
def test_run(prompt, suite, model,rerank):
    ProbSem(
        prompt=prompt,
        suite=suite,
        model=model,
        rerank=rerank
    ).run()
