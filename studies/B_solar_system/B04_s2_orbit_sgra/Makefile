.PHONY: all audit figures clean
all: audit figures
audit:
	python scripts/run_s2_audit.py
figures:
	python scripts/make_s2_figures.py
clean:
	rm -rf scripts/outputs figures_generated
