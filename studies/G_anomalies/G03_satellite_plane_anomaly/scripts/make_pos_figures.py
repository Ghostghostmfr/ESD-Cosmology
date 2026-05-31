"""Figures for Study 28 - Plane of Satellites audit (MATTER channel)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from pos_data import MW_VPOS  # noqa: E402

OUT_DIR = HERE / "outputs"
FIG_DIR = HERE.parent / "figures_generated"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Plane normals (l, b) [deg, galactic]
PLANE_NORMALS = {
    "MW VPOS":    (156.4, -2.2),
    "M31 GPoA":   (206.2,  7.8),
    "CenA plane": (308.7, 18.0),
}


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


def fig_perpendicularity() -> None:
    s = json.loads((OUT_DIR / "summary.json").read_text())
    perp = s["perpendicularity_deviations_deg"]
    hosts = list(perp.keys())
    devs = np.array([perp[h] for h in hosts])
    pass_mask = devs < 30.0
    colors = ["#2a7fbf" if ok else "#a01818" for ok in pass_mask]
    labels = [f"{h}\n{'clean' if h != 'M31 GPoA' else 'Local Group'}"
              for h in hosts]

    fig, ax = plt.subplots(figsize=(8, 4.8))
    x = np.arange(len(hosts))
    ax.bar(x, devs, color=colors, edgecolor="black", linewidth=0.4)
    for xi, d in zip(x, devs):
        ax.text(xi, d + 1.2, f"{d:.1f}$^\\circ$",
                ha="center", fontsize=11, fontweight="bold")
    ax.axhline(30.0, color="black", ls="--", lw=1,
               label=r"gate: 30 deg")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel(r"$|\,\Delta_{\rm normal\,\angle\,\hat g_{\rm matter}}"
                  r" - 90^\circ\,|$  [deg]")
    g_l, g_b = s["g_hat_matter_lb"]
    ax.set_title(f"Study 28 - Plane-of-satellites perpendicularity "
                 f"to $\\hat g_{{\\rm matter}} = ({g_l}, {g_b:+d})$")
    ax.set_ylim(0, max(devs) * 1.25 + 6)
    ax.legend(loc="upper right")
    ax.grid(axis="y", alpha=0.3)
    _save(fig, "fig_pos_perpendicularity")


def fig_directions() -> None:
    s = json.loads((OUT_DIR / "summary.json").read_text())
    g_l, g_b = s["g_hat_matter_lb"]

    fig = plt.figure(figsize=(10, 5.5))
    ax = fig.add_subplot(111, projection="mollweide")

    l, b = _ll_to_rad(g_l, g_b)
    ax.scatter([l], [b], s=240, marker="X", color="#2a7fbf", zorder=6,
               edgecolor="black", linewidths=1.2,
               label=fr"$\hat g_{{\rm matter}}$ ({g_l}, {g_b:+d})")

    colors = {"MW VPOS": "#d96b1f", "M31 GPoA": "#a01818",
              "CenA plane": "#6aa84f"}
    for host, (lh, bh) in PLANE_NORMALS.items():
        l, b = _ll_to_rad(lh, bh)
        ax.scatter([l], [b], s=130, color=colors[host],
                   edgecolor="black", zorder=4,
                   label=f"{host} normal ({lh:.0f}, {bh:+.0f})")

    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.18), ncol=2,
              fontsize=9)
    ax.set_title("Satellite-plane normals vs MATTER-channel $\\hat g$ "
                 "(galactic)", pad=20)
    _save(fig, "fig_pos_directions")


def main() -> int:
    fig_perpendicularity()
    fig_directions()
    # touch import to keep pos_data linked for downstream consumers
    _ = MW_VPOS
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
