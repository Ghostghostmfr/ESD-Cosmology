.PHONY: all audit figures clean
all: audit figures
audit:
	python scripts/run_hi_audit.py
figures:
	python scripts/make_hi_figures.py
clean:
	rm -rf scripts/outputs figures_generated
