PYTHON ?= python
SCRIPTS := scripts
OUTPUTS := $(SCRIPTS)/outputs
FIGURES := figures_generated
.PHONY: all dirs audit figures clean
all: dirs audit figures
dirs:
	@mkdir -p $(OUTPUTS) $(FIGURES)
audit:
	$(PYTHON) $(SCRIPTS)/run_cc_audit.py
figures:
	$(PYTHON) $(SCRIPTS)/make_cc_figures.py
clean:
	@rm -rf $(OUTPUTS) $(FIGURES)
