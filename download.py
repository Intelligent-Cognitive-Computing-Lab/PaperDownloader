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
from tqdm import tqdm

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
    failed_downloads = []

    lines = input_file.read_text(encoding="utf-8").splitlines()
    
    # First pass: count total papers to download
    total_papers = 0
    for raw_line in lines:
        cat_match = cat_regex.match(raw_line)
        if cat_match:
            current_category = slugify(cat_match.group(1))
            continue
            
        line_match = line_regex.match(raw_line)
        if line_match and current_category:
            year, title, url = line_match.groups()
            title_clean = slugify(title.strip())
            target_dir = out_root / current_category / year
            pdf_path = target_dir / f"{title_clean}.pdf"
            
            # Only count if not already downloaded
            if not pdf_path.exists():
                total_papers += 1

    # Second pass: download papers with progress bar
    current_category = None
    processed_papers = 0
    
    with tqdm(total=total_papers, desc="📥 Downloading papers", unit="paper") as pbar:
        for lineno, raw_line in enumerate(lines, start=1):
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
                    tqdm.write(f"⏭️  [skip] {title.strip()} (already downloaded)")
                    continue

                tqdm.write(f"📄 {title.strip()}")
                try:
                    resp = session.get(url, stream=True, timeout=30)
                    resp.raise_for_status()
                    
                    # Get the total file size from headers
                    total_size = int(resp.headers.get('content-length', 0))
                    
                    with pdf_path.open("wb") as fp:
                        # Create progress bar for this file
                        with tqdm(
                            total=total_size,
                            unit='B',
                            unit_scale=True,
                            desc=f"   📥 {title_clean[:30]}...",
                            leave=False,
                            ncols=100
                        ) as file_pbar:
                            for chunk in resp.iter_content(chunk_size=8192):
                                fp.write(chunk)
                                file_pbar.update(len(chunk))
                    
                    processed_papers += 1
                    pbar.set_postfix({"Success": processed_papers})
                    pbar.update(1)
                    
                except Exception as exc:
                    tqdm.write(f"❌ [err] line {lineno}: failed to download {title.strip()} :: {exc}")
                    failed_downloads.append((current_category, title.strip(), url))
                    # Optionally, clean up partial downloads
                    if pdf_path.exists():
                        pdf_path.unlink(missing_ok=True)
                    pbar.update(1)

    # Summary of failed downloads
    if failed_downloads:
        print(f"\n🚨 Summary of failed downloads:")
        for category, title, url in failed_downloads:
            print(f"   - [{category}] {title}")
            print(f"     📎 {url}")
    else:
        print(f"\n🎉 All papers downloaded successfully!")

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
    
    # Check if tqdm is installed
    try:
        from tqdm import tqdm as _
    except ImportError:
        sys.exit("This script requires the tqdm package. Install it with 'pip install tqdm'")
        
    try:
        download_pdfs(args.input, args.out)
    except KeyboardInterrupt:
        sys.exit("Interrupted by user")