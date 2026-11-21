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
- Provide native GitHub Dark & Light mode adaptation across all 40 self-hosted SVG visuals (`20` Dark + `20` Light) via `<picture>`.
- Make every featured production case study (6 cards) and every contact channel (6 cards) individually clickable.
- Preserve all verified credentials from both the live portfolio and original README (Python Data Science libraries, AWS RDS/DynamoDB, Django/Flask/Laravel, MBA Finance & IT, B.E. CSE).

### Non-Goals
- No third-party external image badge services susceptible to downtime or rate-limiting.
- No JavaScript execution inside GitHub Markdown.

## 4. Functional Requirements
1. **Hero Banner (`hero-*.svg`):** `<SB/>` monogram, live availability & `3.5x AI Velocity` pills, gradient display headline, executive summary, stack pills, and styled `Architecture.ts` code card.
2. **Impact KPI Strip (`metrics-*.svg`):** 4 Bento metric cards (`5+ Yrs`, `+30%`, `3.5x`, `10+ hrs`).
3. **Core Technical Pillars (`pillars-*.svg`):** 4 Bento competence cards (Full-Stack Architecture, AI-Augmented Velocity, Performance & Caching, Data & Tech-Finance).
4. **Skills & Tech Stack (`tech-stack-*.svg`):** 2×2 asymmetric Bento matrix covering Backend & Python Data, AI Agentic Engineering, Frontend & UI Systems, and Databases, Cloud & DevOps.
5. **Featured Case Studies (`proj-*-*.svg`):** 6 individually clickable visual case study cards linking live production platforms (Oncquest Healthcare, OncqFieldAssist, Lal Path Labs, Big Basket TMS, Magical Umbrella, Next-Gen Portfolio & Hotel POS).
6. **Career Journey & Credentials (`journey-*.svg`):** Two-column visual timeline displaying 3 production roles (`Abym Technology`, `Finesoft Technologies`, `Magical Umbrella`), Academic Qualifications (`MBA Finance & IT`, `B.E. CSE 74.60% Distinction`), and Profile Snapshot.
7. **Clickable Contact Bento Grid (`card-*-*.svg`):** 3×2 symmetric row of individually clickable cards (Live Portfolio, Resume PDF, LinkedIn, Email, X/Twitter, Phone) plus gradient wave footer and collapsible plain-text `<details>` section.
8. **Shareable Overview PDF (`docs/shubham-bramhane-overview.pdf`):** Clean executive overview tracked in Git and linked in `README.md`.

## 5. Success Metrics
- 100% self-hosted SVG assets (`40` files) with zero external runtime image dependencies.
- 100% pass rate on `python scripts/verify_profile.py`.
- Visual QA pass in headless Chrome for both GitHub Dark (`#0D1117`) and GitHub Light (`#FFFFFF`) simulated `896px` containers.
