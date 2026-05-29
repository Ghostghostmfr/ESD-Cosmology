PY    := python
PYHOME := ../../../../.venv/Scripts/python.exe

.PHONY: all dirs audit figures test clean

all: audit figures

dirs:
	@mkdir -p scripts/outputs figures_generated

audit: dirs
	$(PYHOME) scripts/run_jeans_audit.py

figures: dirs
	$(PYHOME) scripts/make_jeans_figures.py

test: audit
	@echo "[OK] Study 11 gate passed"

clean:
	rm -rf scripts/outputs figures_generated
