PY ?= python

audit:
	$(PY) scripts/run_eht_audit.py

figures:
	$(PY) scripts/make_eht_figures.py

all: audit figures

clean:
	rm -rf scripts/outputs figures_generated

.PHONY: audit figures all clean
