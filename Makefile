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
analysis : env expt_1
expt_1 : test_av1a test_av1b
test_av1a : outputs/tug-of-war_AV-1a_code-davinci-002_results.csv
test_av1b : outputs/tug-of-war_AV-1b_code-davinci-002_results.csv
_split = $(word $2,$(subst _, ,$1))
outputs/%_results.csv : $(PACKAGE)/*.py
	@$(ACTIVATE) ; python -m $(PACKAGE) \
	--prompt $(call _split,$(@F),1) \
	--suite $(call _split,$(@F),2) \
	--model $(call _split,$(@F),3)

## paper	   : generate plots.
.PHONY : paper
paper : analysis expt_1_plots
expt_1_plots : test_av1a_plots test_av1b_plots
test_av1a_plots : outputs/tug-of-war_AV-1a_code-davinci-002_plot.png
test_av1b_plots : outputs/tug-of-war_AV-1b_code-davinci-002_plot.png
outputs/%_plot.png : paper/plots.py
	@$(ACTIVATE) ; cd paper; python -m plots $(@F:_plot.png=)
