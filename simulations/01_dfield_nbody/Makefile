# Simulation 01 - D-field N-body (mini-Millennium analog)
#
# Targets follow the studies/ convention: one Python entry per target.
# Sub-tasks are filled in incrementally; each `make` invocation should
# be runnable as soon as its underlying script lands.
#
# Usage:
#   make all        scaffold-only until sub-task 1.1 (PM solver) lands
#   make ic         generate Zel'dovich initial conditions
#   make sim        run the PM solver (GR baseline, then ESD)
#   make halos      FOF halo finder on the final snapshot
#   make hmf        halo mass function (CSV + figure)
#   make xi         two-point correlation xi(r)
#   make profile    density profile (NFW vs ESD)
#   make test       regression tests on locked constants + small sim
#   make clean      remove outputs/, figures_generated/, snapshots/

PYTHON  ?= python
SCRIPTS := scripts
OUT     := outputs
FIG     := figures_generated
SNAP    := snapshots

SEED    ?= 1234
BOX_MPC ?= 50
NPART   ?= 256

.PHONY: all ic sim halos hmf xi profile test self_test clean dirs

all: dirs self_test ic sim halos hmf xi profile

# Sub-task 1.1 verification: PM solver recovers linear growth D(a).
self_test:
	$(PYTHON) $(SCRIPTS)/run_sim.py --self-test

# Sub-task 1.2a verification: R(u) module matches Study 05 and the
# applicability gate respects Study 19's regime separation.
esd_mod_test:
	$(PYTHON) $(SCRIPTS)/esd_modification.py

# Sub-task 1.3 verification: Zel'dovich IC reproduces input P(k).
ic_test:
	$(PYTHON) $(SCRIPTS)/ic_zeldovich.py

# Sub-task 1.4 verification: FOF recovers planted synthetic clusters.
fof_test:
	$(PYTHON) $(SCRIPTS)/find_halos.py

# Sub-task 1.2b verification: ESD-on must reproduce GR linear growth.
esd_invariance_test:
	$(PYTHON) $(SCRIPTS)/run_sim.py --esd-self-test

# Sub-task 1.5 verification: HMF analysis + Press-Schechter self-test.
hmf_test:
	$(PYTHON) $(SCRIPTS)/halo_mass_function.py

# Sub-task 1.5 smoke: end-to-end pipeline on a small box (~minutes).
hmf_smoke:
	$(PYTHON) $(SCRIPTS)/compare_hmf.py --smoke

# Sub-task 1.5 science: full GR-vs-ESD comparison figure.
hmf_science:
	$(PYTHON) $(SCRIPTS)/compare_hmf.py --science

dirs:
	@mkdir -p $(OUT) $(FIG) $(SNAP)

# --- placeholders until sub-tasks land ---------------------------------------
ic:
	@echo "[ic] placeholder - implement scripts/ic_zeldovich.py (sub-task 1.3)"

sim:
	@echo "[sim] placeholder - implement scripts/run_sim.py (sub-tasks 1.1 + 1.2)"

halos:
	@echo "[halos] placeholder - implement scripts/find_halos.py (sub-task 1.4)"

hmf:
	@echo "[hmf] placeholder - implement scripts/halo_mass_function.py (sub-task 1.5)"

xi:
	@echo "[xi] placeholder - implement scripts/two_point_xi.py (sub-task 1.6)"

profile:
	@echo "[profile] placeholder - implement scripts/halo_profile.py (sub-task 1.7)"

# --- regression tests --------------------------------------------------------
test:
	$(PYTHON) -m pytest -q ../../esd_core/tests

clean:
	rm -rf $(OUT) $(FIG) $(SNAP) __pycache__ $(SCRIPTS)/__pycache__
