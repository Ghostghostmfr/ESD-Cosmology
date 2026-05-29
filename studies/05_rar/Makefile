# Study 05 - SPARC Radial Acceleration Relation reproduction.
#
# Targets:
#   make all          run RAR aggregation + figures (default)
#   make rar          aggregate (g_bar, g_obs) over 175 SPARC galaxies
#   make figures      regenerate fig_rar and fig_rar_residual
#   make test         pytest the esd_core locked constants
#   make clean        remove outputs and generated figures

PYTHON   ?= python
SCRIPTS  := scripts
OUTPUTS  := $(SCRIPTS)/outputs
FIGURES  := figures_generated

.PHONY: all dirs rar figures test clean

all: dirs rar figures

dirs:
	@mkdir -p $(OUTPUTS) $(FIGURES)

rar:
	$(PYTHON) $(SCRIPTS)/run_rar.py

figures:
	$(PYTHON) $(SCRIPTS)/make_rar_figures.py

test:
	$(PYTHON) -m pytest -q ../../esd_core/tests

clean:
	@rm -rf $(OUTPUTS) $(FIGURES)
