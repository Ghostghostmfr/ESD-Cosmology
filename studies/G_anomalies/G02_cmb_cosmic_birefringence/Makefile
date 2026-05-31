# Study 26 - CMB cosmic birefringence (Eskilt & Komatsu 2023).
#
# Targets:
#   make all      dirs + audit + figures (default)
#   make audit    structural action audit + measurement chi^2 vs beta=0
#   make figures  fig_beta_measurements + fig_falsifier_forecast
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
	$(PYTHON) $(SCRIPTS)/run_birefringence_audit.py

figures:
	$(PYTHON) $(SCRIPTS)/make_birefringence_figures.py

clean:
	@rm -rf $(OUTPUTS) $(FIGURES)
