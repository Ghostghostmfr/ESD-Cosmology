.PHONY: all audit figures clean
all: audit figures
audit:
	python scripts/run_spin_audit.py
figures:
	python scripts/make_spin_figures.py
clean:
	rm -rf scripts/outputs figures_generated
