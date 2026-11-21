# Testing Strategy — Visual GitHub Profile README

## 1. Test Pyramid
1. **Automated Static Verification (`scripts/verify_profile.py`):**
   - XML well-formedness & `viewBox` presence across all 48 SVG files in `assets/`.
   - Security/sandbox checks ensuring zero `<script>`, `@import`, or external `http(s)` references inside SVGs.
   - Link integrity verifying every local `src` and `srcset` path (`72` refs) in `README.md` exists on disk.
   - Fact & deliverable checks verifying core URLs (Portfolio, Resume PDF, LinkedIn, X, Email, Phone, flagship platforms) and all 6 mandatory `docs/` deliverables exist and are linked.
2. **Visual Regression & Layout Inspection (Headless Chrome):**
   - Render a simulated GitHub README container (`780px` laptop viewport width) in both Dark (`#0D1117`) and Light (`#FFFFFF`) modes and capture full-page PNG screenshots.
   - Inspect screenshots to verify zero text truncation/overlap inside `Architecture.ts`, 5-axis Engineering Radar labels, animated System Architecture Blueprint nodes, 4-across CTA bar, 2×3 case study grid, and 3×2 contact grid.
3. **PDF Print Inspection:**
   - Render `docs/shubham-bramhane-overview.html` to `docs/shubham-bramhane-overview.pdf` and verify clean pagination and typography.
4. **Post-Push Live GitHub QA:**
   - Verify `https://github.com/shubham-bramhane` on desktop (Dark & Light themes) and mobile viewport (~390px), testing every clickable case study and contact card.

## 2. Commands
```powershell
# Regenerate all 40 SVG visual assets
python scripts/generate_assets.py

# Run automated verification checks
python scripts/verify_profile.py
```

## 3. Critical Edge Cases Verified
- Long email (`shubham.bramhane75@gmail.com`) and portfolio URL (`my-portfolio-beta-bay-93.vercel.app`) fit completely inside `316×82` contact cards without clipping.
- Multi-row pill wrapping in `hero-*.svg` and `tech-stack-*.svg` respects card right boundaries (`max_x`) automatically.
- 2-column project cards (`428px`) and 3-column contact cards (`282px`) stay aligned inside GitHub's `896px` profile width without premature wrapping.
