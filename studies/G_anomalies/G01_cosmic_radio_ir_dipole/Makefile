# Study 25 — Cosmic radio/IR dipole vs CMB kinematic dipole.
#
# Targets:
#   make all      dirs + audit + figures (default)
#   make audit    Ellis-Baldwin vs observed comparison -> outputs/summary.json
#   make figures  fig_dipole_amplitudes + fig_dipole_directions
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
	$(PYTHON) $(SCRIPTS)/run_dipole_audit.py

figures:
	$(PYTHON) $(SCRIPTS)/make_dipole_figures.py

clean:
	@rm -rf $(OUTPUTS) $(FIGURES)
