#!/usr/bin/env python3
"""
download_papers.py

Parse a markdown or plain‑text file that lists robotic‑manipulation papers in the form
shown below and download every linked PDF, saving it into a directory hierarchy
<Type>/<Year>/<Paper_Title>.pdf.

Example snippet expected in the input file (Markdown):

## Sim-to-Real Transfer
- [2025] RE3SIM: Generating High-Fidelity Simulation Data via 3D‑Photorealistic Real‑to‑Sim for Robotic Manipulation [paper](https://arxiv.org/pdf/2502.08645)

The script turns that into:
    downloads/Sim-to-Real_Transfer/2025/RE3SIM_Generating_High_Fidelity_Simulation_Data_via_3D_Photorealistic_Real_to_Sim_for_Robotic_Manipulation.pdf

USAGE
-----
    python download_papers.py papers.md --out downloads

Dependencies: only the standard library plus the *requests* package.
Install it with `pip install requests` if it is not already available.
"""

import argparse
import os
import re
import sys
import unicodedata
from pathlib import Path
from typing import Optional

import requests

# --------------------------- helpers -----------------------------------------

def slugify(text: str) -> str:
    """Convert *text* to an ASCII‑only, filesystem‑friendly slug."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^A-Za-z0-9]+", "_", text)
    return text.strip("_")

# --------------------------- main routine ------------------------------------

def download_pdfs(input_file: Path, out_root: Path) -> None:
    cat_regex = re.compile(r"^##\s+(.*)")
    line_regex = re.compile(
        r"^\s*-\s*\[(\d{4})\]\s*(.+?)\s*\[\[(?:paper|documentation)\]\((https?://[^)]+)\)\]",
        re.IGNORECASE,
    )

    current_category: Optional[str] = None
    session = requests.Session()

    for lineno, raw_line in enumerate(input_file.read_text(encoding="utf-8").splitlines(), start=1):
        # Detect a new category header (## Physics‑aware Policy, etc.)
        cat_match = cat_regex.match(raw_line)
        if cat_match:
            current_category = slugify(cat_match.group(1))
            continue

        # Detect paper entry lines that contain a [paper](URL) hyperlink
        line_match = line_regex.match(raw_line)
        if line_match and current_category:
            year, title, url = line_match.groups()
            year = year.strip()
            title_clean = slugify(title.strip())

            target_dir = out_root / current_category / year
            target_dir.mkdir(parents=True, exist_ok=True)
            pdf_path = target_dir / f"{title_clean}.pdf"

            if pdf_path.exists():
                print(f"[skip] {pdf_path.relative_to(out_root)} (already downloaded)")
                continue

            print(f"[dl ] {title.strip()} -> {pdf_path.relative_to(out_root)}")
            try:
                with session.get(url, stream=True, timeout=30) as resp:
                    resp.raise_for_status()
                    with pdf_path.open("wb") as fp:
                        for chunk in resp.iter_content(chunk_size=8192):
                            fp.write(chunk)
            except Exception as exc:
                print(f"[err] line {lineno}: failed to download {url} :: {exc}", file=sys.stderr)
                # Optionally, clean up partial downloads
                if pdf_path.exists():
                    pdf_path.unlink(missing_ok=True)

# --------------------------- CLI wrapper -------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Download PDFs referenced by [paper](url) links in a markdown list.")
    p.add_argument("input", type=Path, help="Path to the markdown / text file containing the list")
    p.add_argument("--out", type=Path, default=Path("downloads"), help="Root folder to store the PDFs (default: ./downloads)")
    return p.parse_args()

if __name__ == "__main__":
    args = parse_args()
    if not args.input.exists():
        sys.exit(f"Input file {args.input} does not exist")
    try:
        download_pdfs(args.input, args.out)
    except KeyboardInterrupt:
        sys.exit("Interrupted by user")
