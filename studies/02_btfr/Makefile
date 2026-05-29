# Study 02 - Baryonic Tully-Fisher relation: zero-parameter reproduction
# of Higginson 2026 (DOI 10.5281/zenodo.20400008).
#
# Default target reproduces the full paper:
#   make all              fetch + residuals + figure
#
# Individual targets:
#   make fetch_rotmod     download SPARC master MRT + Rotmod_LTG.zip
#   make residuals        run the full V_f^4 residual analysis
#   make fig_residuals    rebuild the 2-panel paper figure
#
# Fast slope-only sanity check (no rotation curves required):
#   make fetch            download abbreviated SPARC table only
#   make test_btfr        OLS slope-only regression
#   make fig_btfr         single-panel slope figure
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

.PHONY: all fetch fetch_rotmod test_btfr fig_btfr residuals fig_residuals test clean dirs

all: dirs fetch_rotmod residuals fig_residuals

dirs:
	@mkdir -p $(OUTPUTS) $(FIGURES) $(DATA)

# --- regression tests on locked constants ------------------------------------
test:
	$(PYTHON) -m pytest -q ../../esd_core/tests

# --- data acquisition --------------------------------------------------------
fetch: dirs
	$(PYTHON) $(SCRIPTS)/fetch_sparc.py

fetch_rotmod: dirs
	$(PYTHON) $(SCRIPTS)/fetch_sparc_rotmod.py

# --- slope-only sanity check -------------------------------------------------
test_btfr: dirs
	$(PYTHON) $(SCRIPTS)/run_btfr_test.py

fig_btfr: dirs
	$(PYTHON) $(SCRIPTS)/make_btfr_figure.py

# --- full residual analysis (paper reproduction) -----------------------------
residuals: dirs
	$(PYTHON) $(SCRIPTS)/run_btfr_residuals.py

fig_residuals: dirs
	$(PYTHON) $(SCRIPTS)/make_btfr_residuals_figure.py

# --- clean -------------------------------------------------------------------
clean:
	@rm -rf $(OUTPUTS) $(FIGURES)
