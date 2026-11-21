#!/usr/bin/env python3
"""
Deterministic SVG visual asset generator (v3.0 — Aurora Glass & Cinematic Bento Edition)
for Shubham Bramhane's GitHub Profile README.
Unified with https://my-portfolio-beta-bay-93.vercel.app/ and his GitHub brand identity.
Generates 50 XML-validated Dark & Light SVGs into ./assets/.
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
        "card_top": "#151929",
        "card_bot": "#0B0D15",
        "card": "#0F121D",
        "card_alt": "#141828",
        "elevated": "#1A1F34",
        "code_bg": "#070910",
        "code_bar": "#111526",
        "border": "#242A45",
        "border_strong": "#364069",
        "specular": "#FFFFFF",
        "specular_op": "0.14",
        "dot_grid": "#2D3559",
        "dot_opacity": "0.48",
        "grid_line": "#1B213A",
        "text": "#F8FAFC",
        "text_sub": "#A8B1CC",
        "text_muted": "#6E7899",
        "rule": "#202742",
        "purple": "#A855F7",
        "purple_soft": "#C084FC",
        "purple_bg": "#21143B",
        "purple_border": "#52308F",
        "fuchsia": "#E879F9",
        "amber": "#FB923C",
        "amber_gold": "#FBBF24",
        "amber_bg": "#2E1C0E",
        "amber_border": "#734219",
        "emerald": "#34D399",
        "emerald_bg": "#0B2C23",
        "emerald_border": "#18634E",
        "cyan": "#38BDF8",
        "cyan_bg": "#0D273F",
        "cyan_border": "#1C567D",
        "rose": "#FB7185",
        "rose_bg": "#331424",
        "rose_border": "#732546",
        "glow_opacity": "0.30",
        "card_glow": "0.16",
        "code_kw": "#C084FC",
        "code_cls": "#38BDF8",
        "code_str": "#34D399",
        "code_prop": "#E2E8F0",
        "code_num": "#546082",
        "code_punct": "#7685AB",
        "code_comment": "#64748B",
        "grad_text_1": "#FFFFFF",
        "grad_text_2": "#D8B4FE",
        "grad_text_3": "#FDBA74",
        "radar_ring": "#293152",
        "mandala": "#F59E0B",
        "mandala_op": "0.16",
    },
    "light": {
        "canvas": "#FFFFFF",
        "card_top": "#FFFFFF",
        "card_bot": "#F6F8FC",
        "card": "#FFFFFF",
        "card_alt": "#F8FAFC",
        "elevated": "#F1F5F9",
        "code_bg": "#0C0F1A",
        "code_bar": "#161B2E",
        "border": "#E2E8F0",
        "border_strong": "#CBD5E1",
        "specular": "#FFFFFF",
        "specular_op": "0.9",
        "dot_grid": "#CBD5E1",
        "dot_opacity": "0.62",
        "grid_line": "#E2E8F0",
        "text": "#0F172A",
        "text_sub": "#475569",
        "text_muted": "#64748B",
        "rule": "#E2E8F0",
        "purple": "#7C3AED",
        "purple_soft": "#6D28D9",
        "purple_bg": "#F3E8FF",
        "purple_border": "#DDD6FE",
        "fuchsia": "#C026D3",
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
        "glow_opacity": "0.16",
        "card_glow": "0.09",
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
        "mandala": "#D97706",
        "mandala_op": "0.18",
    },
}


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def glass_defs(t: dict[str, str], prefix: str = "g") -> str:
    return f"""
    <linearGradient id="{prefix}Card" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{t['card_top']}"/>
      <stop offset="100%" stop-color="{t['card_bot']}"/>
    </linearGradient>
    <linearGradient id="{prefix}Spec" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['specular']}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{t['specular']}" stop-opacity="{t['specular_op']}"/>
      <stop offset="100%" stop-color="{t['specular']}" stop-opacity="0"/>
    </linearGradient>"""


def glass_card(
    x: int,
    y: int,
    w: int,
    h: int,
    rx: int,
    t: dict[str, str],
    accent: str | None = None,
    border: str | None = None,
    prefix: str = "g",
    accent_w: int = 56,
) -> str:
    brd = border or t["border"]
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#{prefix}Card)" stroke="{brd}" stroke-width="1.15"/>',
        f'<line x1="{x + rx}" y1="{y + 0.8}" x2="{x + w - rx}" y2="{y + 0.8}" stroke="url(#{prefix}Spec)" stroke-width="1"/>',
    ]
    if accent:
        parts.append(f'<rect x="{x + 18}" y="{y}" width="{accent_w}" height="3" rx="1.5" fill="{accent}"/>')
    return "\n  ".join(parts)


def mandala_geometry(cx: float, cy: float, r: float, color: str, opacity: str) -> str:
    """Delicate concentric sacred-geometry ornament echoing Shubham's GitHub profile emblem."""
    elems = [
        f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="none" stroke="{color}" stroke-width="0.9" stroke-opacity="{opacity}"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r * 0.72:.1f}" fill="none" stroke="{color}" stroke-width="0.8" stroke-dasharray="3 3" stroke-opacity="{opacity}"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r * 0.44:.1f}" fill="none" stroke="{color}" stroke-width="0.9" stroke-opacity="{opacity}"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r * 0.18:.1f}" fill="{color}" fill-opacity="{opacity}"/>',
    ]
    for k in range(12):
        ang = math.radians(k * 30)
        x1 = cx + r * 0.44 * math.cos(ang)
        y1 = cy + r * 0.44 * math.sin(ang)
        x2 = cx + r * math.cos(ang)
        y2 = cy + r * math.sin(ang)
        px = cx + r * 0.72 * math.cos(ang + math.radians(15))
        py = cy + r * 0.72 * math.sin(ang + math.radians(15))
        elems.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="0.7" stroke-opacity="{opacity}"/>')
        elems.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="1.8" fill="{color}" fill-opacity="{opacity}"/>')
    return "\n    ".join(elems)


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
    font_size: float = 10.6,
    weight: int = 600,
    mono: bool = False,
    width: int | None = None,
) -> tuple[str, int]:
    char_w = 6.9 if mono else 6.4
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
    font_size: float = 10.6,
    mono: bool = False,
) -> str:
    out = []
    cx = start_x
    cy = start_y
    for label, bg, brd, fg, dot in items:
        char_w = 6.9 if mono else 6.4
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
    label_w = int(len(title) * 8.1 + 28)
    rule_x = 18 + label_w
    right_end = width - 6
    sub_svg = ""
    if subtitle:
        sub_svg = f'<text x="{right_end}" y="18.5" text-anchor="end" font-family="{FONT_MONO}" font-size="10.1" fill="{t["text_muted"]}">{esc(subtitle)}</text>'
        rule_end = right_end - int(len(subtitle) * 6.3 + 14)
    else:
        rule_end = right_end
    return f"""
  <g>
    <rect x="6" y="9" width="9" height="9" rx="3" fill="{accent}"/>
    <circle cx="10.5" cy="13.5" r="1.8" fill="#FFFFFF" fill-opacity="0.7"/>
    <text x="23" y="18.5" font-family="{FONT_MONO}" font-size="11.5" font-weight="700" letter-spacing="1.8" fill="{t['text_sub']}">{esc(title)}</text>
    <line x1="{rule_x}" y1="14" x2="{max(rule_x + 20, rule_end)}" y2="14" stroke="{t['rule']}" stroke-width="1"/>
    {sub_svg}
  </g>"""


def build_hero(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 404

    hero_pills = [
        ("✦ PHP 8.3 / Laravel 11", t["elevated"], t["border_strong"], t["text"], None),
        ("✦ Redis (+30% Velocity)", t["elevated"], t["border_strong"], t["text"], None),
        ("✦ React.js & Next.js 16", t["elevated"], t["border_strong"], t["text"], None),
        ("✦ MySQL / PostgreSQL", t["elevated"], t["border_strong"], t["text"], None),
        ("✦ Python & AWS", t["elevated"], t["border_strong"], t["text"], None),
        ("✦ Google Antigravity & Copilot", t["purple_bg"], t["purple_border"], t["purple_soft"], None),
    ]
    pills_svg = render_pills_wrapped(hero_pills, start_x=36, start_y=302, max_x=564, row_gap=34, col_gap=8, height=27, font_size=10.8)

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
    cy = 98
    for idx, (num, markup) in enumerate(code_lines):
        if idx == 8:
            code_svg.append(f'    <rect x="590" y="{cy - 13}" width="376" height="18" fill="#A855F7" fill-opacity="0.13"/>')
            code_svg.append(f'    <rect x="590" y="{cy - 13}" width="3" height="18" fill="{t["purple_soft"]}"/>')
        code_svg.append(f'    <text x="602" y="{cy}" font-family="{FONT_MONO}" font-size="10.4" fill="{t["code_num"]}">{num}</text>')
        code_svg.append(f'    <text x="623" y="{cy}" font-family="{FONT_MONO}" font-size="10.4">{markup}</text>')
        cy += 18.2

    spark_path = "M 606 340 C 640 337, 668 331, 702 325 C 742 318, 774 322, 816 312 C 858 303, 898 306, 946 299"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Shubham Bramhane - Senior Full-Stack Architect and AI-Augmented Engineer">
  <defs>
    {glass_defs(t, "hero")}
    <clipPath id="heroClip">
      <rect x="4" y="4" width="992" height="396" rx="24"/>
    </clipPath>
    <pattern id="dotGrid" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.05" fill="{t['dot_grid']}" fill-opacity="{t['dot_opacity']}"/>
    </pattern>
    <linearGradient id="brandBar" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['purple']}"/>
      <stop offset="35%" stop-color="{t['fuchsia']}"/>
      <stop offset="68%" stop-color="{t['amber']}"/>
      <stop offset="100%" stop-color="{t['emerald']}"/>
    </linearGradient>
    <linearGradient id="sbMark" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#9333EA"/>
      <stop offset="100%" stop-color="#F97316"/>
    </linearGradient>
    <linearGradient id="headlineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['grad_text_1']}"/>
      <stop offset="44%" stop-color="{t['grad_text_2']}"/>
      <stop offset="100%" stop-color="{t['grad_text_3']}"/>
    </linearGradient>
    <linearGradient id="auroraSilk" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['purple']}" stop-opacity="0"/>
      <stop offset="28%" stop-color="{t['purple']}" stop-opacity="0.16"/>
      <stop offset="62%" stop-color="{t['amber']}" stop-opacity="0.13"/>
      <stop offset="100%" stop-color="{t['cyan']}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="sparkArea" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{t['emerald']}" stop-opacity="0.40"/>
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
      <stop offset="0%" stop-color="{t['cyan']}" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="{t['cyan']}" stop-opacity="0"/>
    </radialGradient>
    <style>
      @keyframes pulseDot {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.25; }} }}
      @keyframes blinkCursor {{ 0%, 49% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}
      @keyframes breathe {{ 0%, 100% {{ opacity: 0.95; }} 50% {{ opacity: 0.5; }} }}
      @keyframes twinkle {{ 0%, 100% {{ opacity: 0.85; }} 50% {{ opacity: 0.15; }} }}
      @keyframes flowTrace {{ from {{ stroke-dashoffset: 240; }} to {{ stroke-dashoffset: 0; }} }}
      @keyframes scanBeam {{ 0% {{ transform: translateX(-260px); opacity: 0; }} 20% {{ opacity: 0.85; }} 80% {{ opacity: 0.85; }} 100% {{ transform: translateX(1040px); opacity: 0; }} }}
      .pulse-dot {{ animation: pulseDot 2s ease-in-out infinite; }}
      .blink {{ animation: blinkCursor 1.1s steps(1) infinite; }}
      .orb {{ animation: breathe 6.5s ease-in-out infinite; }}
      .star1 {{ animation: twinkle 3.2s ease-in-out infinite; }}
      .star2 {{ animation: twinkle 4.4s ease-in-out 1.1s infinite; }}
      .trace-flow {{ stroke-dasharray: 28 18; animation: flowTrace 6s linear infinite; }}
      .scan {{ animation: scanBeam 5.5s ease-in-out infinite; }}
    </style>
  </defs>

  <g clip-path="url(#heroClip)">
    <rect x="4" y="4" width="992" height="396" fill="url(#heroCard)"/>
    <rect x="4" y="4" width="992" height="396" fill="url(#dotGrid)"/>
    <circle cx="130" cy="55" r="275" fill="url(#glowPurple)" class="orb"/>
    <circle cx="885" cy="345" r="270" fill="url(#glowAmber)" class="orb"/>
    <circle cx="510" cy="385" r="200" fill="url(#glowCyan)"/>

    <!-- Sweeping Translucent Aurora Silk Ribbon -->
    <path d="M -20 260 C 180 185, 360 325, 580 225 C 760 145, 890 250, 1030 165 L 1030 235 C 880 310, 745 205, 565 280 C 350 370, 175 245, -20 315 Z" fill="url(#auroraSilk)"/>

    <!-- Subtle Golden Sacred-Geometry Watermark Echoing Profile Avatar -->
    <g>{mandala_geometry(518, 72, 62, t['mandala'], '0.10')}</g>

    <!-- Animated Starlight Micro-Particles -->
    <circle cx="520" cy="140" r="1.8" fill="{t['purple_soft']}" class="star1"/>
    <circle cx="485" cy="88" r="1.4" fill="{t['amber_gold']}" class="star2"/>
    <circle cx="556" cy="238" r="1.6" fill="{t['cyan']}" class="star1"/>
    <circle cx="290" cy="64" r="1.3" fill="{t['emerald']}" class="star2"/>

    <!-- Animated Circuit Trace -->
    <path d="M 4 278 H 124 L 148 302 H 572" fill="none" stroke="{t['purple']}" stroke-width="1" stroke-opacity="0.24"/>
    <path d="M 4 278 H 124 L 148 302 H 572" fill="none" stroke="{t['purple_soft']}" stroke-width="1.35" stroke-opacity="0.52" class="trace-flow"/>

    <!-- Top Brand Ribbon + Gliding Light Beam -->
    <rect x="4" y="4" width="992" height="4" fill="url(#brandBar)"/>
    <rect x="0" y="4" width="220" height="4" fill="#FFFFFF" fill-opacity="0.65" class="scan"/>
  </g>
  <rect x="4" y="4" width="992" height="396" rx="24" fill="none" stroke="{t['border']}" stroke-width="1.2"/>
  <line x1="28" y1="8.8" x2="972" y2="8.8" stroke="url(#heroSpec)" stroke-width="1"/>

  <!-- Top Badges Row -->
  <g>
    <!-- Glowing Gradient <SB/> Brand Emblem -->
    <rect x="36" y="28" width="66" height="28" rx="9" fill="url(#sbMark)"/>
    <text x="69" y="46.2" text-anchor="middle" font-family="{FONT_MONO}" font-size="12.2" font-weight="800" fill="#FFFFFF">&lt;SB/&gt;</text>

    <rect x="111" y="28" width="268" height="28" rx="14" fill="{t['emerald_bg']}" stroke="{t['emerald_border']}" stroke-width="1"/>
    <circle cx="126" cy="42" r="3.6" fill="{t['emerald']}" class="pulse-dot"/>
    <text x="137" y="46" font-family="{FONT_SANS}" font-size="11.1" font-weight="600" fill="{t['emerald']}">Available for High-Impact Roles &amp; Advisory</text>

    <rect x="388" y="28" width="136" height="28" rx="14" fill="{t['amber_bg']}" stroke="{t['amber_border']}" stroke-width="1"/>
    <text x="456" y="46" text-anchor="middle" font-family="{FONT_MONO}" font-size="10.8" font-weight="700" fill="{t['amber_gold']}">⚡ 3.5x AI Velocity</text>
  </g>

  <!-- Main Editorial Heading -->
  <g>
    <text x="36" y="108" font-family="{FONT_SANS}" font-size="43" font-weight="800" letter-spacing="-1.0" fill="{t['text']}">Shubham Bramhane</text>
    <text x="36" y="142" font-family="{FONT_SANS}" font-size="22" font-weight="800" letter-spacing="-0.3" fill="url(#headlineGrad)">Architecting High-Throughput Systems</text>
    <text x="36" y="168" font-family="{FONT_SANS}" font-size="22" font-weight="800" letter-spacing="-0.3" fill="url(#headlineGrad)">with AI-Augmented Velocity.</text>

    <text x="36" y="198" font-family="{FONT_SANS}" font-size="12.5" font-weight="700" fill="{t['emerald']}">Senior Full-Stack Architect &amp; AI-Augmented Engineer</text>
    <text x="362" y="198" font-family="{FONT_MONO}" font-size="10.6" font-weight="600" fill="{t['text_muted']}">· 5+ Yrs · MBA Finance &amp; IT</text>

    <text x="36" y="227" font-family="{FONT_SANS}" font-size="12.7" fill="{t['text_sub']}">5+ years mastering PHP 8.3 / Laravel 11, high-concurrency MySQL/PostgreSQL</text>
    <text x="36" y="246" font-family="{FONT_SANS}" font-size="12.7" fill="{t['text_sub']}">&amp; Redis caching (+30% throughput), pan-India healthcare portals, Python</text>
    <text x="36" y="265" font-family="{FONT_SANS}" font-size="12.7" fill="{t['text_sub']}">automation pipelines, and agentic AI workflows (Antigravity &amp; Copilot).</text>
  </g>

  <!-- Stack Highlight Pills -->
  {pills_svg}

  <!-- Right Live Glass IDE + Animated Photon Sparkline Window -->
  <g>
    <rect x="590" y="28" width="376" height="346" rx="16" fill="{t['code_bg']}" stroke="{t['border_strong']}" stroke-width="1.2"/>
    <path d="M606 28 H950 A16 16 0 0 1 966 44 V63 H590 V44 A16 16 0 0 1 606 28 Z" fill="{t['code_bar']}"/>
    <line x1="590" y1="63" x2="966" y2="63" stroke="#222842" stroke-width="1"/>
    <circle cx="609" cy="45.5" r="4.6" fill="#FF5F56"/>
    <circle cx="624" cy="45.5" r="4.6" fill="#FFBD2E"/>
    <circle cx="639" cy="45.5" r="4.6" fill="#27C93F"/>
    <rect x="658" y="35.5" width="108" height="20" rx="6" fill="#1D223B" stroke="#424C7A" stroke-width="0.9"/>
    <text x="712" y="49" text-anchor="middle" font-family="{FONT_MONO}" font-size="10" font-weight="600" fill="#F1F5F9">Architecture.ts</text>
    <text x="778" y="49" font-family="{FONT_MONO}" font-size="9.8" fill="#64748B">Live-Telemetry.log</text>

{chr(10).join(code_svg)}
    <rect x="642" y="252" width="6.5" height="12" rx="1.5" fill="{t['purple_soft']}" class="blink"/>

    <!-- Embedded Live Throughput Telemetry Panel -->
    <line x1="590" y1="278" x2="966" y2="278" stroke="#1E243B" stroke-width="1"/>
    <text x="606" y="295" font-family="{FONT_MONO}" font-size="9.1" font-weight="700" letter-spacing="0.9" fill="#64748B">LIVE TELEMETRY · REDIS + SQL PROFILING</text>
    <text x="950" y="295" text-anchor="end" font-family="{FONT_MONO}" font-size="9.5" font-weight="700" fill="{t['emerald']}">+30% THROUGHPUT</text>

    <!-- Sparkline Area Chart + Animated Traveling Light Photon -->
    <path d="{spark_path} L 946 342 L 606 342 Z" fill="url(#sparkArea)"/>
    <path id="heroSpark" d="{spark_path}" fill="none" stroke="{t['emerald']}" stroke-width="2.2" stroke-linecap="round"/>
    <circle r="3.2" fill="#FFFFFF">
      <animateMotion dur="3.6s" repeatCount="indefinite" path="{spark_path}"/>
    </circle>
    <circle cx="946" cy="299" r="4" fill="{t['emerald']}" class="pulse-dot"/>
    <circle cx="946" cy="299" r="8.5" fill="{t['emerald']}" fill-opacity="0.22" class="pulse-dot"/>

    <!-- Status Bar -->
    <line x1="590" y1="347" x2="966" y2="347" stroke="#1E243B" stroke-width="1"/>
    <circle cx="607" cy="360.5" r="3.2" fill="{t['emerald']}" class="pulse-dot"/>
    <text x="617" y="364" font-family="{FONT_MONO}" font-size="9.6" fill="#94A3B8">Production Ready · AI-Assisted</text>
    <text x="950" y="364" text-anchor="end" font-family="{FONT_MONO}" font-size="9.6" font-weight="700" fill="{t['amber_gold']}">99.9% UPTIME</text>
  </g>
</svg>
"""


def build_cta_button(theme_name: str, key: str, label: str, sub: str, style: str, icon: str) -> str:
    t = THEMES[theme_name]
    w, h = 238, 58
    if style == "primary":
        bg_fill = "url(#ctaPrimary)"
        stroke = "#D8B4FE"
        fg = "#FFFFFF"
        sub_fg = "#FDF4FF"
        icon_col = "#FFFFFF"
        defs = """
  <defs>
    <linearGradient id="ctaPrimary" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#7C3AED"/>
      <stop offset="52%" stop-color="#C026D3"/>
      <stop offset="100%" stop-color="#F97316"/>
    </linearGradient>
    <linearGradient id="ctaSpec" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
  </defs>"""
    else:
        acc = t[style]
        bg_fill = "url(#ctaGlass)"
        stroke = t[f"{style}_border"]
        fg = t["text"]
        sub_fg = acc
        icon_col = acc
        defs = f"""
  <defs>
    <linearGradient id="ctaGlass" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{t[f'{style}_bg']}"/>
      <stop offset="100%" stop-color="{t['card_bot']}"/>
    </linearGradient>
    <linearGradient id="ctaSpec" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{acc}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{acc}" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="{acc}" stop-opacity="0"/>
    </linearGradient>
  </defs>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">
  {defs}
  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" rx="14" fill="{bg_fill}" stroke="{stroke}" stroke-width="1.2"/>
  <line x1="18" y1="2.9" x2="{w - 18}" y2="2.9" stroke="url(#ctaSpec)" stroke-width="1.1"/>
  <g transform="translate(14, 15)">
    {icon.format(c=icon_col)}
  </g>
  <text x="48" y="27.5" font-family="{FONT_SANS}" font-size="13.2" font-weight="800" fill="{fg}">{esc(label)}</text>
  <text x="48" y="43.5" font-family="{FONT_MONO}" font-size="9.6" font-weight="600" fill="{sub_fg}">{esc(sub)}</text>
  <text x="{w - 15}" y="34" text-anchor="end" font-family="{FONT_SANS}" font-size="14" font-weight="800" fill="{icon_col}">↗</text>
</svg>
"""


def build_metrics(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 130

    cards_data = [
        (
            "5+ Yrs",
            "Laravel Ecosystem",
            "Enterprise & Microservices",
            t["purple"],
            "m0",
            f'<rect x="164" y="50" width="9" height="16" rx="2.5" fill="{t["purple"]}" fill-opacity="0.28"/>'
            f'<rect x="177" y="42" width="9" height="24" rx="2.5" fill="{t["purple"]}" fill-opacity="0.48"/>'
            f'<rect x="190" y="33" width="9" height="33" rx="2.5" fill="{t["purple"]}" fill-opacity="0.72"/>'
            f'<rect x="203" y="21" width="9" height="45" rx="2.5" fill="{t["purple"]}"/>',
        ),
        (
            "+30%",
            "Query Velocity",
            "Redis & SQL Profiling",
            t["emerald"],
            "m1",
            f'<path d="M 156 60 C 170 57, 178 48, 188 43 C 198 39, 204 29, 214 23 L 214 64 L 156 64 Z" fill="{t["emerald"]}" fill-opacity="0.18"/>'
            f'<path d="M 156 60 C 170 57, 178 48, 188 43 C 198 39, 204 29, 214 23" fill="none" stroke="{t["emerald"]}" stroke-width="2.2" stroke-linecap="round"/>'
            f'<circle cx="214" cy="23" r="3.6" fill="{t["emerald"]}"/>',
        ),
        (
            "3.5x",
            "AI Sprint Velocity",
            "Antigravity & Copilot",
            t["amber"],
            "m2",
            f'<circle cx="192" cy="42" r="20" fill="none" stroke="{t["border_strong"]}" stroke-width="4.5"/>'
            f'<circle cx="192" cy="42" r="20" fill="none" stroke="{t["amber"]}" stroke-width="4.5" stroke-dasharray="104 130" stroke-linecap="round" transform="rotate(-90 192 42)"/>'
            f'<text x="192" y="45.5" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.5" font-weight="800" fill="{t["amber_gold"]}">AI</text>',
        ),
        (
            "10+ hrs",
            "Weekly Automated",
            "Python Data Pipelines",
            t["cyan"],
            "m3",
            f'<line x1="164" y1="43" x2="212" y2="43" stroke="{t["cyan"]}" stroke-width="2" stroke-dasharray="4 3"/>'
            f'<circle cx="164" cy="43" r="5" fill="{t["cyan_bg"]}" stroke="{t["cyan"]}" stroke-width="1.8"/>'
            f'<circle cx="188" cy="43" r="5" fill="{t["cyan_bg"]}" stroke="{t["cyan"]}" stroke-width="1.8"/>'
            f'<circle cx="212" cy="43" r="5.5" fill="{t["cyan"]}"/>',
        ),
    ]

    glow_defs = []
    cards = []
    x = 4
    for big, title, sub, acc, cid, viz in cards_data:
        glow_defs.append(f"""
    <radialGradient id="{cid}Glow" cx="85%" cy="15%" r="65%">
      <stop offset="0%" stop-color="{acc}" stop-opacity="{t['card_glow']}"/>
      <stop offset="100%" stop-color="{acc}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="{cid}Clip"><rect x="0" y="0" width="236" height="118" rx="16"/></clipPath>""")
        cards.append(f"""
  <g transform="translate({x}, 6)">
    <g clip-path="url(#{cid}Clip)">
      <rect x="0" y="0" width="236" height="118" fill="url(#metCard)"/>
      <rect x="0" y="0" width="236" height="118" fill="url(#{cid}Glow)"/>
    </g>
    <rect x="0" y="0" width="236" height="118" rx="16" fill="none" stroke="{t['border']}" stroke-width="1.15"/>
    <line x1="18" y1="0.8" x2="218" y2="0.8" stroke="url(#metSpec)" stroke-width="1"/>
    <rect x="20" y="0" width="48" height="3" rx="1.5" fill="{acc}"/>
    <text x="20" y="46" font-family="{FONT_SANS}" font-size="30" font-weight="800" letter-spacing="-0.6" fill="{t['text']}">{esc(big)}</text>
    <text x="20" y="76" font-family="{FONT_SANS}" font-size="13" font-weight="700" fill="{acc}">{esc(title)}</text>
    <text x="20" y="96" font-family="{FONT_MONO}" font-size="10.3" fill="{t['text_muted']}">{esc(sub)}</text>
    {viz}
  </g>""")
        x += 252

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Engineering Impact KPI Strip with Data Visuals">
  <defs>
    {glass_defs(t, "met")}
    {"".join(glow_defs)}
  </defs>
  {"".join(cards)}
</svg>
"""


def build_architecture_flow(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 280

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Animated Enterprise System Architecture Blueprint">
  <defs>
    {glass_defs(t, "bp")}
    <pattern id="bpGrid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M 24 0 L 0 0 0 24" fill="none" stroke="{t['grid_line']}" stroke-width="0.7" stroke-opacity="0.65"/>
    </pattern>
    <clipPath id="bpClip">
      <rect x="4" y="36" width="992" height="238" rx="18"/>
    </clipPath>
    <radialGradient id="n1Glow" cx="20%" cy="0%" r="85%"><stop offset="0%" stop-color="{t['cyan']}" stop-opacity="{t['card_glow']}"/><stop offset="100%" stop-color="{t['cyan']}" stop-opacity="0"/></radialGradient>
    <radialGradient id="n2Glow" cx="50%" cy="0%" r="85%"><stop offset="0%" stop-color="{t['purple']}" stop-opacity="{t['card_glow']}"/><stop offset="100%" stop-color="{t['purple']}" stop-opacity="0"/></radialGradient>
    <radialGradient id="n3Glow" cx="50%" cy="0%" r="85%"><stop offset="0%" stop-color="{t['emerald']}" stop-opacity="{t['card_glow']}"/><stop offset="100%" stop-color="{t['emerald']}" stop-opacity="0"/></radialGradient>
    <radialGradient id="n4Glow" cx="80%" cy="0%" r="85%"><stop offset="0%" stop-color="{t['amber']}" stop-opacity="{t['card_glow']}"/><stop offset="100%" stop-color="{t['amber']}" stop-opacity="0"/></radialGradient>
    <linearGradient id="flow1" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="{t['cyan']}"/><stop offset="100%" stop-color="{t['purple']}"/></linearGradient>
    <linearGradient id="flow2" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="{t['purple']}"/><stop offset="100%" stop-color="{t['emerald']}"/></linearGradient>
    <linearGradient id="flow3" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="{t['emerald']}"/><stop offset="100%" stop-color="{t['amber']}"/></linearGradient>
    <style>
      @keyframes packetFlow {{ from {{ stroke-dashoffset: 64; }} to {{ stroke-dashoffset: 0; }} }}
      @keyframes softBlink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}
      .flow-line {{ stroke-dasharray: 7 7; animation: packetFlow 1.7s linear infinite; }}
      .live-glow {{ animation: softBlink 2s ease-in-out infinite; }}
    </style>
  </defs>

  {render_section_header("SYSTEM ARCHITECTURE BLUEPRINT", "HOW I ARCHITECT HIGH-THROUGHPUT PRODUCTION PLATFORMS", t, t["cyan"], w)}

  <g clip-path="url(#bpClip)">
    <rect x="4" y="36" width="992" height="238" fill="url(#bpCard)"/>
    <rect x="4" y="36" width="992" height="238" fill="url(#bpGrid)"/>
  </g>
  <rect x="4" y="36" width="992" height="238" rx="18" fill="none" stroke="{t['border']}" stroke-width="1.2"/>
  <line x1="24" y1="36.8" x2="976" y2="36.8" stroke="url(#bpSpec)" stroke-width="1"/>

  <!-- Animated Fiber-Optic Connector Pipes + Gliding Light Orbs -->
  <g>
    <line x1="226" y1="136" x2="274" y2="136" stroke="url(#flow1)" stroke-width="2.4" class="flow-line"/>
    <polygon points="274,136 266,131 266,141" fill="{t['purple']}"/>
    <circle r="3.4" fill="#FFFFFF"><animateMotion dur="1.6s" repeatCount="indefinite" path="M 226 136 L 269 136"/></circle>

    <line x1="496" y1="136" x2="544" y2="136" stroke="url(#flow2)" stroke-width="2.4" class="flow-line"/>
    <polygon points="544,136 536,131 536,141" fill="{t['emerald']}"/>
    <circle r="3.4" fill="#FFFFFF"><animateMotion dur="1.6s" begin="0.5s" repeatCount="indefinite" path="M 496 136 L 539 136"/></circle>

    <line x1="752" y1="136" x2="796" y2="136" stroke="url(#flow3)" stroke-width="2.4" class="flow-line"/>
    <polygon points="796,136 788,131 788,141" fill="{t['amber']}"/>
    <circle r="3.4" fill="#FFFFFF"><animateMotion dur="1.6s" begin="1.0s" repeatCount="indefinite" path="M 752 136 L 791 136"/></circle>
  </g>

  <!-- Node 1: Client & UI Edge -->
  <g transform="translate(24, 58)">
    <rect x="0" y="0" width="202" height="154" rx="14" fill="url(#bpCard)" stroke="{t['cyan_border']}" stroke-width="1.2"/>
    <rect x="0" y="0" width="202" height="154" rx="14" fill="url(#n1Glow)"/>
    <rect x="16" y="0" width="44" height="3" rx="1.5" fill="{t['cyan']}"/>
    <text x="16" y="25" font-family="{FONT_MONO}" font-size="9.4" font-weight="700" fill="{t['cyan']}">01 · CLIENT &amp; UI EDGE</text>
    <text x="16" y="48" font-family="{FONT_SANS}" font-size="14.5" font-weight="700" fill="{t['text']}">Reactive Interfaces</text>
    <text x="16" y="73" font-family="{FONT_MONO}" font-size="10.3" fill="{t['text_sub']}">▸ React.js &amp; Next.js 16</text>
    <text x="16" y="93" font-family="{FONT_MONO}" font-size="10.3" fill="{t['text_sub']}">▸ Vue.js / Vuex · Blade</text>
    <text x="16" y="113" font-family="{FONT_MONO}" font-size="10.3" fill="{t['text_sub']}">▸ TypeScript · Tailwind</text>
    <rect x="16" y="125" width="170" height="19" rx="6" fill="{t['cyan_bg']}" stroke="{t['cyan_border']}" stroke-width="0.7"/>
    <text x="101" y="137.8" text-anchor="middle" font-family="{FONT_MONO}" font-size="9" font-weight="700" fill="{t['cyan']}">SPA · SSR · RESPONSIVE</text>
  </g>

  <!-- Node 2: Core API + AI-Augmented Engine -->
  <g transform="translate(274, 54)">
    <rect x="0" y="0" width="222" height="162" rx="14" fill="url(#bpCard)" stroke="{t['purple_border']}" stroke-width="1.4"/>
    <rect x="0" y="0" width="222" height="162" rx="14" fill="url(#n2Glow)"/>
    <rect x="16" y="0" width="60" height="3" rx="1.5" fill="{t['purple']}"/>
    <text x="16" y="25" font-family="{FONT_MONO}" font-size="9.4" font-weight="700" fill="{t['purple_soft']}">02 · APPLICATION &amp; AI CORE</text>
    <text x="16" y="48" font-family="{FONT_SANS}" font-size="14.5" font-weight="700" fill="{t['text']}">Laravel 11 &amp; Python</text>
    <text x="16" y="72" font-family="{FONT_MONO}" font-size="10.3" fill="{t['text_sub']}">▸ PHP 8.3 · REST / Swagger</text>
    <text x="16" y="91" font-family="{FONT_MONO}" font-size="10.3" fill="{t['text_sub']}">▸ Django · Flask · Fast ETL</text>
    <rect x="14" y="107" width="194" height="43" rx="9" fill="{t['amber_bg']}" stroke="{t['amber_border']}" stroke-width="1"/>
    <text x="24" y="124" font-family="{FONT_MONO}" font-size="9.3" font-weight="700" fill="{t['amber_gold']}">⚡ 3.5x AI VELOCITY ENGINE</text>
    <text x="24" y="140" font-family="{FONT_MONO}" font-size="9.1" fill="{t['text_sub']}">Antigravity · Copilot · Claude</text>
  </g>

  <!-- Node 3: Data, Cache & Cloud -->
  <g transform="translate(544, 58)">
    <rect x="0" y="0" width="208" height="154" rx="14" fill="url(#bpCard)" stroke="{t['emerald_border']}" stroke-width="1.2"/>
    <rect x="0" y="0" width="208" height="154" rx="14" fill="url(#n3Glow)"/>
    <rect x="16" y="0" width="44" height="3" rx="1.5" fill="{t['emerald']}"/>
    <text x="16" y="25" font-family="{FONT_MONO}" font-size="9.4" font-weight="700" fill="{t['emerald']}">03 · DATA &amp; CLOUD LAYER</text>
    <text x="16" y="48" font-family="{FONT_SANS}" font-size="14.5" font-weight="700" fill="{t['text']}">Cache &amp; Persistence</text>
    <text x="16" y="73" font-family="{FONT_MONO}" font-size="10.3" fill="{t['text_sub']}">▸ Redis Cache (+30% Speed)</text>
    <text x="16" y="93" font-family="{FONT_MONO}" font-size="10.3" fill="{t['text_sub']}">▸ MySQL · PostgreSQL</text>
    <text x="16" y="113" font-family="{FONT_MONO}" font-size="10.3" fill="{t['text_sub']}">▸ AWS RDS &amp; DynamoDB</text>
    <rect x="16" y="125" width="176" height="19" rx="6" fill="{t['emerald_bg']}" stroke="{t['emerald_border']}" stroke-width="0.7"/>
    <text x="104" y="137.8" text-anchor="middle" font-family="{FONT_MONO}" font-size="9" font-weight="700" fill="{t['emerald']}">INDEXED · HIGH-CONCURRENCY</text>
  </g>

  <!-- Node 4: Production Scale -->
  <g transform="translate(796, 58)">
    <rect x="0" y="0" width="180" height="154" rx="14" fill="url(#bpCard)" stroke="{t['amber_border']}" stroke-width="1.2"/>
    <rect x="0" y="0" width="180" height="154" rx="14" fill="url(#n4Glow)"/>
    <rect x="16" y="0" width="44" height="3" rx="1.5" fill="{t['amber']}"/>
    <text x="16" y="25" font-family="{FONT_MONO}" font-size="9.4" font-weight="700" fill="{t['amber_gold']}">04 · PRODUCTION</text>
    <text x="16" y="48" font-family="{FONT_SANS}" font-size="14.5" font-weight="700" fill="{t['text']}">Real-World Impact</text>
    <text x="16" y="73" font-family="{FONT_MONO}" font-size="10.1" fill="{t['text_sub']}">✦ Pan-India Diagnostics</text>
    <text x="16" y="93" font-family="{FONT_MONO}" font-size="10.1" fill="{t['text_sub']}">✦ Big Basket Scale TMS</text>
    <text x="16" y="113" font-family="{FONT_MONO}" font-size="10.1" fill="{t['text_sub']}">✦ 10+ hrs/wk Automated</text>
    <rect x="16" y="125" width="148" height="19" rx="6" fill="{t['amber_bg']}" stroke="{t['amber_border']}" stroke-width="0.7"/>
    <text x="90" y="137.8" text-anchor="middle" font-family="{FONT_MONO}" font-size="9" font-weight="700" fill="{t['amber_gold']}">ENTERPRISE DELIVERY</text>
  </g>

  <!-- Bottom Architecture Telemetry Strip -->
  <line x1="24" y1="232" x2="976" y2="232" stroke="{t['rule']}" stroke-width="1"/>
  <circle cx="34" cy="253" r="3.4" fill="{t['emerald']}" class="live-glow"/>
  <text x="45" y="256.5" font-family="{FONT_MONO}" font-size="10" fill="{t['text_sub']}">CSRF &amp; SQLi Defense  ·  Swagger OpenAPI Specs  ·  Razorpay / Stripe Gateways  ·  GitHub CI/CD  ·  MBA Finance &amp; IT Governance</text>
</svg>
"""


def build_tech_stack_radar(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 428

    cx, cy = 175, 224
    max_r = 80
    axes = [
        ("Laravel & Backend", 0.96, -90, 0, -13, "middle", t["purple_soft"]),
        ("AI Velocity", 0.94, -18, 10, -2, "start", t["amber_gold"]),
        ("DB & Redis", 0.93, 54, 8, 14, "start", t["emerald"]),
        ("Python & AWS", 0.88, 126, -8, 14, "end", t["cyan"]),
        ("Frontend UI", 0.90, 198, -10, -2, "end", t["fuchsia"]),
    ]

    rings = []
    for frac in (0.33, 0.66, 1.0):
        pts = []
        for _, _, deg, _, _, _, _ in axes:
            rad = math.radians(deg)
            pts.append(f"{cx + max_r * frac * math.cos(rad):.1f},{cy + max_r * frac * math.sin(rad):.1f}")
        rings.append(f'<polygon points="{" ".join(pts)}" fill="none" stroke="{t["radar_ring"]}" stroke-width="1"/>')

    spokes = []
    poly_pts = []
    inner_pts = []
    vertex_dots = []
    axis_labels = []
    for label, val, deg, dx, dy, anchor, col in axes:
        rad = math.radians(deg)
        ox = cx + max_r * math.cos(rad)
        oy = cy + max_r * math.sin(rad)
        vx = cx + max_r * val * math.cos(rad)
        vy = cy + max_r * val * math.sin(rad)
        ix = cx + max_r * (val * 0.62) * math.cos(rad)
        iy = cy + max_r * (val * 0.62) * math.sin(rad)
        spokes.append(f'<line x1="{cx}" y1="{cy}" x2="{ox:.1f}" y2="{oy:.1f}" stroke="{t["radar_ring"]}" stroke-width="0.9" stroke-dasharray="3 3"/>')
        poly_pts.append(f"{vx:.1f},{vy:.1f}")
        inner_pts.append(f"{ix:.1f},{iy:.1f}")
        vertex_dots.append(f'<circle cx="{vx:.1f}" cy="{vy:.1f}" r="6.8" fill="{col}" fill-opacity="0.22"/>')
        vertex_dots.append(f'<circle cx="{vx:.1f}" cy="{vy:.1f}" r="3.8" fill="{t["card"]}" stroke="{col}" stroke-width="2.2"/>')
        axis_labels.append(
            f'<text x="{ox + dx:.1f}" y="{oy + dy:.1f}" text-anchor="{anchor}" font-family="{FONT_MONO}" font-size="9.3" font-weight="700" fill="{t["text_sub"]}">{esc(label)}</text>'
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
    {glass_defs(t, "ts")}
    <radialGradient id="radAmb" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="{t['purple']}" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="{t['purple']}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="radarFill" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{t['purple']}" stop-opacity="0.45"/>
      <stop offset="50%" stop-color="{t['cyan']}" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="{t['amber']}" stop-opacity="0.38"/>
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
    {glass_card(4, 38, 342, 382, 16, t, accent=t["purple"], prefix="ts")}
    <circle cx="{cx}" cy="{cy}" r="115" fill="url(#radAmb)"/>
    <text x="24" y="66" font-family="{FONT_MONO}" font-size="11" font-weight="700" letter-spacing="1.1" fill="{t['purple_soft']}">ENGINEERING RADAR</text>
    <text x="24" y="84" font-family="{FONT_SANS}" font-size="11.5" fill="{t['text_muted']}">Multi-domain production capability map</text>

    {"".join(rings)}
    {"".join(spokes)}
    <polygon points="{" ".join(poly_pts)}" fill="url(#radarFill)" stroke="url(#radarStroke)" stroke-width="2.3" stroke-linejoin="round"/>
    <polygon points="{" ".join(inner_pts)}" fill="none" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="1" stroke-dasharray="3 3"/>
    {"".join(vertex_dots)}
    {"".join(axis_labels)}

    <!-- Radar Legend Footer -->
    <line x1="24" y1="354" x2="326" y2="354" stroke="{t['rule']}" stroke-width="1"/>
    <text x="24" y="377" font-family="{FONT_MONO}" font-size="9.6" font-weight="700" fill="{t['emerald']}">● CORE STRENGTH:</text>
    <text x="148" y="377" font-family="{FONT_MONO}" font-size="9.6" fill="{t['text_sub']}">Laravel · Redis · AI</text>
    <text x="24" y="397" font-family="{FONT_MONO}" font-size="9.6" font-weight="700" fill="{t['amber_gold']}">● STRATEGIC EDGE:</text>
    <text x="148" y="397" font-family="{FONT_MONO}" font-size="9.6" fill="{t['text_sub']}">Tech + MBA Finance ROI</text>
  </g>

  <!-- Right Top: Backend & Python Data Science -->
  <g>
    {glass_card(360, 38, 636, 106, 15, t, accent=t["purple"], prefix="ts")}
    <text x="378" y="65" font-family="{FONT_MONO}" font-size="10.8" font-weight="700" letter-spacing="1.1" fill="{t['purple_soft']}">BACKEND ARCHITECTURE &amp; PYTHON DATA SCIENCE</text>
    <text x="976" y="65" text-anchor="end" font-family="{FONT_MONO}" font-size="9.6" fill="{t['text_muted']}">13 TECHNOLOGIES</text>
    {b_svg}
  </g>

  <!-- Right Middle: AI Agentic Engineering -->
  <g>
    {glass_card(360, 154, 636, 96, 15, t, accent=t["amber"], border=t["amber_border"], prefix="ts")}
    <text x="378" y="180" font-family="{FONT_MONO}" font-size="10.8" font-weight="700" letter-spacing="1.1" fill="{t['amber_gold']}">AI AGENTIC ENGINEERING &amp; AUTOMATION</text>
    <rect x="870" y="164" width="108" height="20" rx="10" fill="{t['amber_bg']}" stroke="{t['amber_border']}" stroke-width="0.9"/>
    <text x="924" y="177.2" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.2" font-weight="700" fill="{t['amber_gold']}">⚡ SUPERCHARGED</text>
    {a_svg}
  </g>

  <!-- Right Bottom-Left: Frontend & UI -->
  <g>
    {glass_card(360, 260, 310, 160, 15, t, accent=t["cyan"], prefix="ts")}
    <text x="378" y="286" font-family="{FONT_MONO}" font-size="10.6" font-weight="700" letter-spacing="1.1" fill="{t['cyan']}">FRONTEND &amp; UI SYSTEMS</text>
    {f_svg}
  </g>

  <!-- Right Bottom-Right: Databases, Cloud & DevOps -->
  <g>
    {glass_card(682, 260, 314, 160, 15, t, accent=t["emerald"], prefix="ts")}
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
    w, h = 488, 162
    acc = t[accent_key]
    bg = t[f"{accent_key}_bg"]
    brd = t[f"{accent_key}_border"]

    tag_pills = []
    tx = 20
    for tg in tags:
        svg_p, tw = render_pill(tx, 122, tg, t["elevated"], t["border"], t["text_sub"], height=23, font_size=10.2, mono=True)
        tag_pills.append(svg_p)
        tx += tw + 6

    badge_w = measure_pill(badge, char_w=6.7, pad_x=22, min_w=92)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
  <defs>
    {glass_defs(t, "pr")}
    <radialGradient id="prGlow" cx="92%" cy="18%" r="55%">
      <stop offset="0%" stop-color="{acc}" stop-opacity="{t['card_glow']}"/>
      <stop offset="100%" stop-color="{acc}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="prClip"><rect x="2" y="2" width="{w - 4}" height="{h - 4}" rx="16"/></clipPath>
    <style>
      @keyframes livePulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}
      .lp {{ animation: livePulse 2.2s ease-in-out infinite; }}
    </style>
  </defs>

  <g clip-path="url(#prClip)">
    <rect x="2" y="2" width="{w - 4}" height="{h - 4}" fill="url(#prCard)"/>
    <rect x="2" y="2" width="{w - 4}" height="{h - 4}" fill="url(#prGlow)"/>
  </g>
  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" rx="16" fill="none" stroke="{t['border']}" stroke-width="1.15"/>
  <line x1="20" y1="2.8" x2="{w - 20}" y2="2.8" stroke="url(#prSpec)" stroke-width="1"/>
  <rect x="20" y="2" width="58" height="3" rx="1.5" fill="{acc}"/>

  <!-- Mini Architectural Visual Preview Thumbnail -->
  <g transform="translate(382, 16)">
    <rect x="0" y="0" width="88" height="54" rx="10" fill="{bg}" stroke="{brd}" stroke-width="1"/>
    {thumb_svg.format(c=acc)}
  </g>

  <rect x="20" y="16" width="{badge_w}" height="22" rx="11" fill="{bg}" stroke="{brd}" stroke-width="0.9"/>
  <text x="{20 + badge_w / 2:.1f}" y="30.2" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.5" font-weight="700" fill="{acc}">{esc(badge)}</text>
  <text x="{20 + badge_w + 10}" y="30.2" font-family="{FONT_MONO}" font-size="9.8" fill="{t['text_muted']}">{esc(period)} · {esc(category)}</text>

  <text x="20" y="65" font-family="{FONT_SANS}" font-size="16" font-weight="800" fill="{t['text']}">{esc(title)}</text>
  <text x="20" y="87" font-family="{FONT_SANS}" font-size="11.8" fill="{t['text_sub']}">{esc(desc1)}</text>
  <text x="20" y="104" font-family="{FONT_SANS}" font-size="11.8" fill="{t['text_sub']}">{esc(desc2)}</text>

  {"".join(tag_pills)}

  <circle cx="422" cy="133.5" r="3" fill="{acc}" class="lp"/>
  <text x="430" y="137" font-family="{FONT_MONO}" font-size="9.6" font-weight="700" fill="{acc}">LIVE ↗</text>
</svg>
"""


def build_telemetry_ethos(theme_name: str) -> str:
    """Signature Open-Source Language Distribution + Sacred Geometry Engineering Ethos Strip."""
    t = THEMES[theme_name]
    w, h = 1000, 198

    # Stacked bar widths totaling 516px (x=26..542)
    segments = [
        ("PHP / Laravel", 196, t["purple"]),
        ("Python & ML", 124, t["cyan"]),
        ("TS / React / Next", 104, t["amber"]),
        ("Vue / Blade / JS", 62, t["emerald"]),
        ("SQL / Redis", 30, t["rose"]),
    ]
    bar_rects = []
    legend_items = []
    bx = 26
    lx = 26
    for label, seg_w, col in segments:
        bar_rects.append(f'<rect x="{bx}" y="102" width="{seg_w - 3}" height="10" rx="5" fill="{col}"/>')
        bx += seg_w
        legend_items.append(f'<circle cx="{lx + 4}" cy="129" r="3.4" fill="{col}"/>')
        legend_items.append(f'<text x="{lx + 11}" y="132.4" font-family="{FONT_MONO}" font-size="9.1" fill="{t["text_sub"]}">{esc(label)}</text>')
        lx += int(len(label) * 5.45 + 22)

    repo_chips = [
        ("hotel-pos-laravel", t["purple_bg"], t["purple_border"], t["purple_soft"], t["purple"], 136),
        ("my-portfolio", t["cyan_bg"], t["cyan_border"], t["cyan"], t["cyan"], 108),
        ("Admin-Dashboard", t["emerald_bg"], t["emerald_border"], t["emerald"], t["emerald"], 126),
        ("ML-Recommenders", t["amber_bg"], t["amber_border"], t["amber_gold"], t["amber"], 128),
    ]
    chip_parts = []
    cx = 26
    for label, bg, brd, fg, dot, cw in repo_chips:
        svg_p, _ = render_pill(cx, 152, label, bg, brd, fg, dot_color=dot, height=24, font_size=9.1, mono=True, width=cw)
        chip_parts.append(svg_p)
        cx += cw + 6
    chips_svg = "\n".join(chip_parts)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Open Source Pulse and Engineering Philosophy">
  <defs>
    {glass_defs(t, "eth")}
    <radialGradient id="goldAura" cx="88%" cy="50%" r="55%">
      <stop offset="0%" stop-color="{t['amber_gold']}" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="{t['amber_gold']}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="ethRClip"><rect x="582" y="38" width="414" height="154" rx="16"/></clipPath>
  </defs>

  {render_section_header("OPEN-SOURCE PULSE & ENGINEERING ETHOS", "26 REPOSITORIES · 504+ CONTRIBUTIONS", t, t["amber_gold"], w)}

  <!-- Left Card: Open-Source Language Spectrum & Flagship Repos -->
  <g>
    {glass_card(4, 38, 564, 154, 16, t, accent=t["purple"], prefix="eth")}
    <text x="26" y="67" font-family="{FONT_MONO}" font-size="10.8" font-weight="700" letter-spacing="1.1" fill="{t['purple_soft']}">GITHUB ECOSYSTEM &amp; STACK SPECTRUM</text>
    <rect x="408" y="51" width="138" height="22" rx="11" fill="{t['emerald_bg']}" stroke="{t['emerald_border']}" stroke-width="0.9"/>
    <text x="477" y="65.2" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.5" font-weight="700" fill="{t['emerald']}">26 REPOS · 504+ COMMITS</text>

    <text x="26" y="88" font-family="{FONT_SANS}" font-size="11.5" fill="{t['text_muted']}">Production &amp; open-source distribution across backend, data science &amp; modern UI</text>
    {"".join(bar_rects)}
    {"".join(legend_items)}
    {chips_svg}
  </g>

  <!-- Right Card: Signature Motto & Golden Sacred-Geometry Art (Matching GitHub Avatar) -->
  <g>
    <g clip-path="url(#ethRClip)">
      <rect x="582" y="38" width="414" height="154" fill="url(#ethCard)"/>
      <rect x="582" y="38" width="414" height="154" fill="url(#goldAura)"/>
      <g>{mandala_geometry(936, 115, 68, t['mandala'], t['mandala_op'])}</g>
    </g>
    <rect x="582" y="38" width="414" height="154" rx="16" fill="none" stroke="{t['amber_border']}" stroke-width="1.2"/>
    <line x1="600" y1="38.8" x2="978" y2="38.8" stroke="url(#ethSpec)" stroke-width="1"/>
    <rect x="602" y="38" width="58" height="3" rx="1.5" fill="{t['amber_gold']}"/>

    <text x="604" y="67" font-family="{FONT_MONO}" font-size="10.4" font-weight="700" letter-spacing="1.2" fill="{t['amber_gold']}">ENGINEERING PHILOSOPHY</text>
    <text x="604" y="102" font-family="{FONT_SANS}" font-size="19.5" font-weight="800" fill="{t['text']}">धैर्यं सर्वत्र साधनम्।</text>
    <text x="604" y="124" font-family="{FONT_MONO}" font-size="11" font-weight="600" fill="{t['amber_gold']}">&quot;Patience is the solution to everything.&quot;</text>
    <text x="604" y="150" font-family="{FONT_SANS}" font-size="11.4" fill="{t['text_sub']}">Architecting calm, resilient software where clean</text>
    <text x="604" y="167" font-family="{FONT_SANS}" font-size="11.4" fill="{t['text_sub']}">engineering meets measurable business ROI.</text>
  </g>
</svg>
"""


def build_journey(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 396

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
    <circle cx="34" cy="{ey + 12}" r="11" fill="{color}" fill-opacity="0.14"/>
    <circle cx="34" cy="{ey + 12}" r="6.5" fill="{t['card']}" stroke="{color}" stroke-width="2.2"/>
    <circle cx="34" cy="{ey + 12}" r="2.8" fill="{color}"{pulse_cls}/>
    <text x="54" y="{ey + 8}" font-family="{FONT_MONO}" font-size="10" font-weight="700" fill="{color}">{esc(period)}</text>
    <text x="54" y="{ey + 27}" font-family="{FONT_SANS}" font-size="14.5" font-weight="700" fill="{t['text']}">{esc(role)} <tspan font-size="12" font-weight="600" fill="{t['text_sub']}">— {esc(company)}</tspan></text>
    <text x="54" y="{ey + 47}" font-family="{FONT_SANS}" font-size="11.4" fill="{t['text_sub']}">⚡ {esc(b1)}</text>
    <text x="54" y="{ey + 65}" font-family="{FONT_SANS}" font-size="11.4" fill="{t['text_muted']}">▸ {esc(b2)}</text>""")
        ey += 97

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Career Experience and Academic Credentials">
  <defs>
    {glass_defs(t, "jr")}
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
    {glass_card(4, 38, 564, 352, 16, t, accent=t["purple"], prefix="jr")}
    <text x="24" y="66" font-family="{FONT_MONO}" font-size="11.2" font-weight="700" letter-spacing="1.2" fill="{t['purple_soft']}">PROFESSIONAL EXPERIENCE</text>
    <line x1="34" y1="98" x2="34" y2="294" stroke="url(#spineGrad)" stroke-width="2.2" stroke-dasharray="4 4"/>
    {"".join(exp_svgs)}
  </g>

  <!-- Right Top Panel: Academic Qualifications -->
  <g>
    {glass_card(584, 38, 412, 240, 16, t, accent=t["emerald"], prefix="jr")}
    <text x="604" y="66" font-family="{FONT_MONO}" font-size="11.2" font-weight="700" letter-spacing="1.2" fill="{t['emerald']}">ACADEMIC QUALIFICATIONS</text>

    <rect x="604" y="82" width="372" height="80" rx="12" fill="{t['elevated']}" stroke="{t['emerald_border']}" stroke-width="1"/>
    <circle cx="622" cy="100" r="3.5" fill="{t['emerald']}" class="live-dot"/>
    <text x="632" y="103.5" font-family="{FONT_MONO}" font-size="9.8" font-weight="700" fill="{t['emerald']}">PURSUING · 2024 – PRESENT</text>
    <text x="618" y="125" font-family="{FONT_SANS}" font-size="14" font-weight="700" fill="{t['text']}">MBA in Finance &amp; IT</text>
    <text x="618" y="145" font-family="{FONT_SANS}" font-size="11.6" fill="{t['text_sub']}">Gondwana University · Business ROI &amp; IT Governance</text>

    <rect x="604" y="174" width="372" height="88" rx="12" fill="{t['elevated']}" stroke="{t['cyan_border']}" stroke-width="1"/>
    <text x="618" y="193" font-family="{FONT_MONO}" font-size="9.8" font-weight="700" fill="{t['cyan']}">COMPLETED OCT 2020 · 74.60% DISTINCTION</text>
    <text x="618" y="215" font-family="{FONT_SANS}" font-size="14" font-weight="700" fill="{t['text']}">B.E. in Computer Science</text>
    <text x="618" y="234" font-family="{FONT_SANS}" font-size="11.6" fill="{t['text_sub']}">Gondwana University</text>
    <text x="618" y="250" font-family="{FONT_MONO}" font-size="9.8" fill="{t['text_muted']}">Data Analysis · ML · Deep Learning · Web Dev</text>
  </g>

  <!-- Right Bottom Panel: Base & Languages -->
  <g>
    {glass_card(584, 292, 412, 98, 16, t, accent=t["amber"], prefix="jr")}
    <text x="604" y="319" font-family="{FONT_MONO}" font-size="10.4" font-weight="700" letter-spacing="1.2" fill="{t['amber_gold']}">BASE &amp; COLLABORATION</text>
    <text x="604" y="344" font-family="{FONT_SANS}" font-size="11.8" font-weight="600" fill="{t['text']}">📍 Chandrapur, Maharashtra, India (IST · UTC+5:30)</text>
    <text x="604" y="368" font-family="{FONT_MONO}" font-size="10.6" fill="{t['text_sub']}">🌐 English · Hindi · Marathi  |  Remote &amp; Hybrid Ready</text>
  </g>
</svg>
"""


def build_connect_header(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 90
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Initiate Contact and Connect">
  <defs>
    {glass_defs(t, "cn")}
    <linearGradient id="connectGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['purple']}"/>
      <stop offset="50%" stop-color="{t['amber']}"/>
      <stop offset="100%" stop-color="{t['emerald']}"/>
    </linearGradient>
  </defs>
  {render_section_header("INITIATE CONTACT & CONNECT", "OPEN FOR ROLES, ARCHITECTURE & ADVISORY", t, t["amber"], w)}
  <rect x="4" y="35" width="992" height="49" rx="14" fill="url(#cnCard)" stroke="{t['border']}" stroke-width="1.2"/>
  <rect x="4" y="35" width="5" height="49" rx="2.5" fill="url(#connectGrad)"/>
  <line x1="20" y1="35.8" x2="980" y2="35.8" stroke="url(#cnSpec)" stroke-width="1"/>
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
    w, h = 316, 84
    acc = t[accent_key]
    bg = t[f"{accent_key}_bg"]
    brd = t[f"{accent_key}_border"]
    stroke_col = brd if featured else t["border"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}: {esc(subtitle)}">
  <defs>
    {glass_defs(t, "cc")}
    <radialGradient id="ccGlow" cx="12%" cy="50%" r="55%">
      <stop offset="0%" stop-color="{acc}" stop-opacity="{t['card_glow']}"/>
      <stop offset="100%" stop-color="{acc}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="ccClip"><rect x="2" y="2" width="{w - 4}" height="{h - 4}" rx="14"/></clipPath>
  </defs>
  <g clip-path="url(#ccClip)">
    <rect x="2" y="2" width="{w - 4}" height="{h - 4}" fill="url(#ccCard)"/>
    <rect x="2" y="2" width="{w - 4}" height="{h - 4}" fill="url(#ccGlow)"/>
  </g>
  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" rx="14" fill="none" stroke="{stroke_col}" stroke-width="1.2"/>
  <line x1="16" y1="2.8" x2="{w - 16}" y2="2.8" stroke="url(#ccSpec)" stroke-width="1"/>
  <rect x="16" y="2" width="46" height="3" rx="1.5" fill="{acc}"/>
  <g transform="translate(16, 21)">
    <rect x="0" y="0" width="40" height="40" rx="10" fill="{bg}" stroke="{brd}" stroke-width="1"/>
    {icon_svg.format(c=acc)}
  </g>
  <text x="68" y="39" font-family="{FONT_SANS}" font-size="14.5" font-weight="700" fill="{t['text']}">{esc(title)}</text>
  <text x="{w - 18}" y="39" text-anchor="end" font-family="{FONT_SANS}" font-size="14" font-weight="700" fill="{acc}">↗</text>
  <text x="68" y="58" font-family="{FONT_MONO}" font-size="{9.7 if len(subtitle) > 28 else 10.6}" fill="{t['text_sub']}">{esc(subtitle)}</text>
</svg>
"""


def build_footer(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 76
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Shubham Bramhane Footer">
  <defs>
    {glass_defs(t, "ft")}
    <clipPath id="footClip">
      <rect x="4" y="4" width="992" height="68" rx="16"/>
    </clipPath>
    <linearGradient id="footWave1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['purple']}" stop-opacity="0.24"/>
      <stop offset="50%" stop-color="{t['amber']}" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="{t['emerald']}" stop-opacity="0.24"/>
    </linearGradient>
    <linearGradient id="footWave2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['cyan']}" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="{t['fuchsia']}" stop-opacity="0.15"/>
    </linearGradient>
    <linearGradient id="footLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['purple']}"/>
      <stop offset="50%" stop-color="{t['amber']}"/>
      <stop offset="100%" stop-color="{t['emerald']}"/>
    </linearGradient>
    <style>
      @keyframes footShimmer {{ 0% {{ transform: translateX(-220px); opacity: 0; }} 25% {{ opacity: 0.75; }} 75% {{ opacity: 0.75; }} 100% {{ transform: translateX(1020px); opacity: 0; }} }}
      .shimmer {{ animation: footShimmer 6s ease-in-out infinite; }}
    </style>
  </defs>
  <g clip-path="url(#footClip)">
    <rect x="4" y="4" width="992" height="68" fill="url(#ftCard)"/>
    <path d="M0 52 Q250 20 500 46 T1000 34 L1000 76 L0 76 Z" fill="url(#footWave1)"/>
    <path d="M0 40 Q280 64 560 32 T1000 50 L1000 76 L0 76 Z" fill="url(#footWave2)"/>
    <rect x="4" y="69" width="992" height="3" fill="url(#footLine)"/>
    <rect x="0" y="69" width="180" height="3" fill="#FFFFFF" class="shimmer"/>
  </g>
  <rect x="4" y="4" width="992" height="68" rx="16" fill="none" stroke="{t['border']}" stroke-width="1.2"/>
  <line x1="22" y1="4.8" x2="978" y2="4.8" stroke="url(#ftSpec)" stroke-width="1"/>
  <text x="500" y="43" text-anchor="middle" font-family="{FONT_MONO}" font-size="11.2" font-weight="700" letter-spacing="0.9" fill="{t['text_sub']}">&lt;SB/&gt;  SHUBHAM BRAMHANE  ·  ARCHITECTING HIGH-THROUGHPUT SYSTEMS WITH AI VELOCITY</text>
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
        '<circle cx="78" cy="20" r="3.2" fill="{c}"/>',
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
        '<rect x="18" y="25" width="22" height="5" rx="2" fill="{c}" fill-opacity="0.75"/>'
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
            f"telemetry-{theme}.svg": build_telemetry_ethos(theme),
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
