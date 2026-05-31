# Study 03 - SPARC rotation-curve reproduction (paper 1, Sec. SPARC).
#
# Default target reproduces the published head-to-head numbers:
#   make all              residuals + all three figures
#
# Individual targets:
#   make residuals        run the full 175-galaxy, 117-M/L analysis
#   make figures          rebuild the gallery + Delta-chi^2 hist + scatter
#   make fetch            populate data/ from local mirror or network
#                          (no-op if data is already shipped, which it is)
#
# Misc:
#   make test             pytest the esd_core locked constants
#   make clean            remove all outputs and generated figures
#
# This study has no GPU / JAX / Boltzmann dependency.

PYTHON   ?= python
SCRIPTS  := scripts
OUTPUTS  := $(SCRIPTS)/outputs
FIGURES  := figures_generated
DATA     := data

.PHONY: all fetch residuals figures test clean dirs

all: dirs residuals figures

dirs:
	@mkdir -p $(OUTPUTS) $(FIGURES) $(DATA)

# --- regression tests on locked constants ------------------------------------
test:
	$(PYTHON) -m pytest -q ../../../esd_core/tests

# --- data acquisition --------------------------------------------------------
fetch: dirs
	$(PYTHON) $(SCRIPTS)/fetch_sparc_rotmod.py

# --- full per-galaxy analysis (paper reproduction) ---------------------------
residuals: dirs
	$(PYTHON) $(SCRIPTS)/run_rotation_curves.py

figures: dirs
	$(PYTHON) $(SCRIPTS)/make_rotation_curves_figures.py

# --- clean -------------------------------------------------------------------
clean:
	@rm -rf $(OUTPUTS) $(FIGURES)
