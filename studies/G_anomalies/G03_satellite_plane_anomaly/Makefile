# Study 28 - Plane of Satellites.
PYTHON   ?= python
SCRIPTS  := scripts
OUTPUTS  := $(SCRIPTS)/outputs
FIGURES  := figures_generated

.PHONY: all dirs audit figures clean
all: dirs audit figures
dirs:
	@mkdir -p $(OUTPUTS) $(FIGURES)
audit:
	$(PYTHON) $(SCRIPTS)/run_pos_audit.py
figures:
	$(PYTHON) $(SCRIPTS)/make_pos_figures.py
clean:
	@rm -rf $(OUTPUTS) $(FIGURES)
