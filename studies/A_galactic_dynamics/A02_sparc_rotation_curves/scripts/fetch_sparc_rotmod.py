"""Fetch and cache the full SPARC distribution for study 03.

Same behaviour as `studies/A01_baryonic_tully_fisher/scripts/fetch_sparc_rotmod.py`: if the
shipped data files in `data/` are already present (which they are in
this distribution), this is a no-op.  Otherwise we try, in order:

  1. A local development mirror inside the larger UTF workspace,
  2. the CWRU SPARC distribution
       http://astroweb.cwru.edu/SPARC/SPARC_Lelli2016c.mrt
       http://astroweb.cwru.edu/SPARC/Rotmod_LTG.zip
  3. a VizieR fallback for the master table.

On success writes:
  data/SPARC_Lelli2016c.mrt
  data/Rotmod_LTG/<Galaxy>_rotmod.dat   (175 files)
"""

from __future__ import annotations

import argparse
import io
import os
import shutil
import sys
import urllib.request
import zipfile

_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(_HERE, "..", "data"))
MRT_PATH = os.path.join(DATA_DIR, "SPARC_Lelli2016c.mrt")
ROTMOD_DIR = os.path.join(DATA_DIR, "Rotmod_LTG")

# Optional local development mirror (exists only inside the larger UTF
# workspace; silently skipped in a standalone deployment).
LOCAL_MIRROR = os.path.abspath(
    os.path.join(_HERE, "..", "..", "..", "..", "..", "repro", "data")
)
LOCAL_MRT = os.path.join(LOCAL_MIRROR, "SPARC_Lelli2016c.mrt")
LOCAL_ROTMOD_DIR = os.path.join(LOCAL_MIRROR, "Rotmod_LTG")

MRT_URLS = [
    "http://astroweb.cwru.edu/SPARC/SPARC_Lelli2016c.mrt",
    "https://cdsarc.cds.unistra.fr/ftp/J/AJ/152/157/table1.dat",
]
ROTMOD_URLS = [
    "http://astroweb.cwru.edu/SPARC/Rotmod_LTG.zip",
]


def _download(urls: list[str], dest: str) -> None:
    last_err: Exception | None = None
    for url in urls:
        print(f"[fetch] downloading {url}")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "esd-rc/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                payload = r.read()
            with open(dest, "wb") as f:
                f.write(payload)
            print(f"[fetch]   -> wrote {dest} ({len(payload)} bytes)")
            return
        except Exception as e:  # noqa: BLE001
            print(f"[fetch]   -> failed: {e}")
            last_err = e
    raise RuntimeError(f"All mirrors failed for {dest}; last error: {last_err}")


def _download_zip_and_extract(urls: list[str], extract_to: str) -> None:
    last_err: Exception | None = None
    for url in urls:
        print(f"[fetch] downloading {url}")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "esd-rc/1.0"})
            with urllib.request.urlopen(req, timeout=120) as r:
                payload = r.read()
            print(f"[fetch]   -> got {len(payload)} bytes, extracting")
            os.makedirs(extract_to, exist_ok=True)
            with zipfile.ZipFile(io.BytesIO(payload)) as zf:
                for info in zf.infolist():
                    if info.is_dir():
                        continue
                    name = os.path.basename(info.filename)
                    if not name:
                        continue
                    with zf.open(info) as src:
                        data = src.read()
                    with open(os.path.join(extract_to, name), "wb") as dst:
                        dst.write(data)
            n = len(os.listdir(extract_to))
            print(f"[fetch]   -> extracted to {extract_to} (total {n} files)")
            return
        except Exception as e:  # noqa: BLE001
            print(f"[fetch]   -> failed: {e}")
            last_err = e
    raise RuntimeError(f"All mirrors failed for rotmod archive; last error: {last_err}")


def _copy_from_local(force: bool) -> tuple[bool, bool]:
    have_mrt = os.path.exists(MRT_PATH) and not force
    have_rotmod = (
        os.path.isdir(ROTMOD_DIR)
        and len([f for f in os.listdir(ROTMOD_DIR)
                 if f.endswith("_rotmod.dat")]) > 100
        and not force
    )
    if not have_mrt and os.path.exists(LOCAL_MRT):
        print(f"[fetch] copying master table from local mirror: {LOCAL_MRT}")
        shutil.copyfile(LOCAL_MRT, MRT_PATH)
        have_mrt = True
    if not have_rotmod and os.path.isdir(LOCAL_ROTMOD_DIR):
        files = [f for f in os.listdir(LOCAL_ROTMOD_DIR)
                 if f.endswith("_rotmod.dat")]
        if len(files) > 100:
            print(f"[fetch] copying {len(files)} rotmod files from local mirror")
            os.makedirs(ROTMOD_DIR, exist_ok=True)
            for f in files:
                shutil.copyfile(os.path.join(LOCAL_ROTMOD_DIR, f),
                                os.path.join(ROTMOD_DIR, f))
            have_rotmod = True
    return have_mrt, have_rotmod


def fetch(force: bool = False) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    have_mrt, have_rotmod = _copy_from_local(force)
    if not have_mrt:
        _download(MRT_URLS, MRT_PATH)
    else:
        print(f"[fetch] master table cache OK: {MRT_PATH}")
    if not have_rotmod:
        _download_zip_and_extract(ROTMOD_URLS, ROTMOD_DIR)
    else:
        n = len([f for f in os.listdir(ROTMOD_DIR) if f.endswith("_rotmod.dat")])
        print(f"[fetch] rotmod cache OK: {ROTMOD_DIR} ({n} files)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--force", action="store_true", help="redownload even if cached")
    args = ap.parse_args()
    try:
        fetch(force=args.force)
    except Exception as e:  # noqa: BLE001
        print(f"[fetch] ERROR: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
