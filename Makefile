SHELL := /usr/bin/env bash
EXEC = python=3.10
PACKAGE = probsem
INSTALL = pip install -e .
ACTIVATE = source activate $(PACKAGE)
.DEFAULT_GOAL := help

## help      : print available build commands.
.PHONY : help
help : Makefile
	@sed -n 's/^##//p' $<

## update    : update repo with latest version from GitHub.
.PHONY : update
update :
	@git pull origin main

## env       : setup environment and install dependencies.
.PHONY : env
env : $(PACKAGE).egg-info/
$(PACKAGE).egg-info/ : setup.py requirements.txt
	@conda create -yn $(PACKAGE) $(EXEC)
	@$(ACTIVATE) ; $(INSTALL)

## test      : run testing pipeline.
.PHONY : test
test : mypy pylint pytest
mypy : env html/mypy/index.html
pylint : env html/pylint/index.html
pytest : env html/coverage/index.html
html/mypy/index.html : $(PACKAGE)/*.py
	@$(ACTIVATE) ; mypy \
	-p $(PACKAGE) \
	--ignore-missing-imports \
	--html-report $(@D)
html/pylint/index.html : html/pylint/index.json
	@$(ACTIVATE) ; pylint-json2html -o $@ -e utf-8 $<
html/pylint/index.json : $(PACKAGE)/*.py
	@mkdir -p $(@D)
	@$(ACTIVATE) ; pylint $(PACKAGE) \
	--disable C0114,C0115,C0116 \
	--generated-members torch.* \
	--output-format=colorized,json:$@ \
	|| pylint-exit $$?
html/coverage/index.html : html/pytest/report.html
	@$(ACTIVATE) ; coverage html -d $(@D)
html/pytest/report.html : $(PACKAGE)/*.py test/*.py
	@$(ACTIVATE) ; coverage run --branch -m pytest \
	--html=$@ --self-contained-html

## analysis  : run analysis pipeline.
.PHONY : analysis
analysis : env tug-of-war
tug-of-war : benchmark_av benchmark_pp
benchmark_av : suite_av1 suite_av2
benchmark_pp : suite_pp1a suite_pp1b suite_pp1c suite_pp2a suite_pp2b suite_pp2c
suite_av1 : outputs/tug-of-war_AV-1_code-davinci-002_results.csv
suite_av2 : outputs/tug-of-war_AV-2_code-davinci-002_results.csv
suite_pp1a : outputs/tug-of-war_PP-1a_code-davinci-002_results.csv
suite_pp1b : outputs/tug-of-war_PP-1b_code-davinci-002_results.csv
suite_pp1c : outputs/tug-of-war_PP-1c_code-davinci-002_results.csv
suite_pp2a : outputs/tug-of-war_PP-2a_code-davinci-002_results.csv
suite_pp2b : outputs/tug-of-war_PP-2b_code-davinci-002_results.csv
suite_pp2c : outputs/tug-of-war_PP-2c_code-davinci-002_results.csv
_split = $(word $2,$(subst _, ,$1))
outputs/%_results.csv : $(PACKAGE)/*.py
	@$(ACTIVATE) ; python -m $(PACKAGE) \
	--prompt $(call _split,$(@F),1) \
	--suite $(call _split,$(@F),2) \
	--model $(call _split,$(@F),3)

## paper	  : generate plots.
.PHONY : paper
paper : analysis tug-of-war-plots
tug-of-war-plots : benchmark_av_plots benchmark_pp_plots
benchmark_av_plots : suite_av1_plots suite_av2_plots
benchmark_pp_plots : suite_pp1_plots suite_pp2_plots
suite_av1_plots : outputs/tug-of-war_AV-1_code-davinci-002_plot.png
suite_av2_plots : outputs/tug-of-war_AV-2_code-davinci-002_plot.png
suite_pp1_plots : outputs/tug-of-war_PP-1_code-davinci-002_plot.png
suite_pp2_plots : outputs/tug-of-war_PP-2_code-davinci-002_plot.png
outputs/%_plot.png : paper/plots.py
	@$(ACTIVATE) ; cd paper; python -m plots $(@F:_plot.png=)
