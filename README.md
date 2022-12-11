[![Tests](https://github.com/benlipkin/probsem/actions/workflows/testing.yml/badge.svg)](https://github.com/benlipkin/probsem/actions/workflows/testing.yml)

# ProbSem

## Summary

This repository explores the efficacy of large language models trained jointly on natural text and source code to act as probabilistic semantic parsers.

This work extends the notion of using LLMs for natural language guided program synthesis from single programs to distributions over programs.

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
### REPLICATE PAPER RESULTS:

# a full pipeline from env to figures is provided
make paper

### RUN CUSTOM ANALYSIS:

# write an example test suite in inputs folder, e.g.,
nano inputs/domain.txt
nano inputs/domain_benchmark.json

# then, score that test suite on the command line
conda activate probsem
python -m probsem --prompt domain --suite benchmark

# default model is OpenAI code-davinci-002
# all OpenAI and HuggingFace causal models supported
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)