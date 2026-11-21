#!/usr/bin/env python3
"""
Deterministic SVG visual asset generator (v7.0 — GTA VI Vice Sunset Edition)
for Shubham Bramhane's GitHub Profile README.
Deep Vice twilight glass, flamingo pink, Miami sunset coral-gold & Ocean Drive turquoise.
Generates 48 XML-validated Dark & Light Bento SVGs into ./assets/.
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
        "card_top": "#161024",
        "card_bot": "#0B0814",
        "card": "#110C1D",
        "card_alt": "#161026",
        "elevated": "#1D1530",
        "code_bg": "#080610",
        "code_bar": "#130E21",
        "border": "#2B2042",
        "border_strong": "#3F2F61",
        "specular": "#FFD6EB",
        "specular_op": "0.22",
        "dot_grid": "#332550",
        "dot_opacity": "0.52",
        "grid_line": "#221838",
        "text": "#FFF8FC",
        "text_sub": "#C4B5D4",
        "text_muted": "#837399",
        "rule": "#271C3D",
        # Signature GTA VI Vice Sunset Palette: Flamingo Pink, Ocean Drive Aqua, Sunset Coral-Gold, Palm Mint, Neon Lavender
        "pink": "#FF4D94",
        "pink_bright": "#FF80B5",
        "pink_bg": "#2E1025",
        "pink_border": "#6E2354",
        "aqua": "#00E5FF",
        "aqua_bright": "#6EF2FF",
        "aqua_bg": "#092533",
        "aqua_border": "#155A75",
        "coral": "#FF9248",
        "coral_gold": "#FFC457",
        "coral_bg": "#2E1910",
        "coral_border": "#6E3B21",
        "mint": "#2CE6B8",
        "mint_bg": "#0B2926",
        "mint_border": "#175C54",
        "palm": "#D8B4FE",
        "palm_bg": "#21143B",
        "palm_border": "#4C2E82",
        "glow_opacity": "0.28",
        "card_glow": "0.17",
        "radar_ring": "#2F224A",
        "ornament": "#FF9248",
        "ornament_op": "0.20",
    },
    "light": {
        "canvas": "#FFFFFF",
        "card_top": "#FFFFFF",
        "card_bot": "#FFF6FA",
        "card": "#FFFFFF",
        "card_alt": "#FFF8FB",
        "elevated": "#F9EFF5",
        "code_bg": "#120C20",
        "code_bar": "#1C1330",
        "border": "#EADAE5",
        "border_strong": "#DAC1D4",
        "specular": "#FFFFFF",
        "specular_op": "0.95",
        "dot_grid": "#DEC9D8",
        "dot_opacity": "0.65",
        "grid_line": "#F0E2EC",
        "text": "#180E29",
        "text_sub": "#53426B",
        "text_muted": "#7C6B94",
        "rule": "#ECDEE8",
        "pink": "#DB2777",
        "pink_bright": "#BE185D",
        "pink_bg": "#FCE7F3",
        "pink_border": "#F9A8D4",
        "aqua": "#0891B2",
        "aqua_bright": "#0E7490",
        "aqua_bg": "#ECFEFF",
        "aqua_border": "#A5F3FC",
        "coral": "#EA580C",
        "coral_gold": "#D97706",
        "coral_bg": "#FFF7ED",
        "coral_border": "#FED7AA",
        "mint": "#0D9488",
        "mint_bg": "#CCFBF1",
        "mint_border": "#99F6E4",
        "palm": "#7C3AED",
        "palm_bg": "#F3E8FF",
        "palm_border": "#DDD6FE",
        "glow_opacity": "0.14",
        "card_glow": "0.09",
        "radar_ring": "#E2CFE0",
        "ornament": "#EA580C",
        "ornament_op": "0.20",
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
    </linearGradient>
    <linearGradient id="{prefix}ViceBar" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['pink']}"/>
      <stop offset="50%" stop-color="{t['coral_gold']}"/>
      <stop offset="100%" stop-color="{t['aqua']}"/>
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
        parts.append(f'<rect x="{x + 18}" y="{y}" width="{accent_w}" height="2.8" rx="1.4" fill="{accent}"/>')
    return "\n  ".join(parts)


def vice_sun_ornament(cx: float, cy: float, r: float, color_top: str, color_bot: str, slice_color: str, opacity: str) -> str:
    """Iconic Vice City retro-modern striped sunset disc + radiating horizon lines."""
    elems = [
        f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="{color_top}" fill-opacity="{opacity}"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r * 1.15:.1f}" fill="none" stroke="{color_bot}" stroke-width="0.9" stroke-dasharray="4 4" stroke-opacity="{opacity}"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r * 0.72:.1f}" fill="none" stroke="{color_top}" stroke-width="0.9" stroke-opacity="{opacity}"/>',
    ]
    # Classic Vice Sunset horizontal slice lines across lower half of sun
    for idx, frac in enumerate((0.12, 0.30, 0.48, 0.66, 0.82)):
        yy = cy + r * frac
        half = math.sqrt(max(0.0, r * r - (r * frac) ** 2)) + 4
        sw = 2.0 + idx * 0.9
        elems.append(f'<line x1="{cx - half:.1f}" y1="{yy:.1f}" x2="{cx + half:.1f}" y2="{yy:.1f}" stroke="{slice_color}" stroke-width="{sw:.1f}" stroke-opacity="0.85"/>')
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
        parts.append(f'<circle cx="{x + 11.5}" cy="{y + height / 2:.1f}" r="2.9" fill="{dot_color}"/>')
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
        sub_svg = f'<text x="{right_end}" y="18.5" text-anchor="end" font-family="{FONT_MONO}" font-size="10.0" fill="{t["text_muted"]}">{esc(subtitle)}</text>'
        rule_end = right_end - int(len(subtitle) * 6.3 + 14)
    else:
        rule_end = right_end
    return f"""
  <g>
    <rect x="6" y="9" width="9" height="9" rx="2.8" fill="{accent}"/>
    <circle cx="10.5" cy="13.5" r="1.8" fill="#FFFFFF" fill-opacity="0.8"/>
    <text x="23" y="18.5" font-family="{FONT_MONO}" font-size="11.4" font-weight="700" letter-spacing="1.9" fill="{t['text_sub']}">{esc(title)}</text>
    <line x1="{rule_x}" y1="13.8" x2="{max(rule_x + 20, rule_end)}" y2="13.8" stroke="{t['rule']}" stroke-width="1"/>
    {sub_svg}
  </g>"""


def build_cta_button(theme_name: str, key: str, label: str, sub: str, style: str, icon: str) -> str:
    t = THEMES[theme_name]
    w, h = 238, 58
    if style == "primary":
        bg_fill = "url(#ctaVice)"
        stroke = "#FF99C8"
        fg = "#FFFFFF"
        sub_fg = "#FFF0F7"
        icon_col = "#FFFFFF"
        defs = """
  <defs>
    <linearGradient id="ctaVice" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF2E88"/>
      <stop offset="52%" stop-color="#FF6B57"/>
      <stop offset="100%" stop-color="#FFB84D"/>
    </linearGradient>
    <linearGradient id="ctaSpec" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.60"/>
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
  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" rx="13" fill="{bg_fill}" stroke="{stroke}" stroke-width="1.2"/>
  <line x1="18" y1="2.9" x2="{w - 18}" y2="2.9" stroke="url(#ctaSpec)" stroke-width="1.1"/>
  <g transform="translate(14, 15)">
    {icon.format(c=icon_col)}
  </g>
  <text x="48" y="27.5" font-family="{FONT_SANS}" font-size="13.2" font-weight="700" fill="{fg}">{esc(label)}</text>
  <text x="48" y="43.5" font-family="{FONT_MONO}" font-size="9.5" font-weight="700" fill="{sub_fg}">{esc(sub)}</text>
  <text x="{w - 15}" y="34" text-anchor="end" font-family="{FONT_SANS}" font-size="14" font-weight="700" fill="{icon_col}">↗</text>
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
            t["pink"],
            "m0",
            f'<rect x="164" y="50" width="9" height="16" rx="2.5" fill="{t["pink"]}" fill-opacity="0.28"/>'
            f'<rect x="177" y="42" width="9" height="24" rx="2.5" fill="{t["pink"]}" fill-opacity="0.48"/>'
            f'<rect x="190" y="33" width="9" height="33" rx="2.5" fill="{t["pink"]}" fill-opacity="0.72"/>'
            f'<rect x="203" y="21" width="9" height="45" rx="2.5" fill="{t["pink"]}"/>',
        ),
        (
            "+30%",
            "Query Velocity",
            "Redis & SQL Profiling",
            t["aqua"],
            "m1",
            f'<path d="M 156 60 C 170 57, 178 48, 188 43 C 198 39, 204 29, 214 23 L 214 64 L 156 64 Z" fill="{t["aqua"]}" fill-opacity="0.18"/>'
            f'<path d="M 156 60 C 170 57, 178 48, 188 43 C 198 39, 204 29, 214 23" fill="none" stroke="{t["aqua"]}" stroke-width="2.2" stroke-linecap="round"/>'
            f'<circle cx="214" cy="23" r="3.6" fill="{t["aqua"]}"/>',
        ),
        (
            "3.5x",
            "AI Sprint Velocity",
            "Antigravity & Copilot",
            t["coral_gold"],
            "m2",
            f'<circle cx="192" cy="42" r="20" fill="none" stroke="{t["border_strong"]}" stroke-width="4.2"/>'
            f'<circle cx="192" cy="42" r="20" fill="none" stroke="{t["coral"]}" stroke-width="4.2" stroke-dasharray="104 130" stroke-linecap="round" transform="rotate(-90 192 42)"/>'
            f'<text x="192" y="45.5" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.5" font-weight="700" fill="{t["coral_gold"]}">AI</text>',
        ),
        (
            "10+ hrs",
            "Weekly Automated",
            "Python Data Pipelines",
            t["mint"],
            "m3",
            f'<line x1="164" y1="43" x2="212" y2="43" stroke="{t["mint"]}" stroke-width="2" stroke-dasharray="4 3"/>'
            f'<circle cx="164" cy="43" r="5" fill="{t["mint_bg"]}" stroke="{t["mint"]}" stroke-width="1.8"/>'
            f'<circle cx="188" cy="43" r="5" fill="{t["mint_bg"]}" stroke="{t["mint"]}" stroke-width="1.8"/>'
            f'<circle cx="212" cy="43" r="5.5" fill="{t["mint"]}"/>',
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
    <rect x="20" y="0" width="48" height="2.8" rx="1.4" fill="{acc}"/>
    <text x="20" y="46" font-family="{FONT_SANS}" font-size="29" font-weight="700" letter-spacing="-0.5" fill="{t['text']}">{esc(big)}</text>
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
      <path d="M 24 0 L 0 0 0 24" fill="none" stroke="{t['grid_line']}" stroke-width="0.7" stroke-opacity="0.7"/>
    </pattern>
    <clipPath id="bpClip">
      <rect x="4" y="36" width="992" height="238" rx="18"/>
    </clipPath>
    <radialGradient id="n1Glow" cx="20%" cy="0%" r="85%"><stop offset="0%" stop-color="{t['aqua']}" stop-opacity="{t['card_glow']}"/><stop offset="100%" stop-color="{t['aqua']}" stop-opacity="0"/></radialGradient>
    <radialGradient id="n2Glow" cx="50%" cy="0%" r="85%"><stop offset="0%" stop-color="{t['pink']}" stop-opacity="{t['card_glow']}"/><stop offset="100%" stop-color="{t['pink']}" stop-opacity="0"/></radialGradient>
    <radialGradient id="n3Glow" cx="50%" cy="0%" r="85%"><stop offset="0%" stop-color="{t['mint']}" stop-opacity="{t['card_glow']}"/><stop offset="100%" stop-color="{t['mint']}" stop-opacity="0"/></radialGradient>
    <radialGradient id="n4Glow" cx="80%" cy="0%" r="85%"><stop offset="0%" stop-color="{t['coral']}" stop-opacity="{t['card_glow']}"/><stop offset="100%" stop-color="{t['coral']}" stop-opacity="0"/></radialGradient>
    <linearGradient id="flow1" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="{t['aqua']}"/><stop offset="100%" stop-color="{t['pink']}"/></linearGradient>
    <linearGradient id="flow2" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="{t['pink']}"/><stop offset="100%" stop-color="{t['mint']}"/></linearGradient>
    <linearGradient id="flow3" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="{t['mint']}"/><stop offset="100%" stop-color="{t['coral']}"/></linearGradient>
    <style>
      @keyframes packetFlow {{ from {{ stroke-dashoffset: 64; }} to {{ stroke-dashoffset: 0; }} }}
      @keyframes softBlink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}
      .flow-line {{ stroke-dasharray: 7 7; animation: packetFlow 1.7s linear infinite; }}
      .live-glow {{ animation: softBlink 2.2s ease-in-out infinite; }}
    </style>
  </defs>

  {render_section_header("SYSTEM ARCHITECTURE BLUEPRINT", "HOW I ARCHITECT HIGH-THROUGHPUT PRODUCTION PLATFORMS", t, t["aqua"], w)}

  <g clip-path="url(#bpClip)">
    <rect x="4" y="36" width="992" height="238" fill="url(#bpCard)"/>
    <rect x="4" y="36" width="992" height="238" fill="url(#bpGrid)"/>
  </g>
  <rect x="4" y="36" width="992" height="238" rx="18" fill="none" stroke="{t['border']}" stroke-width="1.2"/>
  <line x1="24" y1="36.8" x2="976" y2="36.8" stroke="url(#bpSpec)" stroke-width="1"/>

  <!-- Animated Vice-Neon Fiber-Optic Pipes + Gliding Light Orbs -->
  <g>
    <line x1="226" y1="136" x2="274" y2="136" stroke="url(#flow1)" stroke-width="2.3" class="flow-line"/>
    <polygon points="274,136 266,131 266,141" fill="{t['pink']}"/>
    <circle r="3.3" fill="#FFFFFF"><animateMotion dur="1.7s" repeatCount="indefinite" path="M 226 136 L 269 136"/></circle>

    <line x1="496" y1="136" x2="544" y2="136" stroke="url(#flow2)" stroke-width="2.3" class="flow-line"/>
    <polygon points="544,136 536,131 536,141" fill="{t['mint']}"/>
    <circle r="3.3" fill="#FFFFFF"><animateMotion dur="1.7s" begin="0.55s" repeatCount="indefinite" path="M 496 136 L 539 136"/></circle>

    <line x1="752" y1="136" x2="796" y2="136" stroke="url(#flow3)" stroke-width="2.3" class="flow-line"/>
    <polygon points="796,136 788,131 788,141" fill="{t['coral']}"/>
    <circle r="3.3" fill="#FFFFFF"><animateMotion dur="1.7s" begin="1.1s" repeatCount="indefinite" path="M 752 136 L 791 136"/></circle>
  </g>

  <!-- Node 1: Client & UI Edge -->
  <g transform="translate(24, 58)">
    <rect x="0" y="0" width="202" height="154" rx="14" fill="url(#bpCard)" stroke="{t['aqua_border']}" stroke-width="1.2"/>
    <rect x="0" y="0" width="202" height="154" rx="14" fill="url(#n1Glow)"/>
    <rect x="16" y="0" width="44" height="2.8" rx="1.4" fill="{t['aqua']}"/>
    <text x="16" y="25" font-family="{FONT_MONO}" font-size="9.4" font-weight="700" fill="{t['aqua_bright']}">01 · CLIENT &amp; UI EDGE</text>
    <text x="16" y="48" font-family="{FONT_SANS}" font-size="14.5" font-weight="700" fill="{t['text']}">Reactive Interfaces</text>
    <text x="16" y="73" font-family="{FONT_MONO}" font-size="10.3" fill="{t['text_sub']}">▸ React.js &amp; Next.js 16</text>
    <text x="16" y="93" font-family="{FONT_MONO}" font-size="10.3" fill="{t['text_sub']}">▸ Vue.js / Vuex · Blade</text>
    <text x="16" y="113" font-family="{FONT_MONO}" font-size="10.3" fill="{t['text_sub']}">▸ TypeScript · Tailwind</text>
    <rect x="16" y="125" width="170" height="19" rx="6" fill="{t['aqua_bg']}" stroke="{t['aqua_border']}" stroke-width="0.7"/>
    <text x="101" y="137.8" text-anchor="middle" font-family="{FONT_MONO}" font-size="9" font-weight="700" fill="{t['aqua_bright']}">SPA · SSR · RESPONSIVE</text>
  </g>

  <!-- Node 2: Core API + AI-Augmented Engine -->
  <g transform="translate(274, 54)">
    <rect x="0" y="0" width="222" height="162" rx="14" fill="url(#bpCard)" stroke="{t['pink_border']}" stroke-width="1.4"/>
    <rect x="0" y="0" width="222" height="162" rx="14" fill="url(#n2Glow)"/>
    <rect x="16" y="0" width="60" height="2.8" rx="1.4" fill="url(#bpViceBar)"/>
    <text x="16" y="25" font-family="{FONT_MONO}" font-size="9.4" font-weight="700" fill="{t['pink_bright']}">02 · APPLICATION &amp; AI CORE</text>
    <text x="16" y="48" font-family="{FONT_SANS}" font-size="14.5" font-weight="700" fill="{t['text']}">Laravel 11 &amp; Python</text>
    <text x="16" y="72" font-family="{FONT_MONO}" font-size="10.3" fill="{t['text_sub']}">▸ PHP 8.3 · REST / Swagger</text>
    <text x="16" y="91" font-family="{FONT_MONO}" font-size="10.3" fill="{t['text_sub']}">▸ Django · Flask · Fast ETL</text>
    <rect x="14" y="107" width="194" height="43" rx="9" fill="{t['coral_bg']}" stroke="{t['coral_border']}" stroke-width="1"/>
    <text x="24" y="124" font-family="{FONT_MONO}" font-size="9.3" font-weight="700" fill="{t['coral_gold']}">✦ 3.5x AI VELOCITY ENGINE</text>
    <text x="24" y="140" font-family="{FONT_MONO}" font-size="9.1" fill="{t['text_sub']}">Antigravity · Copilot · Claude</text>
  </g>

  <!-- Node 3: Data, Cache & Cloud -->
  <g transform="translate(544, 58)">
    <rect x="0" y="0" width="208" height="154" rx="14" fill="url(#bpCard)" stroke="{t['mint_border']}" stroke-width="1.2"/>
    <rect x="0" y="0" width="208" height="154" rx="14" fill="url(#n3Glow)"/>
    <rect x="16" y="0" width="44" height="2.8" rx="1.4" fill="{t['mint']}"/>
    <text x="16" y="25" font-family="{FONT_MONO}" font-size="9.4" font-weight="700" fill="{t['mint']}">03 · DATA &amp; CLOUD LAYER</text>
    <text x="16" y="48" font-family="{FONT_SANS}" font-size="14.5" font-weight="700" fill="{t['text']}">Cache &amp; Persistence</text>
    <text x="16" y="73" font-family="{FONT_MONO}" font-size="10.3" fill="{t['text_sub']}">▸ Redis Cache (+30% Speed)</text>
    <text x="16" y="93" font-family="{FONT_MONO}" font-size="10.3" fill="{t['text_sub']}">▸ MySQL · PostgreSQL</text>
    <text x="16" y="113" font-family="{FONT_MONO}" font-size="10.3" fill="{t['text_sub']}">▸ AWS RDS &amp; DynamoDB</text>
    <rect x="16" y="125" width="176" height="19" rx="6" fill="{t['mint_bg']}" stroke="{t['mint_border']}" stroke-width="0.7"/>
    <text x="104" y="137.8" text-anchor="middle" font-family="{FONT_MONO}" font-size="9" font-weight="700" fill="{t['mint']}">INDEXED · HIGH-CONCURRENCY</text>
  </g>

  <!-- Node 4: Production Scale -->
  <g transform="translate(796, 58)">
    <rect x="0" y="0" width="180" height="154" rx="14" fill="url(#bpCard)" stroke="{t['coral_border']}" stroke-width="1.2"/>
    <rect x="0" y="0" width="180" height="154" rx="14" fill="url(#n4Glow)"/>
    <rect x="16" y="0" width="44" height="2.8" rx="1.4" fill="{t['coral']}"/>
    <text x="16" y="25" font-family="{FONT_MONO}" font-size="9.4" font-weight="700" fill="{t['coral_gold']}">04 · PRODUCTION</text>
    <text x="16" y="48" font-family="{FONT_SANS}" font-size="14.5" font-weight="700" fill="{t['text']}">Real-World Impact</text>
    <text x="16" y="73" font-family="{FONT_MONO}" font-size="10.1" fill="{t['text_sub']}">✦ Pan-India Diagnostics</text>
    <text x="16" y="93" font-family="{FONT_MONO}" font-size="10.1" fill="{t['text_sub']}">✦ Big Basket Scale TMS</text>
    <text x="16" y="113" font-family="{FONT_MONO}" font-size="10.1" fill="{t['text_sub']}">✦ 10+ hrs/wk Automated</text>
    <rect x="16" y="125" width="148" height="19" rx="6" fill="{t['coral_bg']}" stroke="{t['coral_border']}" stroke-width="0.7"/>
    <text x="90" y="137.8" text-anchor="middle" font-family="{FONT_MONO}" font-size="9" font-weight="700" fill="{t['coral_gold']}">ENTERPRISE DELIVERY</text>
  </g>

  <!-- Bottom Architecture Telemetry Strip -->
  <line x1="24" y1="232" x2="976" y2="232" stroke="{t['rule']}" stroke-width="1"/>
  <circle cx="34" cy="253" r="3.4" fill="{t['aqua']}" class="live-glow"/>
  <text x="45" y="256.5" font-family="{FONT_MONO}" font-size="10" fill="{t['text_sub']}">CSRF &amp; SQLi Defense  ·  Swagger OpenAPI Specs  ·  Razorpay / Stripe Gateways  ·  GitHub CI/CD  ·  MBA Finance &amp; IT Governance</text>
</svg>
"""


def build_tech_stack_radar(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 428

    cx, cy = 175, 224
    max_r = 80
    axes = [
        ("Laravel & Backend", 0.96, -90, 0, -13, "middle", t["pink_bright"]),
        ("AI Velocity", 0.94, -18, 10, -2, "start", t["coral_gold"]),
        ("DB & Redis", 0.93, 54, 8, 14, "start", t["mint"]),
        ("Python & AWS", 0.88, 126, -8, 14, "end", t["aqua_bright"]),
        ("Frontend UI", 0.90, 198, -10, -2, "end", t["palm"]),
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
        ("PHP 8.3 & Laravel 11", t["pink_bg"], t["pink_border"], t["pink_bright"], t["pink"]),
        ("REST & Swagger", t["elevated"], t["border"], t["text"], None),
        ("Python", t["pink_bg"], t["pink_border"], t["pink_bright"], t["pink"]),
        ("Django", t["elevated"], t["border"], t["text"], None),
        ("Flask", t["elevated"], t["border"], t["text"], None),
        ("Node.js", t["elevated"], t["border"], t["text"], None),
        ("Pandas", t["aqua_bg"], t["aqua_border"], t["aqua_bright"], None),
        ("NumPy", t["aqua_bg"], t["aqua_border"], t["aqua_bright"], None),
        ("SciPy", t["aqua_bg"], t["aqua_border"], t["aqua_bright"], None),
        ("Scikit-learn", t["aqua_bg"], t["aqua_border"], t["aqua_bright"], None),
        ("OpenCV", t["aqua_bg"], t["aqua_border"], t["aqua_bright"], None),
        ("Matplotlib", t["aqua_bg"], t["aqua_border"], t["aqua_bright"], None),
        ("Seaborn", t["aqua_bg"], t["aqua_border"], t["aqua_bright"], None),
    ]
    ai_pills = [
        ("Google Antigravity IDE", t["coral_bg"], t["coral_border"], t["coral_gold"], t["coral"]),
        ("GitHub Copilot", t["coral_bg"], t["coral_border"], t["coral_gold"], t["coral"]),
        ("Claude 3.7", t["elevated"], t["border"], t["text"], None),
        ("GPT-4", t["elevated"], t["border"], t["text"], None),
        ("Prompt Architecture", t["elevated"], t["border"], t["text"], None),
        ("Autonomous Refactoring", t["elevated"], t["border"], t["text"], None),
        ("Synthetic QA", t["elevated"], t["border"], t["text"], None),
    ]
    frontend_pills = [
        ("React.js", t["aqua_bg"], t["aqua_border"], t["aqua_bright"], t["aqua"]),
        ("Next.js 16", t["aqua_bg"], t["aqua_border"], t["aqua_bright"], t["aqua"]),
        ("Vue.js & Vuex", t["elevated"], t["border"], t["text"], None),
        ("TypeScript", t["elevated"], t["border"], t["text"], None),
        ("JS / AJAX", t["elevated"], t["border"], t["text"], None),
        ("Tailwind CSS", t["elevated"], t["border"], t["text"], None),
        ("Blade", t["elevated"], t["border"], t["text"], None),
    ]
    cloud_pills = [
        ("MySQL", t["mint_bg"], t["mint_border"], t["mint"], t["mint"]),
        ("PostgreSQL", t["mint_bg"], t["mint_border"], t["mint"], t["mint"]),
        ("Redis Cache", t["mint_bg"], t["mint_border"], t["mint"], t["mint"]),
        ("AWS RDS & DynamoDB", t["coral_bg"], t["coral_border"], t["coral_gold"], t["coral"]),
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
      <stop offset="0%" stop-color="{t['pink']}" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="{t['pink']}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="radarFill" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{t['pink']}" stop-opacity="0.42"/>
      <stop offset="50%" stop-color="{t['coral_gold']}" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="{t['aqua']}" stop-opacity="0.36"/>
    </linearGradient>
    <linearGradient id="radarStroke" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{t['pink_bright']}"/>
      <stop offset="50%" stop-color="{t['coral_gold']}"/>
      <stop offset="100%" stop-color="{t['aqua']}"/>
    </linearGradient>
  </defs>

  {render_section_header("CAPABILITY RADAR & TECH STACK", "FULL-STACK DEPTH + AI ACCELERATORS", t, t["pink"], w)}

  <!-- Left Bento: 5-Axis Vice Radar -->
  <g>
    {glass_card(4, 38, 342, 382, 16, t, accent="url(#tsViceBar)", prefix="ts")}
    <circle cx="{cx}" cy="{cy}" r="115" fill="url(#radAmb)"/>
    <text x="24" y="66" font-family="{FONT_MONO}" font-size="11" font-weight="700" letter-spacing="1.1" fill="{t['pink_bright']}">ENGINEERING RADAR</text>
    <text x="24" y="84" font-family="{FONT_SANS}" font-size="11.5" fill="{t['text_muted']}">Multi-domain production capability map</text>

    {"".join(rings)}
    {"".join(spokes)}
    <polygon points="{" ".join(poly_pts)}" fill="url(#radarFill)" stroke="url(#radarStroke)" stroke-width="2.2" stroke-linejoin="round"/>
    <polygon points="{" ".join(inner_pts)}" fill="none" stroke="#FFFFFF" stroke-opacity="0.20" stroke-width="1" stroke-dasharray="3 3"/>
    {"".join(vertex_dots)}
    {"".join(axis_labels)}

    <!-- Radar Legend Footer -->
    <line x1="24" y1="354" x2="326" y2="354" stroke="{t['rule']}" stroke-width="1"/>
    <text x="24" y="377" font-family="{FONT_MONO}" font-size="9.6" font-weight="700" fill="{t['aqua_bright']}">● CORE STRENGTH:</text>
    <text x="148" y="377" font-family="{FONT_MONO}" font-size="9.6" fill="{t['text_sub']}">Laravel · Redis · AI</text>
    <text x="24" y="397" font-family="{FONT_MONO}" font-size="9.6" font-weight="700" fill="{t['coral_gold']}">● STRATEGIC EDGE:</text>
    <text x="148" y="397" font-family="{FONT_MONO}" font-size="9.6" fill="{t['text_sub']}">Tech + MBA Finance ROI</text>
  </g>

  <!-- Right Top: Backend & Python Data Science -->
  <g>
    {glass_card(360, 38, 636, 106, 15, t, accent=t["pink"], prefix="ts")}
    <text x="378" y="65" font-family="{FONT_MONO}" font-size="10.8" font-weight="700" letter-spacing="1.1" fill="{t['pink_bright']}">BACKEND ARCHITECTURE &amp; PYTHON DATA SCIENCE</text>
    <text x="976" y="65" text-anchor="end" font-family="{FONT_MONO}" font-size="9.6" fill="{t['text_muted']}">13 TECHNOLOGIES</text>
    {b_svg}
  </g>

  <!-- Right Middle: AI Agentic Engineering -->
  <g>
    {glass_card(360, 154, 636, 96, 15, t, accent="url(#tsViceBar)", border=t["coral_border"], prefix="ts")}
    <text x="378" y="180" font-family="{FONT_MONO}" font-size="10.8" font-weight="700" letter-spacing="1.1" fill="{t['coral_gold']}">AI AGENTIC ENGINEERING &amp; AUTOMATION</text>
    <rect x="870" y="164" width="108" height="20" rx="10" fill="{t['coral_bg']}" stroke="{t['coral_border']}" stroke-width="0.9"/>
    <text x="924" y="177.2" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.2" font-weight="700" fill="{t['coral_gold']}">✦ 3.5x VELOCITY</text>
    {a_svg}
  </g>

  <!-- Right Bottom-Left: Frontend & UI -->
  <g>
    {glass_card(360, 260, 310, 160, 15, t, accent=t["aqua"], prefix="ts")}
    <text x="378" y="286" font-family="{FONT_MONO}" font-size="10.6" font-weight="700" letter-spacing="1.1" fill="{t['aqua_bright']}">FRONTEND &amp; UI SYSTEMS</text>
    {f_svg}
  </g>

  <!-- Right Bottom-Right: Databases, Cloud & DevOps -->
  <g>
    {glass_card(682, 260, 314, 160, 15, t, accent=t["mint"], prefix="ts")}
    <text x="698" y="286" font-family="{FONT_MONO}" font-size="10.6" font-weight="700" letter-spacing="1.1" fill="{t['mint']}">DATABASES, CLOUD &amp; DEVOPS</text>
    {c_svg}
  </g>
</svg>
"""


def build_projects_header(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 44
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Featured Production Case Studies">
  {render_section_header("FEATURED PRODUCTION MISSIONS", "CLICK ANY CARD TO LAUNCH LIVE PLATFORM", t, t["coral"], w)}
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
  <rect x="20" y="2" width="58" height="2.8" rx="1.4" fill="{acc}"/>

  <!-- Mini Architectural Visual Preview Thumbnail -->
  <g transform="translate(382, 16)">
    <rect x="0" y="0" width="88" height="54" rx="10" fill="{bg}" stroke="{brd}" stroke-width="1"/>
    {thumb_svg.format(c=acc)}
  </g>

  <rect x="20" y="16" width="{badge_w}" height="22" rx="11" fill="{bg}" stroke="{brd}" stroke-width="0.9"/>
  <text x="{20 + badge_w / 2:.1f}" y="30.2" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.5" font-weight="700" fill="{acc}">{esc(badge)}</text>
  <text x="{20 + badge_w + 10}" y="30.2" font-family="{FONT_MONO}" font-size="9.8" fill="{t['text_muted']}">{esc(period)} · {esc(category)}</text>

  <text x="20" y="65" font-family="{FONT_SANS}" font-size="16" font-weight="700" fill="{t['text']}">{esc(title)}</text>
  <text x="20" y="87" font-family="{FONT_SANS}" font-size="11.8" fill="{t['text_sub']}">{esc(desc1)}</text>
  <text x="20" y="104" font-family="{FONT_SANS}" font-size="11.8" fill="{t['text_sub']}">{esc(desc2)}</text>

  {"".join(tag_pills)}

  <circle cx="422" cy="133.5" r="3" fill="{acc}" class="lp"/>
  <text x="430" y="137" font-family="{FONT_MONO}" font-size="9.6" font-weight="700" fill="{acc}">LIVE ↗</text>
</svg>
"""


def build_telemetry_ethos(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 1000, 198

    segments = [
        ("PHP / Laravel", 196, t["pink"]),
        ("Python & ML", 124, t["aqua"]),
        ("TS / React / Next", 104, t["coral_gold"]),
        ("Vue / Blade / JS", 62, t["mint"]),
        ("SQL / Redis", 30, t["palm"]),
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
        ("hotel-pos-laravel", t["pink_bg"], t["pink_border"], t["pink_bright"], t["pink"], 136),
        ("my-portfolio", t["aqua_bg"], t["aqua_border"], t["aqua_bright"], t["aqua"], 108),
        ("Admin-Dashboard", t["mint_bg"], t["mint_border"], t["mint"], t["mint"], 126),
        ("ML-Recommenders", t["coral_bg"], t["coral_border"], t["coral_gold"], t["coral"], 128),
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
    <radialGradient id="sunsetAura" cx="88%" cy="50%" r="58%">
      <stop offset="0%" stop-color="{t['pink']}" stop-opacity="0.22"/>
      <stop offset="55%" stop-color="{t['coral']}" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="{t['coral']}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="ethRClip"><rect x="582" y="38" width="414" height="154" rx="16"/></clipPath>
  </defs>

  {render_section_header("OPEN-SOURCE PULSE & ENGINEERING ETHOS", "26 REPOSITORIES · 504+ CONTRIBUTIONS", t, t["pink"], w)}

  <!-- Left Card: Open-Source Language Spectrum & Flagship Repos -->
  <g>
    {glass_card(4, 38, 564, 154, 16, t, accent=t["pink"], prefix="eth")}
    <text x="26" y="67" font-family="{FONT_MONO}" font-size="10.8" font-weight="700" letter-spacing="1.1" fill="{t['pink_bright']}">GITHUB ECOSYSTEM &amp; STACK SPECTRUM</text>
    <rect x="408" y="51" width="138" height="22" rx="11" fill="{t['aqua_bg']}" stroke="{t['aqua_border']}" stroke-width="0.9"/>
    <text x="477" y="65.2" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.5" font-weight="700" fill="{t['aqua_bright']}">26 REPOS · 504+ COMMITS</text>

    <text x="26" y="88" font-family="{FONT_SANS}" font-size="11.5" fill="{t['text_muted']}">Production &amp; open-source distribution across backend, data science &amp; modern UI</text>
    {"".join(bar_rects)}
    {"".join(legend_items)}
    {chips_svg}
  </g>

  <!-- Right Card: Engineering Philosophy + Vice Sunset Disc -->
  <g>
    <g clip-path="url(#ethRClip)">
      <rect x="582" y="38" width="414" height="154" fill="url(#ethCard)"/>
      <rect x="582" y="38" width="414" height="154" fill="url(#sunsetAura)"/>
      <g>{vice_sun_ornament(932, 118, 56, t['coral_gold'], t['pink'], t['card'], '0.32')}</g>
    </g>
    <rect x="582" y="38" width="414" height="154" rx="16" fill="none" stroke="{t['pink_border']}" stroke-width="1.2"/>
    <line x1="600" y1="38.8" x2="978" y2="38.8" stroke="url(#ethSpec)" stroke-width="1"/>
    <rect x="602" y="38" width="58" height="2.8" rx="1.4" fill="url(#ethViceBar)"/>

    <text x="604" y="67" font-family="{FONT_MONO}" font-size="10.4" font-weight="700" letter-spacing="1.2" fill="{t['coral_gold']}">ENGINEERING PHILOSOPHY</text>
    <text x="604" y="102" font-family="{FONT_SANS}" font-size="19.5" font-weight="700" fill="{t['text']}">धैर्यं सर्वत्र साधनम्।</text>
    <text x="604" y="124" font-family="{FONT_MONO}" font-size="11" font-weight="600" fill="{t['pink_bright']}">&quot;Patience is the solution to everything.&quot;</text>
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
            t["aqua_bright"],
            True,
        ),
        (
            "2022 – 2023 · FULL-STACK",
            "Laravel Developer",
            "Finesoft Technologies Pvt. Ltd · Noida",
            "Full-stack Blade & Vue.js delivery · 3rd-party payment gateways & SMS",
            "High-concurrency relational DB schemas with optimized query execution",
            t["pink_bright"],
            False,
        ),
        (
            "2021 – 2022 · AUTOMATION",
            "Python Developer",
            "Magical Umbrella Pvt. Ltd",
            "Automated routine data pipelines in Python — saved 10+ manual hrs/week",
            "Engineered secure RESTful backend APIs & relational database designs",
            t["coral_gold"],
            False,
        ),
    ]

    exp_svgs = []
    ey = 82
    for period, role, company, b1, b2, color, live in exp_items:
        pulse_cls = ' class="live-dot"' if live else ""
        exp_svgs.append(f"""
    <circle cx="34" cy="{ey + 12}" r="11" fill="{color}" fill-opacity="0.15"/>
    <circle cx="34" cy="{ey + 12}" r="6.5" fill="{t['card']}" stroke="{color}" stroke-width="2.2"/>
    <circle cx="34" cy="{ey + 12}" r="2.8" fill="{color}"{pulse_cls}/>
    <text x="54" y="{ey + 8}" font-family="{FONT_MONO}" font-size="10" font-weight="700" fill="{color}">{esc(period)}</text>
    <text x="54" y="{ey + 27}" font-family="{FONT_SANS}" font-size="14.5" font-weight="700" fill="{t['text']}">{esc(role)} <tspan font-size="12" font-weight="600" fill="{t['text_sub']}">— {esc(company)}</tspan></text>
    <text x="54" y="{ey + 47}" font-family="{FONT_SANS}" font-size="11.4" fill="{t['text_sub']}">✦ {esc(b1)}</text>
    <text x="54" y="{ey + 65}" font-family="{FONT_SANS}" font-size="11.4" fill="{t['text_muted']}">▸ {esc(b2)}</text>""")
        ey += 97

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Career Experience and Academic Credentials">
  <defs>
    {glass_defs(t, "jr")}
    <linearGradient id="spineGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{t['aqua']}"/>
      <stop offset="50%" stop-color="{t['pink']}"/>
      <stop offset="100%" stop-color="{t['coral_gold']}"/>
    </linearGradient>
    <style>
      @keyframes pulseNode {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.25; }} }}
      .live-dot {{ animation: pulseNode 2.2s ease-in-out infinite; }}
    </style>
  </defs>

  {render_section_header("CAREER JOURNEY & CREDENTIALS", "5+ YEARS PRODUCTION · MBA + B.E. CSE", t, t["aqua"], w)}

  <!-- Left Panel: Work Experience -->
  <g>
    {glass_card(4, 38, 564, 352, 16, t, accent="url(#jrViceBar)", prefix="jr")}
    <text x="24" y="66" font-family="{FONT_MONO}" font-size="11.2" font-weight="700" letter-spacing="1.2" fill="{t['pink_bright']}">PROFESSIONAL EXPERIENCE</text>
    <line x1="34" y1="98" x2="34" y2="294" stroke="url(#spineGrad)" stroke-width="2.2" stroke-dasharray="4 4"/>
    {"".join(exp_svgs)}
  </g>

  <!-- Right Top Panel: Academic Qualifications -->
  <g>
    {glass_card(584, 38, 412, 240, 16, t, accent=t["aqua"], prefix="jr")}
    <text x="604" y="66" font-family="{FONT_MONO}" font-size="11.2" font-weight="700" letter-spacing="1.2" fill="{t['aqua_bright']}">ACADEMIC QUALIFICATIONS</text>

    <rect x="604" y="82" width="372" height="80" rx="12" fill="{t['elevated']}" stroke="{t['aqua_border']}" stroke-width="1"/>
    <circle cx="622" cy="100" r="3.5" fill="{t['aqua']}" class="live-dot"/>
    <text x="632" y="103.5" font-family="{FONT_MONO}" font-size="9.8" font-weight="700" fill="{t['aqua_bright']}">PURSUING · 2024 – PRESENT</text>
    <text x="618" y="125" font-family="{FONT_SANS}" font-size="14" font-weight="700" fill="{t['text']}">MBA in Finance &amp; IT</text>
    <text x="618" y="145" font-family="{FONT_SANS}" font-size="11.6" fill="{t['text_sub']}">Gondwana University · Business ROI &amp; IT Governance</text>

    <rect x="604" y="174" width="372" height="88" rx="12" fill="{t['elevated']}" stroke="{t['pink_border']}" stroke-width="1"/>
    <text x="618" y="193" font-family="{FONT_MONO}" font-size="9.8" font-weight="700" fill="{t['pink_bright']}">COMPLETED OCT 2020 · 74.60% DISTINCTION</text>
    <text x="618" y="215" font-family="{FONT_SANS}" font-size="14" font-weight="700" fill="{t['text']}">B.E. in Computer Science</text>
    <text x="618" y="234" font-family="{FONT_SANS}" font-size="11.6" fill="{t['text_sub']}">Gondwana University</text>
    <text x="618" y="250" font-family="{FONT_MONO}" font-size="9.8" fill="{t['text_muted']}">Data Analysis · ML · Deep Learning · Web Dev</text>
  </g>

  <!-- Right Bottom Panel: Base & Languages -->
  <g>
    {glass_card(584, 292, 412, 98, 16, t, accent=t["coral"], prefix="jr")}
    <text x="604" y="319" font-family="{FONT_MONO}" font-size="10.4" font-weight="700" letter-spacing="1.2" fill="{t['coral_gold']}">BASE &amp; COLLABORATION</text>
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
  </defs>
  {render_section_header("INITIATE CONTACT & CONNECT", "OPEN FOR ROLES, ARCHITECTURE & ADVISORY", t, t["coral"], w)}
  <rect x="4" y="35" width="992" height="49" rx="14" fill="url(#cnCard)" stroke="{t['border']}" stroke-width="1.2"/>
  <rect x="4" y="35" width="5" height="49" rx="2.5" fill="url(#cnViceBar)"/>
  <line x1="20" y1="35.8" x2="980" y2="35.8" stroke="url(#cnSpec)" stroke-width="1"/>
  <text x="26" y="64" font-family="{FONT_SANS}" font-size="14" font-weight="700" fill="{t['text']}">Explore my live portfolio, download my resume, or connect directly across channels below.</text>
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
  <rect x="16" y="2" width="46" height="2.8" rx="1.4" fill="{acc}"/>
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
      <stop offset="0%" stop-color="{t['pink']}" stop-opacity="0.26"/>
      <stop offset="50%" stop-color="{t['coral_gold']}" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="{t['aqua']}" stop-opacity="0.26"/>
    </linearGradient>
    <linearGradient id="footWave2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t['aqua']}" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="{t['pink']}" stop-opacity="0.18"/>
    </linearGradient>
    <style>
      @keyframes footShimmer {{ 0% {{ transform: translateX(-220px); opacity: 0; }} 25% {{ opacity: 0.8; }} 75% {{ opacity: 0.8; }} 100% {{ transform: translateX(1020px); opacity: 0; }} }}
      .shimmer {{ animation: footShimmer 5.8s ease-in-out infinite; }}
    </style>
  </defs>
  <g clip-path="url(#footClip)">
    <rect x="4" y="4" width="992" height="68" fill="url(#ftCard)"/>
    <path d="M0 52 Q250 20 500 46 T1000 34 L1000 76 L0 76 Z" fill="url(#footWave1)"/>
    <path d="M0 40 Q280 64 560 32 T1000 50 L1000 76 L0 76 Z" fill="url(#footWave2)"/>
    <rect x="4" y="69" width="992" height="3" fill="url(#ftViceBar)"/>
    <rect x="0" y="69" width="180" height="3" fill="#FFFFFF" class="shimmer"/>
  </g>
  <rect x="4" y="4" width="992" height="68" rx="16" fill="none" stroke="{t['border']}" stroke-width="1.2"/>
  <line x1="22" y1="4.8" x2="978" y2="4.8" stroke="url(#ftSpec)" stroke-width="1"/>
  <text x="500" y="43" text-anchor="middle" font-family="{FONT_MONO}" font-size="11.2" font-weight="700" letter-spacing="1.0" fill="{t['text_sub']}">&lt;SB/&gt;  SHUBHAM BRAMHANE  ·  ARCHITECTING HIGH-THROUGHPUT SYSTEMS WITH AI VELOCITY</text>
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
        "coral",
        '<path d="M8 4 H16 L21 9 V23 H8 Z" fill="none" stroke="{c}" stroke-width="1.8" stroke-linejoin="round"/>'
        '<polyline points="16,4 16,9 21,9" fill="none" stroke="{c}" stroke-width="1.5"/>'
        '<line x1="11" y1="14.5" x2="18" y2="14.5" stroke="{c}" stroke-width="1.5" stroke-linecap="round"/>'
        '<line x1="11" y1="18.5" x2="16" y2="18.5" stroke="{c}" stroke-width="1.5" stroke-linecap="round"/>',
    ),
    (
        "linkedin",
        "LinkedIn Profile",
        "IN/SHUBHAM1602",
        "aqua",
        '<rect x="6.5" y="11" width="3.2" height="10.5" rx="0.9" fill="{c}"/>'
        '<circle cx="8.1" cy="7.5" r="1.8" fill="{c}"/>'
        '<path d="M12.5 11 H15.5 V12.7 C16.3 11.4 17.5 10.7 19.1 10.7 C21.3 10.7 22.2 12.2 22.2 14.8 V21.5 H19 V15.4 C19 14 18.4 13.3 17.3 13.3 C16.2 13.3 15.6 14.1 15.6 15.4 V21.5 H12.5 Z" fill="{c}"/>',
    ),
    (
        "contact",
        "Initiate Contact",
        "DIRECT EMAIL",
        "mint",
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
        "mint",
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
        "aqua",
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
        "pink",
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
        "coral",
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
        "aqua",
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
        "palm",
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
        "pink",
        '<circle cx="20" cy="20" r="8.5" fill="none" stroke="{c}" stroke-width="1.8"/>'
        '<ellipse cx="20" cy="20" rx="3.8" ry="8.5" fill="none" stroke="{c}" stroke-width="1.5"/>'
        '<line x1="11.5" y1="20" x2="28.5" y2="20" stroke="{c}" stroke-width="1.5"/>',
        True,
    ),
    (
        "resume",
        "Download Resume",
        "Shubham_Bramhane_Resume.pdf",
        "coral",
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
        "aqua",
        '<rect x="13" y="17.5" width="3" height="9.5" rx="0.8" fill="{c}"/>'
        '<circle cx="14.5" cy="14" r="1.7" fill="{c}"/>'
        '<path d="M19 17.5 H21.8 V19.1 C22.5 17.9 23.7 17.2 25.1 17.2 C27.2 17.2 28 18.7 28 21.1 V27 H25 V21.6 C25 20.3 24.4 19.7 23.4 19.7 C22.4 19.7 21.9 20.4 21.9 21.6 V27 H19 Z" fill="{c}"/>',
        False,
    ),
    (
        "email",
        "Email",
        "shubham.bramhane75@gmail.com",
        "mint",
        '<rect x="12" y="14" width="16" height="12" rx="2.2" fill="none" stroke="{c}" stroke-width="1.8"/>'
        '<polyline points="12.5,15.2 20,21 27.5,15.2" fill="none" stroke="{c}" stroke-width="1.8" stroke-linejoin="round"/>',
        False,
    ),
    (
        "twitter",
        "X / Twitter",
        "@shubhbramhane16",
        "palm",
        '<path d="M13 13 L18.7 20.6 L12.8 27 H15.2 L19.8 22 L23.6 27 H27.2 L21.2 19 L26.7 13 H24.3 L20.1 17.6 L16.6 13 Z" fill="{c}"/>',
        False,
    ),
    (
        "phone",
        "Phone",
        "+91-8857916707",
        "pink",
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
