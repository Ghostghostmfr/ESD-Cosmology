# Study 35 - ISW x galaxy cross-correlation audit
PYTHON ?= python
SCRIPTS := scripts
OUTPUTS := $(SCRIPTS)/outputs
FIGURES := figures_generated

.PHONY: all dirs audit figures clean
all: dirs audit figures
dirs:
	@mkdir -p $(OUTPUTS) $(FIGURES)
audit:
	$(PYTHON) $(SCRIPTS)/run_isw_audit.py
figures:
	$(PYTHON) $(SCRIPTS)/make_isw_figures.py
clean:
	@rm -rf $(OUTPUTS) $(FIGURES)
