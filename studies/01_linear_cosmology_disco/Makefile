# Study 01 - Linear-Cosmology and Galactic-Dynamics Closure
#
# Regenerates every audit table and figure in the paper from the locked
# constants in esd_core/ plus the DISCO-EB linear-cosmology solver runs.
#
# Usage:
#   make all              run everything under the default (primary) reading
#   make audits           background-sector audits only (no disco required)
#   make disco            DISCO-EB runs (requires GPU/CPU JAX + disco-eb)
#   make analysis         analysis scripts that consume disco outputs
#   make test             run regression tests on locked constants
#   make figures          rebuild paper figures from existing outputs
#   make clean            remove generated outputs and figures
#
#   make disco READING=closure-pool   re-run disco with the closure-pool
#                                     (zero-parameter, c-derived) Omega_b
#   make all_both                     run disco twice (primary + closure-pool)
#
# Reading selector
# ----------------
# READING=primary       (default) Omega_b = 0.0493 (Planck 2018 anchor)
# READING=closure-pool  Omega_b = 0.05009 (derived from c via Identity B)
#
# Reading-independent observables (a_0, m_D, lambda_D, n_s, S_8) are
# identical under both options.  Only Omega_b, omega_b h^2, and the
# BAO chi^2/dof differ.

READING        ?= primary
READING_FLAG   := --reading $(READING)

PYTHON   ?= python
SCRIPTS  := scripts
OUTPUTS  := $(SCRIPTS)/outputs
FIGURES  := figures_generated

.PHONY: all all_both audits disco analysis test figures clean dirs \
        step1 step2 step3 step4 step5 step6 step7 \
        step8a step8b step10 step12 step14 step15 step17 step19 \
        run_lcdm run_phase2a run_phase2a_conv run_phase2b run_esd_full \
        verify_phase2a compute_s8 fig_step19

all: audits disco analysis figures

all_both:
	$(MAKE) disco READING=primary
	$(MAKE) disco READING=closure-pool

dirs:
	@mkdir -p $(OUTPUTS) $(FIGURES)

# --- regression tests on locked constants -------------------------------------
test:
	$(PYTHON) -m pytest -q ../../esd_core/tests

# --- background-sector audits (no DISCO-EB dependency) -----------------------
audits: dirs step1 step2 step3 step5 step6 step12 step15 step17

step1:  ; $(PYTHON) $(SCRIPTS)/step1_dfield_constants_audit.py
step2:  ; $(PYTHON) $(SCRIPTS)/step2_fsigma8_bracket.py
step3:  ; $(PYTHON) $(SCRIPTS)/step3_closure_derivation.py
step5:  ; $(PYTHON) $(SCRIPTS)/step5_disformal_mlens_mdyn.py
step6:  ; $(PYTHON) $(SCRIPTS)/step6_sparc_rar.py
step12: ; $(PYTHON) $(SCRIPTS)/step12_identityB_audit.py
step15: ; $(PYTHON) $(SCRIPTS)/step15_gamma_chi_decomposition.py
step17: ; $(PYTHON) $(SCRIPTS)/step17_coupling_channel_audit.py

# --- DISCO-EB solver runs (requires jax + disco-eb) --------------------------
disco: dirs run_lcdm run_phase2a run_phase2a_conv run_phase2b run_esd_full \
       verify_phase2a

run_lcdm:        ; $(PYTHON) $(SCRIPTS)/run_lcdm_baseline.py
run_phase2a:     ; $(PYTHON) $(SCRIPTS)/run_phase2a_locked.py $(READING_FLAG)
run_phase2a_conv:; $(PYTHON) $(SCRIPTS)/run_phase2a_convergence.py $(READING_FLAG)
run_phase2b:     ; $(PYTHON) $(SCRIPTS)/run_phase2b_cascade_locked.py $(READING_FLAG)
run_esd_full:    ; $(PYTHON) $(SCRIPTS)/run_esd_full.py
verify_phase2a:  ; $(PYTHON) $(SCRIPTS)/verify_phase2a_6pct.py

# --- analysis (consumes disco outputs in $(OUTPUTS)) -------------------------
analysis: dirs compute_s8 step4 step7 step8a step8b step10 step14 step19

compute_s8: ; $(PYTHON) $(SCRIPTS)/compute_s8.py
step4:      ; $(PYTHON) $(SCRIPTS)/step4_isw_low_ell.py
step7:      ; $(PYTHON) $(SCRIPTS)/step7_tier1_wl_s8_om_placement.py
step8a:     ; $(PYTHON) $(SCRIPTS)/step8_routeA_bao.py
step8b:     ; $(PYTHON) $(SCRIPTS)/step8_routeB_shear_shape.py
step10:     ; $(PYTHON) $(SCRIPTS)/step10_joint_omegab_ns_covariance.py
step14:     ; $(PYTHON) $(SCRIPTS)/step14_residual_decomposition.py
step19:     ; $(PYTHON) $(SCRIPTS)/step19_cmb_peak_ratio.py

# --- figures (rebuild from existing outputs) ---------------------------------
figures: dirs fig_step19

fig_step19: ; $(PYTHON) $(SCRIPTS)/make_step19_figure.py

# --- clean -------------------------------------------------------------------
clean:
	@rm -rf $(OUTPUTS) $(FIGURES)
	@find $(SCRIPTS) -name "*.npz" -delete 2>/dev/null || true
