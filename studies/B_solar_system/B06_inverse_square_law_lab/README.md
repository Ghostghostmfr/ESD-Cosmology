# Study B06 — Inverse-square-law lab tests (Eöt-Wash, HUST)

**Status:** 4/4 gates PASS.

Tabletop tests of Newton's $1/r^2$ law parameterize a Yukawa
deviation:

$$
V(r) = -\frac{G m_1 m_2}{r}\left[1 + \alpha\, e^{-r/\lambda}\right].
$$

The strongest bounds in the $10\,\mu\text{m}$–$1\,\text{mm}$ band come
from Eöt-Wash torsion-balance experiments (Kapner+ 2007 PRL 98 021101;
Lee+ 2020 PRL 124 101101) and HUST (Tan+ 2020 PRL 124 051301).

## ESD prediction

At lab benchtop scales the local acceleration is dominated by Earth's
surface gravity $g_\oplus \simeq 9.81$ m s$^{-2}$, giving $u_{\rm lab}
= 4 g_\oplus/a_0 \approx 3.3\times 10^{11}$ and $R(u_{\rm lab}) \sim
10^{-19}$. The closure-pool kernel cannot produce a Yukawa
contribution at these scales; the predicted $\alpha$ is zero
identically (no scalar dilaton in the metric sector — Study 19).

## Anchors

| experiment | $\lambda$ (μm) | $|\alpha|$ 95% upper bound | ref |
|---|---|---|---|
| Lee+ 2020 (Eöt-Wash) | 38   | $1$           | PRL 124 101101 |
| Lee+ 2020 (Eöt-Wash) | 52   | $0.1$         | PRL 124 101101 |
| Kapner+ 2007         | 56   | $0.1$         | PRL 98 021101 |
| Tan+ 2020 (HUST)     | 70   | $0.014$       | PRL 124 051301 |
| Tan+ 2020 (HUST)     | 480  | $9\times10^{-6}$ | PRL 124 051301 |

## Gates

| # | Claim | Gate | Verdict |
|---|---|---|---|
| 1 | $R(u_{\rm lab}) \le 10^{-15}$ at Earth surface | $\le 10^{-15}$ | PASS |
| 2 | Predicted $|\alpha|$ inside all 5 published bounds | inside | PASS |
| 3 | Max $|\alpha_{\rm ESD}|/|\alpha_{\rm bound}|$ across all $\lambda$ $\le 10^{-3}$ | $\le 10^{-3}$ | PASS |
| 4 | h-blindness: $|R(60)-R(80)| \le 10^{-6}$ | $\le 10^{-6}$ | PASS |

## Run

```bash
cd studies/B_solar_system/B06_inverse_square_law_lab
pip install -r requirements.txt
make all
```
