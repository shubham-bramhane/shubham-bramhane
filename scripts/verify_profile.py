#!/usr/bin/env python3
"""
Verification suite for Shubham Bramhane's Visual GitHub Profile README.
Validates SVG XML safety, asset links in README.md, mandatory profile facts,
and presence of project documentation deliverables.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
ASSETS = ROOT / "assets"

REQUIRED_DOCS = [
    "docs/prd.md",
    "docs/trd.md",
    "docs/implementation-plan.md",
    "docs/testing-strategy.md",
    "docs/deployment-plan.md",
    "docs/shubham-bramhane-overview.pdf",
]

REQUIRED_README_FACTS = [
    "Shubham Bramhane",
    "https://my-portfolio-beta-bay-93.vercel.app/",
    "https://my-portfolio-beta-bay-93.vercel.app/shubham_bramhane_resume.pdf",
    "https://www.linkedin.com/in/shubham1602/",
    "https://x.com/shubhbramhane16",
    "shubham.bramhane75@gmail.com",
    "+91-8857916707",
    "https://oncquestlabs.com",
    "https://www.lalpathlabs.com",
    "https://bbtms.centumlearnpro.in",
]


def main() -> int:
    errors: list[str] = []

    if not README.exists():
        print("FAIL: README.md not found")
        return 1

    readme_text = README.read_text(encoding="utf-8")

    # 1. Check all local asset references exist
    refs = re.findall(r'(?:src|srcset)="([^"]+)"', readme_text)
    if not refs:
        errors.append("No image/source asset references found in README.md")

    for ref in refs:
        if ref.startswith(("http://", "https://")):
            continue
        target = ROOT / ref.lstrip("./")
        if not target.exists():
            errors.append(f"Missing referenced asset: {ref}")

    # 2. Validate every SVG in assets/
    svg_files = sorted(ASSETS.glob("*.svg"))
    if not svg_files:
        errors.append("No SVG assets found in assets/")

    for svg in svg_files:
        raw = svg.read_text(encoding="utf-8")
        try:
            root = ET.fromstring(raw.encode("utf-8"))
        except ET.ParseError as exc:
            errors.append(f"Invalid XML in {svg.name}: {exc}")
            continue

        if "viewBox" not in root.attrib:
            errors.append(f"Missing viewBox in {svg.name}")
        if "<script" in raw.lower():
            errors.append(f"Forbidden <script> tag in {svg.name}")
        sanitized = raw.replace("http://www.w3.org/2000/svg", "")
        if "http://" in sanitized.lower() or "https://" in sanitized.lower() or "@import" in sanitized.lower():
            errors.append(f"External network reference found in {svg.name}")

    # 3. Verify core profile facts in README.md
    for fact in REQUIRED_README_FACTS:
        if fact not in readme_text:
            errors.append(f"Required profile info missing from README.md: {fact}")

    # 4. Verify mandatory engineering documentation + PDF exist and are linked
    for doc in REQUIRED_DOCS:
        doc_path = ROOT / doc
        if not doc_path.exists():
            errors.append(f"Missing documentation deliverable: {doc}")
        elif doc_path.stat().st_size == 0:
            errors.append(f"Empty documentation deliverable: {doc}")
        if doc not in readme_text:
            errors.append(f"Documentation link missing from README.md: {doc}")

    if errors:
        print("VERIFICATION FAILED:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"VERIFICATION PASSED: {len(svg_files)} SVGs valid, {len(refs)} asset refs verified, {len(REQUIRED_DOCS)} docs checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
