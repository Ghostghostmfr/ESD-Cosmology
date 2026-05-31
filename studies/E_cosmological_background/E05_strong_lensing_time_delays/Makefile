# Study 31 - Strong Lensing Time Delays audit.
PYTHON   ?= python
SCRIPTS  := scripts
OUTPUTS  := $(SCRIPTS)/outputs
FIGURES  := figures_generated

.PHONY: all dirs audit figures clean
all: dirs audit figures
dirs:
	@mkdir -p $(OUTPUTS) $(FIGURES)
audit:
	$(PYTHON) $(SCRIPTS)/run_tdelay_audit.py
figures:
	$(PYTHON) $(SCRIPTS)/make_tdelay_figures.py
clean:
	@rm -rf $(OUTPUTS) $(FIGURES)
