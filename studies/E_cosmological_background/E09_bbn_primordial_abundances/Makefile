.PHONY: all audit figures clean

all: audit figures

audit:
	python scripts/run_bbn_audit.py

figures:
	python scripts/make_bbn_figures.py

clean:
	rm -rf scripts/outputs figures_generated
