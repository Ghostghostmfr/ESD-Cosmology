"""Soft check for the jax/disco-eb runners: stub the heavy deps and
exercise each runner's imports, argparse, and parameter-dict construction
without ever building jax/disco-eb.

What this catches:
  * import-time typos / module drift / missing esd_core symbols
  * argparse syntax errors and bad --reading wiring
  * parameter-dict-construction bugs (wrong keys, wrong types)
  * accidental side effects at import time

What this does NOT catch:
  * numerical correctness of the Boltzmann solve
  * jax tracing/jit errors that only surface at runtime
  * disco-eb API surface drift (the stubs accept anything)
"""
from __future__ import annotations

import importlib
import os
import sys
import types
from pathlib import Path

_HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# 1. Install minimal stubs for jax + disco-eb stack BEFORE any runner import
# ---------------------------------------------------------------------------
def _make_stub(name: str, **attrs) -> types.ModuleType:
    m = types.ModuleType(name)
    for k, v in attrs.items():
        setattr(m, k, v)
    sys.modules[name] = m
    return m


class _StubArray:
    def __init__(self, *a, **kw): pass
    def __getattr__(self, _): return self
    def __call__(self, *a, **kw): return self
    def __getitem__(self, _): return self
    def __iter__(self): return iter(())


def _stub_callable(*a, **kw):
    return _StubArray()


def _attach_dynamic_getattr(mod: types.ModuleType) -> None:
    """Make any attribute lookup on `mod` return a callable stub."""
    def __getattr__(name: str):
        v = _stub_callable
        setattr(mod, name, v)
        return v
    mod.__getattr__ = __getattr__  # type: ignore[attr-defined]


import numpy as _np

jnp = _make_stub("jax.numpy",
                 array=_np.asarray, asarray=_np.asarray,
                 zeros=_np.zeros, ones=_np.ones, linspace=_np.linspace,
                 logspace=_np.logspace, log=_np.log, log10=_np.log10,
                 exp=_np.exp, sqrt=_np.sqrt, pi=_np.pi, where=_np.where,
                 concatenate=_np.concatenate, stack=_np.stack,
                 ndarray=_np.ndarray, float64=_np.float64, float32=_np.float32,
                 int32=_np.int32, int64=_np.int64)

jax_random = _make_stub("jax.random", PRNGKey=_stub_callable, split=_stub_callable)
jax_lax    = _make_stub("jax.lax",    scan=_stub_callable, cond=_stub_callable)
jax_tree_util = _make_stub("jax.tree_util",
                           tree_map=lambda f, *xs: xs[0],
                           register_pytree_node=lambda *a, **k: None)

jax_mod = _make_stub("jax",
                     numpy=jnp, random=jax_random, lax=jax_lax,
                     tree_util=jax_tree_util,
                     jit=lambda f=None, **k: (f if f else (lambda g: g)),
                     vmap=lambda f=None, **k: (f if f else (lambda g: g)),
                     grad=lambda f=None, **k: (f if f else (lambda g: g)),
                     value_and_grad=lambda f=None, **k: (f if f else (lambda g: g)),
                     devices=lambda *a, **k: [_StubArray()],
                     default_backend=lambda: "cpu",
                     config=types.SimpleNamespace(update=lambda *a, **k: None,
                                                  jax_enable_x64=True))
jax_mod.numpy = jnp
jax_mod.random = jax_random
jax_mod.lax = jax_lax
jax_mod.tree_util = jax_tree_util

_make_stub("jaxlib")
_make_stub("equinox", Module=type("Module", (), {}))
diffrax = _make_stub("diffrax",
                     ODETerm=_stub_callable, Tsit5=_stub_callable,
                     Dopri5=_stub_callable, Kvaerno5=_stub_callable,
                     PIDController=_stub_callable, diffeqsolve=_stub_callable,
                     SaveAt=_stub_callable)

discoeb_bg = _make_stub("discoeb.background",
                        evolve_background=_stub_callable,
                        get_z_to_t_interpolator=_stub_callable)
discoeb_boltz = _make_stub("discoeb.boltzmann",
                           evolve_perturbations=_stub_callable)
discoeb_perturbations = _make_stub("discoeb.perturbations",
                                   evolve_perturbations=_stub_callable,
                                   evolve_perturbations_batched=_stub_callable)
discoeb = _make_stub("discoeb",
                     background=discoeb_bg,
                     boltzmann=discoeb_boltz,
                     perturbations=discoeb_perturbations)

for _m in (discoeb_bg, discoeb_boltz, discoeb_perturbations, discoeb, diffrax):
    _attach_dynamic_getattr(_m)


# ---------------------------------------------------------------------------
# 2. Exercise each runner
# ---------------------------------------------------------------------------
RUNNERS = [
    "esd_background",
    "esd_primordial",
    "run_lcdm_baseline",
    "run_phase2a_locked",
    "run_phase2a_convergence",
    "run_phase2b_cascade_locked",
    "run_esd_full",
    "verify_phase2a_6pct",
]

sys.path.insert(0, str(_HERE))

results: list[tuple[str, str, str]] = []
for name in RUNNERS:
    try:
        if name in sys.modules:
            del sys.modules[name]
        m = importlib.import_module(name)
    except Exception as e:
        results.append((name, "IMPORT_FAIL", f"{type(e).__name__}: {e}"))
        continue

    # Verify argparse stubs for runners that expose --reading
    note = "imported"
    if hasattr(m, "main"):
        try:
            sig_ok = True
            import inspect
            sig = inspect.signature(m.main)
            note = f"imported; main{sig}"
        except Exception as e:
            note = f"imported; main introspection failed: {e}"
    results.append((name, "OK", note))


# ---------------------------------------------------------------------------
# 3. Exercise esd_locked_param_dict reading toggle from esd_background
# ---------------------------------------------------------------------------
print("=" * 78)
print("Runner soft-check results")
print("=" * 78)
for name, status, note in results:
    print(f"  [{status:^11s}] {name:34s}  {note}")

print()
print("=" * 78)
print("esd_locked_param_dict(reading=...) cross-reading test")
print("=" * 78)
import esd_background as _bg
import esd_core as ESD

for r in ("primary", "closure-pool"):
    p = _bg.esd_locked_param_dict(reading=r)
    expected_b = ESD.omega_b(r)
    ok = abs(p["Omegab"] - expected_b) < 1e-12
    print(f"  reading={r:14s}  Omegab={p['Omegab']:.7f}  "
          f"expected={expected_b:.7f}  {'OK' if ok else 'MISMATCH'}")

# ---------------------------------------------------------------------------
# 4. Argparse smoke test for the three --reading runners
# ---------------------------------------------------------------------------
import subprocess
import sys as _sys

print()
print("=" * 78)
print("CLI --help smoke test (under stubs)")
print("=" * 78)
for s in ("run_phase2a_locked.py",
          "run_phase2a_convergence.py",
          "run_phase2b_cascade_locked.py"):
    # Re-exec the script with --help in a subprocess that pre-loads this
    # stub module via PYTHONSTARTUP-style injection: simplest path is to
    # invoke this same file as a wrapper that imports the runner module
    # and triggers its parser.  Cheaper here: just inspect for --reading.
    src = (_HERE / s).read_text(encoding="utf-8")
    has_reading_flag = "--reading" in src
    has_choices_pc   = "primary" in src and "closure-pool" in src
    import re
    has_main_threaded = bool(
        re.search(r"reading\s*=\s*\w+\.reading", src)
    )
    print(f"  {s:34s}  --reading defined: {has_reading_flag}  "
          f"choices ok: {has_choices_pc}  threaded to main: {has_main_threaded}")

print()
print("Done.")
