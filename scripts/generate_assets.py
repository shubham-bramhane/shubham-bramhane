#!/usr/bin/env python3
"""
Deterministic SVG visual asset generator (v2.0 — Cinematic Data-Driven Bento Edition)
for Shubham Bramhane's GitHub Profile README.
Aligned with https://my-portfolio-beta-bay-93.vercel.app/
Generates matched Dark & Light interactive-style SVG visuals into ./assets/.
Zero third-party dependencies — Python standard library only.
"""

from __future__ import annotations

import html
import math
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "assets"

FONT_SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
FONT_MONO = "'Cascadia Code', 'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

THEMES = {
    "dark": {
        "canvas": "#0D1117",
        "card": "#0E1019",
        "card_alt": "#141726",
        "card_deep": "#090B12",
        "elevated": "#191D30",
        "code_bg": "#080A12",
        "code_bar": "#111424",
        "border": "#232842",
        "border_strong": "#333A5E",
        "dot_grid": "#2A3152",
        "dot_opacity": "0.52",
        "grid_line": "#1A2036",
        "text": "#F8FAFC",
        "text_sub": "#A6AFC9",
        "text_muted": "#6E7796",
        "rule": "#1F253D",
        "purple": "#A855F7",
        "purple_soft": "#C084FC",
        "purple_bg": "#211438",
        "purple_border": "#4C2B80",
        "amber": "#FB923C",
        "amber_gold": "#FBBF24",
        "amber_bg": "#2E1C0E",
        "amber_border": "#6B3E17",
        "emerald": "#34D399",
        "emerald_bg": "#0B2B22",
        "emerald_border": "#165C48",
        "cyan": "#38BDF8",
        "cyan_bg": "#0D273D",
        "cyan_border": "#1A5175",
        "rose": "#FB7185",
        "rose_bg": "#331422",
        "rose_border": "#6E2442",
        "glow_opacity": "0.26",
        "code_kw": "#C084FC",
        "code_cls": "#38BDF8",
        "code_str": "#34D399",
        "code_prop": "#E2E8F0",
        "code_num": "#546080",
        "code_punct": "#7684A8",
        "code_comment": "#64748B",
        "grad_text_1": "#FFFFFF",
        "grad_text_2": "#C084FC",
        "grad_text_3": "#FB923C",
        "radar_ring": "#262D4A",
    },
    "light": {
        "canvas": "#FFFFFF",
        "card": "#FFFFFF",
        "card_alt": "#F8FAFC",
        "card_deep": "#F1F5F9",
        "elevated": "#F1F5F9",
        "code_bg": "#0D101B",
        "code_bar": "#171B2E",
        "border": "#E2E8F0",
        "border_strong": "#CBD5E1",
        "dot_grid": "#CBD5E1",
        "dot_opacity": "0.6",
        "grid_line": "#E2E8F0",
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
        "glow_opacity": "0.14",
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
        "radar_ring": "#CBD5E1",
    },
}


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def measure_pill(label: str, char_w: float = 6.7, pad_x: int = 20, min_w: int = 50) -> int:
    return max(min_w, int(round(len(label) * char_w + pad_x)))


def render_pill(
    x: int,
    y: int,
    label: str,
    bg: str,
    border: str,
    fg: str,
    dot_color: str | None = None,
    height: int = 25,
    font_size: float = 10.8,
    weight: int = 600,
    mono: bool = False,
    width: int | None = None,
) -> tuple[str, int]:
    char_w = 6.9 if mono else 6.45
    pad = 28 if dot_color else 19
    w = width if width is not None else measure_pill(label, char_w=char_w, pad_x=pad)
    rx = height // 2
    family = FONT_MONO if mono else FONT_SANS
    text_y = y + (height / 2) + (font_size * 0.35)
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{height}" rx="{rx}" '
        f'fill="{bg}" stroke="{border}" stroke-width="1"/>'
    ]
    if dot_color:
        parts.append(f'<circle cx="{x + 11.5}" cy="{y + height / 2:.1f}" r="3" fill="{dot_color}"/>')
        parts.append(
            f'<text x="{x + 20}" y="{text_y:.1f}" font-family="{family}" font-size="{font_size}" '
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
    row_gap: int = 31,
    col_gap: int = 7,
    height: int = 25,
    font_size: float = 10.8,
    mono: bool = False,
) -> str:
    out = []
    cx = start_x
    cy = start_y
    for label, bg, brd, fg, dot in items:
        char_w = 6.9 if mono else 6.45
        pad = 28 if dot else 19
        pw = measure_pill(label, char_w=char_w, pad_x=pad)
        if cx + pw > max_x and cx > start_x:
            cx = start_x
            cy += row_gap
        svg_p, actual_w = render_pill(
            cx, cy, label, bg, brd, fg, dot_color=dot, height=height, font_size=font_size, mono=mono, width=pw
        )
        out.append(svg_p)
        cx += actual_w + col_gap
    return "\n".join(out)


def render_section_header(title: str, subtitle: str, t: dict[str, str], accent: str, width: int = 1000) -> str:
    label_w = int(len(title) * 8.1 + 26)
    rule_x = 18 + label_w
    right_end = width - 6
    sub_svg = ""
    if subtitle:
        sub_svg = f'<text x="{right_end}" y="18.5" text-anchor="end" font-family="{FONT_MONO}" font-size="10.2" fill="{t["text_muted"]}">{esc(subtitle)}</text>'
        rule_end = right_end - int(len(subtitle) * 6.4 + 14)
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
    w, h = 1000, 396

    hero_pills = [
        ("✦ PHP 8.3 / Laravel 11", t["elevated"], t["border_strong"], t["text"], None),
        ("✦ Redis (+30% Velocity)", t["elevated"], t["border_strong"], t["text"], None),
        ("✦ React.js & Next.js 16", t["elevated"], t["border_strong"], t["text"], None),
        ("✦ MySQL / PostgreSQL", t["elevated"], t["border_strong"], t["text"], None),
        ("✦ Python & AWS", t["elevated"], t["border_strong"], t["text"], None),
        ("✦ Google Antigravity & Copilot", t["purple_bg"], t["purple_border"], t["purple_soft"], None),
    ]
    pills_svg = render_pills_wrapped(hero_pills, start_x=36, start_y=298, max_x=562, row_gap=33, col_gap=8, height=26, font_size=10.8)

    code_lines = [
        ("01", f'<tspan fill="{t["code_comment"]}">// shubham-bramhane.ts — Enterprise Core</tspan>'),
        ("02", f'<tspan fill="{t["code_kw"]}">export const</tspan> <tspan fill="{t["code_cls"]}" font-weight="700">architect</tspan> <tspan fill="{t["code_punct"]}">= &#123;</tspan>'),
        ("03", f'  <tspan fill="{t["code_prop"]}">name</tspan><tspan fill="{t["code_punct"]}">:</tspan> <tspan fill="{t["code_str"]}">"Shubham Bramhane"</tspan><tspan fill="{t["code_punct"]}">,</tspan>'),
        ("04", f'  <tspan fill="{t["code_prop"]}">role</tspan><tspan fill="{t["code_punct"]}">:</tspan> <tspan fill="{t["code_str"]}">"Full-Stack Architect &amp; AI Eng"</tspan><tspan fill="{t["code_punct"]}">,</tspan>'),
        ("05", f'  <tspan fill="{t["code_prop"]}">backend</tspan><tspan fill="{t["code_punct"]}">: [</tspan><tspan fill="{t["code_str"]}">"Laravel 11"</tspan><tspan fill="{t["code_punct"]}">,</tspan> <tspan fill="{t["code_str"]}">"Redis"</tspan><tspan fill="{t["code_punct"]}">,</tspan> <tspan fill="{t["code_str"]}">"Python"</tspan><tspan fill="{t["code_punct"]}">],</tspan>'),
        ("06", f'  <tspan fill="{t["code_prop"]}">frontend</tspan><tspan fill="{t["code_punct"]}">: [</tspan><tspan fill="{t["code_str"]}">"React"</tspan><tspan fill="{t["code_punct"]}">,</tspan> <tspan fill="{t["code_str"]}">"Vue"</tspan><tspan fill="{t["code_punct"]}">,</tspan> <tspan fill="{t["code_str"]}">"Next.js 16"</tspan><tspan fill="{t["code_punct"]}">],</tspan>'),
        ("07", f'  <tspan fill="{t["code_prop"]}">cloudDB</tspan><tspan fill="{t["code_punct"]}">: [</tspan><tspan fill="{t["code_str"]}">"MySQL"</tspan><tspan fill="{t["code_punct"]}">,</tspan> <tspan fill="{t["code_str"]}">"Postgres"</tspan><tspan fill="{t["code_punct"]}">,</tspan> <tspan fill="{t["code_str"]}">"AWS"</tspan><tspan fill="{t["code_punct"]}">],</tspan>'),
        ("08", f'  <tspan fill="{t["code_prop"]}">aiFlow</tspan><tspan fill="{t["code_punct"]}">: [</tspan><tspan fill="{t["code_str"]}">"Antigravity"</tspan><tspan fill="{t["code_punct"]}">,</tspan> <tspan fill="{t["code_str"]}">"Copilot"</tspan><tspan fill="{t["code_punct"]}">],</tspan>'),
        ("09", f'  <tspan fill="{t["code_prop"]}">velocity</tspan><tspan fill="{t["code_punct"]}">:</tspan> <tspan fill="{t["code_str"]}">"3.5x AI · +30% Query"</tspan>'),
        ("10", f'<tspan fill="{t["code_punct"]}">&#125;;</tspan>'),
    ]

    code_svg = []
    cy = 96
    for idx, (num, markup) in enumerate(code_lines):
        if idx == 8:
            code_svg.append(f'    <rect x="590" y="{cy - 13}" width="376" height="18" fill="#A855F7" fill-opacity="0.11"/>')
        code_svg.append(f'    <text x="602" y="{cy}" font-family="{FONT_MONO}" font-size="10.4" fill="{t["code_num"]}">{num}</text>')
        code_svg.append(f'    <text x="623" y="{cy}" font-family="{FONT_MONO}" font-size="10.4">{markup}</text>')
        cy += 18.2

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Shubham Bramhane - Senior Full-Stack Architect and AI-Augmented Engineer">
  <defs>
    <clipPath id="heroClip">
      <rect x="4" y="4" width="992" height="388" rx="22"/>
    </clipPath>
    <pattern id="dotGrid" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.1" fill="{t['dot_grid']}" fill-opacity="{t['dot_opacity']}"/>
    </pattern>
    <linearGradient id="brandBar" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['purple']}"/>
      <stop offset="45%" stop-color="{t['amber']}"/>
      <stop offset="78%" stop-color="{t['emerald']}"/>
      <stop offset="100%" stop-color="{t['cyan']}"/>
    </linearGradient>
    <linearGradient id="headlineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['grad_text_1']}"/>
      <stop offset="45%" stop-color="{t['grad_text_2']}"/>
      <stop offset="100%" stop-color="{t['grad_text_3']}"/>
    </linearGradient>
    <linearGradient id="sparkArea" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{t['emerald']}" stop-opacity="0.38"/>
      <stop offset="100%" stop-color="{t['emerald']}" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="glowPurple" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{t['purple']}" stop-opacity="{t['glow_opacity']}"/>
      <stop offset="100%" stop-color="{t['purple']}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowAmber" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{t['amber']}" stop-opacity="{t['glow_opacity']}"/>
      <stop offset="100%" stop-color="{t['amber']}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowCyan" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{t['cyan']}" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="{t['cyan']}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="heroBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{t['card']}"/>
      <stop offset="100%" stop-color="{t['card_alt']}"/>
    </linearGradient>
    <style>
      @keyframes pulseDot {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.25; }} }}
      @keyframes blinkCursor {{ 0%, 49% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}
      @keyframes breathe {{ 0%, 100% {{ opacity: 0.95; }} 50% {{ opacity: 0.5; }} }}
      @keyframes flowTrace {{ from {{ stroke-dashoffset: 240; }} to {{ stroke-dashoffset: 0; }} }}
      @keyframes scanBeam {{ 0% {{ transform: translateX(-260px); opacity: 0; }} 20% {{ opacity: 0.9; }} 80% {{ opacity: 0.9; }} 100% {{ transform: translateX(1020px); opacity: 0; }} }}
      .pulse-dot {{ animation: pulseDot 2s ease-in-out infinite; }}
      .blink {{ animation: blinkCursor 1.1s steps(1) infinite; }}
      .orb {{ animation: breathe 6s ease-in-out infinite; }}
      .trace-flow {{ stroke-dasharray: 28 18; animation: flowTrace 6s linear infinite; }}
      .scan {{ animation: scanBeam 5.5s ease-in-out infinite; }}
    </style>
  </defs>

  <g clip-path="url(#heroClip)">
    <rect x="4" y="4" width="992" height="388" fill="url(#heroBg)"/>
    <rect x="4" y="4" width="992" height="388" fill="url(#dotGrid)"/>
    <circle cx="130" cy="55" r="250" fill="url(#glowPurple)" class="orb"/>
    <circle cx="885" cy="340" r="260" fill="url(#glowAmber)" class="orb"/>
    <circle cx="520" cy="370" r="190" fill="url(#glowCyan)"/>

    <!-- Subtle Animated Architectural Circuit Traces -->
    <path d="M 4 272 H 120 L 144 296 H 572" fill="none" stroke="{t['purple']}" stroke-width="1" stroke-opacity="0.22"/>
    <path d="M 4 272 H 120 L 144 296 H 572" fill="none" stroke="{t['purple_soft']}" stroke-width="1.3" stroke-opacity="0.45" class="trace-flow"/>
    <path d="M 590 198 H 566 L 548 180 V 4" fill="none" stroke="{t['cyan']}" stroke-width="1" stroke-opacity="0.18"/>

    <!-- Top Brand Ribbon + Gliding Light Beam -->
    <rect x="4" y="4" width="992" height="4" fill="url(#brandBar)"/>
    <rect x="0" y="4" width="220" height="4" fill="#FFFFFF" fill-opacity="0.55" class="scan"/>
  </g>
  <rect x="4" y="4" width="992" height="388" rx="22" fill="none" stroke="{t['border']}" stroke-width="1.2"/>

  <!-- Top Badges Row -->
  <g>
    <rect x="36" y="28" width="66" height="27" rx="9" fill="{t['elevated']}" stroke="{t['border_strong']}" stroke-width="1"/>
    <text x="69" y="45.5" text-anchor="middle" font-family="{FONT_MONO}" font-size="12.2" font-weight="800" fill="{t['text']}">&lt;SB/&gt;</text>

    <rect x="111" y="28" width="268" height="27" rx="13.5" fill="{t['emerald_bg']}" stroke="{t['emerald_border']}" stroke-width="1"/>
    <circle cx="126" cy="41.5" r="3.6" fill="{t['emerald']}" class="pulse-dot"/>
    <text x="137" y="45.4" font-family="{FONT_SANS}" font-size="11.1" font-weight="600" fill="{t['emerald']}">Available for High-Impact Roles &amp; Advisory</text>

    <rect x="388" y="28" width="136" height="27" rx="13.5" fill="{t['amber_bg']}" stroke="{t['amber_border']}" stroke-width="1"/>
    <text x="456" y="45.4" text-anchor="middle" font-family="{FONT_MONO}" font-size="10.8" font-weight="700" fill="{t['amber_gold']}">⚡ 3.5x AI Velocity</text>
  </g>

  <!-- Main Editorial Heading -->
  <g>
    <text x="36" y="106" font-family="{FONT_SANS}" font-size="42" font-weight="800" letter-spacing="-1.0" fill="{t['text']}">Shubham Bramhane</text>
    <text x="36" y="139" font-family="{FONT_SANS}" font-size="22" font-weight="800" letter-spacing="-0.3" fill="url(#headlineGrad)">Architecting High-Throughput Systems</text>
    <text x="36" y="165" font-family="{FONT_SANS}" font-size="22" font-weight="800" letter-spacing="-0.3" fill="url(#headlineGrad)">with AI-Augmented Velocity.</text>

    <text x="36" y="195" font-family="{FONT_SANS}" font-size="12.5" font-weight="700" fill="{t['emerald']}">Senior Full-Stack Architect &amp; AI-Augmented Engineer</text>
    <text x="362" y="195" font-family="{FONT_MONO}" font-size="10.6" font-weight="600" fill="{t['text_muted']}">· 5+ Yrs · MBA Finance &amp; IT</text>

    <text x="36" y="224" font-family="{FONT_SANS}" font-size="12.7" fill="{t['text_sub']}">5+ years mastering PHP 8.3 / Laravel 11, high-concurrency MySQL/PostgreSQL</text>
    <text x="36" y="243" font-family="{FONT_SANS}" font-size="12.7" fill="{t['text_sub']}">&amp; Redis caching (+30% throughput), pan-India healthcare portals, Python</text>
    <text x="36" y="262" font-family="{FONT_SANS}" font-size="12.7" fill="{t['text_sub']}">automation pipelines, and agentic AI workflows (Antigravity &amp; Copilot).</text>
  </g>

  <!-- Stack Highlight Pills -->
  {pills_svg}

  <!-- Right Live IDE + Telemetry Sparkline Window -->
  <g>
    <rect x="590" y="28" width="376" height="338" rx="16" fill="{t['code_bg']}" stroke="{t['border_strong']}" stroke-width="1.2"/>
    <path d="M606 28 H950 A16 16 0 0 1 966 44 V63 H590 V44 A16 16 0 0 1 606 28 Z" fill="{t['code_bar']}"/>
    <line x1="590" y1="63" x2="966" y2="63" stroke="#22273D" stroke-width="1"/>
    <circle cx="609" cy="45.5" r="4.6" fill="#FF5F56"/>
    <circle cx="624" cy="45.5" r="4.6" fill="#FFBD2E"/>
    <circle cx="639" cy="45.5" r="4.6" fill="#27C93F"/>
    <rect x="658" y="35.5" width="108" height="20" rx="6" fill="#1D2238" stroke="#3B446E" stroke-width="0.9"/>
    <text x="712" y="49" text-anchor="middle" font-family="{FONT_MONO}" font-size="10" font-weight="600" fill="#F1F5F9">Architecture.ts</text>
    <text x="778" y="49" font-family="{FONT_MONO}" font-size="9.8" fill="#64748B">Live-Telemetry.log</text>

{chr(10).join(code_svg)}
    <rect x="642" y="250" width="6.5" height="12" rx="1.5" fill="{t['purple_soft']}" class="blink"/>

    <!-- Embedded Live Throughput Telemetry Panel -->
    <line x1="590" y1="274" x2="966" y2="274" stroke="#1E243B" stroke-width="1"/>
    <text x="606" y="292" font-family="{FONT_MONO}" font-size="9.2" font-weight="700" letter-spacing="0.9" fill="#64748B">LIVE TELEMETRY · REDIS + SQL PROFILING</text>
    <text x="950" y="292" text-anchor="end" font-family="{FONT_MONO}" font-size="9.6" font-weight="700" fill="{t['emerald']}">+30% THROUGHPUT</text>

    <!-- Sparkline Area Chart -->
    <path d="M 606 334 C 640 331, 668 326, 702 321 C 742 315, 774 318, 816 308 C 858 299, 898 303, 946 296 L 946 336 L 606 336 Z" fill="url(#sparkArea)"/>
    <path d="M 606 334 C 640 331, 668 326, 702 321 C 742 315, 774 318, 816 308 C 858 299, 898 303, 946 296" fill="none" stroke="{t['emerald']}" stroke-width="2" stroke-linecap="round"/>
    <circle cx="946" cy="296" r="4" fill="{t['emerald']}" class="pulse-dot"/>
    <circle cx="946" cy="296" r="8" fill="{t['emerald']}" fill-opacity="0.22" class="pulse-dot"/>

    <!-- Status Bar -->
    <line x1="590" y1="340" x2="966" y2="340" stroke="#1E243B" stroke-width="1"/>
    <circle cx="607" cy="353" r="3.2" fill="{t['emerald']}" class="pulse-dot"/>
    <text x="617" y="356.5" font-family="{FONT_MONO}" font-size="9.6" fill="#94A3B8">Production Ready · AI-Assisted</text>
    <text x="950" y="356.5" text-anchor="end" font-family="{FONT_MONO}" font-size="9.6" font-weight="700" fill="{t['amber_gold']}">99.9% UPTIME</text>
  </g>
</svg>
"""


def build_cta_button(theme_name: str, key: str, label: str, sub: str, style: str, icon: str) -> str:
    t = THEMES[theme_name]
    w, h = 238, 56
    if style == "primary":
        bg_fill = "url(#ctaPrimary)"
        stroke = "#C084FC"
        fg = "#FFFFFF"
        sub_fg = "#F3E8FF"
        icon_col = "#FFFFFF"
        defs = f"""
  <defs>
    <linearGradient id="ctaPrimary" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#9333EA"/>
      <stop offset="55%" stop-color="#C026D3"/>
      <stop offset="100%" stop-color="#F97316"/>
    </linearGradient>
  </defs>"""
    else:
        acc = t[style]
        bg_fill = t[f"{style}_bg"]
        stroke = t[f"{style}_border"]
        fg = t["text"]
        sub_fg = acc
        icon_col = acc
        defs = ""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">
  {defs}
  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" rx="13" fill="{bg_fill}" stroke="{stroke}" stroke-width="1.2"/>
  <g transform="translate(14, 14)">
    {icon.format(c=icon_col)}
  </g>
  <text x="48" y="26.5" font-family="{FONT_SANS}" font-size="13" font-weight="800" fill="{fg}">{esc(label)}</text>
  <text x="48" y="42.5" font-family="{FONT_MONO}" font-size="9.8" font-weight="600" fill="{sub_fg}">{esc(sub)}</text>
  <text x="{w - 15}" y="33" text-anchor="end" font-family="{FONT_SANS}" font-size="14" font-weight="800" fill="{icon_col}">↗</text>
</svg>
"""


def build_metrics(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 128

    cards_data = [
        (
            "5+ Yrs",
            "Laravel Ecosystem",
            "Enterprise & Microservices",
            t["purple"],
            # Mini ascending bar chart
            f'<rect x="164" y="48" width="9" height="16" rx="2.5" fill="{t["purple"]}" fill-opacity="0.28"/>'
            f'<rect x="177" y="40" width="9" height="24" rx="2.5" fill="{t["purple"]}" fill-opacity="0.45"/>'
            f'<rect x="190" y="31" width="9" height="33" rx="2.5" fill="{t["purple"]}" fill-opacity="0.7"/>'
            f'<rect x="203" y="20" width="9" height="44" rx="2.5" fill="{t["purple"]}"/>',
        ),
        (
            "+30%",
            "Query Velocity",
            "Redis & SQL Profiling",
            t["emerald"],
            # Mini glowing rising sparkline
            f'<path d="M 156 58 C 170 55, 178 46, 188 42 C 198 38, 204 28, 214 22 L 214 62 L 156 62 Z" fill="{t["emerald"]}" fill-opacity="0.16"/>'
            f'<path d="M 156 58 C 170 55, 178 46, 188 42 C 198 38, 204 28, 214 22" fill="none" stroke="{t["emerald"]}" stroke-width="2.2" stroke-linecap="round"/>'
            f'<circle cx="214" cy="22" r="3.5" fill="{t["emerald"]}"/>',
        ),
        (
            "3.5x",
            "AI Sprint Velocity",
            "Antigravity & Copilot",
            t["amber"],
            # Circular velocity gauge ring
            f'<circle cx="192" cy="40" r="20" fill="none" stroke="{t["border_strong"]}" stroke-width="4.5"/>'
            f'<circle cx="192" cy="40" r="20" fill="none" stroke="{t["amber"]}" stroke-width="4.5" stroke-dasharray="102 130" stroke-linecap="round" transform="rotate(-90 192 40)"/>'
            f'<text x="192" y="43.5" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.5" font-weight="800" fill="{t["amber_gold"]}">AI</text>',
        ),
        (
            "10+ hrs",
            "Weekly Automated",
            "Python Data Pipelines",
            t["cyan"],
            # Mini automated node flow graphic
            f'<line x1="164" y1="42" x2="212" y2="42" stroke="{t["cyan"]}" stroke-width="2" stroke-dasharray="4 3"/>'
            f'<circle cx="164" cy="42" r="5" fill="{t["cyan_bg"]}" stroke="{t["cyan"]}" stroke-width="1.8"/>'
            f'<circle cx="188" cy="42" r="5" fill="{t["cyan_bg"]}" stroke="{t["cyan"]}" stroke-width="1.8"/>'
            f'<circle cx="212" cy="42" r="5.5" fill="{t["cyan"]}"/>',
        ),
    ]

    cards = []
    x = 4
    for big, title, sub, acc, viz in cards_data:
        cards.append(f"""
  <g transform="translate({x}, 6)">
    <rect x="0" y="0" width="236" height="116" rx="16" fill="{t['card']}" stroke="{t['border']}" stroke-width="1.2"/>
    <rect x="20" y="0" width="48" height="3" rx="1.5" fill="{acc}"/>
    <text x="20" y="45" font-family="{FONT_SANS}" font-size="30" font-weight="800" letter-spacing="-0.6" fill="{t['text']}">{esc(big)}</text>
    <text x="20" y="74" font-family="{FONT_SANS}" font-size="13" font-weight="700" fill="{acc}">{esc(title)}</text>
    <text x="20" y="95" font-family="{FONT_MONO}" font-size="10.3" fill="{t['text_muted']}">{esc(sub)}</text>
    {viz}
  </g>""")
        x += 252

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Engineering Impact KPI Strip with Data Visuals">
  {"".join(cards)}
</svg>
"""


def build_architecture_flow(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 276

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Animated Enterprise System Architecture Blueprint">
  <defs>
    <pattern id="bpGrid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M 24 0 L 0 0 0 24" fill="none" stroke="{t['grid_line']}" stroke-width="0.7" stroke-opacity="0.65"/>
    </pattern>
    <clipPath id="bpClip">
      <rect x="4" y="36" width="992" height="234" rx="18"/>
    </clipPath>
    <linearGradient id="flow1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['cyan']}"/>
      <stop offset="100%" stop-color="{t['purple']}"/>
    </linearGradient>
    <linearGradient id="flow2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['purple']}"/>
      <stop offset="100%" stop-color="{t['emerald']}"/>
    </linearGradient>
    <linearGradient id="flow3" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['emerald']}"/>
      <stop offset="100%" stop-color="{t['amber']}"/>
    </linearGradient>
    <style>
      @keyframes packetFlow {{ from {{ stroke-dashoffset: 64; }} to {{ stroke-dashoffset: 0; }} }}
      @keyframes softBlink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}
      .flow-line {{ stroke-dasharray: 8 8; animation: packetFlow 1.8s linear infinite; }}
      .live-glow {{ animation: softBlink 2s ease-in-out infinite; }}
    </style>
  </defs>

  {render_section_header("SYSTEM ARCHITECTURE BLUEPRINT", "HOW I ARCHITECT HIGH-THROUGHPUT PRODUCTION PLATFORMS", t, t["cyan"], w)}

  <g clip-path="url(#bpClip)">
    <rect x="4" y="36" width="992" height="234" fill="{t['card']}"/>
    <rect x="4" y="36" width="992" height="234" fill="url(#bpGrid)"/>
  </g>
  <rect x="4" y="36" width="992" height="234" rx="18" fill="none" stroke="{t['border']}" stroke-width="1.2"/>

  <!-- Animated Connector Pipes Between Layers -->
  <g>
    <!-- Pipe 1 -->
    <line x1="226" y1="134" x2="274" y2="134" stroke="url(#flow1)" stroke-width="2.6" class="flow-line"/>
    <polygon points="274,134 266,129 266,139" fill="{t['purple']}"/>
    <!-- Pipe 2 -->
    <line x1="496" y1="134" x2="544" y2="134" stroke="url(#flow2)" stroke-width="2.6" class="flow-line"/>
    <polygon points="544,134 536,129 536,139" fill="{t['emerald']}"/>
    <!-- Pipe 3 -->
    <line x1="752" y1="134" x2="796" y2="134" stroke="url(#flow3)" stroke-width="2.6" class="flow-line"/>
    <polygon points="796,134 788,129 788,139" fill="{t['amber']}"/>
  </g>

  <!-- Node 1: Client & UI Edge -->
  <g transform="translate(24, 58)">
    <rect x="0" y="0" width="202" height="152" rx="14" fill="{t['card_alt']}" stroke="{t['cyan_border']}" stroke-width="1.2"/>
    <rect x="16" y="0" width="44" height="3" rx="1.5" fill="{t['cyan']}"/>
    <text x="16" y="25" font-family="{FONT_MONO}" font-size="9.5" font-weight="700" fill="{t['cyan']}">01 · CLIENT &amp; UI EDGE</text>
    <text x="16" y="48" font-family="{FONT_SANS}" font-size="14.5" font-weight="700" fill="{t['text']}">Reactive Interfaces</text>
    <text x="16" y="72" font-family="{FONT_MONO}" font-size="10.4" fill="{t['text_sub']}">▸ React.js &amp; Next.js 16</text>
    <text x="16" y="92" font-family="{FONT_MONO}" font-size="10.4" fill="{t['text_sub']}">▸ Vue.js / Vuex · Blade</text>
    <text x="16" y="112" font-family="{FONT_MONO}" font-size="10.4" fill="{t['text_sub']}">▸ TypeScript · Tailwind</text>
    <rect x="16" y="124" width="170" height="18" rx="6" fill="{t['cyan_bg']}"/>
    <text x="101" y="136.2" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.2" font-weight="700" fill="{t['cyan']}">SPA · SSR · RESPONSIVE</text>
  </g>

  <!-- Node 2: Core API + AI-Augmented Engine -->
  <g transform="translate(274, 54)">
    <rect x="0" y="0" width="222" height="160" rx="14" fill="{t['card_alt']}" stroke="{t['purple_border']}" stroke-width="1.4"/>
    <rect x="16" y="0" width="60" height="3" rx="1.5" fill="{t['purple']}"/>
    <text x="16" y="25" font-family="{FONT_MONO}" font-size="9.5" font-weight="700" fill="{t['purple_soft']}">02 · APPLICATION &amp; AI CORE</text>
    <text x="16" y="48" font-family="{FONT_SANS}" font-size="14.5" font-weight="700" fill="{t['text']}">Laravel 11 &amp; Python</text>
    <text x="16" y="72" font-family="{FONT_MONO}" font-size="10.4" fill="{t['text_sub']}">▸ PHP 8.3 · REST / Swagger</text>
    <text x="16" y="91" font-family="{FONT_MONO}" font-size="10.4" fill="{t['text_sub']}">▸ Django · Flask · Fast ETL</text>
    <rect x="14" y="106" width="194" height="42" rx="9" fill="{t['amber_bg']}" stroke="{t['amber_border']}" stroke-width="1"/>
    <text x="24" y="123" font-family="{FONT_MONO}" font-size="9.4" font-weight="700" fill="{t['amber_gold']}">⚡ 3.5x AI VELOCITY ENGINE</text>
    <text x="24" y="139" font-family="{FONT_MONO}" font-size="9.2" fill="{t['text_sub']}">Antigravity · Copilot · Claude</text>
  </g>

  <!-- Node 3: Data, Cache & Cloud -->
  <g transform="translate(544, 58)">
    <rect x="0" y="0" width="208" height="152" rx="14" fill="{t['card_alt']}" stroke="{t['emerald_border']}" stroke-width="1.2"/>
    <rect x="16" y="0" width="44" height="3" rx="1.5" fill="{t['emerald']}"/>
    <text x="16" y="25" font-family="{FONT_MONO}" font-size="9.5" font-weight="700" fill="{t['emerald']}">03 · DATA &amp; CLOUD LAYER</text>
    <text x="16" y="48" font-family="{FONT_SANS}" font-size="14.5" font-weight="700" fill="{t['text']}">Cache &amp; Persistence</text>
    <text x="16" y="72" font-family="{FONT_MONO}" font-size="10.4" fill="{t['text_sub']}">▸ Redis Cache (+30% Speed)</text>
    <text x="16" y="92" font-family="{FONT_MONO}" font-size="10.4" fill="{t['text_sub']}">▸ MySQL · PostgreSQL</text>
    <text x="16" y="112" font-family="{FONT_MONO}" font-size="10.4" fill="{t['text_sub']}">▸ AWS RDS &amp; DynamoDB</text>
    <rect x="16" y="124" width="176" height="18" rx="6" fill="{t['emerald_bg']}"/>
    <text x="104" y="136.2" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.2" font-weight="700" fill="{t['emerald']}">INDEXED · HIGH-CONCURRENCY</text>
  </g>

  <!-- Node 4: Production Scale -->
  <g transform="translate(796, 58)">
    <rect x="0" y="0" width="180" height="152" rx="14" fill="{t['card_alt']}" stroke="{t['amber_border']}" stroke-width="1.2"/>
    <rect x="16" y="0" width="44" height="3" rx="1.5" fill="{t['amber']}"/>
    <text x="16" y="25" font-family="{FONT_MONO}" font-size="9.5" font-weight="700" fill="{t['amber_gold']}">04 · PRODUCTION</text>
    <text x="16" y="48" font-family="{FONT_SANS}" font-size="14.5" font-weight="700" fill="{t['text']}">Real-World Impact</text>
    <text x="16" y="72" font-family="{FONT_MONO}" font-size="10.2" fill="{t['text_sub']}">✦ Pan-India Diagnostics</text>
    <text x="16" y="92" font-family="{FONT_MONO}" font-size="10.2" fill="{t['text_sub']}">✦ Big Basket Scale TMS</text>
    <text x="16" y="112" font-family="{FONT_MONO}" font-size="10.2" fill="{t['text_sub']}">✦ 10+ hrs/wk Automated</text>
    <rect x="16" y="124" width="148" height="18" rx="6" fill="{t['amber_bg']}"/>
    <text x="90" y="136.2" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.2" font-weight="700" fill="{t['amber_gold']}">ENTERPRISE DELIVERY</text>
  </g>

  <!-- Bottom Architecture Telemetry Strip -->
  <line x1="24" y1="230" x2="976" y2="230" stroke="{t['rule']}" stroke-width="1"/>
  <circle cx="34" cy="250" r="3.4" fill="{t['emerald']}" class="live-glow"/>
  <text x="45" y="253.5" font-family="{FONT_MONO}" font-size="10" fill="{t['text_sub']}">CSRF &amp; SQLi Defense  ·  Swagger OpenAPI Specs  ·  Razorpay / Stripe Gateways  ·  GitHub CI/CD  ·  MBA Finance &amp; IT Governance</text>
</svg>
"""


def build_tech_stack_radar(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 424

    # Radar geometry (centered inside Left Bento Card: x=4..346, y=38..418)
    cx, cy = 175, 224
    max_r = 80
    axes = [
        ("Laravel & Backend", 0.96, -90, 0, -13, "middle"),
        ("AI Velocity", 0.94, -18, 10, -2, "start"),
        ("DB & Redis", 0.93, 54, 8, 14, "start"),
        ("Python & AWS", 0.88, 126, -8, 14, "end"),
        ("Frontend UI", 0.90, 198, -10, -2, "end"),
    ]

    rings = []
    for frac in (0.35, 0.65, 1.0):
        pts = []
        for _, _, deg, _, _, _ in axes:
            rad = math.radians(deg)
            pts.append(f"{cx + max_r * frac * math.cos(rad):.1f},{cy + max_r * frac * math.sin(rad):.1f}")
        rings.append(f'<polygon points="{" ".join(pts)}" fill="none" stroke="{t["radar_ring"]}" stroke-width="1"/>')

    spokes = []
    poly_pts = []
    vertex_dots = []
    axis_labels = []
    for label, val, deg, dx, dy, anchor in axes:
        rad = math.radians(deg)
        ox = cx + max_r * math.cos(rad)
        oy = cy + max_r * math.sin(rad)
        vx = cx + max_r * val * math.cos(rad)
        vy = cy + max_r * val * math.sin(rad)
        spokes.append(f'<line x1="{cx}" y1="{cy}" x2="{ox:.1f}" y2="{oy:.1f}" stroke="{t["radar_ring"]}" stroke-width="0.9" stroke-dasharray="3 3"/>')
        poly_pts.append(f"{vx:.1f},{vy:.1f}")
        vertex_dots.append(f'<circle cx="{vx:.1f}" cy="{vy:.1f}" r="4.2" fill="{t["card"]}" stroke="{t["purple_soft"]}" stroke-width="2.2"/>')
        axis_labels.append(
            f'<text x="{ox + dx:.1f}" y="{oy + dy:.1f}" text-anchor="{anchor}" font-family="{FONT_MONO}" font-size="9.4" font-weight="700" fill="{t["text_sub"]}">{esc(label)}</text>'
        )

    backend_pills = [
        ("PHP 8.3 & Laravel 11", t["purple_bg"], t["purple_border"], t["purple_soft"], t["purple"]),
        ("REST & Swagger", t["elevated"], t["border"], t["text"], None),
        ("Python", t["purple_bg"], t["purple_border"], t["purple_soft"], t["purple"]),
        ("Django", t["elevated"], t["border"], t["text"], None),
        ("Flask", t["elevated"], t["border"], t["text"], None),
        ("Node.js", t["elevated"], t["border"], t["text"], None),
        ("Pandas", t["cyan_bg"], t["cyan_border"], t["cyan"], None),
        ("NumPy", t["cyan_bg"], t["cyan_border"], t["cyan"], None),
        ("SciPy", t["cyan_bg"], t["cyan_border"], t["cyan"], None),
        ("Scikit-learn", t["cyan_bg"], t["cyan_border"], t["cyan"], None),
        ("OpenCV", t["cyan_bg"], t["cyan_border"], t["cyan"], None),
        ("Matplotlib", t["cyan_bg"], t["cyan_border"], t["cyan"], None),
        ("Seaborn", t["cyan_bg"], t["cyan_border"], t["cyan"], None),
    ]
    ai_pills = [
        ("Google Antigravity IDE", t["amber_bg"], t["amber_border"], t["amber_gold"], t["amber"]),
        ("GitHub Copilot", t["amber_bg"], t["amber_border"], t["amber_gold"], t["amber"]),
        ("Claude 3.7", t["elevated"], t["border"], t["text"], None),
        ("GPT-4", t["elevated"], t["border"], t["text"], None),
        ("Prompt Architecture", t["elevated"], t["border"], t["text"], None),
        ("Autonomous Refactoring", t["elevated"], t["border"], t["text"], None),
        ("Synthetic QA", t["elevated"], t["border"], t["text"], None),
    ]
    frontend_pills = [
        ("React.js", t["cyan_bg"], t["cyan_border"], t["cyan"], t["cyan"]),
        ("Next.js 16", t["cyan_bg"], t["cyan_border"], t["cyan"], t["cyan"]),
        ("Vue.js & Vuex", t["elevated"], t["border"], t["text"], None),
        ("TypeScript", t["elevated"], t["border"], t["text"], None),
        ("JS / AJAX", t["elevated"], t["border"], t["text"], None),
        ("Tailwind CSS", t["elevated"], t["border"], t["text"], None),
        ("Blade", t["elevated"], t["border"], t["text"], None),
    ]
    cloud_pills = [
        ("MySQL", t["emerald_bg"], t["emerald_border"], t["emerald"], t["emerald"]),
        ("PostgreSQL", t["emerald_bg"], t["emerald_border"], t["emerald"], t["emerald"]),
        ("Redis Cache", t["emerald_bg"], t["emerald_border"], t["emerald"], t["emerald"]),
        ("AWS RDS & DynamoDB", t["amber_bg"], t["amber_border"], t["amber_gold"], t["amber"]),
        ("GitHub CI/CD", t["elevated"], t["border"], t["text"], None),
        ("JIRA", t["elevated"], t["border"], t["text"], None),
        ("Postman", t["elevated"], t["border"], t["text"], None),
        ("Razorpay / Stripe", t["elevated"], t["border"], t["text"], None),
    ]

    b_svg = render_pills_wrapped(backend_pills, start_x=378, start_y=84, max_x=974, row_gap=30, col_gap=6, height=24, font_size=10.4)
    a_svg = render_pills_wrapped(ai_pills, start_x=378, start_y=194, max_x=974, row_gap=30, col_gap=6, height=24, font_size=10.4)
    f_svg = render_pills_wrapped(frontend_pills, start_x=378, start_y=304, max_x=654, row_gap=30, col_gap=6, height=24, font_size=10.4)
    c_svg = render_pills_wrapped(cloud_pills, start_x=698, start_y=304, max_x=976, row_gap=30, col_gap=6, height=24, font_size=10.4)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Engineering Capability Radar and Technical Ecosystem">
  <defs>
    <linearGradient id="radarFill" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{t['purple']}" stop-opacity="0.42"/>
      <stop offset="55%" stop-color="{t['cyan']}" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="{t['amber']}" stop-opacity="0.34"/>
    </linearGradient>
    <linearGradient id="radarStroke" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{t['purple_soft']}"/>
      <stop offset="50%" stop-color="{t['cyan']}"/>
      <stop offset="100%" stop-color="{t['amber']}"/>
    </linearGradient>
  </defs>

  {render_section_header("CAPABILITY RADAR & TECH STACK", "FULL-STACK DEPTH + AI ACCELERATORS", t, t["purple"], w)}

  <!-- Left Bento: 5-Axis Capability Radar Chart -->
  <g>
    <rect x="4" y="38" width="342" height="380" rx="16" fill="{t['card']}" stroke="{t['border']}" stroke-width="1.2"/>
    <rect x="24" y="38" width="58" height="3" rx="1.5" fill="{t['purple']}"/>
    <text x="24" y="66" font-family="{FONT_MONO}" font-size="11" font-weight="700" letter-spacing="1.1" fill="{t['purple_soft']}">ENGINEERING RADAR</text>
    <text x="24" y="84" font-family="{FONT_SANS}" font-size="11.5" fill="{t['text_muted']}">Multi-domain production capability map</text>

    {"".join(rings)}
    {"".join(spokes)}
    <polygon points="{" ".join(poly_pts)}" fill="url(#radarFill)" stroke="url(#radarStroke)" stroke-width="2.2" stroke-linejoin="round"/>
    {"".join(vertex_dots)}
    {"".join(axis_labels)}

    <!-- Radar Legend Footer -->
    <line x1="24" y1="354" x2="326" y2="354" stroke="{t['rule']}" stroke-width="1"/>
    <text x="24" y="376" font-family="{FONT_MONO}" font-size="9.6" font-weight="700" fill="{t['emerald']}">● CORE STRENGTH:</text>
    <text x="148" y="376" font-family="{FONT_MONO}" font-size="9.6" fill="{t['text_sub']}">Laravel · Redis · AI</text>
    <text x="24" y="396" font-family="{FONT_MONO}" font-size="9.6" font-weight="700" fill="{t['amber_gold']}">● STRATEGIC EDGE:</text>
    <text x="148" y="396" font-family="{FONT_MONO}" font-size="9.6" fill="{t['text_sub']}">Tech + MBA Finance ROI</text>
  </g>

  <!-- Right Top: Backend & Python Data Science -->
  <g>
    <rect x="360" y="38" width="636" height="106" rx="15" fill="{t['card']}" stroke="{t['border']}" stroke-width="1.2"/>
    <rect x="378" y="38" width="54" height="3" rx="1.5" fill="{t['purple']}"/>
    <text x="378" y="65" font-family="{FONT_MONO}" font-size="10.8" font-weight="700" letter-spacing="1.1" fill="{t['purple_soft']}">BACKEND ARCHITECTURE &amp; PYTHON DATA SCIENCE</text>
    <text x="976" y="65" text-anchor="end" font-family="{FONT_MONO}" font-size="9.6" fill="{t['text_muted']}">13 TECHNOLOGIES</text>
    {b_svg}
  </g>

  <!-- Right Middle: AI Agentic Engineering -->
  <g>
    <rect x="360" y="154" width="636" height="96" rx="15" fill="{t['card']}" stroke="{t['amber_border']}" stroke-width="1.2"/>
    <rect x="378" y="154" width="54" height="3" rx="1.5" fill="{t['amber']}"/>
    <text x="378" y="180" font-family="{FONT_MONO}" font-size="10.8" font-weight="700" letter-spacing="1.1" fill="{t['amber_gold']}">AI AGENTIC ENGINEERING &amp; AUTOMATION</text>
    <rect x="870" y="164" width="108" height="20" rx="10" fill="{t['amber_bg']}" stroke="{t['amber_border']}" stroke-width="0.9"/>
    <text x="924" y="177.2" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.2" font-weight="700" fill="{t['amber_gold']}">⚡ SUPERCHARGED</text>
    {a_svg}
  </g>

  <!-- Right Bottom-Left: Frontend & UI -->
  <g>
    <rect x="360" y="260" width="310" height="158" rx="15" fill="{t['card']}" stroke="{t['border']}" stroke-width="1.2"/>
    <rect x="378" y="260" width="48" height="3" rx="1.5" fill="{t['cyan']}"/>
    <text x="378" y="286" font-family="{FONT_MONO}" font-size="10.6" font-weight="700" letter-spacing="1.1" fill="{t['cyan']}">FRONTEND &amp; UI SYSTEMS</text>
    {f_svg}
  </g>

  <!-- Right Bottom-Right: Databases, Cloud & DevOps -->
  <g>
    <rect x="682" y="260" width="314" height="158" rx="15" fill="{t['card']}" stroke="{t['border']}" stroke-width="1.2"/>
    <rect x="698" y="260" width="48" height="3" rx="1.5" fill="{t['emerald']}"/>
    <text x="698" y="286" font-family="{FONT_MONO}" font-size="10.6" font-weight="700" letter-spacing="1.1" fill="{t['emerald']}">DATABASES, CLOUD &amp; DEVOPS</text>
    {c_svg}
  </g>
</svg>
"""


def build_projects_header(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 44
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Featured Production Case Studies">
  {render_section_header("FEATURED PRODUCTION CASE STUDIES", "CLICK ANY CARD TO LAUNCH LIVE PLATFORM", t, t["emerald"], w)}
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
    thumb_svg: str,
) -> str:
    t = THEMES[theme_name]
    w, h = 488, 160
    acc = t[accent_key]
    bg = t[f"{accent_key}_bg"]
    brd = t[f"{accent_key}_border"]

    tag_pills = []
    tx = 20
    for tg in tags:
        svg_p, tw = render_pill(tx, 121, tg, t["elevated"], t["border"], t["text_sub"], height=23, font_size=10.2, mono=True)
        tag_pills.append(svg_p)
        tx += tw + 6

    badge_w = measure_pill(badge, char_w=6.7, pad_x=22, min_w=92)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" rx="16" fill="{t['card']}" stroke="{t['border']}" stroke-width="1.2"/>
  <rect x="20" y="2" width="58" height="3" rx="1.5" fill="{acc}"/>

  <!-- Mini Architectural Visual Preview Thumbnail (Top-Right) -->
  <g transform="translate(382, 16)">
    <rect x="0" y="0" width="88" height="54" rx="10" fill="{bg}" stroke="{brd}" stroke-width="1"/>
    {thumb_svg.format(c=acc)}
  </g>

  <rect x="20" y="16" width="{badge_w}" height="22" rx="11" fill="{bg}" stroke="{brd}" stroke-width="0.9"/>
  <text x="{20 + badge_w / 2:.1f}" y="30.2" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.5" font-weight="700" fill="{acc}">{esc(badge)}</text>
  <text x="{20 + badge_w + 10}" y="30.2" font-family="{FONT_MONO}" font-size="9.8" fill="{t['text_muted']}">{esc(period)} · {esc(category)}</text>

  <text x="20" y="64" font-family="{FONT_SANS}" font-size="16" font-weight="800" fill="{t['text']}">{esc(title)}</text>
  <text x="20" y="86" font-family="{FONT_SANS}" font-size="11.8" fill="{t['text_sub']}">{esc(desc1)}</text>
  <text x="20" y="103" font-family="{FONT_SANS}" font-size="11.8" fill="{t['text_sub']}">{esc(desc2)}</text>

  {"".join(tag_pills)}

  <!-- Live CTA Indicator Bottom-Right -->
  <circle cx="422" cy="132.5" r="3" fill="{acc}"/>
  <text x="430" y="136" font-family="{FONT_MONO}" font-size="9.6" font-weight="700" fill="{acc}">LIVE ↗</text>
</svg>
"""


def build_journey(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 400

    exp_items = [
        (
            "2023 – PRESENT · CURRENT ROLE",
            "Laravel Developer",
            "Abym Technology Pvt. Ltd · Noida",
            "+30% performance boost via SQL optimization & Redis caching · Swagger APIs",
            "Modular full-stack platforms with Laravel 11, React.js & Vue.js",
            t["emerald"],
            True,
        ),
        (
            "2022 – 2023 · FULL-STACK",
            "Laravel Developer",
            "Finesoft Technologies Pvt. Ltd · Noida",
            "Full-stack Blade & Vue.js delivery · 3rd-party payment gateways & SMS",
            "High-concurrency relational DB schemas with optimized query execution",
            t["purple"],
            False,
        ),
        (
            "2021 – 2022 · AUTOMATION",
            "Python Developer",
            "Magical Umbrella Pvt. Ltd",
            "Automated routine data pipelines in Python — saved 10+ manual hrs/week",
            "Engineered secure RESTful backend APIs & relational database designs",
            t["cyan"],
            False,
        ),
    ]

    exp_svgs = []
    ey = 82
    for period, role, company, b1, b2, color, live in exp_items:
        pulse_cls = ' class="live-dot"' if live else ""
        exp_svgs.append(f"""
    <circle cx="34" cy="{ey + 12}" r="6.8" fill="{t['card']}" stroke="{color}" stroke-width="2.2"/>
    <circle cx="34" cy="{ey + 12}" r="2.8" fill="{color}"{pulse_cls}/>
    <text x="54" y="{ey + 8}" font-family="{FONT_MONO}" font-size="10" font-weight="700" fill="{color}">{esc(period)}</text>
    <text x="54" y="{ey + 27}" font-family="{FONT_SANS}" font-size="14.5" font-weight="700" fill="{t['text']}">{esc(role)} <tspan font-size="12" font-weight="600" fill="{t['text_sub']}">— {esc(company)}</tspan></text>
    <text x="54" y="{ey + 47}" font-family="{FONT_SANS}" font-size="11.4" fill="{t['text_sub']}">⚡ {esc(b1)}</text>
    <text x="54" y="{ey + 65}" font-family="{FONT_SANS}" font-size="11.4" fill="{t['text_muted']}">▸ {esc(b2)}</text>""")
        ey += 97

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Career Experience and Academic Credentials">
  <defs>
    <linearGradient id="spineGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{t['emerald']}"/>
      <stop offset="50%" stop-color="{t['purple']}"/>
      <stop offset="100%" stop-color="{t['cyan']}"/>
    </linearGradient>
    <style>
      @keyframes pulseNode {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.25; }} }}
      .live-dot {{ animation: pulseNode 2s ease-in-out infinite; }}
    </style>
  </defs>

  {render_section_header("CAREER JOURNEY & CREDENTIALS", "5+ YEARS PRODUCTION · MBA + B.E. CSE", t, t["cyan"], w)}

  <!-- Left Panel: Work Experience -->
  <g>
    <rect x="4" y="38" width="564" height="354" rx="16" fill="{t['card']}" stroke="{t['border']}" stroke-width="1.2"/>
    <rect x="24" y="38" width="60" height="3" rx="1.5" fill="{t['purple']}"/>
    <text x="24" y="66" font-family="{FONT_MONO}" font-size="11.2" font-weight="700" letter-spacing="1.2" fill="{t['purple_soft']}">PROFESSIONAL EXPERIENCE</text>
    <line x1="34" y1="98" x2="34" y2="294" stroke="url(#spineGrad)" stroke-width="2" stroke-dasharray="4 4"/>
    {"".join(exp_svgs)}
  </g>

  <!-- Right Top Panel: Academic Qualifications -->
  <g>
    <rect x="584" y="38" width="412" height="238" rx="16" fill="{t['card']}" stroke="{t['border']}" stroke-width="1.2"/>
    <rect x="604" y="38" width="60" height="3" rx="1.5" fill="{t['emerald']}"/>
    <text x="604" y="66" font-family="{FONT_MONO}" font-size="11.2" font-weight="700" letter-spacing="1.2" fill="{t['emerald']}">ACADEMIC QUALIFICATIONS</text>

    <rect x="604" y="82" width="372" height="79" rx="12" fill="{t['elevated']}" stroke="{t['emerald_border']}" stroke-width="1"/>
    <circle cx="622" cy="100" r="3.5" fill="{t['emerald']}" class="live-dot"/>
    <text x="632" y="103.5" font-family="{FONT_MONO}" font-size="9.8" font-weight="700" fill="{t['emerald']}">PURSUING · 2024 – PRESENT</text>
    <text x="618" y="125" font-family="{FONT_SANS}" font-size="14" font-weight="700" fill="{t['text']}">MBA in Finance &amp; IT</text>
    <text x="618" y="145" font-family="{FONT_SANS}" font-size="11.6" fill="{t['text_sub']}">Gondwana University · Business ROI &amp; IT Governance</text>

    <rect x="604" y="173" width="372" height="87" rx="12" fill="{t['elevated']}" stroke="{t['border']}" stroke-width="1"/>
    <text x="618" y="192" font-family="{FONT_MONO}" font-size="9.8" font-weight="700" fill="{t['cyan']}">COMPLETED OCT 2020 · 74.60% DISTINCTION</text>
    <text x="618" y="214" font-family="{FONT_SANS}" font-size="14" font-weight="700" fill="{t['text']}">B.E. in Computer Science</text>
    <text x="618" y="233" font-family="{FONT_SANS}" font-size="11.6" fill="{t['text_sub']}">Gondwana University</text>
    <text x="618" y="249" font-family="{FONT_MONO}" font-size="9.8" fill="{t['text_muted']}">Data Analysis · ML · Deep Learning · Web Dev</text>
  </g>

  <!-- Right Bottom Panel: Identity & Motto -->
  <g>
    <rect x="584" y="290" width="412" height="102" rx="16" fill="{t['card']}" stroke="{t['border']}" stroke-width="1.2"/>
    <rect x="604" y="290" width="60" height="3" rx="1.5" fill="{t['amber']}"/>
    <text x="604" y="317" font-family="{FONT_MONO}" font-size="10.4" font-weight="700" letter-spacing="1.2" fill="{t['amber_gold']}">PROFILE SNAPSHOT</text>
    <text x="604" y="341" font-family="{FONT_SANS}" font-size="11.6" fill="{t['text_sub']}">📍 Chandrapur, Maharashtra · 🌐 English, Hindi, Marathi</text>
    <text x="604" y="368" font-family="{FONT_MONO}" font-size="11" font-weight="600" fill="{t['purple_soft']}">✦ &quot;Patience is the solution to everything&quot;</text>
  </g>
</svg>
"""


def build_connect_header(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 90
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Initiate Contact and Connect">
  <defs>
    <linearGradient id="connectGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['purple']}"/>
      <stop offset="50%" stop-color="{t['amber']}"/>
      <stop offset="100%" stop-color="{t['emerald']}"/>
    </linearGradient>
  </defs>
  {render_section_header("INITIATE CONTACT & CONNECT", "OPEN FOR ROLES, ARCHITECTURE & ADVISORY", t, t["amber"], w)}
  <rect x="4" y="35" width="992" height="49" rx="14" fill="{t['card']}" stroke="{t['border']}" stroke-width="1.2"/>
  <rect x="4" y="35" width="5" height="49" rx="2.5" fill="url(#connectGrad)"/>
  <text x="26" y="64" font-family="{FONT_SANS}" font-size="14" font-weight="700" fill="{t['text']}">Explore my live Next.js portfolio, download my resume, or connect directly across channels below.</text>
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
  <text x="68" y="57" font-family="{FONT_MONO}" font-size="{9.7 if len(subtitle) > 28 else 10.6}" fill="{t['text_sub']}">{esc(subtitle)}</text>
</svg>
"""


def build_footer(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 74
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Shubham Bramhane Footer">
  <defs>
    <clipPath id="footClip">
      <rect x="4" y="4" width="992" height="66" rx="16"/>
    </clipPath>
    <linearGradient id="footWave1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['purple']}" stop-opacity="0.22"/>
      <stop offset="50%" stop-color="{t['amber']}" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="{t['emerald']}" stop-opacity="0.22"/>
    </linearGradient>
    <linearGradient id="footWave2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['cyan']}" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="{t['purple']}" stop-opacity="0.14"/>
    </linearGradient>
    <linearGradient id="footLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['purple']}"/>
      <stop offset="50%" stop-color="{t['amber']}"/>
      <stop offset="100%" stop-color="{t['emerald']}"/>
    </linearGradient>
    <style>
      @keyframes footShimmer {{ 0% {{ transform: translateX(-220px); opacity: 0; }} 25% {{ opacity: 0.7; }} 75% {{ opacity: 0.7; }} 100% {{ transform: translateX(1020px); opacity: 0; }} }}
      .shimmer {{ animation: footShimmer 6s ease-in-out infinite; }}
    </style>
  </defs>
  <g clip-path="url(#footClip)">
    <rect x="4" y="4" width="992" height="66" fill="{t['card']}"/>
    <path d="M0 50 Q250 20 500 44 T1000 34 L1000 74 L0 74 Z" fill="url(#footWave1)"/>
    <path d="M0 40 Q280 62 560 32 T1000 48 L1000 74 L0 74 Z" fill="url(#footWave2)"/>
    <rect x="4" y="67" width="992" height="3" fill="url(#footLine)"/>
    <rect x="0" y="67" width="180" height="3" fill="#FFFFFF" class="shimmer"/>
  </g>
  <rect x="4" y="4" width="992" height="66" rx="16" fill="none" stroke="{t['border']}" stroke-width="1.2"/>
  <text x="500" y="42" text-anchor="middle" font-family="{FONT_MONO}" font-size="11.2" font-weight="700" letter-spacing="0.9" fill="{t['text_sub']}">&lt;SB/&gt;  SHUBHAM BRAMHANE  ·  ARCHITECTING HIGH-THROUGHPUT SYSTEMS WITH AI VELOCITY</text>
</svg>
"""


CTA_BUTTONS = [
    (
        "portfolio",
        "Explore Portfolio",
        "LIVE NEXT.JS SHOWCASE",
        "primary",
        '<circle cx="14" cy="14" r="9.5" fill="none" stroke="{c}" stroke-width="1.8"/>'
        '<ellipse cx="14" cy="14" rx="4.2" ry="9.5" fill="none" stroke="{c}" stroke-width="1.5"/>'
        '<line x1="4.5" y1="14" x2="23.5" y2="14" stroke="{c}" stroke-width="1.5"/>',
    ),
    (
        "resume",
        "Download Resume",
        "VERIFIED PDF CV",
        "amber",
        '<path d="M8 4 H16 L21 9 V23 H8 Z" fill="none" stroke="{c}" stroke-width="1.8" stroke-linejoin="round"/>'
        '<polyline points="16,4 16,9 21,9" fill="none" stroke="{c}" stroke-width="1.5"/>'
        '<line x1="11" y1="14.5" x2="18" y2="14.5" stroke="{c}" stroke-width="1.5" stroke-linecap="round"/>'
        '<line x1="11" y1="18.5" x2="16" y2="18.5" stroke="{c}" stroke-width="1.5" stroke-linecap="round"/>',
    ),
    (
        "linkedin",
        "LinkedIn Profile",
        "IN/SHUBHAM1602",
        "cyan",
        '<rect x="6.5" y="11" width="3.2" height="10.5" rx="0.9" fill="{c}"/>'
        '<circle cx="8.1" cy="7.5" r="1.8" fill="{c}"/>'
        '<path d="M12.5 11 H15.5 V12.7 C16.3 11.4 17.5 10.7 19.1 10.7 C21.3 10.7 22.2 12.2 22.2 14.8 V21.5 H19 V15.4 C19 14 18.4 13.3 17.3 13.3 C16.2 13.3 15.6 14.1 15.6 15.4 V21.5 H12.5 Z" fill="{c}"/>',
    ),
    (
        "contact",
        "Initiate Contact",
        "DIRECT EMAIL",
        "emerald",
        '<rect x="5" y="7.5" width="18" height="13" rx="2.4" fill="none" stroke="{c}" stroke-width="1.8"/>'
        '<polyline points="5.8,8.8 14,15.2 22.2,8.8" fill="none" stroke="{c}" stroke-width="1.8" stroke-linejoin="round"/>',
    ),
]


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
        '<polyline points="10,36 22,36 29,22 37,40 46,16 56,34 65,24 78,20" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="78" cy="20" r="3" fill="{c}"/>',
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
        '<path d="M 16 40 C 30 38, 34 18, 50 22 C 62 25, 64 16, 74 16" fill="none" stroke="{c}" stroke-width="2" stroke-dasharray="4 3"/>'
        '<circle cx="16" cy="40" r="4" fill="{c}"/><circle cx="50" cy="22" r="3.5" fill="none" stroke="{c}" stroke-width="2"/><circle cx="74" cy="16" r="4" fill="{c}"/>',
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
        '<rect x="14" y="34" width="9" height="10" rx="2" fill="{c}" fill-opacity="0.35"/>'
        '<rect x="28" y="27" width="9" height="17" rx="2" fill="{c}" fill-opacity="0.55"/>'
        '<rect x="42" y="21" width="9" height="23" rx="2" fill="{c}" fill-opacity="0.78"/>'
        '<rect x="56" y="13" width="9" height="31" rx="2" fill="{c}"/>'
        '<polyline points="16,28 32,20 48,16 66,9" fill="none" stroke="{c}" stroke-width="1.6" stroke-linecap="round"/>',
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
        '<rect x="12" y="11" width="64" height="32" rx="5" fill="none" stroke="{c}" stroke-width="1.5"/>'
        '<line x1="12" y1="20" x2="76" y2="20" stroke="{c}" stroke-width="1.2"/>'
        '<rect x="18" y="25" width="22" height="5" rx="2" fill="{c}" fill-opacity="0.7"/>'
        '<rect x="18" y="33" width="38" height="5" rx="2" fill="{c}" fill-opacity="0.4"/>'
        '<circle cx="65" cy="31" r="6" fill="none" stroke="{c}" stroke-width="1.6"/>',
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
        '<rect x="12" y="20" width="16" height="14" rx="3" fill="none" stroke="{c}" stroke-width="1.6"/>'
        '<rect x="36" y="20" width="16" height="14" rx="3" fill="{c}" fill-opacity="0.3" stroke="{c}" stroke-width="1.6"/>'
        '<rect x="60" y="20" width="16" height="14" rx="3" fill="{c}"/>'
        '<line x1="28" y1="27" x2="36" y2="27" stroke="{c}" stroke-width="1.6"/>'
        '<line x1="52" y1="27" x2="60" y2="27" stroke="{c}" stroke-width="1.6"/>',
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
        '<rect x="12" y="10" width="36" height="16" rx="4" fill="{c}" fill-opacity="0.35" stroke="{c}" stroke-width="1.4"/>'
        '<rect x="52" y="10" width="24" height="34" rx="4" fill="none" stroke="{c}" stroke-width="1.4"/>'
        '<rect x="12" y="30" width="16" height="14" rx="4" fill="none" stroke="{c}" stroke-width="1.4"/>'
        '<rect x="32" y="30" width="16" height="14" rx="4" fill="{c}"/>',
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
    for old in ASSETS_DIR.glob("*.svg"):
        old.unlink()

    generated = []
    for theme in ("dark", "light"):
        outputs = {
            f"hero-{theme}.svg": build_hero(theme),
            f"metrics-{theme}.svg": build_metrics(theme),
            f"architecture-flow-{theme}.svg": build_architecture_flow(theme),
            f"tech-stack-{theme}.svg": build_tech_stack_radar(theme),
            f"projects-header-{theme}.svg": build_projects_header(theme),
            f"journey-{theme}.svg": build_journey(theme),
            f"connect-header-{theme}.svg": build_connect_header(theme),
            f"footer-{theme}.svg": build_footer(theme),
        }
        for key, label, sub, style, icon in CTA_BUTTONS:
            outputs[f"cta-{key}-{theme}.svg"] = build_cta_button(theme, key, label, sub, style, icon)
        for key, title, cat, badge, period, d1, d2, tags, acc, thumb in PROJECT_CARDS:
            outputs[f"proj-{key}-{theme}.svg"] = build_project_card(
                theme, title, cat, badge, period, d1, d2, tags, acc, thumb
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
