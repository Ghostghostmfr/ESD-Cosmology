# Study 48 - ESD vs MOND formal statistical verdict.
#
# Two operating modes
# -------------------
# make summary   STANDALONE — generates figures from the published headline
#                numbers embedded in the script.  No prerequisites; always
#                works on a fresh clone.
#
# make all       FULL VERIFICATION — reads the per-galaxy CSV from study 03
#                and checks every W/T/L count and Sigma_Delta-chi2 value
#                against the published results.  Requires:
#                  cd ../A02_sparc_rotation_curves && make residuals

PYTHON   ?= python
SCRIPTS  := scripts
OUTPUTS  := $(SCRIPTS)/outputs
FIGURES  := figures_generated
STUDY03  := ../A02_sparc_rotation_curves

.PHONY: all summary verdict clean dirs

all: summary verdict

summary: dirs
	$(PYTHON) $(SCRIPTS)/esd_vs_mond_standalone.py

verdict: dirs
	$(PYTHON) $(SCRIPTS)/esd_vs_mond_verdict.py

dirs:
	@mkdir -p $(OUTPUTS) $(FIGURES)

clean:
	rm -rf $(OUTPUTS)/*.json $(OUTPUTS)/*.txt $(FIGURES)/*.png
