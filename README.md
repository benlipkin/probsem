[![Tests](https://github.com/benlipkin/probsem/actions/workflows/testing.yml/badge.svg)](https://github.com/benlipkin/probsem/actions/workflows/testing.yml)

# ProbSem

## Summary

This repository provides a pipeline that uses LLMs to calculate probabilities over strings (e.g., natural language text, source code, etc.) within enumerated hypothesis spaces, conditioned on custom prompts and flexible context.

The repo was initially developed to explore the efficacy of large language models trained jointly on natural text and source code to act as probabilistic semantic parsers, extending the notion of using LLMs for natural language guided program synthesis from single programs to distributions over programs.

This initial use case informed initial library design, but it has since been modified to be more general.

## Version Note

The `main` branch is under development and evolving. To replicate specific papers, `git checkout` the corresponding branch, e.g., `CogSci2023`, and follow instructions in the corresponding `README.md`.

## Getting Started

Requirements: [Anaconda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html), [GNU Make](https://www.gnu.org/software/make/manual/make.html)

```bash
# download the repo
git clone --branch main --depth 1 git@github.com:benlipkin/probsem.git

# build environment
make env

# test installation
make test

# NOTE: to use OpenAI models, place an API key at ~/.openai_api_key
```

## Run

```bash
# write a sample test suite in inputs folder, e.g.,
nano inputs/prompt.txt
nano inputs/prompt_benchmark.json
# (check out the example files in inputs for more details on structure)

# then, score that test suite on the command line
conda activate probsem
python -m probsem --prompt prompt --test benchmark
# additional args provided for token-level norming and softmax temp

# default model is OpenAI code-davinci-002
# all OpenAI and HuggingFace causal models supported
```

## Citation

```bibtex
@software{LipkinProbSem2023,
  author = {Lipkin, Benjamin},
  title = {ProbSem: LLM-mediated probabilistic semantic parsing.},
  url = {https://github.com/benlipkin/probsem},
  year = {2023}
}
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)