# Deployment Plan — Visual GitHub Profile README

## 1. Environment & Prerequisites
- **Target Repository:** `https://github.com/shubham-bramhane/shubham-bramhane` (`main` branch).
- **Local Tools:** Git, Python 3.10+ (standard library only), and Google Chrome (only when regenerating the PDF overview or visual QA previews).
- **Secrets / Env Vars:** None.

## 2. Regeneration & Validation Steps
```powershell
# 1. Regenerate 48 Dark/Light SVG visuals (v7.0 GTA VI Vice Sunset Edition)
python scripts/generate_assets.py

# 2. Regenerate shareable 1-page PDF overview (after editing docs/shubham-bramhane-overview.html)
Start-Process -FilePath "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList @('--headless=new','--disable-gpu','--no-pdf-header-footer','--print-to-pdf=D:\shubham-bramhane\docs\shubham-bramhane-overview.pdf','file:///D:/shubham-bramhane/docs/shubham-bramhane-overview.html') -Wait

# 3. Validate all assets, links, facts & documentation deliverables
python scripts/verify_profile.py
```

## 3. Release Procedure
```powershell
git status
git add README.md assets/ scripts/ docs/
git commit -m "Redesign GitHub profile README with portfolio-aligned Bento visuals"
git push origin main
```

## 4. Post-Deployment Smoke Checks
1. Open `https://github.com/shubham-bramhane` and confirm Hero, KPI Strip, Pillars, Tech Stack, 6 Case Study Cards, Journey Timeline, 6 Contact Cards, and Footer render cleanly.
2. Switch GitHub Appearance Settings between Dark Default and Light Default to verify `<picture>` theme adaptation.
3. Click the Hero, Resume PDF (`shubham_bramhane_resume.pdf`), Portfolio, LinkedIn, and Project links to verify HTTP 200 targets.

## 5. Rollback Procedure
- Revert cleanly via Git without losing history:
  ```powershell
  git revert HEAD
  git push origin main
  ```
- Or restore the previous plain-text README (`62e02cc`) directly if needed.
