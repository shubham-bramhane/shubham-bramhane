# Technical Requirements Document (TRD) — Visual GitHub Profile README

## 1. System Architecture
This repository (`shubham-bramhane/shubham-bramhane`) is a static GitHub Profile repository driven by GitHub Flavored Markdown, sanitized HTML `<picture>` containers, and self-hosted SVG assets built deterministically from Python.

```text
scripts/generate_assets.py ──▶ assets/*-{dark,light}.svg (40 SVGs) ──▶ README.md (<picture> + clickable <a> cards)
scripts/verify_profile.py  ──▶ XML well-formedness, sandbox hygiene, link & doc verification
docs/shubham-bramhane-overview.html ──▶ Chrome headless (--print-to-pdf) ──▶ docs/shubham-bramhane-overview.pdf
```

## 2. Technology Stack
- **Markup:** GitHub Flavored Markdown + GitHub-allowed HTML (`<div>`, `<p>`, `<a>`, `<picture>`, `<source>`, `<img>`, `<details>`, `<summary>`, `<br/>`).
- **Visual Assets:** 40 standalone SVG files (`20` Dark + `20` Light) using system sans/mono font stacks and subtle GPU-friendly CSS `@keyframes` (`pulseDot`, `blinkCursor`, `breathe`, `pulseNode`).
- **Tooling:** Python 3 standard library only (`pathlib`, `html`, `xml.etree.ElementTree`, `re`, `sys`).
- **PDF Pipeline:** Print-styled HTML/CSS compiled via Google Chrome headless (`--print-to-pdf`).

## 3. Asset Inventory & Dimensions
| Asset Pattern | ViewBox | Rendered Width | Purpose |
| :--- | :---: | :---: | :--- |
| `assets/hero-{dark,light}.svg` | `1000×362` | `100%` | Portfolio-aligned Hero + `Architecture.ts` window |
| `assets/metrics-{dark,light}.svg` | `1000×114` | `100%` | 4-card engineering impact KPI strip |
| `assets/pillars-{dark,light}.svg` | `1000×236` | `100%` | 4-column core technical pillars |
| `assets/tech-stack-{dark,light}.svg` | `1000×396` | `100%` | 4-quadrant full-stack + AI capabilities matrix |
| `assets/projects-header-{dark,light}.svg` | `1000×46` | `100%` | Case studies eyebrow header |
| `assets/proj-{oncquest,fieldassist,lalpath,bigbasket,umbrella,portfolio}-{dark,light}.svg` | `486×152` | `428px` | 6 clickable 2×3 project case study cards |
| `assets/journey-{dark,light}.svg` | `1000×396` | `100%` | Career timeline + Academic credentials + Snapshot |
| `assets/connect-header-{dark,light}.svg` | `1000×92` | `100%` | Contact callout header |
| `assets/card-{portfolio,resume,linkedin,email,twitter,phone}-{dark,light}.svg` | `316×82` | `282px` | 6 clickable 3×2 contact Bento cards |
| `assets/footer-{dark,light}.svg` | `1000×68` | `100%` | Gradient wave `<SB/>` closing bar |

## 4. Layout & Sanitization Constraints
- **GitHub Desktop Container (~896px):**
  - 2-column project cards: `2 × 428px + spacing ≈ 866px <= 896px` (wraps to 1 column on mobile).
  - 3-column contact cards: `3 × 282px + spacing ≈ 862px <= 896px` (wraps cleanly on mobile).
- **SVG Image Sandbox:** No `@import`, external font URLs, external `<image>` links, or `<script>` tags inside `.svg` files (enforced by `scripts/verify_profile.py`).
- **Security:** Repository contains zero credentials, secrets, or private endpoints; all links are public portfolio/profile URLs.
