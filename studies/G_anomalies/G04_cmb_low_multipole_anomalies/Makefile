# Study 29 - CMB low-ell anomalies bundle.
PYTHON   ?= python
SCRIPTS  := scripts
OUTPUTS  := $(SCRIPTS)/outputs
FIGURES  := figures_generated

.PHONY: all dirs audit figures clean
all: dirs audit figures
dirs:
	@mkdir -p $(OUTPUTS) $(FIGURES)
audit:
	$(PYTHON) $(SCRIPTS)/run_low_ell_audit.py
figures:
	$(PYTHON) $(SCRIPTS)/make_low_ell_figures.py
clean:
	@rm -rf $(OUTPUTS) $(FIGURES)
