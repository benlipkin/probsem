[![Tests](https://github.com/benlipkin/probsem/actions/workflows/testing.yml/badge.svg)](https://github.com/benlipkin/probsem/actions/workflows/testing.yml)

# ProbSem

## Summary

This repository provides a framework to leverage large language models (LLMs) to assign context-conditional probability distributions over queried strings.

It is intended to be flexible and support a wide range of research applications spanning linguistics, cognitive science, program synthesis, and NLP.

Here are a few examples:

- Cloze Completion Task
    ```bash
    .. prompt, task instructions ..
    context:    The color of the Boston sky during January is
    query1:     blue  # P=0.4
    query2:     gray  # P=0.6
    ```

- Multiple Choice QA
    ```bash
    .. prompt, task instructions ..
    context:    The girl pushed the boy.
    posttext:   Which of the following logically entails?
                A: The girl was pushed by the boy.
                B: The boy was pushed by the boy.
                C: The boy was pushed by the girl.
                D: The girl was pushed by the girl.
                The correct response is:
    query1:     A   # P=0.03
    query2:     B   # P=0.01
    query3:     C   # P=0.95
    query4:     D   # P=0.01
    ```

- Semantic Parsing
    ```scheme
    .. prompt, task instructions ..
    pretext:    ;; Player strengths were distributed ~N(50,20)
    context:    ;; X has nearly average strength.
    query1:     (λ (x) (= (abs (- (strength x) 50)) 0))   ;; P=0.1
    query2:     (λ (x) (< (abs (- (strength x) 50)) 10))  ;; P=0.9
    ```

- Code completion
    ```python
    .. prompt, task instructions ..
    context:    def reverse(lst:list):
    query1:       return lst[::-1]      # P=0.40
    query2:       return reversed(lst)  # P=0.30
    query3:       lst.reverse()         # P=0.20
    query4:       list.reverse(lst)     # P=0.10
    ```

In each of these examples, a user may define a flexible frame of reference using the concatenation of a `prompt`, `context`, and optional `pretext` and `posttext`, which wrap the `context`, to derive a probability distribution over possible completions defined as `queries`. The precise formulation of such evaluations can be explored further by viewing the examples in the `inputs` folder or checking out the [BENCHMARKS.md](https://github.com/benlipkin/probsem/blob/main/BENCHMARKS.md) walkthrough.

### Version Note

_The name of this repository `ProbSem` is a legacy reference to the original use case for which it was developed: **Prob**abilistic **Sem**antic Parsing. It was generalized into its current form after expressed interest from collaborators and colleagues._

As such the `main` branch is under development and evolving. To replicate specific papers, `git checkout` the corresponding paper branch and follow instructions in the associated `README.md`.

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

The first step is to generate your benchmark. This includes, at minimum, a `Prompt` file and one `TestSuite`. See [BENCHMARKS.md](https://github.com/benlipkin/probsem/blob/main/BENCHMARKS.md) for more info on the structure of these files.

```bash
nano inputs/prompt.txt
nano inputs/prompt_testsuite.json
```

Once a prompt and test suite are defined, they can be evaluated at the command line. For a given prompt `prompt` and test suite `testsuite`, as shown above, the following syntax can be used for evaluation.

### CLI

```bash
python -m probsem --prompt prompt --test testsuite
```

The prompt `*.txt` file and test suite `*.json` file must share the same prefix (`prompt` above) to be linked, and are assumed by default to exist in the `inputs` folder. This default, and others, can be overwritten. See below.

Optional arguments (and other relevant internal details):

- `--input_dir [STR] {default: "inputs"}` Update path to directory containing the benchmark files to be read in.
- `--output_dir [STR] {default: "outputs"}` Update path to directory where output files should be saved. On each run, a CSV is saved with the resulting scores.
- `--model [STR] {default: "code-davinci-002"}` Customize the model used for scoring. All OpenAI API engines and HuggingFace CausalLM models are currently supported. HF models run on GPU by default else CPU if not available.
- `--norm [BOOL True] {default: False}` This flag can be used to turn on normalization. By default scores returned reflect the sum of the query token context-conditional log-probabilties. When this flag is passed, these values are normalized for the number of tokens, uniquely for each tokenizer.
- `--temp [FLOAT >0] {default: 1.0}` Following the derivation of individual query-level scores, a probability distribution over the batch of queries is calculated by passing the array of logit scores to a softmax function with temperature parameter $\alpha$. Specifying $\alpha<1.0$ decreases the entropy of the returned multinomial distribution and $\alpha>1.0$ increases the entropy. Entropy is qualitatively inverse to the _peakiness_ of the distribution, being maximized at the uniform distribution and 0 when all probability mass is on a single value.

### API

An API is also supported for integration with existing applications. To run the same default example from above, the following code will suffice.

```python
from probsem.probsem import ProbSem

probsem = ProbSem(
    prompt="prompt",
    test="testsuite",
)
results = probsem.run()
```

## Issues/Contributing

If you find any particular aspects of this repository unclear, or if you encounter any errors, please open an issue. Comments on documentation, examples, and clarity are also appreciated. If you find an issue, and have ideas on how to address it, feel free to open a pull request. Community contributions are greatly appreciated.

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
