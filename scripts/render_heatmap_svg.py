#!/usr/bin/env python3
"""
scripts/render_heatmap_svg.py

Generates an animated vector SVG calendar (`contrib-heatmap.svg`) based on GitHub contribution graph dataset.
Features rounded calendar cells, metric summary boxes, diagonal reveal animations, and dark GitHub palette.
"""

import json
import sys
import xml.sax.saxutils as xml_escape
from datetime import datetime, timedelta
from pathlib import Path
from config import CONTRIBUTIONS_JSON, GITHUB_USERNAME, HEATMAP_SVG

# Dark Mode Color Palette
COLOR_MAP = {
    0: "#161b22",
    1: "#0e4429",
    2: "#006d32",
    3: "#26a641",
    4: "#39d353",
}

CELL_SIZE = 11
CELL_GAP = 3
HEADER_HEIGHT = 36
PADDING_X = 22
PADDING_Y = 16


def load_contributions(filepath: Path) -> dict:
    """Load JSON contribution dataset or return fallback empty dict."""
    if not filepath.is_file():
        print(f"Warning: Contribution file not found at {filepath}", file=sys.stderr)
        return {}

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def build_calendar_grid(days: list[dict]) -> tuple[list[list[dict]], list[tuple[int, str]]]:
    """Group 365 daily objects into 53 weekly columns of 7 days (Sunday to Saturday)."""
    if not days:
        return [], []

    date_dict = {d["date"]: d for d in days}
    sorted_dates = sorted(date_dict.keys())
    start_dt = datetime.strptime(sorted_dates[0], "%Y-%m-%d")
    end_dt = datetime.strptime(sorted_dates[-1], "%Y-%m-%d")

    curr_dt = start_dt - timedelta(days=(start_dt.weekday() + 1) % 7)

    weeks = []
    month_labels = []

    current_week = []
    week_idx = 0
    last_month = None

    while curr_dt <= end_dt or len(current_week) > 0:
        d_str = curr_dt.strftime("%Y-%m-%d")
        month_str = curr_dt.strftime("%b")

        if curr_dt.day <= 7 and month_str != last_month:
            month_labels.append((week_idx, month_str))
            last_month = month_str

        day_obj = date_dict.get(d_str, {"date": d_str, "count": 0, "level": 0})
        current_week.append(day_obj)

        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []
            week_idx += 1

        curr_dt += timedelta(days=1)

        if curr_dt > end_dt + timedelta(days=7) and len(current_week) == 0:
            break

    return weeks, month_labels


def generate_heatmap_svg(data: dict, output_path: Path = HEATMAP_SVG) -> None:
    """Generate animated contribution graph heatmap SVG with CSS keyframe transitions."""
    days = data.get("days", [])
    total_contribs = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)

    weeks, month_labels = build_calendar_grid(days)
    num_weeks = max(len(weeks), 53)

    grid_width = num_weeks * (CELL_SIZE + CELL_GAP)
    width = PADDING_X * 2 + grid_width + 40
    header_bar_height = 36
    stats_card_height = 42

    calendar_y_start = header_bar_height + PADDING_Y + stats_card_height + 24
    grid_height = 7 * (CELL_SIZE + CELL_GAP)
    height = calendar_y_start + grid_height + PADDING_Y + 16

    svg_parts = []
    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}">'
    )
    svg_parts.append("<defs>")
    svg_parts.append("  <style>")
    svg_parts.append("    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&amp;display=swap');")
    svg_parts.append("    .bg { fill: #0d1117; rx: 10px; ry: 10px; stroke: #30363d; stroke-width: 1px; }")
    svg_parts.append("    .header { fill: #161b22; rx: 10px; ry: 10px; }")
    svg_parts.append("    .title { font-family: 'Fira Code', monospace; font-size: 11px; fill: #8b949e; font-weight: 600; }")
    svg_parts.append("    .dot-red { fill: #ff5f56; }")
    svg_parts.append("    .dot-yellow { fill: #ffbd2e; }")
    svg_parts.append("    .dot-green { fill: #27c93f; }")
    
    svg_parts.append("    .stat-card { fill: #161b22; rx: 6px; ry: 6px; stroke: #21262d; stroke-width: 1px; }")
    svg_parts.append("    .stat-label { font-family: 'Fira Code', monospace; font-size: 9.5px; fill: #8b949e; font-weight: 600; }")
    svg_parts.append("    .stat-val { font-family: 'Fira Code', monospace; font-size: 13px; fill: #39d353; font-weight: 700; }")
    
    svg_parts.append("    .lbl { font-family: 'Fira Code', monospace; font-size: 10px; fill: #7d8590; }")
    svg_parts.append("    .day-cell { rx: 2px; ry: 2px; opacity: 0; animation: cellScale 0.3s ease-out forwards; }")
    
    svg_parts.append("    @keyframes cellScale {")
    svg_parts.append("      0% { opacity: 0; transform: scale(0.3); }")
    svg_parts.append("      100% { opacity: 1; transform: scale(1); }")
    svg_parts.append("    }")

    for w_idx in range(num_weeks):
        for d_idx in range(7):
            delay = round((w_idx * 0.012) + (d_idx * 0.008), 3)
            svg_parts.append(f"    .c-{w_idx}-{d_idx} {{ animation-delay: {delay}s; transform-origin: center; }}")

    svg_parts.append("  </style>")
    svg_parts.append("</defs>")

    svg_parts.append(f'<rect class="bg" width="{width}" height="{height}" />')
    svg_parts.append(f'<rect class="header" width="{width}" height="{header_bar_height}" />')
    svg_parts.append('<circle class="dot-red" cx="18" cy="18" r="5" />')
    svg_parts.append('<circle class="dot-yellow" cx="34" cy="18" r="5" />')
    svg_parts.append('<circle class="dot-green" cx="50" cy="18" r="5" />')

    window_title = xml_escape.escape(f"{GITHUB_USERNAME}@terminal:~ $ cat contributions.sh")
    svg_parts.append(f'<text class="title" x="68" y="22">{window_title}</text>')

    # Stats Summary Cards
    stats = [
        ("TOTAL CONTRIBUTIONS", f"{total_contribs} Year"),
        ("CURRENT STREAK", f"🔥 {current_streak} Days"),
        ("LONGEST STREAK", f"⚡ {longest_streak} Days"),
    ]

    card_width = 240
    card_height = 36
    start_x = PADDING_X
    gap = 14

    for idx, (label, val_str) in enumerate(stats):
        cx = start_x + idx * (card_width + gap)
        cy = header_bar_height + PADDING_Y
        svg_parts.append(f'<rect class="stat-card" x="{cx}" y="{cy}" width="{card_width}" height="{card_height}" />')
        svg_parts.append(f'<text class="stat-label" x="{cx + 12}" y="{cy + 15}">{label}</text>')
        svg_parts.append(f'<text class="stat-val" x="{cx + 12}" y="{cy + 30}">{val_str}</text>')

    # Month Labels
    label_y = calendar_y_start - 8
    start_grid_x = PADDING_X + 28

    for w_idx, m_str in month_labels:
        mx = start_grid_x + (w_idx * (CELL_SIZE + CELL_GAP))
        svg_parts.append(f'<text class="lbl" x="{mx}" y="{label_y}">{m_str}</text>')

    # Day of week labels (Mon, Wed, Fri)
    day_labels = [("Mon", 1), ("Wed", 3), ("Fri", 5)]
    for d_name, d_idx in day_labels:
        dy = calendar_y_start + (d_idx * (CELL_SIZE + CELL_GAP)) + 9
        svg_parts.append(f'<text class="lbl" x="{PADDING_X}" y="{dy}">{d_name}</text>')

    # Calendar Cells Grid
    for w_idx, week in enumerate(weeks):
        cx = start_grid_x + (w_idx * (CELL_SIZE + CELL_GAP))
        for d_idx, day in enumerate(week):
            cy = calendar_y_start + (d_idx * (CELL_SIZE + CELL_GAP))
            lvl = day.get("level", 0)
            fill_color = COLOR_MAP.get(lvl, COLOR_MAP[0])
            count = day.get("count", 0)
            date_str = day.get("date", "")

            title_tip = f"{count} contributions on {date_str}"
            svg_parts.append(
                f'<rect class="day-cell c-{w_idx}-{d_idx}" x="{cx}" y="{cy}" width="{CELL_SIZE}" height="{CELL_SIZE}" fill="{fill_color}">'
                f'<title>{title_tip}</title>'
                f'</rect>'
            )

    # Heatmap Legend at bottom
    legend_y = height - 12
    legend_x_start = width - PADDING_X - 120
    svg_parts.append(f'<text class="lbl" x="{legend_x_start - 30}" y="{legend_y + 9}">Less</text>')
    for lvl in range(5):
        lx = legend_x_start + (lvl * (CELL_SIZE + 2))
        svg_parts.append(
            f'<rect x="{lx}" y="{legend_y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" fill="{COLOR_MAP[lvl]}" />'
        )
    svg_parts.append(f'<text class="lbl" x="{legend_x_start + (5 * (CELL_SIZE + 2)) + 6}" y="{legend_y + 9}">More</text>')

    svg_parts.append("</svg>")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))

    print(f"[render_heatmap_svg] Generated contribution heatmap SVG: {output_path}")


def main() -> None:
    """Main function to render heatmap SVG."""
    data = load_contributions(CONTRIBUTIONS_JSON)
    generate_heatmap_svg(data, HEATMAP_SVG)


if __name__ == "__main__":
    main()
