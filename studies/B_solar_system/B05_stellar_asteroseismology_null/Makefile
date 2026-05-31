.PHONY: all audit figures clean
all: audit figures
audit:
	python scripts/run_stellar_audit.py
figures:
	python scripts/make_stellar_figures.py
clean:
	rm -rf scripts/outputs figures_generated
