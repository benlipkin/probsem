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
analysis : env av1a av1b av2a av2b av2c
av1a : outputs/tug-of-war_AV-1a_code-davinci-002_results.csv
av1b : outputs/tug-of-war_AV-1b_code-davinci-002_results.csv
av2a : outputs/tug-of-war-mix_AV-2a_code-davinci-002_results.csv
av2b : outputs/tug-of-war-mix_AV-2b_code-davinci-002_results.csv
av2c : outputs/tug-of-war-mix_AV-2c_code-davinci-002_results.csv
_split = $(word $2,$(subst _, ,$1))
outputs/%_results.csv : $(PACKAGE)/*.py
	@$(ACTIVATE) ; python -m $(PACKAGE) \
	--prompt $(call _split,$(@F),1) \
	--suite $(call _split,$(@F),2) \
	--model $(call _split,$(@F),3)

## paper	   : generate plots and tables for paper.
.PHONY : paper
paper : analysis plots tables
plots : norms av1a_plot av1b_plot av2a_plot av2b_plot av2c_plot
tables : norms av1_table av2_table
norms : av1a_data av1b_data av2a_data av2b_data av2c_data
av1a_data : outputs/tug-of-war_AV-1a_code-davinci-002_data.csv
av1b_data : outputs/tug-of-war_AV-1b_code-davinci-002_data.csv
av2a_data : outputs/tug-of-war-mix_AV-2a_code-davinci-002_data.csv
av2b_data : outputs/tug-of-war-mix_AV-2b_code-davinci-002_data.csv
av2c_data : outputs/tug-of-war-mix_AV-2c_code-davinci-002_data.csv
av1a_plot : outputs/tug-of-war_AV-1a_code-davinci-002_plot.png
av1b_plot : outputs/tug-of-war_AV-1b_code-davinci-002_plot.png
av2a_plot : outputs/tug-of-war-mix_AV-2a_code-davinci-002_plot.png
av2b_plot : outputs/tug-of-war-mix_AV-2b_code-davinci-002_plot.png
av2c_plot : outputs/tug-of-war-mix_AV-2c_code-davinci-002_plot.png
av1_table : outputs/tug-of-war_AV-1_stats.tex
av2_table : outputs/tug-of-war-mix_AV-2_stats.tex
outputs/%_data.csv : paper/norms.py
	@$(ACTIVATE) ; cd $(<D) ; python -m $(word 1,$(subst ., ,$(<F))) $(@F)
outputs/%_plot.png : paper/plots.py
	@$(ACTIVATE) ; cd $(<D) ; python -m $(word 1,$(subst ., ,$(<F))) $(@F)
outputs/%_stats.tex : paper/tables.py
	@$(ACTIVATE) ; cd $(<D) ; python -m $(word 1,$(subst ., ,$(<F))) $(@F)