.PHONY: all audit figures clean

all: audit figures

audit:
	python scripts/run_slacs_einstein_audit.py

figures:
	python scripts/make_slacs_einstein_figures.py

clean:
	rm -rf scripts/outputs figures_generated
