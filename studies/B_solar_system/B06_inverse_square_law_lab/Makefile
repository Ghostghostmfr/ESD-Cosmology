.PHONY: all audit figures clean
all: audit figures
audit:
	python scripts/run_isl_audit.py
figures:
	python scripts/make_isl_figures.py
clean:
	rm -rf scripts/outputs figures_generated
