"""Figures for Study 29 - CMB low-ell anomalies (multi-channel)."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE / "outputs"
FIG_DIR = HERE.parent / "figures_generated"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Observable directions (l, b) [deg, galactic]
PLANCK_HEMI    = (221.0, -22.0)
QUAD_OCT_AXIS  = (240.0,  60.0)
COLD_SPOT      = (210.0, -57.0)


def _save(fig, stem: str) -> None:
    for ext in ("png", "pdf"):
        path = FIG_DIR / f"{stem}.{ext}"
        fig.savefig(path, dpi=160, bbox_inches="tight")
        print(f"wrote {path}")
    plt.close(fig)


def _ll_to_rad(l_deg: float, b_deg: float) -> tuple[float, float]:
    l = np.deg2rad(((l_deg + 180.0) % 360.0) - 180.0)
    b = np.deg2rad(b_deg)
    return l, b


def fig_channel_verdicts() -> None:
    s = json.loads((OUT_DIR / "summary.json").read_text())
    h = s["hemi_amplitude"]
    verdicts = s["channel_verdicts"]

    rows = [
        ("MATTER\namplitude",
         f"A_hemi pred/obs = {h['ratio_pred_over_obs']:.2f}\n"
         f"({h['delta_in_sigma']:+.1f} sigma)",
         verdicts["matter_amplitude"]),
        ("DISFORMAL\naxis",
         f"quad-oct sep = {s['disformal_quad_oct_sep_deg']:.1f} deg\n"
         f"vs $\\hat g_{{\\rm matter}}$",
         verdicts["disformal_axis"]),
        ("PHOTON\naxis",
         f"Planck hemi sep = {s['photon_axis_sep_deg']:.1f} deg\n"
         f"vs $\\hat g_{{\\rm photon}}$",
         verdicts["photon_axis"]),
    ]
    labels = [r[0] for r in rows]
    texts = [r[1] for r in rows]
    pass_mask = [r[2] == "PASS" for r in rows]
    colors = ["#2a7fbf" if ok else "#a01818" for ok in pass_mask]
    values = [1.0, 1.0, 1.0]

    fig, ax = plt.subplots(figsize=(9, 4.6))
    x = np.arange(len(labels))
    ax.bar(x, values, color=colors, edgecolor="black", linewidth=0.5)
    for xi, txt, ok in zip(x, texts, pass_mask):
        ax.text(xi, 0.5, txt, ha="center", va="center",
                fontsize=10, color="white", fontweight="bold")
        ax.text(xi, 1.04, "PASS" if ok else "FAIL",
                ha="center", fontsize=12, fontweight="bold",
                color=("#2a7fbf" if ok else "#a01818"))
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_yticks([])
    ax.set_ylim(0, 1.15)
    ax.set_title(f"Study 29 - per-channel verdicts ({s['verdict']})")
    _save(fig, "fig_low_ell_channel_verdicts")


def fig_directions() -> None:
    s = json.loads((OUT_DIR / "summary.json").read_text())
    gm_l, gm_b = s["g_hat_matter_lb"]
    gp_l, gp_b = s["g_hat_photon_lb"]

    fig = plt.figure(figsize=(10, 5.5))
    ax = fig.add_subplot(111, projection="mollweide")

    l, b = _ll_to_rad(gm_l, gm_b)
    ax.scatter([l], [b], s=260, marker="X", color="#2a7fbf", zorder=6,
               edgecolor="black", linewidths=1.2,
               label=fr"$\hat g_{{\rm matter}}$ ({gm_l}, {gm_b:+d})")
    l, b = _ll_to_rad(gp_l, gp_b)
    ax.scatter([l], [b], s=260, marker="X", color="#d96b1f", zorder=6,
               edgecolor="black", linewidths=1.2,
               label=fr"$\hat g_{{\rm photon}}$ ({gp_l}, {gp_b:+d})")

    targets = {
        "Planck hemi axis": PLANCK_HEMI,
        "Quad-oct axis":    QUAD_OCT_AXIS,
        "Cold Spot":        COLD_SPOT,
    }
    target_colors = {
        "Planck hemi axis": "#d4a017",
        "Quad-oct axis":    "#6aa84f",
        "Cold Spot":        "#6a6a6a",
    }
    for name, (lt, bt) in targets.items():
        l, b = _ll_to_rad(lt, bt)
        ax.scatter([l], [b], s=130, color=target_colors[name],
                   edgecolor="black", zorder=4,
                   label=f"{name} ({lt:.0f}, {bt:+.0f})")

    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.20), ncol=2,
              fontsize=9)
    cs = s["cross_channel_sep_deg"]
    ax.set_title(f"CMB low-$\\ell$ axes vs $\\hat g$ per channel "
                 f"(matter-photon sep {cs:.1f} deg)", pad=20)
    _save(fig, "fig_low_ell_directions")


def fig_hemi_amplitude() -> None:
    s = json.loads((OUT_DIR / "summary.json").read_text())
    h = s["hemi_amplitude"]
    obs = h["A_hemi_obs"]
    obs_sig = h["A_hemi_obs_sigma"]
    pred = h["A_hemi_pred"]
    plo = h.get("A_hemi_pred_lower", pred)
    phi = h.get("A_hemi_pred_upper", pred)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    x = [0, 1]
    ax.bar(x[0], obs, color="#d96b1f", edgecolor="black", linewidth=0.4,
           yerr=obs_sig, ecolor="black", capsize=6,
           label=f"Planck observed = {obs:.3f} +/- {obs_sig:.3f}")
    ax.bar(x[1], pred, color="#2a7fbf", edgecolor="black", linewidth=0.4,
           yerr=[[pred - plo], [phi - pred]], ecolor="black", capsize=6,
           label=f"ESD MATTER channel = {pred:.3f}")
    ax.set_xticks(x)
    ax.set_xticklabels(["Observed", "ESD predicted"])
    ax.set_ylabel(r"$A_{\rm hemi}$ (dipolar modulation amplitude)")
    ax.set_title(f"Study 29 - hemispherical-modulation amplitude "
                 f"({h['delta_in_sigma']:+.2f} sigma, "
                 f"pred/obs = {h['ratio_pred_over_obs']:.2f})")
    ax.set_ylim(0, max(obs + obs_sig, phi) * 1.25)
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    _save(fig, "fig_low_ell_hemi_amplitude")


def main() -> int:
    fig_channel_verdicts()
    fig_directions()
    fig_hemi_amplitude()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
