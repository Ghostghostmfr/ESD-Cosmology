# Study 06 - CMB & LSS lock audit. Closed-form: every framework lock
# is compared against the published Planck 2018 / KiDS-1000 / DES Y3 /
# SH0ES / BBN / BICEP-Keck / McGaugh+2016 constraint that measures the
# same observable, with a signed pull (lock - measured)/sigma table.
# No Boltzmann solver, no data download. Runs in milliseconds.
#
# Targets:
#   make all          run audit + figures (default)
#   make audit        produce the pull table and acceptance verdict
#   make figures      regenerate fig_S8_Om_tension and fig_pull_bars
#   make test         pytest the esd_core locked constants
#   make clean        remove outputs and generated figures

PYTHON   ?= python
SCRIPTS  := scripts
OUTPUTS  := $(SCRIPTS)/outputs
FIGURES  := figures_generated

.PHONY: all dirs audit figures test clean

all: dirs audit figures

dirs:
	@mkdir -p $(OUTPUTS) $(FIGURES)

audit:
	$(PYTHON) $(SCRIPTS)/run_cmb_lss_audit.py

figures:
	$(PYTHON) $(SCRIPTS)/make_audit_figures.py

test:
	$(PYTHON) -m pytest -q ../../../esd_core/tests

clean:
	@rm -rf $(OUTPUTS) $(FIGURES)
