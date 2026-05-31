.PHONY: all audit figures clean
all: audit figures
audit:
	python scripts/run_love_audit.py
figures:
	python scripts/make_love_figures.py
clean:
	rm -rf scripts/outputs figures_generated
