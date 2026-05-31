.PHONY: all audit figures clean
all: audit figures
audit:
	python scripts/run_nicer_audit.py
figures:
	python scripts/make_nicer_figures.py
clean:
	rm -rf scripts/outputs figures_generated
