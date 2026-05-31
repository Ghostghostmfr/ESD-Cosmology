.PHONY: all audit figures clean
all: audit figures
audit:
	python scripts/run_scalar_audit.py
figures:
	python scripts/make_scalar_figures.py
clean:
	rm -rf scripts/outputs figures_generated
