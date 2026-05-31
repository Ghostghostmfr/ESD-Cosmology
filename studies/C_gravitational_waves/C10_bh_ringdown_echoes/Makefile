.PHONY: all audit figures clean
all: audit figures
audit:
	python scripts/run_echo_audit.py
figures:
	python scripts/make_echo_figures.py
clean:
	rm -rf scripts/outputs figures_generated
