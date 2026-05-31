# Study 07 - DESI Y1 BAO chi^2 reproduction across cosmologies. Tests
# whether DESI Y1 distinguishes ESD's PRIMARY vs CLOSURE-POOL readings
# of Identity B, and whether either matches Planck-LCDM at the DESI
# data points.
#
# Targets:
#   make all          run chi^2 + figures (default)
#   make chi2         compute chi^2 / dof for every cosmology
#   make figures      regenerate fig_desi_y1_{distance_ladder,residuals}
#   make clean        remove outputs and generated figures

PYTHON   ?= python
SCRIPTS  := scripts
OUTPUTS  := $(SCRIPTS)/outputs
FIGURES  := figures_generated

.PHONY: all dirs chi2 figures clean

all: dirs chi2 figures

dirs:
	@mkdir -p $(OUTPUTS) $(FIGURES)

chi2:
	$(PYTHON) $(SCRIPTS)/run_desi_y1_bao.py

figures:
	$(PYTHON) $(SCRIPTS)/make_desi_figures.py

clean:
	@rm -rf $(OUTPUTS) $(FIGURES)
