# Study 23 - NANOGrav 15-yr SGWB reproduction.
#
# Targets:
#   make all          run audit + figures (default)
#   make audit        run the audit script -> outputs/summary.json
#   make figures      regenerate all figures
#   make clean        remove outputs and generated figures

PYTHON   ?= python
SCRIPTS  := scripts
OUTPUTS  := $(SCRIPTS)/outputs
FIGURES  := figures_generated

.PHONY: all dirs audit figures clean

all: dirs audit figures

dirs:
	@mkdir -p $(OUTPUTS) $(FIGURES)

audit:
	$(PYTHON) $(SCRIPTS)/run_nanograv_audit.py

figures:
	$(PYTHON) $(SCRIPTS)/make_nanograv_figures.py

clean:
	@rm -rf $(OUTPUTS) $(FIGURES)
