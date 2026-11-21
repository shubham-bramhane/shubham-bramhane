#!/usr/bin/env python3
"""
Deterministic SVG visual asset generator for Shubham Bramhane's GitHub Profile README.
Aligned with the visual language of https://my-portfolio-beta-bay-93.vercel.app/
Generates matched Dark & Light Bento-style SVG visuals into ./assets/.
Zero third-party dependencies — Python standard library only.
"""

from __future__ import annotations

import html
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "assets"

FONT_SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
FONT_MONO = "'Cascadia Code', 'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

THEMES = {
    "dark": {
        "canvas": "#0D1117",
        "card": "#10121B",
        "card_alt": "#151826",
        "elevated": "#1A1E30",
        "code_bg": "#0A0C14",
        "code_bar": "#121524",
        "border": "#22273D",
        "border_strong": "#2E3554",
        "dot_grid": "#252B45",
        "dot_opacity": "0.55",
        "text": "#F8FAFC",
        "text_sub": "#A1A9C0",
        "text_muted": "#6B7490",
        "rule": "#1F2438",
        # Signature portfolio palette: Electric Purple, Sunset Coral/Amber, Emerald, Cyan, Rose
        "purple": "#A855F7",
        "purple_soft": "#C084FC",
        "purple_bg": "#211536",
        "purple_border": "#442870",
        "amber": "#FB923C",
        "amber_gold": "#FBBF24",
        "amber_bg": "#2E1E10",
        "amber_border": "#663D19",
        "emerald": "#34D399",
        "emerald_bg": "#0C2B22",
        "emerald_border": "#165745",
        "cyan": "#38BDF8",
        "cyan_bg": "#0E283D",
        "cyan_border": "#184C6E",
        "rose": "#FB7185",
        "rose_bg": "#331422",
        "rose_border": "#6B2441",
        "glow_opacity": "0.22",
        "code_kw": "#C084FC",
        "code_cls": "#38BDF8",
        "code_str": "#34D399",
        "code_prop": "#E2E8F0",
        "code_num": "#55607D",
        "code_punct": "#7683A3",
        "code_comment": "#64748B",
        "grad_text_1": "#FFFFFF",
        "grad_text_2": "#C084FC",
        "grad_text_3": "#FDBA74",
    },
    "light": {
        "canvas": "#FFFFFF",
        "card": "#FFFFFF",
        "card_alt": "#F8FAFC",
        "elevated": "#F1F5F9",
        "code_bg": "#0E111B",
        "code_bar": "#171B2B",
        "border": "#E2E8F0",
        "border_strong": "#CBD5E1",
        "dot_grid": "#CBD5E1",
        "dot_opacity": "0.6",
        "text": "#0F172A",
        "text_sub": "#475569",
        "text_muted": "#64748B",
        "rule": "#E2E8F0",
        "purple": "#7C3AED",
        "purple_soft": "#6D28D9",
        "purple_bg": "#F3E8FF",
        "purple_border": "#DDD6FE",
        "amber": "#EA580C",
        "amber_gold": "#D97706",
        "amber_bg": "#FFF7ED",
        "amber_border": "#FED7AA",
        "emerald": "#059669",
        "emerald_bg": "#ECFDF5",
        "emerald_border": "#A7F3D0",
        "cyan": "#0284C7",
        "cyan_bg": "#E0F2FE",
        "cyan_border": "#BAE6FD",
        "rose": "#E11D48",
        "rose_bg": "#FFF1F2",
        "rose_border": "#FECDD3",
        "glow_opacity": "0.13",
        "code_kw": "#C084FC",
        "code_cls": "#38BDF8",
        "code_str": "#34D399",
        "code_prop": "#F1F5F9",
        "code_num": "#64748B",
        "code_punct": "#94A3B8",
        "code_comment": "#94A3B8",
        "grad_text_1": "#4C1D95",
        "grad_text_2": "#7C3AED",
        "grad_text_3": "#EA580C",
    },
}


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def measure_pill(label: str, char_w: float = 6.9, pad_x: int = 22, min_w: int = 52) -> int:
    return max(min_w, int(round(len(label) * char_w + pad_x)))


def render_pill(
    x: int,
    y: int,
    label: str,
    bg: str,
    border: str,
    fg: str,
    dot_color: str | None = None,
    height: int = 26,
    font_size: int = 11.2,
    weight: int = 600,
    mono: bool = False,
    width: int | None = None,
) -> tuple[str, int]:
    char_w = 7.0 if mono else 6.6
    pad = 30 if dot_color else 20
    w = width if width is not None else measure_pill(label, char_w=char_w, pad_x=pad)
    rx = height // 2
    family = FONT_MONO if mono else FONT_SANS
    text_y = y + (height / 2) + (font_size * 0.35)
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{height}" rx="{rx}" '
        f'fill="{bg}" stroke="{border}" stroke-width="1"/>'
    ]
    if dot_color:
        parts.append(f'<circle cx="{x + 12}" cy="{y + height / 2:.1f}" r="3.2" fill="{dot_color}"/>')
        parts.append(
            f'<text x="{x + 21}" y="{text_y:.1f}" font-family="{family}" font-size="{font_size}" '
            f'font-weight="{weight}" fill="{fg}">{esc(label)}</text>'
        )
    else:
        parts.append(
            f'<text x="{x + w / 2:.1f}" y="{text_y:.1f}" text-anchor="middle" font-family="{family}" '
            f'font-size="{font_size}" font-weight="{weight}" fill="{fg}">{esc(label)}</text>'
        )
    return "\n".join(parts), w


def render_pills_wrapped(
    items: list[tuple[str, str, str, str, str | None]],
    start_x: int,
    start_y: int,
    max_x: int,
    row_gap: int = 34,
    col_gap: int = 8,
    height: int = 26,
    font_size: float = 11.2,
    mono: bool = False,
) -> str:
    out = []
    cx = start_x
    cy = start_y
    for label, bg, brd, fg, dot in items:
        char_w = 7.0 if mono else 6.6
        pad = 30 if dot else 20
        pw = measure_pill(label, char_w=char_w, pad_x=pad)
        if cx + pw > max_x and cx > start_x:
            cx = start_x
            cy += row_gap
        svg_p, actual_w = render_pill(cx, cy, label, bg, brd, fg, dot_color=dot, height=height, font_size=font_size, mono=mono, width=pw)
        out.append(svg_p)
        cx += actual_w + col_gap
    return "\n".join(out)


def render_section_header(title: str, subtitle: str, t: dict[str, str], accent: str, width: int = 1000) -> str:
    label_w = int(len(title) * 8.1 + 26)
    rule_x = 18 + label_w
    right_end = width - 6
    sub_svg = ""
    if subtitle:
        sub_svg = f'<text x="{right_end}" y="18.5" text-anchor="end" font-family="{FONT_MONO}" font-size="10.5" fill="{t["text_muted"]}">{esc(subtitle)}</text>'
        rule_end = right_end - int(len(subtitle) * 6.6 + 14)
    else:
        rule_end = right_end
    return f"""
  <g>
    <rect x="6" y="10" width="8" height="8" rx="2.5" fill="{accent}"/>
    <text x="22" y="18.5" font-family="{FONT_MONO}" font-size="11.5" font-weight="700" letter-spacing="1.8" fill="{t['text_sub']}">{esc(title)}</text>
    <line x1="{rule_x}" y1="14" x2="{max(rule_x + 20, rule_end)}" y2="14" stroke="{t['rule']}" stroke-width="1"/>
    {sub_svg}
  </g>"""


def build_hero(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 362

    hero_pills = [
        ("✦ PHP 8.3 / Laravel 11", t["elevated"], t["border_strong"], t["text"], None),
        ("✦ Redis (+30% Velocity)", t["elevated"], t["border_strong"], t["text"], None),
        ("✦ React.js & Next.js 16", t["elevated"], t["border_strong"], t["text"], None),
        ("✦ MySQL / PostgreSQL", t["elevated"], t["border_strong"], t["text"], None),
        ("✦ Python & AWS", t["elevated"], t["border_strong"], t["text"], None),
        ("✦ Google Antigravity & Copilot", t["purple_bg"], t["purple_border"], t["purple_soft"], None),
    ]
    pills_svg = render_pills_wrapped(hero_pills, start_x=36, start_y=264, max_x=572, row_gap=34, col_gap=8, height=27, font_size=11.0)

    code_lines = [
        ("01", f'<tspan fill="{t["code_comment"]}">// shubham-bramhane.ts — Core Architecture</tspan>'),
        ("02", f'<tspan fill="{t["code_kw"]}">export const</tspan> <tspan fill="{t["code_cls"]}" font-weight="700">engineer</tspan> <tspan fill="{t["code_punct"]}">= &#123;</tspan>'),
        ("03", f'  <tspan fill="{t["code_prop"]}">name</tspan><tspan fill="{t["code_punct"]}">:</tspan> <tspan fill="{t["code_str"]}">"Shubham Bramhane"</tspan><tspan fill="{t["code_punct"]}">,</tspan>'),
        ("04", f'  <tspan fill="{t["code_prop"]}">role</tspan><tspan fill="{t["code_punct"]}">:</tspan> <tspan fill="{t["code_str"]}">"Senior Full-Stack Architect"</tspan><tspan fill="{t["code_punct"]}">,</tspan>'),
        ("05", f'  <tspan fill="{t["code_prop"]}">exp</tspan><tspan fill="{t["code_punct"]}">:</tspan>  <tspan fill="{t["code_str"]}">"5+ Years Production"</tspan><tspan fill="{t["code_punct"]}">,</tspan>'),
        ("06", f'  <tspan fill="{t["code_prop"]}">backend</tspan><tspan fill="{t["code_punct"]}">: [</tspan><tspan fill="{t["code_str"]}">"Laravel 11"</tspan><tspan fill="{t["code_punct"]}">,</tspan> <tspan fill="{t["code_str"]}">"Redis"</tspan><tspan fill="{t["code_punct"]}">,</tspan> <tspan fill="{t["code_str"]}">"Python"</tspan><tspan fill="{t["code_punct"]}">],</tspan>'),
        ("07", f'  <tspan fill="{t["code_prop"]}">frontend</tspan><tspan fill="{t["code_punct"]}">: [</tspan><tspan fill="{t["code_str"]}">"React"</tspan><tspan fill="{t["code_punct"]}">,</tspan> <tspan fill="{t["code_str"]}">"Vue"</tspan><tspan fill="{t["code_punct"]}">,</tspan> <tspan fill="{t["code_str"]}">"Next.js 16"</tspan><tspan fill="{t["code_punct"]}">],</tspan>'),
        ("08", f'  <tspan fill="{t["code_prop"]}">dbCloud</tspan><tspan fill="{t["code_punct"]}">: [</tspan><tspan fill="{t["code_str"]}">"MySQL"</tspan><tspan fill="{t["code_punct"]}">,</tspan> <tspan fill="{t["code_str"]}">"Postgres"</tspan><tspan fill="{t["code_punct"]}">,</tspan> <tspan fill="{t["code_str"]}">"AWS"</tspan><tspan fill="{t["code_punct"]}">],</tspan>'),
        ("09", f'  <tspan fill="{t["code_prop"]}">aiStack</tspan><tspan fill="{t["code_punct"]}">: [</tspan><tspan fill="{t["code_str"]}">"Antigravity"</tspan><tspan fill="{t["code_punct"]}">,</tspan> <tspan fill="{t["code_str"]}">"Copilot"</tspan><tspan fill="{t["code_punct"]}">],</tspan>'),
        ("10", f'  <tspan fill="{t["code_prop"]}">impact</tspan><tspan fill="{t["code_punct"]}">:</tspan>  <tspan fill="{t["code_str"]}">"+30% Throughput · 3.5x AI"</tspan>'),
        ("11", f'<tspan fill="{t["code_punct"]}">&#125;;</tspan>'),
    ]

    code_svg = []
    cy = 96
    for num, markup in code_lines:
        code_svg.append(f'    <text x="604" y="{cy}" font-family="{FONT_MONO}" font-size="10.6" fill="{t["code_num"]}">{num}</text>')
        code_svg.append(f'    <text x="625" y="{cy}" font-family="{FONT_MONO}" font-size="10.6">{markup}</text>')
        cy += 18.8

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Shubham Bramhane - Senior Full-Stack Architect and AI-Augmented Engineer">
  <defs>
    <clipPath id="heroClip">
      <rect x="4" y="4" width="992" height="354" rx="22"/>
    </clipPath>
    <pattern id="dotGrid" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.1" fill="{t['dot_grid']}" fill-opacity="{t['dot_opacity']}"/>
    </pattern>
    <linearGradient id="brandBar" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['purple']}"/>
      <stop offset="52%" stop-color="{t['amber']}"/>
      <stop offset="100%" stop-color="{t['emerald']}"/>
    </linearGradient>
    <linearGradient id="headlineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['grad_text_1']}"/>
      <stop offset="48%" stop-color="{t['grad_text_2']}"/>
      <stop offset="100%" stop-color="{t['grad_text_3']}"/>
    </linearGradient>
    <radialGradient id="glowPurple" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{t['purple']}" stop-opacity="{t['glow_opacity']}"/>
      <stop offset="100%" stop-color="{t['purple']}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowAmber" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{t['amber']}" stop-opacity="{t['glow_opacity']}"/>
      <stop offset="100%" stop-color="{t['amber']}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="heroBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{t['card']}"/>
      <stop offset="100%" stop-color="{t['card_alt']}"/>
    </linearGradient>
    <style>
      @keyframes pulseDot {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}
      @keyframes blinkCursor {{ 0%, 49% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}
      @keyframes breathe {{ 0%, 100% {{ opacity: 0.95; }} 50% {{ opacity: 0.55; }} }}
      .pulse-dot {{ animation: pulseDot 2.1s ease-in-out infinite; }}
      .blink {{ animation: blinkCursor 1.15s steps(1) infinite; }}
      .orb {{ animation: breathe 6.5s ease-in-out infinite; }}
    </style>
  </defs>

  <g clip-path="url(#heroClip)">
    <rect x="4" y="4" width="992" height="354" fill="url(#heroBg)"/>
    <rect x="4" y="4" width="992" height="354" fill="url(#dotGrid)"/>
    <circle cx="140" cy="45" r="245" fill="url(#glowPurple)" class="orb"/>
    <circle cx="885" cy="315" r="250" fill="url(#glowAmber)" class="orb"/>
    <rect x="4" y="4" width="992" height="4" fill="url(#brandBar)"/>
  </g>
  <rect x="4" y="4" width="992" height="354" rx="22" fill="none" stroke="{t['border']}" stroke-width="1.2"/>

  <!-- Top Badges Row -->
  <g>
    <!-- <SB/> Mark -->
    <rect x="36" y="28" width="66" height="28" rx="9" fill="{t['elevated']}" stroke="{t['border_strong']}" stroke-width="1"/>
    <text x="69" y="46.2" text-anchor="middle" font-family="{FONT_MONO}" font-size="12.5" font-weight="800" fill="{t['text']}">&lt;SB/&gt;</text>

    <!-- Live Availability Badge -->
    <rect x="112" y="28" width="268" height="28" rx="14" fill="{t['emerald_bg']}" stroke="{t['emerald_border']}" stroke-width="1"/>
    <circle cx="127" cy="42" r="3.8" fill="{t['emerald']}" class="pulse-dot"/>
    <text x="138" y="46" font-family="{FONT_SANS}" font-size="11.2" font-weight="600" fill="{t['emerald']}">Available for High-Impact Roles &amp; Advisory</text>

    <!-- AI Velocity Badge -->
    <rect x="390" y="28" width="136" height="28" rx="14" fill="{t['amber_bg']}" stroke="{t['amber_border']}" stroke-width="1"/>
    <text x="458" y="46" text-anchor="middle" font-family="{FONT_MONO}" font-size="11" font-weight="700" fill="{t['amber_gold']}">⚡ 3.5x AI Velocity</text>
  </g>

  <!-- Main Display Heading -->
  <g>
    <text x="36" y="101" font-family="{FONT_SANS}" font-size="37" font-weight="800" letter-spacing="-0.8" fill="{t['text']}">Shubham Bramhane</text>
    <text x="36" y="132" font-family="{FONT_SANS}" font-size="18.2" font-weight="800" letter-spacing="-0.2" fill="url(#headlineGrad)">Architecting High-Throughput Systems · AI Velocity.</text>

    <text x="36" y="161" font-family="{FONT_SANS}" font-size="12.8" font-weight="700" fill="{t['emerald']}">Senior Full-Stack Architect &amp; AI-Augmented Engineer</text>
    <text x="372" y="161" font-family="{FONT_MONO}" font-size="11.2" font-weight="600" fill="{t['text_muted']}">· 5+ Yrs · MBA Finance</text>

    <text x="36" y="191" font-family="{FONT_SANS}" font-size="12.8" fill="{t['text_sub']}">Senior Full-Stack Engineer with 5+ years mastering the Laravel ecosystem,</text>
    <text x="36" y="211" font-family="{FONT_SANS}" font-size="12.8" fill="{t['text_sub']}">high-concurrency MySQL/PostgreSQL + Redis architectures, pan-India healthcare</text>
    <text x="36" y="231" font-family="{FONT_SANS}" font-size="12.8" fill="{t['text_sub']}">portals, Python data automation, and agentic AI engineering workflows.</text>
  </g>

  <!-- Stack Highlight Pills -->
  {pills_svg}

  <!-- Right Interactive-Look Code Window (Architecture.ts) -->
  <g>
    <rect x="590" y="28" width="376" height="304" rx="16" fill="{t['code_bg']}" stroke="{t['border_strong']}" stroke-width="1.2"/>
    <path d="M606 28 H950 A16 16 0 0 1 966 44 V64 H590 V44 A16 16 0 0 1 606 28 Z" fill="{t['code_bar']}"/>
    <line x1="590" y1="64" x2="966" y2="64" stroke="#22273D" stroke-width="1"/>
    <circle cx="609" cy="46" r="4.8" fill="#FF5F56"/>
    <circle cx="624" cy="46" r="4.8" fill="#FFBD2E"/>
    <circle cx="639" cy="46" r="4.8" fill="#27C93F"/>
    <rect x="658" y="36" width="108" height="21" rx="6" fill="#1D2238" stroke="#363E63" stroke-width="0.9"/>
    <text x="712" y="50" text-anchor="middle" font-family="{FONT_MONO}" font-size="10.2" font-weight="600" fill="#F1F5F9">Architecture.ts</text>
    <text x="780" y="50" font-family="{FONT_MONO}" font-size="10" fill="#64748B">AI-Engine.json</text>

{chr(10).join(code_svg)}
    <rect x="646" y="274" width="6.5" height="12.5" rx="1.5" fill="{t['purple_soft']}" class="blink"/>

    <!-- Window Status Footer -->
    <line x1="590" y1="298" x2="966" y2="298" stroke="#22273D" stroke-width="1"/>
    <circle cx="608" cy="315" r="3.5" fill="{t['emerald']}" class="pulse-dot"/>
    <text x="618" y="318.8" font-family="{FONT_MONO}" font-size="10" fill="#94A3B8">Production Ready · AI-Assisted</text>
    <rect x="816" y="304" width="136" height="21" rx="10.5" fill="#2E1E10" stroke="#663D19" stroke-width="0.9"/>
    <text x="884" y="317.8" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.6" font-weight="700" fill="#FBBF24">+30% Throughput</text>
  </g>
</svg>
"""


def build_metrics(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 114
    metrics = [
        ("5+ Yrs", "Laravel Ecosystem", "Enterprise & Microservices", t["purple"]),
        ("+30%", "Query Velocity", "Redis & Database Profiling", t["emerald"]),
        ("3.5x", "AI Sprint Velocity", "Antigravity & Copilot", t["amber"]),
        ("10+ hrs", "Weekly Automated", "Python Data Pipelines", t["cyan"]),
    ]
    cards = []
    x = 4
    for big, title, sub, acc in metrics:
        cards.append(f"""
  <g transform="translate({x}, 4)">
    <rect x="0" y="0" width="236" height="104" rx="15" fill="{t['card']}" stroke="{t['border']}" stroke-width="1.2"/>
    <rect x="20" y="0" width="46" height="3" rx="1.5" fill="{acc}"/>
    <text x="20" y="44" font-family="{FONT_SANS}" font-size="29" font-weight="800" letter-spacing="-0.6" fill="{t['text']}">{esc(big)}</text>
    <text x="20" y="68" font-family="{FONT_SANS}" font-size="13" font-weight="700" fill="{acc}">{esc(title)}</text>
    <text x="20" y="87" font-family="{FONT_MONO}" font-size="10.5" fill="{t['text_muted']}">{esc(sub)}</text>
  </g>""")
        x += 252
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Key Engineering Impact Metrics">
  {"".join(cards)}
</svg>
"""


def build_pillars(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 236
    pillars = [
        {
            "x": 4,
            "acc": t["purple"],
            "bg": t["purple_bg"],
            "brd": t["purple_border"],
            "badge": "MVC & MODULAR",
            "title": "Full-Stack Architecture",
            "d1": "Resilient Laravel 11 APIs,",
            "d2": "React / Vue UIs & clean MVC",
            "tag1": "Laravel 11 · PHP 8.3",
            "tag2": "React · Vue · Next.js 16",
            "icon": (
                '<polyline points="14,13 9,18 14,23" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
                '<polyline points="22,13 27,18 22,23" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
                '<line x1="19.5" y1="11.5" x2="16.5" y2="24.5" stroke="{c}" stroke-width="1.9" stroke-linecap="round"/>'
            ),
        },
        {
            "x": 256,
            "acc": t["amber"],
            "bg": t["amber_bg"],
            "brd": t["amber_border"],
            "badge": "3.5x MULTIPLIER",
            "title": "AI-Augmented Velocity",
            "d1": "Agentic multi-file refactors,",
            "d2": "prompt systems & QA automation",
            "tag1": "Antigravity · Copilot",
            "tag2": "Claude 3.7 · GPT-4",
            "icon": (
                '<polygon points="19.5,8.5 11.5,19 17.5,19 16.5,27.5 24.5,17 18.5,17" fill="none" stroke="{c}" stroke-width="1.8" stroke-linejoin="round"/>'
            ),
        },
        {
            "x": 508,
            "acc": t["emerald"],
            "bg": t["emerald_bg"],
            "brd": t["emerald_border"],
            "badge": "+30% THROUGHPUT",
            "title": "Performance & Caching",
            "d1": "Redis clusters, SQL profiling",
            "d2": "& indexing for high-traffic apps",
            "tag1": "Redis · MySQL · Postgres",
            "tag2": "AWS RDS · DynamoDB",
            "icon": (
                '<ellipse cx="18" cy="12.5" rx="8" ry="3.2" fill="none" stroke="{c}" stroke-width="1.8"/>'
                '<path d="M10 12.5 V18 C10 19.8 13.6 21.2 18 21.2 C22.4 21.2 26 19.8 26 18 V12.5" fill="none" stroke="{c}" stroke-width="1.8"/>'
                '<path d="M10 18 V23.5 C10 25.3 13.6 26.7 18 26.7 C22.4 26.7 26 25.3 26 23.5 V18" fill="none" stroke="{c}" stroke-width="1.8"/>'
            ),
        },
        {
            "x": 760,
            "acc": t["cyan"],
            "bg": t["cyan_bg"],
            "brd": t["cyan_border"],
            "badge": "DATA + MBA ROI",
            "title": "Data & Tech-Finance",
            "d1": "Python ML/analytics pipelines",
            "d2": "aligned with finance & IT ROI",
            "tag1": "Python · Pandas · OpenCV",
            "tag2": "Scikit-learn · MBA Finance",
            "icon": (
                '<rect x="9" y="19" width="4" height="8" rx="1.2" fill="{c}"/>'
                '<rect x="16" y="14" width="4" height="13" rx="1.2" fill="{c}"/>'
                '<rect x="23" y="9" width="4" height="18" rx="1.2" fill="{c}"/>'
            ),
        },
    ]

    cards = []
    for p in pillars:
        acc = p["acc"]
        cards.append(f"""
  <g transform="translate({p['x']}, 38)">
    <rect x="0" y="0" width="236" height="192" rx="16" fill="{t['card']}" stroke="{t['border']}" stroke-width="1.2"/>
    <rect x="18" y="0" width="54" height="3" rx="1.5" fill="{acc}"/>
    <g transform="translate(18, 18)">
      <rect x="0" y="0" width="36" height="36" rx="10" fill="{p['bg']}" stroke="{p['brd']}" stroke-width="1"/>
      {p['icon'].format(c=acc)}
    </g>
    <rect x="114" y="24" width="104" height="22" rx="11" fill="{p['bg']}" stroke="{p['brd']}" stroke-width="0.9"/>
    <text x="166" y="38.4" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.2" font-weight="700" fill="{acc}">{esc(p['badge'])}</text>
    <text x="18" y="82" font-family="{FONT_SANS}" font-size="15.5" font-weight="700" fill="{t['text']}">{esc(p['title'])}</text>
    <text x="18" y="103" font-family="{FONT_SANS}" font-size="12.2" fill="{t['text_sub']}">{esc(p['d1'])}</text>
    <text x="18" y="120" font-family="{FONT_SANS}" font-size="12.2" fill="{t['text_sub']}">{esc(p['d2'])}</text>
    <line x1="18" y1="138" x2="218" y2="138" stroke="{t['rule']}" stroke-width="1"/>
    <text x="18" y="157" font-family="{FONT_MONO}" font-size="10.6" font-weight="600" fill="{acc}">{esc(p['tag1'])}</text>
    <text x="18" y="175" font-family="{FONT_MONO}" font-size="10.6" fill="{t['text_muted']}">{esc(p['tag2'])}</text>
  </g>""")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Core Technical Pillars">
  {render_section_header("CORE TECHNICAL PILLARS", "ENTERPRISE & AI-AUGMENTED ENGINEERING", t, t["purple"], w)}
  {"".join(cards)}
</svg>
"""


def build_tech_stack(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 396

    backend_pills = [
        ("PHP 8.3 & Laravel 11", t["purple_bg"], t["purple_border"], t["purple_soft"], t["purple"]),
        ("REST APIs & Swagger", t["elevated"], t["border"], t["text"], None),
        ("Python", t["purple_bg"], t["purple_border"], t["purple_soft"], t["purple"]),
        ("Django", t["elevated"], t["border"], t["text"], None),
        ("Flask", t["elevated"], t["border"], t["text"], None),
        ("Node.js / Express", t["elevated"], t["border"], t["text"], None),
        ("Pandas", t["cyan_bg"], t["cyan_border"], t["cyan"], None),
        ("NumPy", t["cyan_bg"], t["cyan_border"], t["cyan"], None),
        ("SciPy", t["cyan_bg"], t["cyan_border"], t["cyan"], None),
        ("Scikit-learn", t["cyan_bg"], t["cyan_border"], t["cyan"], None),
        ("Matplotlib", t["cyan_bg"], t["cyan_border"], t["cyan"], None),
        ("Seaborn", t["cyan_bg"], t["cyan_border"], t["cyan"], None),
        ("OpenCV", t["cyan_bg"], t["cyan_border"], t["cyan"], None),
    ]

    ai_pills = [
        ("Google Antigravity IDE", t["amber_bg"], t["amber_border"], t["amber_gold"], t["amber"]),
        ("GitHub Copilot", t["amber_bg"], t["amber_border"], t["amber_gold"], t["amber"]),
        ("Claude 3.7", t["elevated"], t["border"], t["text"], None),
        ("GPT-4", t["elevated"], t["border"], t["text"], None),
        ("Prompt Architecture", t["elevated"], t["border"], t["text"], None),
        ("Autonomous Refactoring", t["elevated"], t["border"], t["text"], None),
        ("Synthetic QA Testing", t["elevated"], t["border"], t["text"], None),
    ]

    frontend_pills = [
        ("React.js", t["cyan_bg"], t["cyan_border"], t["cyan"], t["cyan"]),
        ("Next.js 16", t["cyan_bg"], t["cyan_border"], t["cyan"], t["cyan"]),
        ("Vue.js & Vuex", t["elevated"], t["border"], t["text"], None),
        ("TypeScript", t["elevated"], t["border"], t["text"], None),
        ("JavaScript / AJAX", t["elevated"], t["border"], t["text"], None),
        ("Tailwind CSS & CSS3", t["elevated"], t["border"], t["text"], None),
        ("Blade Templates", t["elevated"], t["border"], t["text"], None),
    ]

    cloud_pills = [
        ("MySQL", t["emerald_bg"], t["emerald_border"], t["emerald"], t["emerald"]),
        ("PostgreSQL", t["emerald_bg"], t["emerald_border"], t["emerald"], t["emerald"]),
        ("Redis Cache Clusters", t["emerald_bg"], t["emerald_border"], t["emerald"], t["emerald"]),
        ("AWS (RDS · DynamoDB)", t["amber_bg"], t["amber_border"], t["amber_gold"], t["amber"]),
        ("Git & GitHub CI/CD", t["elevated"], t["border"], t["text"], None),
        ("JIRA", t["elevated"], t["border"], t["text"], None),
        ("Postman", t["elevated"], t["border"], t["text"], None),
        ("Razorpay / Stripe", t["elevated"], t["border"], t["text"], None),
    ]

    b_svg = render_pills_wrapped(backend_pills, start_x=24, start_y=92, max_x=538, row_gap=34, col_gap=7, height=26, font_size=11.0)
    a_svg = render_pills_wrapped(ai_pills, start_x=592, start_y=92, max_x=968, row_gap=34, col_gap=7, height=26, font_size=11.0)
    f_svg = render_pills_wrapped(frontend_pills, start_x=24, start_y=282, max_x=466, row_gap=34, col_gap=7, height=26, font_size=11.0)
    c_svg = render_pills_wrapped(cloud_pills, start_x=520, start_y=282, max_x=966, row_gap=34, col_gap=7, height=26, font_size=11.0)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Skills and Tech Stack Ecosystem">
  {render_section_header("SKILLS & TECH STACK", "PRODUCTION-READY FULL-STACK + AI ECOSYSTEM", t, t["amber"], w)}

  <!-- Card 1: Backend & Python Data Science -->
  <g>
    <rect x="4" y="38" width="556" height="176" rx="16" fill="{t['card']}" stroke="{t['border']}" stroke-width="1.2"/>
    <rect x="24" y="38" width="60" height="3" rx="1.5" fill="{t['purple']}"/>
    <text x="24" y="68" font-family="{FONT_MONO}" font-size="11.2" font-weight="700" letter-spacing="1.2" fill="{t['purple_soft']}">BACKEND ARCHITECTURE &amp; PYTHON DATA</text>
    <rect x="458" y="52" width="84" height="22" rx="11" fill="{t['elevated']}" stroke="{t['border']}" stroke-width="1"/>
    <text x="500" y="66.2" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.6" font-weight="600" fill="{t['text_sub']}">13 TOOLS</text>
    {b_svg}
  </g>

  <!-- Card 2: AI Agentic Engineering -->
  <g>
    <rect x="574" y="38" width="422" height="176" rx="16" fill="{t['card']}" stroke="{t['amber_border']}" stroke-width="1.2"/>
    <rect x="592" y="38" width="60" height="3" rx="1.5" fill="{t['amber']}"/>
    <text x="592" y="68" font-family="{FONT_MONO}" font-size="11.2" font-weight="700" letter-spacing="1.2" fill="{t['amber_gold']}">AI AGENTIC ENGINEERING</text>
    <rect x="866" y="52" width="112" height="22" rx="11" fill="{t['amber_bg']}" stroke="{t['amber_border']}" stroke-width="1"/>
    <text x="922" y="66.2" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.5" font-weight="700" fill="{t['amber_gold']}">⚡ SUPERCHARGED</text>
    {a_svg}
  </g>

  <!-- Card 3: Frontend & UI Systems -->
  <g>
    <rect x="4" y="230" width="484" height="158" rx="16" fill="{t['card']}" stroke="{t['border']}" stroke-width="1.2"/>
    <rect x="24" y="230" width="60" height="3" rx="1.5" fill="{t['cyan']}"/>
    <text x="24" y="260" font-family="{FONT_MONO}" font-size="11.2" font-weight="700" letter-spacing="1.2" fill="{t['cyan']}">FRONTEND &amp; UI SYSTEMS</text>
    <rect x="392" y="244" width="76" height="22" rx="11" fill="{t['elevated']}" stroke="{t['border']}" stroke-width="1"/>
    <text x="430" y="258.2" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.6" font-weight="600" fill="{t['text_sub']}">SPA / SSR</text>
    {f_svg}
  </g>

  <!-- Card 4: Databases, Cloud & DevOps -->
  <g>
    <rect x="502" y="230" width="494" height="158" rx="16" fill="{t['card']}" stroke="{t['border']}" stroke-width="1.2"/>
    <rect x="520" y="230" width="60" height="3" rx="1.5" fill="{t['emerald']}"/>
    <text x="520" y="260" font-family="{FONT_MONO}" font-size="11.2" font-weight="700" letter-spacing="1.2" fill="{t['emerald']}">DATABASES, CLOUD &amp; DEVOPS</text>
    <rect x="886" y="244" width="92" height="22" rx="11" fill="{t['elevated']}" stroke="{t['border']}" stroke-width="1"/>
    <text x="932" y="258.2" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.6" font-weight="600" fill="{t['text_sub']}">SCALE &amp; SEC</text>
    {c_svg}
  </g>
</svg>
"""


def build_projects_header(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 46
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Featured Production Case Studies">
  {render_section_header("FEATURED CASE STUDIES & SYSTEMS", "CLICK ANY CARD TO OPEN LIVE PLATFORM", t, t["emerald"], w)}
</svg>
"""


def build_project_card(
    theme_name: str,
    title: str,
    category: str,
    badge: str,
    period: str,
    desc1: str,
    desc2: str,
    tags: list[str],
    accent_key: str,
) -> str:
    t = THEMES[theme_name]
    w, h = 486, 152
    acc = t[accent_key]
    bg = t[f"{accent_key}_bg"]
    brd = t[f"{accent_key}_border"]

    tag_pills = []
    tx = 20
    for tg in tags:
        svg_p, tw = render_pill(tx, 114, tg, t["elevated"], t["border"], t["text_sub"], height=23, font_size=10.3, mono=True)
        tag_pills.append(svg_p)
        tx += tw + 6

    badge_w = measure_pill(badge, char_w=6.8, pad_x=24, min_w=92)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" rx="16" fill="{t['card']}" stroke="{t['border']}" stroke-width="1.2"/>
  <rect x="20" y="2" width="56" height="3" rx="1.5" fill="{acc}"/>

  <rect x="20" y="16" width="{badge_w}" height="22" rx="11" fill="{bg}" stroke="{brd}" stroke-width="0.9"/>
  <text x="{20 + badge_w / 2:.1f}" y="30.2" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.6" font-weight="700" fill="{acc}">{esc(badge)}</text>
  <text x="{20 + badge_w + 10}" y="30.2" font-family="{FONT_MONO}" font-size="10" fill="{t['text_muted']}">{esc(period)} · {esc(category)}</text>
  <text x="{w - 20}" y="31" text-anchor="end" font-family="{FONT_SANS}" font-size="14" font-weight="700" fill="{acc}">↗</text>

  <text x="20" y="61" font-family="{FONT_SANS}" font-size="16" font-weight="700" fill="{t['text']}">{esc(title)}</text>
  <text x="20" y="82" font-family="{FONT_SANS}" font-size="12" fill="{t['text_sub']}">{esc(desc1)}</text>
  <text x="20" y="99" font-family="{FONT_SANS}" font-size="12" fill="{t['text_sub']}">{esc(desc2)}</text>

  {"".join(tag_pills)}
</svg>
"""


def build_journey(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 396

    exp_items = [
        (
            "2023 – PRESENT",
            "Laravel Developer",
            "Abym Technology Pvt. Ltd · Noida",
            "+30% performance via SQL optimization & Redis caching · Swagger REST APIs",
            "Modular full-stack web applications with Laravel, React.js & Vue.js",
            t["emerald"],
            True,
        ),
        (
            "2022 – 2023",
            "Laravel Developer",
            "Finesoft Technologies Pvt. Ltd · Noida",
            "Full-stack Blade & Vue.js delivery · 3rd-party payment gateways & SMS",
            "High-concurrency relational database schemas with optimized queries",
            t["purple"],
            False,
        ),
        (
            "2021 – 2022",
            "Python Developer",
            "Magical Umbrella Pvt. Ltd",
            "Automated routine data pipelines in Python — saved 10+ manual hrs/week",
            "Built secure RESTful backend APIs & relational database architectures",
            t["cyan"],
            False,
        ),
    ]

    exp_svgs = []
    ey = 82
    for period, role, company, b1, b2, color, live in exp_items:
        pulse_cls = ' class="live-dot"' if live else ""
        exp_svgs.append(f"""
    <circle cx="34" cy="{ey + 12}" r="6.5" fill="{t['card']}" stroke="{color}" stroke-width="2.2"/>
    <circle cx="34" cy="{ey + 12}" r="2.7" fill="{color}"{pulse_cls}/>
    <text x="54" y="{ey + 8}" font-family="{FONT_MONO}" font-size="10.2" font-weight="700" fill="{color}">{esc(period)}</text>
    <text x="54" y="{ey + 27}" font-family="{FONT_SANS}" font-size="14.5" font-weight="700" fill="{t['text']}">{esc(role)} <tspan font-size="12.2" font-weight="600" fill="{t['text_sub']}">— {esc(company)}</tspan></text>
    <text x="54" y="{ey + 47}" font-family="{FONT_SANS}" font-size="11.5" fill="{t['text_sub']}">⚡ {esc(b1)}</text>
    <text x="54" y="{ey + 65}" font-family="{FONT_SANS}" font-size="11.5" fill="{t['text_muted']}">▸ {esc(b2)}</text>""")
        ey += 96

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Career Experience and Academic Credentials">
  <defs>
    <linearGradient id="spineGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{t['emerald']}"/>
      <stop offset="50%" stop-color="{t['purple']}"/>
      <stop offset="100%" stop-color="{t['cyan']}"/>
    </linearGradient>
    <style>
      @keyframes pulseNode {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}
      .live-dot {{ animation: pulseNode 2s ease-in-out infinite; }}
    </style>
  </defs>

  {render_section_header("CAREER JOURNEY & CREDENTIALS", "5+ YEARS PRODUCTION · MBA + B.E. CSE", t, t["cyan"], w)}

  <!-- Left Panel: Work Experience -->
  <g>
    <rect x="4" y="38" width="564" height="350" rx="16" fill="{t['card']}" stroke="{t['border']}" stroke-width="1.2"/>
    <rect x="24" y="38" width="60" height="3" rx="1.5" fill="{t['purple']}"/>
    <text x="24" y="66" font-family="{FONT_MONO}" font-size="11.2" font-weight="700" letter-spacing="1.2" fill="{t['purple_soft']}">PROFESSIONAL EXPERIENCE</text>
    <line x1="34" y1="98" x2="34" y2="290" stroke="url(#spineGrad)" stroke-width="2" stroke-dasharray="4 4"/>
    {"".join(exp_svgs)}
  </g>

  <!-- Right Top Panel: Academic Qualifications -->
  <g>
    <rect x="584" y="38" width="412" height="236" rx="16" fill="{t['card']}" stroke="{t['border']}" stroke-width="1.2"/>
    <rect x="604" y="38" width="60" height="3" rx="1.5" fill="{t['emerald']}"/>
    <text x="604" y="66" font-family="{FONT_MONO}" font-size="11.2" font-weight="700" letter-spacing="1.2" fill="{t['emerald']}">ACADEMIC QUALIFICATIONS</text>

    <!-- MBA Card -->
    <rect x="604" y="82" width="372" height="78" rx="12" fill="{t['elevated']}" stroke="{t['border']}" stroke-width="1"/>
    <circle cx="622" cy="100" r="3.5" fill="{t['emerald']}" class="live-dot"/>
    <text x="632" y="103.5" font-family="{FONT_MONO}" font-size="9.8" font-weight="700" fill="{t['emerald']}">PURSUING · 2024 – PRESENT</text>
    <text x="618" y="125" font-family="{FONT_SANS}" font-size="14" font-weight="700" fill="{t['text']}">MBA in Finance &amp; IT</text>
    <text x="618" y="145" font-family="{FONT_SANS}" font-size="11.8" fill="{t['text_sub']}">Gondwana University · Strategy, Finance &amp; IT</text>

    <!-- BE Card -->
    <rect x="604" y="172" width="372" height="86" rx="12" fill="{t['elevated']}" stroke="{t['border']}" stroke-width="1"/>
    <text x="618" y="191" font-family="{FONT_MONO}" font-size="9.8" font-weight="700" fill="{t['cyan']}">COMPLETED OCT 2020 · 74.60% DISTINCTION</text>
    <text x="618" y="213" font-family="{FONT_SANS}" font-size="14" font-weight="700" fill="{t['text']}">B.E. in Computer Science</text>
    <text x="618" y="232" font-family="{FONT_SANS}" font-size="11.8" fill="{t['text_sub']}">Gondwana University</text>
    <text x="618" y="248" font-family="{FONT_MONO}" font-size="10" fill="{t['text_muted']}">Data Analysis · ML · Deep Learning · Web Dev</text>
  </g>

  <!-- Right Bottom Panel: Profile Snapshot & Motto -->
  <g>
    <rect x="584" y="288" width="412" height="100" rx="16" fill="{t['card']}" stroke="{t['border']}" stroke-width="1.2"/>
    <rect x="604" y="288" width="60" height="3" rx="1.5" fill="{t['amber']}"/>
    <text x="604" y="316" font-family="{FONT_MONO}" font-size="10.5" font-weight="700" letter-spacing="1.2" fill="{t['amber_gold']}">PROFILE SNAPSHOT</text>
    <text x="604" y="340" font-family="{FONT_SANS}" font-size="11.6" fill="{t['text_sub']}">📍 Chandrapur, Maharashtra · 🌐 English, Hindi, Marathi</text>
    <text x="604" y="366" font-family="{FONT_MONO}" font-size="11.2" font-weight="600" fill="{t['purple_soft']}">✦ &quot;Patience is the solution to everything&quot;</text>
  </g>
</svg>
"""


def build_connect_header(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 92
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Initiate Contact and Connect">
  <defs>
    <linearGradient id="connectGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['purple']}"/>
      <stop offset="50%" stop-color="{t['amber']}"/>
      <stop offset="100%" stop-color="{t['emerald']}"/>
    </linearGradient>
  </defs>
  {render_section_header("INITIATE CONTACT & CONNECT", "OPEN FOR ROLES, ARCHITECTURE & ADVISORY", t, t["amber"], w)}
  <rect x="4" y="36" width="992" height="50" rx="14" fill="{t['card']}" stroke="{t['border']}" stroke-width="1.2"/>
  <rect x="4" y="36" width="5" height="50" rx="2.5" fill="url(#connectGrad)"/>
  <text x="26" y="65" font-family="{FONT_SANS}" font-size="14.2" font-weight="700" fill="{t['text']}">Explore my live Next.js portfolio, download my resume, or connect directly across channels below.</text>
</svg>
"""


def build_contact_card(
    theme_name: str,
    title: str,
    subtitle: str,
    accent_key: str,
    icon_svg: str,
    featured: bool = False,
) -> str:
    t = THEMES[theme_name]
    w, h = 316, 82
    acc = t[accent_key]
    bg = t[f"{accent_key}_bg"]
    brd = t[f"{accent_key}_border"]
    stroke_col = brd if featured else t["border"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}: {esc(subtitle)}">
  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" rx="14" fill="{t['card']}" stroke="{stroke_col}" stroke-width="1.2"/>
  <rect x="16" y="2" width="46" height="3" rx="1.5" fill="{acc}"/>
  <g transform="translate(16, 20)">
    <rect x="0" y="0" width="40" height="40" rx="10" fill="{bg}" stroke="{brd}" stroke-width="1"/>
    {icon_svg.format(c=acc)}
  </g>
  <text x="68" y="38" font-family="{FONT_SANS}" font-size="14.5" font-weight="700" fill="{t['text']}">{esc(title)}</text>
  <text x="{w - 18}" y="38" text-anchor="end" font-family="{FONT_SANS}" font-size="14" font-weight="700" fill="{acc}">↗</text>
  <text x="68" y="57" font-family="{FONT_MONO}" font-size="{9.8 if len(subtitle) > 28 else 10.8}" fill="{t['text_sub']}">{esc(subtitle)}</text>
</svg>
"""


def build_footer(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 68
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Shubham Bramhane Footer">
  <defs>
    <clipPath id="footClip">
      <rect x="4" y="4" width="992" height="60" rx="16"/>
    </clipPath>
    <linearGradient id="footWave" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['purple']}" stop-opacity="0.18"/>
      <stop offset="50%" stop-color="{t['amber']}" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="{t['emerald']}" stop-opacity="0.18"/>
    </linearGradient>
    <linearGradient id="footLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['purple']}"/>
      <stop offset="50%" stop-color="{t['amber']}"/>
      <stop offset="100%" stop-color="{t['emerald']}"/>
    </linearGradient>
  </defs>
  <g clip-path="url(#footClip)">
    <rect x="4" y="4" width="992" height="60" fill="{t['card']}"/>
    <path d="M0 44 Q250 18 500 38 T1000 30 L1000 68 L0 68 Z" fill="url(#footWave)"/>
    <rect x="4" y="61" width="992" height="3" fill="url(#footLine)"/>
  </g>
  <rect x="4" y="4" width="992" height="60" rx="16" fill="none" stroke="{t['border']}" stroke-width="1.2"/>
  <text x="500" y="39" text-anchor="middle" font-family="{FONT_MONO}" font-size="11.2" font-weight="600" letter-spacing="0.9" fill="{t['text_sub']}">&lt;SB/&gt;  SHUBHAM BRAMHANE  ·  LARAVEL · FULL-STACK ARCHITECTURE · AI-AUGMENTED VELOCITY</text>
</svg>
"""


PROJECT_CARDS = [
    (
        "oncquest",
        "Oncquest Healthcare & Admin",
        "Healthcare",
        "+30% VELOCITY",
        "2023–Present",
        "Pan-India diagnostic booking platform & centralized admin",
        "control center with Redis caching & optimized SQL pipelines.",
        ["Laravel", "React.js", "Vue.js", "Redis", "MySQL"],
        "emerald",
    ),
    (
        "fieldassist",
        "OncqFieldAssist Logistics",
        "Healthcare Ops",
        "LIVE LOGISTICS",
        "2023–2024",
        "Real-time field operations app for phlebotomists managing",
        "home sample collections, verification & live order dispatch.",
        ["Laravel", "PHP", "MySQL", "Field Ops"],
        "cyan",
    ),
    (
        "lalpath",
        "Lal Path Labs & SEO Engine",
        "Healthcare",
        "SEO & GROWTH",
        "2023–2024",
        "Continuous feature engineering & custom dynamic SEO engine",
        "for a premier pan-India healthcare diagnostics chain.",
        ["Laravel", "PHP", "SEO Engine", "MySQL"],
        "purple",
    ),
    (
        "bigbasket",
        "TMS (Big Basket) Training System",
        "Enterprise",
        "ENTERPRISE TMS",
        "2023–2024",
        "Centralized enterprise training platform handling trainer",
        "allocations, participant tracking, certs & eval analytics.",
        ["Laravel", "PHP", "MySQL", "REST API"],
        "amber",
    ),
    (
        "umbrella",
        "Magical Umbrella Automation",
        "Enterprise",
        "10+ HRS/WK SAVED",
        "2021–2022",
        "Automated Python data processing pipelines & REST workflows",
        "eliminating repetitive manual reporting & speeding delivery.",
        ["Python", "Automation", "REST APIs", "MySQL"],
        "cyan",
    ),
    (
        "portfolio",
        "Next-Gen Portfolio & Hotel POS",
        "Full-Stack",
        "LIVE SHOWCASE",
        "2024–Present",
        "Interactive Next.js 16 + TypeScript portfolio hub alongside",
        "offline-first Laravel LAN POS & open-source repositories.",
        ["Next.js 16", "React", "TypeScript", "Laravel POS"],
        "purple",
    ),
]

CONTACT_CARDS = [
    (
        "portfolio",
        "Live Portfolio",
        "my-portfolio-beta-bay-93.vercel.app",
        "purple",
        '<circle cx="20" cy="20" r="8.5" fill="none" stroke="{c}" stroke-width="1.8"/>'
        '<ellipse cx="20" cy="20" rx="3.8" ry="8.5" fill="none" stroke="{c}" stroke-width="1.5"/>'
        '<line x1="11.5" y1="20" x2="28.5" y2="20" stroke="{c}" stroke-width="1.5"/>',
        True,
    ),
    (
        "resume",
        "Download Resume",
        "Shubham_Bramhane_Resume.pdf",
        "amber",
        '<path d="M14 11 H22 L27 16 V29 H14 Z" fill="none" stroke="{c}" stroke-width="1.8" stroke-linejoin="round"/>'
        '<polyline points="22,11 22,16 27,16" fill="none" stroke="{c}" stroke-width="1.6"/>'
        '<line x1="17" y1="20.5" x2="24" y2="20.5" stroke="{c}" stroke-width="1.5" stroke-linecap="round"/>'
        '<line x1="17" y1="24.5" x2="22" y2="24.5" stroke="{c}" stroke-width="1.5" stroke-linecap="round"/>',
        True,
    ),
    (
        "linkedin",
        "LinkedIn",
        "linkedin.com/in/shubham1602",
        "cyan",
        '<rect x="13" y="17.5" width="3" height="9.5" rx="0.8" fill="{c}"/>'
        '<circle cx="14.5" cy="14" r="1.7" fill="{c}"/>'
        '<path d="M19 17.5 H21.8 V19.1 C22.5 17.9 23.7 17.2 25.1 17.2 C27.2 17.2 28 18.7 28 21.1 V27 H25 V21.6 C25 20.3 24.4 19.7 23.4 19.7 C22.4 19.7 21.9 20.4 21.9 21.6 V27 H19 Z" fill="{c}"/>',
        False,
    ),
    (
        "email",
        "Email",
        "shubham.bramhane75@gmail.com",
        "emerald",
        '<rect x="12" y="14" width="16" height="12" rx="2.2" fill="none" stroke="{c}" stroke-width="1.8"/>'
        '<polyline points="12.5,15.2 20,21 27.5,15.2" fill="none" stroke="{c}" stroke-width="1.8" stroke-linejoin="round"/>',
        False,
    ),
    (
        "twitter",
        "X / Twitter",
        "@shubhbramhane16",
        "purple",
        '<path d="M13 13 L18.7 20.6 L12.8 27 H15.2 L19.8 22 L23.6 27 H27.2 L21.2 19 L26.7 13 H24.3 L20.1 17.6 L16.6 13 Z" fill="{c}"/>',
        False,
    ),
    (
        "phone",
        "Phone",
        "+91-8857916707",
        "rose",
        '<path d="M14.5 13 C13.7 13 13 13.7 13 14.6 C13 21.1 18.1 26.2 24.6 26.2 C25.5 26.2 26.2 25.5 26.2 24.7 V22.5 C26.2 21.9 25.8 21.4 25.1 21.3 L22.7 20.8 C22.2 20.7 21.7 20.9 21.4 21.3 L20.4 22.4 C18.6 21.5 17.7 20.6 16.8 18.8 L17.9 17.8 C18.3 17.5 18.5 17 18.4 16.5 L17.9 14.1 C17.8 13.5 17.3 13 16.7 13 Z" fill="none" stroke="{c}" stroke-width="1.7" stroke-linejoin="round"/>',
        False,
    ),
]


def write_and_validate(path: Path, svg_text: str) -> None:
    ET.fromstring(svg_text.encode("utf-8"))
    path.write_text(svg_text.strip() + "\n", encoding="utf-8")


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    # Clean stale SVGs from earlier iterations so assets/ stays spotless
    for old in ASSETS_DIR.glob("*.svg"):
        old.unlink()

    generated = []
    for theme in ("dark", "light"):
        outputs = {
            f"hero-{theme}.svg": build_hero(theme),
            f"metrics-{theme}.svg": build_metrics(theme),
            f"pillars-{theme}.svg": build_pillars(theme),
            f"tech-stack-{theme}.svg": build_tech_stack(theme),
            f"projects-header-{theme}.svg": build_projects_header(theme),
            f"journey-{theme}.svg": build_journey(theme),
            f"connect-header-{theme}.svg": build_connect_header(theme),
            f"footer-{theme}.svg": build_footer(theme),
        }
        for key, title, cat, badge, period, d1, d2, tags, acc in PROJECT_CARDS:
            outputs[f"proj-{key}-{theme}.svg"] = build_project_card(
                theme, title, cat, badge, period, d1, d2, tags, acc
            )
        for key, title, sub, acc, icon_svg, feat in CONTACT_CARDS:
            outputs[f"card-{key}-{theme}.svg"] = build_contact_card(
                theme, title, sub, acc, icon_svg, featured=feat
            )

        for filename, content in outputs.items():
            out_path = ASSETS_DIR / filename
            write_and_validate(out_path, content)
            generated.append(out_path.name)

    print(f"Generated and validated {len(generated)} SVG assets in {ASSETS_DIR}")


if __name__ == "__main__":
    main()
