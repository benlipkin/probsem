# Benchmark Walkthrough

As explained in the [README.md](https://github.com/benlipkin/probsem/blob/main/README.md), evaluations of new benchmarks require materials to be prepared in a certain form. The critical components are a `Prompt` and at least one `TestSuite`.

## Prompts

Your prompt should define any general context you'd like to be prepended to all your evaluations. This often includes a description of the domain of interest, general instructions, sometimes few shot examples, and generally any text that should be available to your model across your evaluations. 

For example, for a reading comprehension task, an introduction, the passage itself, and some task instructions to answer questions might be included. See `inputs/test.txt` for an example.

```
This next section will involve a reading comprehension test. 

Please read the following paragraph, and answer any questions that follow.

The following was sourced from the top of https://en.wikipedia.org/wiki/Wikipedia:Large_language_models on 01/30/2023

"""
Large language models (LLMs) such as GPT-3 are increasingly being used to generate text.
These tools should be used with care, since they can generate content that is biased, non-verifiable, constitutes original research, or fails to follow our other policies and guidelines.
Editors retain full responsibility for LLM-assisted edits, which should still comply with all relevant Wikipedia policies.
While the use of LLMs is not prohibited, their use should be reserved to experienced editors, who should carefully scrutinize their LLM-assisted edits before hitting Publish. 
The use of such programs to create whole articles or generate passages from scratch is forbidden.
Furthermore, LLM use must be declared in the edit summary.
"""

Based on the above paragraph, please answer the following questions.

```

## TestSuites

Next, you can develop a series of test suites to evaluate individual collections of test cases for a prompt. For example, for our reading comprehension task, each unique class of question about our passage would typically be placed in a separate test suite.

Within each test suite JSON file, there are several components: the `pretext`, `context`, `posttext`, and `queries`. Following the prompt, the `pretext` is the next thing concatenated to an LLM evaluation. It provides any test suite specific instructions or specifications. For example, two test suites might require two different question formats, one T/F and one multiple-choice. The `posttext`, which wraps the `context` on the other side, is also static across a test suite. Both `pretext` and `posttext` are optional, and can be left as an empty string `""` if not needed. 

The core manipulation of any test suite is in the `context` and the `queries`. For a given test suite, the full cross-product of these is evaluated. For example, a user might specify several unique questions, but want to evaluate the labels `True` vs. `False` for each of them. Pasted below is an example from `inputs/test_A.json` that does just this.

```json
{
    "pretext": "The following questions are based on the above text, and should be answered True or False.",
    "context": [
        {
            "text": "The author is discussing the role of LLMs in Wikipedia editing.", 
            "expected": 0
        }, {
            "text": "LLM use for wikipedia editing is accepted without restrictions.", 
            "expected": 1
        }
    ],
    "posttext": "The correct answer is:",
    "queries": [
        "True",
        "False"
    ]
}
```

As you can see, for a single pretext and posttext, a variety of questions of similar form can be iterated over in context, and for each, logit scores or a normalized probability distribution over the queries can be returned. 

You may also note that each context example includes an integer under the `expected` key. This integer maps to the index of the query expected to have the maximum score. This allows for automatic accuracy evaluation. If, however, there is no ground-truth answer, this value can be substituted with `-1`, which disables automated scoring. 

Let's check out `inputs/test_B.json` next, which poses a different question format and has no a-priori correct answer.

```json
{
    "pretext": "The following questions are based on the above text, and should be answered via Multiple Choice response.",
    "context": [
        {
            "text": "Based on the above passage, the author believes that LLM use for writing is as a whole:\nA) Only positive.\nB) Mostly positive.\nC) Mostly negative.\nD) Only negative.", 
            "expected": -1
        }
    ],
    "posttext": "The correct answer is:",
    "queries": [
        "A",
        "B",
        "C",
        "D"
    ]
}
```

As shown above, the text of the `pretext`, `context`, `posttext`, or any of the `queries` may also be a multiline entry. However, for JSON parsing purposes, these must be written on a single line, and the character `\n` used explicitly to represent any line breaks.

Now try making your own:

```bash
nano inputs/prompt.txt
nano inputs/prompt_testsute.json
```