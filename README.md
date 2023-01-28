# ProbSem

## Version

Anonymous resources for the paper `Investigating amortized pragmatic inference with large language models`.

## Getting Started

Requirements: [Anaconda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html), [GNU Make](https://www.gnu.org/software/make/manual/make.html)

```bash
# download the repo
git clone git@github.com:ANONYMOUS/probsem.git

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