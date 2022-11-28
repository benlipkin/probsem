[![Tests](https://github.com/benlipkin/probsem/actions/workflows/testing.yml/badge.svg)](https://github.com/benlipkin/probsem/actions/workflows/testing.yml)

# ProbSem

## Summary

This repository explores the efficacy of large language models trained jointly on natural text and source code to act as probabilistic semantic parsers.

This work extends the notion of using LLMs for natural language guided program synthesis from single programs to distributions over programs.

## Alpha Status

This repository is currently under development and evolving rapidly. It should be considered unstable, and more information will be made available once more established.

## Getting Started

Requirements: [Anaconda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html), [GNU Make](https://www.gnu.org/software/make/manual/make.html)

```bash
# download the repo
git clone git@github.com:benlipkin/probsem.git

# build environment
make env

# test installation
make test
```

## Run

```bash
# first, write example test suite in inputs folder, e.g., 
nano inputs/tug-of-war.txt
nano inputs/tug-of-war_A.json

# then, score that test suite on the command line
conda activate probsem
python -m probsem --prompt tug-of-war --suite A

# default model is OpenAI code-davinci-002
# all OpenAI and HuggingFace causal models supported
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
