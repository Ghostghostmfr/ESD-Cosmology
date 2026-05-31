.PHONY: all audit figures clean
all: audit figures
audit:
	python scripts/run_ringdown_audit.py
figures:
	python scripts/make_ringdown_figures.py
clean:
	rm -rf scripts/outputs figures_generated
