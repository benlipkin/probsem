# ProbSem

## Version

Resources for the paper `Evaluating statistical language models as pragmatic reasoners` presented at `CogSci2023`.

For the most recent version of the `ProbSem` library, checkout the `main` branch.

## Getting Started

Requirements: [Anaconda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html), [GNU Make](https://www.gnu.org/software/make/manual/make.html)

```bash
# download the repo
git clone --branch CogSci2023 git@github.com:benlipkin/probsem.git

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

# the results are also available in `outputs`

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

## Citation
```bibtex
@inproceedings{Lipkin2023,
	author = {Lipkin, Benjamin and Wong, Lionel and Grand, Gabriel and Tenenbaum, Josh},
	title = {Evaluating statistical language models as pragmatic reasoners},
	year = {2023},
	journal = {Proceedings of the annual meeting of the cognitive science society},
}
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)