# Study 04 - a_0 derivation: zero-parameter reproduction of the
# standalone "First-Principles Derivation of MOND a_0" paper.
#
# Targets:
#   make all            run derivation + figures (default)
#   make derivation     reproduce headline numbers (no data download)
#   make figures        regenerate fig_a0_vs_H0 and fig_fb_scan
#   make test           pytest the esd_core locked constants
#   make clean          remove outputs and generated figures
#
# This study has no data download: a_0 is a closed-form prediction
# from the locked Identity B + Planck cosmological parameters.

PYTHON   ?= python
SCRIPTS  := scripts
OUTPUTS  := $(SCRIPTS)/outputs
FIGURES  := figures_generated

.PHONY: all dirs derivation figures test clean

all: dirs derivation figures

dirs:
	@mkdir -p $(OUTPUTS) $(FIGURES)

derivation:
	$(PYTHON) $(SCRIPTS)/run_a0_derivation.py

figures:
	$(PYTHON) $(SCRIPTS)/make_a0_figures.py

test:
	$(PYTHON) -m pytest -q ../../../esd_core/tests

clean:
	@rm -rf $(OUTPUTS) $(FIGURES)
