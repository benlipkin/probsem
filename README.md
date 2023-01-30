[![Tests](https://github.com/benlipkin/probsem/actions/workflows/testing.yml/badge.svg)](https://github.com/benlipkin/probsem/actions/workflows/testing.yml)

# ProbSem

## Summary

This repository provides a framework to leverage large language models (LLMs) to assign context-conditional probability distributions over queried strings.

It is intended to be flexible and support a wide range of use cases including linguistic minimal pairs, multiple-choice QA, semantic parsing, and program synthesis.

Here are a few examples:

```bash
.. prompt, task instructions ..
Context:    The color of the Boston sky during January is:
Query1:     Blue  # P=0.4
Query2:     Gray  # P=0.6
```

```bash
.. prompt, task instructions ..
Context:    The girl pushed the boy.
Posttext:   Which of the following logically entails?
            A: The girl was pushed by the boy.
            B: The boy was pushed by the boy.
            C: The boy was pushed by the girl.
            D: The girl was pushed by the girl.
            The correct response is:
Query1:     A   # P=0.03
Query2:     B   # P=0.01
Query3:     C   # P=0.95
Query4:     D   # P=0.01
```

```scheme
.. prompt, task instructions ..
Pretext:    ;; Player strengths were distributed ~N(50,20)
Context:    ;; Jack has nearly average strength.
Query1:     (= (abs (- (strength 'jack) 50)) 0)   ;; P=0.1
Query2:     (< (abs (- (strength 'jack) 50)) 10)  ;; P=0.9
``` 

```python
.. prompt, task instructions ..
Context:    def reverse(lst:list):
Query1:       return lst[::-1]      # P=0.40
Query2:       return reversed(lst)  # P=0.30
Query3:       lst.reverse()         # P=0.20
Query4:       list.reverse(lst)     # P=0.10
```

In each of these examples, a user may define a flexible frame of reference using the concatenation of a `prompt`, `context`, and optional `pretext` and `posttext`, which wrap the `context`, to derive a probability distribution over possible completions defined as `queries`. The precise formulation of such evaluations can be explored further by viewing the examples in the `inputs` folder.

_NOTE: The name of this repository `ProbSem` is a legacy reference to the original use case for which it was developed: **Prob**abilistic **Sem**antic and Pragmatic analysis._

## Version Note

The `main` branch is under development and evolving. To replicate specific papers, `git checkout` the corresponding paper branch and follow instructions in the associated `README.md`.

## Getting Started

Requirements: [Anaconda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html), [GNU Make](https://www.gnu.org/software/make/manual/make.html)

```bash
# download the repo
git clone --branch main --depth 1 git@github.com:benlipkin/probsem.git

# build environment
make env

# test installation
make test

# NOTE: to use OpenAI models, an API key is required at ~/.openai_api_key
```

## Run

The first step is to generate a sample test suite. Start by writing your prompt, which should define any general context you'd like to be prepended to all your evaluations, in a text file in the inputs folder. Prompts often include a description of the domain of interest, general instructions, sometimes few shot examples, and generally any text that should be available to your model across your evaluations. See `inputs/test.txt` for an example.

```bash
nano inputs/prompt.txt
```

Next, write a series of test suites to evaluate individual collections of test cases for a prompt. For example, for a reading comprehension task, the passage would be placed in the prompt, and each unique class of question about that passage would typically be placed in a separate test suite.

```
nano inputs/prompt_testsuiteA.json
nano inputs/prompt_testsuiteB.json
```

Within each test suite JSON file, there are several components, the `pretext`, `context`, `posttext`, and `queries`. Following the prompt, the `pretext` is the next thing concatenated to an LLM evaluation. It provides any test suite specific instructions or specifications. For example, two test suites might require two different question formats, one T/F and one multiple-choice. The `posttext`, which wraps the `context` (to be explained shortly) on the other side, is also static across a test suite. The core manipulation of any test suite is in the `context` and the `queries`. For a given test suite, the full cross-product of these is evaluated. For example, a user might specify several unique questions, but want to evaluate the labels `True` vs. `False` for each of them. Pasted below is an example from `inputs/test_A.json` that does just this.

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

As you can see, for a single pretext and posttext, a variety of questions of similar form can be iterated over in context, and for each, scores or a distribution over the queries will be returned. You may also note that each context example includes an integer under the `expected` key. This integer maps to the index of the query expected to have the maximum score. This allows for automatic accuracy evaluation. If, however, there is no ground-truth answer, this value can be substituted with `-1`, which disables automated scoring. See `inputs/test_B.json` for an example.

Once a prompt and test suite are defined, they can be evaluated at the command line using the following syntax:

```bash
conda activate probsem
python -m probsem --prompt prompt --test testsuiteA
python -m probsem --prompt prompt --test testsuiteB
```

As you can see, in order to evaluate the file `inputs/prompt_testsuiteA.json`, the string "prompt" is passed to the `--prompt` flag and "testsuiteA" to the `--test` flag. `*.json` files must be prefixed with their appropriate prompt to make sure the corresponding text file, here `inputs/prompt.txt`, gets read in. The default `--input_dir` is the `inputs` folder, but can be updated by the user. An `--output_dir` flag is provided as well, else default `outputs`.

Additional optional arguments are available as well. 
- `--normalize` divides the sum of token-level log-probabilities estimated by the model for each query by the number of tokens.
- `--temperature FLOAT` can be used to adjust the entropy of the final distribution over queries by dividing the logits before being passed to a softmax function. Temperatures <1.0 decrease entropy and temperatures >1.0 increase entropy. Entropy is qualitatively inverse to the _peakiness_ of the multinomial, being maximized at the uniform distribution and 0 when all mass is on a single value.

## Issues/Contributing

If you find that any particular components of this repository are unclear, or if you run into any errors, please open an issue. Comments on documentation, examples, and clarity are appreciated as well. If you find an issue, and have ideas on how to address it, then feel free to open a pull request. Community contributions are appreciated.

## Citation

```bibtex
@software{LipkinProbSem2023,
  author = {Lipkin, Benjamin},
  title = {ProbSem},
  url = {https://github.com/benlipkin/probsem},
  year = {2023}
}
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)