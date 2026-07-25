#!/usr/bin/env python3
"""
scripts/render_cp_stats_svg.py

Generates a dual Neofetch-style terminal SVG (`cp-stats.svg`) displaying real-time
Codeforces and LeetCode statistics.
Features dark GitHub aesthetic, progress bars, SVG keyframe animations, and vector badges.
"""

import json
import sys
import xml.sax.saxutils as xml_escape
from pathlib import Path
from config import CODEFORCES_JSON, CP_STATS_SVG, LEETCODE_JSON


def load_json(filepath: Path) -> dict:
    """Safely load JSON metrics file or return empty fallback dict."""
    if filepath.is_file():
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[render_cp_stats_svg] Warning: Could not read {filepath}: {e}", file=sys.stderr)
    return {}


def generate_cp_stats_svg(output_path: Path = CP_STATS_SVG) -> None:
    """Generate dual terminal window SVG for Codeforces and LeetCode stats."""
    cf = load_json(CODEFORCES_JSON)
    lc = load_json(LEETCODE_JSON)

    width = 880
    height = 270
    card_width = 425
    header_bar_height = 36

    svg_parts = []
    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">'
    )
    svg_parts.append("<defs>")
    svg_parts.append("  <style>")
    svg_parts.append("    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&amp;display=swap');")
    svg_parts.append("    .card-bg { fill: #0d1117; rx: 10px; ry: 10px; stroke: #30363d; stroke-width: 1px; }")
    svg_parts.append("    .header { fill: #161b22; rx: 10px; ry: 10px; }")
    svg_parts.append("    .title { font-family: 'Fira Code', monospace; font-size: 12px; fill: #8b949e; font-weight: 600; }")
    svg_parts.append("    .dot-red { fill: #ff5f56; }")
    svg_parts.append("    .dot-yellow { fill: #ffbd2e; }")
    svg_parts.append("    .dot-green { fill: #27c93f; }")
    
    # Typography & Colors
    svg_parts.append("    .txt { font-family: 'Fira Code', monospace; font-size: 12px; }")
    svg_parts.append("    .platform-title { font-size: 14px; font-weight: 700; }")
    svg_parts.append("    .cf-title { fill: #f0883e; }")
    svg_parts.append("    .lc-title { fill: #ffa657; }")
    
    svg_parts.append("    .key { fill: #79c0ff; font-weight: 600; }")
    svg_parts.append("    .val { fill: #c9d1d9; font-weight: 500; }")
    svg_parts.append("    .val-highlight { fill: #58a6ff; font-weight: 700; }")
    
    # Difficulty Colors
    svg_parts.append("    .easy { fill: #39d353; font-weight: 600; }")
    svg_parts.append("    .medium { fill: #ffbd2e; font-weight: 600; }")
    svg_parts.append("    .hard { fill: #ff5f56; font-weight: 600; }")
    
    # Meter bars
    svg_parts.append("    .bar-bg { fill: #21262d; rx: 4px; ry: 4px; }")
    svg_parts.append("    .bar-easy { fill: #2ea043; rx: 4px; ry: 4px; }")
    svg_parts.append("    .bar-medium { fill: #d29922; rx: 4px; ry: 4px; }")
    svg_parts.append("    .bar-hard { fill: #f85149; rx: 4px; ry: 4px; }")

    # Staggered Fade In
    svg_parts.append("    .anim { opacity: 0; animation: fadeIn 0.4s ease-out forwards; }")
    svg_parts.append("    @keyframes fadeIn { 0% { opacity: 0; transform: translateY(5px); } 100% { opacity: 1; transform: translateY(0); } }")
    
    svg_parts.append("    .l-1 { animation-delay: 0.05s; }")
    svg_parts.append("    .l-2 { animation-delay: 0.10s; }")
    svg_parts.append("    .l-3 { animation-delay: 0.15s; }")
    svg_parts.append("    .l-4 { animation-delay: 0.20s; }")
    svg_parts.append("    .l-5 { animation-delay: 0.25s; }")
    svg_parts.append("    .l-6 { animation-delay: 0.30s; }")

    svg_parts.append("  </style>")
    svg_parts.append("</defs>")

    # ------------------ CODEFORCES CARD (LEFT) ------------------
    cf_x = 10
    svg_parts.append(f'<g transform="translate({cf_x}, 0)">')
    svg_parts.append(f'  <rect class="card-bg" width="{card_width}" height="{height}" />')
    svg_parts.append(f'  <rect class="header" width="{card_width}" height="{header_bar_height}" />')
    svg_parts.append('  <circle class="dot-red" cx="18" cy="18" r="5" />')
    svg_parts.append('  <circle class="dot-yellow" cx="34" cy="18" r="5" />')
    svg_parts.append('  <circle class="dot-green" cx="50" cy="18" r="5" />')
    
    cf_handle = xml_escape.escape(cf.get("handle", "Code_da_vinci"))
    svg_parts.append(f'  <text class="title" x="68" y="22">codeforces@terminal:~ $ cat {cf_handle}.stats</text>')

    # Card Content
    cf_rating = cf.get("rating", 0)
    cf_max_rating = cf.get("max_rating", 0)
    cf_rank = xml_escape.escape(str(cf.get("rank", "Newbie")))
    cf_contests = cf.get("contests", 0)
    cf_solved = cf.get("problems_solved", 0)

    y = 65
    svg_parts.append(f'  <text class="txt platform-title cf-title anim l-1" x="22" y="{y}">🏆 Codeforces Statistics</text>')
    
    y += 30
    svg_parts.append(f'  <g class="anim l-2">')
    svg_parts.append(f'    <text class="txt key" x="22" y="{y}">Current Rating:</text>')
    svg_parts.append(f'    <text class="txt val-highlight" x="160" y="{y}">{cf_rating}</text>')
    svg_parts.append(f'    <text class="txt key" x="230" y="{y}">Max Rating:</text>')
    svg_parts.append(f'    <text class="txt val" x="340" y="{y}">{cf_max_rating}</text>')
    svg_parts.append(f'  </g>')

    y += 26
    svg_parts.append(f'  <g class="anim l-3">')
    svg_parts.append(f'    <text class="txt key" x="22" y="{y}">Current Rank:</text>')
    svg_parts.append(f'    <text class="txt val" x="160" y="{y}">{cf_rank}</text>')
    svg_parts.append(f'  </g>')

    y += 26
    svg_parts.append(f'  <g class="anim l-4">')
    svg_parts.append(f'    <text class="txt key" x="22" y="{y}">Problems Solved:</text>')
    svg_parts.append(f'    <text class="txt val-highlight" x="160" y="{y}">{cf_solved}</text>')
    svg_parts.append(f'  </g>')

    y += 26
    svg_parts.append(f'  <g class="anim l-5">')
    svg_parts.append(f'    <text class="txt key" x="22" y="{y}">Contests Attended:</text>')
    svg_parts.append(f'    <text class="txt val" x="160" y="{y}">{cf_contests}</text>')
    svg_parts.append(f'  </g>')

    # Problem solving visual badge
    y += 36
    svg_parts.append(f'  <g class="anim l-6">')
    svg_parts.append(f'    <rect class="bar-bg" x="22" y="{y-12}" width="380" height="22" rx="4" />')
    svg_parts.append(f'    <text class="txt val" x="32" y="{y+2}">⚡ Competitive Rating Tier: {cf_rank}</text>')
    svg_parts.append(f'  </g>')

    svg_parts.append('</g>')

    # ------------------ LEETCODE CARD (RIGHT) ------------------
    lc_x = 445
    svg_parts.append(f'<g transform="translate({lc_x}, 0)">')
    svg_parts.append(f'  <rect class="card-bg" width="{card_width}" height="{height}" />')
    svg_parts.append(f'  <rect class="header" width="{card_width}" height="{header_bar_height}" />')
    svg_parts.append('  <circle class="dot-red" cx="18" cy="18" r="5" />')
    svg_parts.append('  <circle class="dot-yellow" cx="34" cy="18" r="5" />')
    svg_parts.append('  <circle class="dot-green" cx="50" cy="18" r="5" />')

    lc_user = xml_escape.escape(lc.get("username", "vivekjadhav07"))
    svg_parts.append(f'  <text class="title" x="68" y="22">leetcode@terminal:~ $ cat {lc_user}.stats</text>')

    lc_total = lc.get("total_solved", 0)
    lc_easy = lc.get("easy_solved", 0)
    lc_med = lc.get("medium_solved", 0)
    lc_hard = lc.get("hard_solved", 0)
    lc_rank = lc.get("ranking", 0)
    lc_c_rating = lc.get("contest_rating", 0)
    lc_acc = lc.get("acceptance_rate", 0.0)

    y = 65
    svg_parts.append(f'  <text class="txt platform-title lc-title anim l-1" x="22" y="{y}">💡 LeetCode Statistics</text>')

    y += 30
    svg_parts.append(f'  <g class="anim l-2">')
    svg_parts.append(f'    <text class="txt key" x="22" y="{y}">Total Solved:</text>')
    svg_parts.append(f'    <text class="txt val-highlight" x="140" y="{y}">{lc_total}</text>')
    svg_parts.append(f'    <text class="txt key" x="220" y="{y}">Acceptance:</text>')
    svg_parts.append(f'    <text class="txt val" x="330" y="{y}">{lc_acc}%</text>')
    svg_parts.append(f'  </g>')

    # Problem Breakdown Row (Easy / Med / Hard)
    y += 28
    bar_max_w = 230
    e_w = int((lc_easy / max(lc_total, 1)) * bar_max_w)
    m_w = int((lc_med / max(lc_total, 1)) * bar_max_w)
    h_w = int((lc_hard / max(lc_total, 1)) * bar_max_w)

    svg_parts.append(f'  <g class="anim l-3">')
    svg_parts.append(f'    <text class="txt easy" x="22" y="{y}">Easy: {lc_easy}</text>')
    svg_parts.append(f'    <text class="txt medium" x="120" y="{y}">Med: {lc_med}</text>')
    svg_parts.append(f'    <text class="txt hard" x="220" y="{y}">Hard: {lc_hard}</text>')
    svg_parts.append(f'  </g>')

    # Stacked Progress Meter Bar
    y += 12
    svg_parts.append(f'  <g class="anim l-4">')
    svg_parts.append(f'    <rect class="bar-bg" x="22" y="{y}" width="{bar_max_w}" height="8" rx="4" />')
    cur_x = 22
    if e_w > 0:
        svg_parts.append(f'    <rect class="bar-easy" x="{cur_x}" y="{y}" width="{e_w}" height="8" />')
        cur_x += e_w
    if m_w > 0:
        svg_parts.append(f'    <rect class="bar-medium" x="{cur_x}" y="{y}" width="{m_w}" height="8" />')
        cur_x += m_w
    if h_w > 0:
        svg_parts.append(f'    <rect class="bar-hard" x="{cur_x}" y="{y}" width="{h_w}" height="8" />')
    svg_parts.append(f'  </g>')

    y += 32
    svg_parts.append(f'  <g class="anim l-5">')
    svg_parts.append(f'    <text class="txt key" x="22" y="{y}">Global Ranking:</text>')
    svg_parts.append(f'    <text class="txt val" x="160" y="{y}">#{lc_rank:,}</text>')
    svg_parts.append(f'  </g>')

    y += 26
    svg_parts.append(f'  <g class="anim l-6">')
    svg_parts.append(f'    <text class="txt key" x="22" y="{y}">Contest Rating:</text>')
    svg_parts.append(f'    <text class="txt val-highlight" x="160" y="{y}">{lc_c_rating if lc_c_rating > 0 else "N/A"}</text>')
    svg_parts.append(f'  </g>')

    svg_parts.append('</g>')

    svg_parts.append('</svg>')

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))

    print(f"[render_cp_stats_svg] Competitive programming SVG saved to: {output_path}")


def main() -> None:
    """Main function to create CP Stats SVG."""
    generate_cp_stats_svg(CP_STATS_SVG)


if __name__ == "__main__":
    main()
