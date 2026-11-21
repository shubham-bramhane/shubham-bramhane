# Technical Requirements Document (TRD) — Visual GitHub Profile README

## 1. System Architecture
This repository (`shubham-bramhane/shubham-bramhane`) is a static GitHub Profile repository driven by GitHub Flavored Markdown, sanitized HTML `<picture>` containers, and self-hosted SVG assets built deterministically from Python.

```text
scripts/generate_assets.py ──▶ assets/*-{dark,light}.svg (50 SVGs) ──▶ README.md (<picture> + responsive clickable <a> grids)
scripts/verify_profile.py  ──▶ XML well-formedness, sandbox hygiene, link & doc verification
docs/shubham-bramhane-overview.html ──▶ Chrome headless (--print-to-pdf) ──▶ docs/shubham-bramhane-overview.pdf
```

## 2. Technology Stack
- **Markup:** GitHub Flavored Markdown + GitHub-allowed HTML (`<div>`, `<p>`, `<a>`, `<picture>`, `<source>`, `<img>`, `<details>`, `<summary>`, `<br/>`).
- **Visual Assets:** 2 bespoke GTA VI Vice-Sunset painterly Hero Banner PNGs (`hero-banner-{dark,light}.png`, transparent rounded corners) + 48 standalone Bento SVG files (`24` Dark + `24` Light) styled in the **GTA VI Vice Sunset** system (Vice twilight glass `#161024`/`#0B0814`, flamingo pink `#FF4D94`, Miami sunset coral-gold `#FF9248`/`#FFC457`, Ocean Drive aqua `#00E5FF`, palm mint `#2CE6B8`, pastel sunlit Light Mode `#FFFFFF`/`#FFF6FA`), using refined typography, specular top hairlines, ambient corner halos, CSS `@keyframes`, and declarative SMIL `<animateMotion>` traveling data photons.
- **Tooling:** Python 3 standard library only (`pathlib`, `html`, `math`, `xml.etree.ElementTree`, `re`, `sys`).
- **PDF Pipeline:** Print-styled HTML/CSS compiled via Google Chrome headless (`--print-to-pdf`).

## 3. Asset Inventory & Dimensions
| Asset Pattern | ViewBox | Rendered Width | Purpose |
| :--- | :---: | :---: | :--- |
| `assets/hero-banner-{dark,light}.png` | `1200×594` | `100%` | Minimalist 3D Studio Frosted-Glass & Glacier Light Hero Banner |
| `assets/cta-{portfolio,resume,linkedin,contact}-{dark,light}.svg` | `238×58` | `24%` | 4-across specular glowing clickable Hero Action Bar |
| `assets/metrics-{dark,light}.svg` | `1000×130` | `100%` | 4-card KPI strip with embedded bar/sparkline/radial/pipeline charts |
| `assets/architecture-flow-{dark,light}.svg` | `1000×280` | `100%` | Animated 4-layer Architecture Blueprint with gliding fiber-optic light orbs |
| `assets/tech-stack-{dark,light}.svg` | `1000×428` | `100%` | 5-axis Engineering Capability Radar + 4-quadrant Glass Stack Matrix |
| `assets/projects-header-{dark,light}.svg` | `1000×44` | `100%` | Case studies eyebrow header |
| `assets/proj-{oncquest,fieldassist,lalpath,bigbasket,umbrella,portfolio}-{dark,light}.svg` | `488×162` | `48.5%` | 6 clickable 2×3 glass project cards with mini architectural thumbnails |
| `assets/telemetry-{dark,light}.svg` | `1000×198` | `100%` | Open-Source Language Spectrum + Golden Mandala Philosophy Card |
| `assets/journey-{dark,light}.svg` | `1000×396` | `100%` | Career timeline + Academic credentials + Base & Collaboration card |
| `assets/connect-header-{dark,light}.svg` | `1000×90` | `100%` | Contact callout header |
| `assets/card-{portfolio,resume,linkedin,email,twitter,phone}-{dark,light}.svg` | `316×84` | `32%` | 6 clickable 3×2 glass contact Bento cards |
| `assets/footer-{dark,light}.svg` | `1000×76` | `100%` | Animated dual-wave shimmer `<SB/>` closing bar |

## 4. Layout & Sanitization Constraints
- **Responsive Multi-Column Alignment Across All Viewports (760px–1440px+):**
  - 4-button Hero CTA bar: `width="24%"` (`4 × 24% = 96%`).
  - 2-column project cards: `width="48.5%"` (`2 × 48.5% = 97%`).
  - 3-column contact cards: `width="32%"` (`3 × 32% = 96%`).
- **SVG Image Sandbox:** No `@import`, external font URLs, external `<image>` links, or `<script>` tags inside `.svg` files (enforced by `scripts/verify_profile.py`).
- **HTML Attribute Hygiene:** Avoid raw `>` characters inside `alt="..."` attributes to prevent HTML tag truncation across parsers.
