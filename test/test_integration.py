import pytest

from probsem.probsem import ProbSem


@pytest.mark.parametrize("sample", [pytest.param("sample_1"), pytest.param("sample_2")])
def test_run(sample):
    ProbSem(
        prompt="prompt",
        sample=sample,
        model="Salesforce/codegen-2B-mono",
    ).run()
