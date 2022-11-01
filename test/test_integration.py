from probsem.probsem import ProbSem


def test_run():
    ProbSem(
        prompt="prompt",
        sample="sample",
        model="Salesforce/codegen-2B-mono",
    ).run()
