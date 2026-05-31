.PHONY: all audit figures clean
all: audit figures
audit:
	python scripts/run_pulsar_audit.py
figures:
	python scripts/make_pulsar_figures.py
clean:
	rm -rf scripts/outputs figures_generated
