"""Fetch and cache SPARC Table 1 (Lelli, McGaugh & Schombert 2016).

Tries mirrors in order; on success writes `data/sparc_table1.dat`.
Idempotent — if the cached copy already exists, prints a notice and
returns success.
"""

from __future__ import annotations

import os
import sys
import urllib.request

_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(_HERE, "..", "data"))
CACHE_PATH = os.path.join(DATA_DIR, "sparc_table1.dat")

SPARC_URLS = [
    "https://cdsarc.cds.unistra.fr/ftp/J/AJ/152/157/table1.dat",
    "http://astroweb.cwru.edu/SPARC/SPARC_Lelli2016c.mrt",
]


def fetch(force: bool = False) -> str:
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(CACHE_PATH) and not force:
        print(f"[fetch_sparc] cache already populated: {CACHE_PATH}")
        return CACHE_PATH
    last_err: Exception | None = None
    for url in SPARC_URLS:
        print(f"[fetch_sparc] fetching {url}")
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "esd-btfr-test/1.0"}
            )
            with urllib.request.urlopen(req, timeout=30) as r:
                payload = r.read()
            with open(CACHE_PATH, "wb") as f:
                f.write(payload)
            print(f"[fetch_sparc] wrote {CACHE_PATH} ({len(payload)} bytes)")
            return CACHE_PATH
        except Exception as e:  # noqa: BLE001
            print(f"[fetch_sparc]  -> failed: {e}")
            last_err = e
    raise RuntimeError(
        f"All SPARC mirrors failed; last error: {last_err}"
    )


if __name__ == "__main__":
    try:
        fetch()
    except Exception as e:  # noqa: BLE001
        print(f"[fetch_sparc] ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)
