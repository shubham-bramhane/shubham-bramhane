# Product Requirements Document (PRD) — Visual GitHub Profile README

## 1. Problem Statement
The original `README.md` for `github.com/shubham-bramhane` was an outdated plain-text Markdown profile that did not reflect Shubham Bramhane's current portfolio brand (`https://my-portfolio-beta-bay-93.vercel.app/`), 5+ years of production engineering experience, enterprise healthcare/TMS case studies, or AI-augmented engineering workflow.

## 2. Target Audience / Personas
- **Technical Recruiters & Engineering Leaders:** Need an immediate high-signal visual scan of seniority (5+ years), measurable impact (`+30%` query velocity, `3.5x` AI sprint velocity, `10+ hrs/wk` automated), flagship production platforms, and one-click access to Live Portfolio, Resume PDF, LinkedIn, Email, X, and Phone.
- **Peers & Collaborators:** Look for concrete system architecture depth across Laravel 11, React/Next.js/Vue, Redis/MySQL/PostgreSQL, Python automation/data science, AWS, and agentic AI workflows.
- **Profile Owner (Shubham Bramhane):** Needs a maintainable, self-hosted visual profile that matches his Next.js portfolio aesthetic and never breaks due to third-party badge/stats outages.

## 3. Goals & Non-Goals
### Goals
- Align the GitHub Profile README 1:1 with the Obsidian + Electric Purple / Sunset Coral-Amber / Emerald Bento visual identity of `https://my-portfolio-beta-bay-93.vercel.app/`.
- Provide native GitHub Dark & Light mode adaptation across all 50 self-hosted SVG visuals (`25` Dark + `25` Light) via `<picture>`.
- Elevate the profile with Obsidian Glass depth (specular top rims, ambient corner halos, aurora silk ribbons), bespoke vector data visualizations (live photon sparkline, KPI mini-charts, animated 4-layer System Architecture Blueprint, 5-axis Engineering Capability Radar, stacked language spectrum), and a signature `धैर्यं सर्वत्र साधनम्।` Engineering Philosophy card echoing the GitHub avatar's golden sacred-geometry motif.
- Make the Hero CTA bar (4 buttons), featured production case studies (6 cards), and contact channels (6 cards) individually clickable with responsive percentage widths (`24%`, `48.5%`, `32%`) so multi-column alignment holds across laptop and desktop screens.
- Preserve all verified credentials from both the live portfolio and original README (Python Data Science libraries, AWS RDS/DynamoDB, Django/Flask/Laravel, MBA Finance & IT, B.E. CSE).

### Non-Goals
- No third-party external image badge services susceptible to downtime or rate-limiting.
- No JavaScript execution inside GitHub Markdown.

## 4. Functional Requirements
1. **Hero Banner (`hero-*.svg`):** `<SB/>` monogram, animated circuit traces & top shimmer scanline, live availability & `3.5x AI Velocity` pills, 2-line gradient display headline, stack pills, and `Architecture.ts` IDE window with embedded live Redis+SQL throughput sparkline.
2. **Hero Action CTA Bar (`cta-*-*.svg`):** 4 individually clickable glowing CTA buttons (`Explore Portfolio`, `Download Resume`, `LinkedIn Profile`, `Initiate Contact`) at `width="24%"`.
3. **Impact KPI Strip (`metrics-*.svg`):** 4 Bento metric cards (`5+ Yrs`, `+30%`, `3.5x`, `10+ hrs`) with embedded bar histogram, area sparkline, radial gauge, and automated pipeline visuals.
4. **Animated System Architecture Blueprint (`architecture-flow-*.svg`):** 4-stage production flow diagram with animated dashed packet streams connecting Client Edge → Laravel 11 & AI Engine → Data & Cloud → Production Impact.
5. **Capability Radar & Tech Stack (`tech-stack-*.svg`):** 5-axis Pentagon Engineering Radar paired with a 4-quadrant full-stack + AI capabilities Bento matrix.
6. **Featured Case Studies (`proj-*-*.svg`):** 6 individually clickable visual case study cards (`width="48.5%"`) featuring bespoke mini architectural thumbnails and `● LIVE ↗` indicators.
7. **Career Journey & Credentials (`journey-*.svg`):** Two-column visual timeline displaying 3 production roles (`Abym Technology`, `Finesoft Technologies`, `Magical Umbrella`), Academic Qualifications (`MBA Finance & IT`, `B.E. CSE 74.60% Distinction`), and Profile Snapshot.
8. **Clickable Contact Bento Grid (`card-*-*.svg`):** 3×2 symmetric row (`width="32%"`) of individually clickable cards (Live Portfolio, Resume PDF, LinkedIn, Email, X/Twitter, Phone) plus animated shimmer wave footer and collapsible plain-text `<details>` section.
9. **Shareable Overview PDF (`docs/shubham-bramhane-overview.pdf`):** Clean 1-page executive overview tracked in Git and linked in `README.md`.

## 5. Success Metrics
- 100% self-hosted SVG assets (`50` files) with zero external runtime image dependencies.
- 100% pass rate on `python scripts/verify_profile.py`.
- Visual QA pass in headless Chrome for both GitHub Dark (`#0D1117`) and GitHub Light (`#FFFFFF`) simulated `780px` containers.
