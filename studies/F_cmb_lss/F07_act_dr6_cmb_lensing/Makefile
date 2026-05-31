# Study 24 - ACT DR6 CMB lensing audit.
#
# Targets:
#   make all      run audit + figures (default)
#   make audit    run the audit script
#   make figures  regenerate figures
#   make clean    remove outputs and generated figures

PYTHON  ?= python
SCRIPTS := scripts
OUTPUTS := $(SCRIPTS)/outputs
FIGURES := figures_generated

.PHONY: all dirs audit figures clean

all: dirs audit figures

dirs:
	@mkdir -p $(OUTPUTS) $(FIGURES)

audit:
	$(PYTHON) $(SCRIPTS)/run_act_lensing_audit.py

figures:
	$(PYTHON) $(SCRIPTS)/make_act_lensing_figures.py

clean:
	@rm -rf $(OUTPUTS) $(FIGURES)
