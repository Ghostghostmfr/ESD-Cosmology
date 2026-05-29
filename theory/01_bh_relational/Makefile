# Use the active environment's python by default.
# Override with:  make PY=/path/to/python  audit
PY ?= python

audit:
	$(PY) scripts/run_bh_audit.py

figures:
	$(PY) scripts/make_bh_figures.py

all: audit figures

clean:
	rm -rf scripts/outputs figures_generated

.PHONY: audit figures all clean
