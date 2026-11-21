# Implementation Plan — Visual GitHub Profile README

## Phase 1: Portfolio & GitHub Audit (Completed)
- Audited existing `README.md`, live portfolio (`https://my-portfolio-beta-bay-93.vercel.app/`), and public GitHub profile/repositories (`github.com/shubham-bramhane`).
- Cataloged verified work history (5+ years), live production case studies, metrics, AI agentic stack, academic credentials, and social/contact links.

## Phase 2: Portfolio-Matched Bento Design System & SVG Generator (Completed)
- Engineered `scripts/generate_assets.py` matching the live portfolio's Obsidian + Electric Purple / Sunset Amber / Emerald / Cyan aesthetic with full Dark and Light themes.
- Generated 40 XML-validated SVGs under `assets/` covering Hero, KPI Strip, Core Pillars, Tech Stack, 6 Clickable Case Study Cards, Career & Education Timeline, 6 Clickable Contact Cards, and Footer Wave.

## Phase 3: README Assembly & Documentation Suite (Completed)
- Assembled `README.md` with `<picture>` Dark/Light switching, clickable 2×3 project gallery, clickable 3×2 contact grid, and collapsible plain-text `<details>` fallback.
- Created/updated `docs/prd.md`, `docs/trd.md`, `docs/implementation-plan.md`, `docs/testing-strategy.md`, `docs/deployment-plan.md`, and generated `docs/shubham-bramhane-overview.pdf`.

## Phase 4: Automated & Visual QA (Completed)
- Built `scripts/verify_profile.py` to enforce XML validity, sandbox safety, asset link parity, profile completeness, and documentation deliverables.
- Rendered full simulated GitHub Dark (`#0D1117`, `896px`) and Light (`#FFFFFF`, `896px`) HTML previews via headless Google Chrome and visually inspected screenshots to verify alignment, wrapping, and typography.

## Phase 5: Future Roadmap (Planned)
- **Live Open-Source Repo Spotlights:** Add dedicated clickable cards for `hotel-pos-laravel` and `Admin-Dashboard` or auto-sync repo stars via a lightweight GitHub Actions workflow.
- **MBA Completion Milestone:** Update MBA in Finance & IT status badge from `PURSUING` to `COMPLETED` upon graduation.
