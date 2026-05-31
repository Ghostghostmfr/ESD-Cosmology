# Study 22 — DESI Y1 BAO + Planck 2018 CMB prior joint w0-wa test.
# Tests whether ESD's locked w0=-1, wa=0 prediction is consistent with
# the joint dark-energy constraint.
#
# Targets:
#   make all      dirs + audit + figures (default)
#   make audit    chi^2 scan -> outputs/summary.json + outputs/chi2_grid.npz
#   make figures  fig_w0wa_contours + fig_bao_residuals
#   make clean    remove outputs and generated figures

PYTHON   ?= python
SCRIPTS  := scripts
OUTPUTS  := $(SCRIPTS)/outputs
FIGURES  := figures_generated

.PHONY: all dirs audit figures clean

all: dirs audit figures

dirs:
	@mkdir -p $(OUTPUTS) $(FIGURES)

audit:
	$(PYTHON) $(SCRIPTS)/run_w0wa_audit.py

figures:
	$(PYTHON) $(SCRIPTS)/make_w0wa_figures.py

clean:
	@rm -rf $(OUTPUTS) $(FIGURES)
