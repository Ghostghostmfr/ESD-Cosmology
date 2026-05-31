.PHONY: all audit figures clean
all: audit figures
audit:
	python scripts/run_friction_audit.py
figures:
	python scripts/make_friction_figures.py
clean:
	rm -rf scripts/outputs figures_generated
