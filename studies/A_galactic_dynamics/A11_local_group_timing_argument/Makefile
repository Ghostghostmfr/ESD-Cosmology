.PHONY: all audit figures clean

all: audit figures

audit:
	python scripts/run_lg_timing_audit.py

figures:
	python scripts/make_lg_timing_figures.py

clean:
	rm -rf scripts/outputs figures_generated
