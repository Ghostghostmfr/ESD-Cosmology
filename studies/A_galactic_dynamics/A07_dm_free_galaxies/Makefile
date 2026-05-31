PY ?= python

audit:
	$(PY) scripts/run_udg_audit.py

figures:
	$(PY) scripts/make_udg_figures.py

all: audit figures

clean:
	rm -rf scripts/outputs figures_generated

.PHONY: audit figures all clean
