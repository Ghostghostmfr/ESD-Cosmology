# Study 32 - 21cm Cosmic Dawn audit.
PYTHON   ?= python
SCRIPTS  := scripts
OUTPUTS  := $(SCRIPTS)/outputs
FIGURES  := figures_generated

.PHONY: all dirs audit figures clean
all: dirs audit figures
dirs:
	@mkdir -p $(OUTPUTS) $(FIGURES)
audit:
	$(PYTHON) $(SCRIPTS)/run_21cm_audit.py
figures:
	$(PYTHON) $(SCRIPTS)/make_21cm_figures.py
clean:
	@rm -rf $(OUTPUTS) $(FIGURES)
