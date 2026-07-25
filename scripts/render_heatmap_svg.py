#!/usr/bin/env python3
"""
scripts/render_heatmap_svg.py

Reads data/contributions.json and generates `contrib-heatmap.svg` featuring:
- 53-week GitHub contribution calendar layout with rounded cells.
- Terminal theme header with live stats (Total Contributions, Current Streak, Longest Streak).
- Animated diagonal cell reveal using CSS keyframes and staggered delays.
- Month and day labels with Less -> More color legend.
"""

import json
import sys
import xml.sax.saxutils as xml_escape
from datetime import datetime
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parent.parent
INPUT_JSON = ROOT_DIR / "data" / "contributions.json"
OUTPUT_SVG = ROOT_DIR / "contrib-heatmap.svg"

# Color Palette - GitHub Dark Mode Green Theme
COLOR_MAP = {
    0: "#161b22",  # Empty cell
    1: "#0e4429",  # Low
    2: "#006d32",  # Medium-low
    3: "#26a641",  # Medium-high
    4: "#39d353",  # High
}

STROKE_MAP = {
    0: "#21262d",
    1: "#0e4429",
    2: "#006d32",
    3: "#26a641",
    4: "#39d353",
}

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def load_contributions_data(input_path: Path) -> dict:
    """Load json data from input file."""
    if not input_path.exists():
        print(f"Error: Contributions data file '{input_path}' not found.", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_heatmap_svg(data: dict, output_path: Path) -> None:
    """Render animated SVG heatmap from contribution data."""
    days = data.get("days", [])
    total_contribs = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)

    # Layout dimensions & coordinates
    width = 830
    header_bar_height = 36
    stats_bar_height = 42
    padding_x = 35
    grid_start_y = header_bar_height + stats_bar_height + 30
    cell_size = 11
    cell_gap = 3
    step = cell_size + cell_gap  # 14px step

    # Calculate grid bounds
    # Organise days into 53 weeks x 7 days
    num_weeks = 53
    grid_cells = []
    month_labels = []

    last_month = None

    for idx, day_info in enumerate(days):
        col = idx // 7
        row = idx % 7

        if col >= num_weeks:
            break

        # Check for month label at the start of a week
        date_str = day_info.get("date", "")
        if date_str:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            month_num = dt.month
            if row == 0 and month_num != last_month:
                month_labels.append((col, MONTH_NAMES[month_num - 1]))
                last_month = month_num

        grid_cells.append({
            "col": col,
            "row": row,
            "date": date_str,
            "count": day_info.get("count", 0),
            "level": day_info.get("level", 0),
        })

    grid_height = (7 * step)
    footer_height = 40
    height = grid_start_y + grid_height + footer_height

    svg_parts = []
    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">'
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
    
    # Stats card fonts
    svg_parts.append("    .stat-label { font-family: 'Fira Code', monospace; font-size: 10px; fill: #8b949e; font-weight: 500; }")
    svg_parts.append("    .stat-val { font-family: 'Fira Code', monospace; font-size: 14px; fill: #39d353; font-weight: 700; }")
    svg_parts.append("    .stat-box { fill: #161b22; stroke: #21262d; rx: 6px; }")
    
    # Axis & legend text
    svg_parts.append("    .lbl { font-family: 'Fira Code', monospace; font-size: 10px; fill: #7d8590; }")
    
    # Heatmap Cell Animations: Diagonal pop & scale-in
    svg_parts.append("    .cell { transform-origin: center; opacity: 0; animation: diagReveal 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; }")
    svg_parts.append("    @keyframes diagReveal {")
    svg_parts.append("      0% { opacity: 0; transform: scale(0.2); }")
    svg_parts.append("      100% { opacity: 1; transform: scale(1); }")
    svg_parts.append("    }")

    # Generate CSS rules for diagonal animation delays
    for c in range(num_weeks):
        for r in range(7):
            delay = round((c * 0.015) + (r * 0.015), 3)
            svg_parts.append(f"    .d-{c}-{r} {{ animation-delay: {delay}s; }}")

    svg_parts.append("  </style>")
    svg_parts.append("</defs>")

    # Main Card Frame
    svg_parts.append(f'<rect class="bg" width="{width}" height="{height}" />')

    # Header Bar
    svg_parts.append(f'<rect class="header" width="{width}" height="{header_bar_height}" />')
    svg_parts.append('<circle class="dot-red" cx="18" cy="18" r="5" />')
    svg_parts.append('<circle class="dot-yellow" cx="34" cy="18" r="5" />')
    svg_parts.append('<circle class="dot-green" cx="50" cy="18" r="5" />')

    window_title = xml_escape.escape("Vivek-2108@terminal:~ $ cat contributions.sh")
    svg_parts.append(f'<text class="title" x="68" y="22">{window_title}</text>')

    # Stats Summary Cards (Top Section)
    stats = [
        ("TOTAL CONTRIBUTIONS", f"{total_contribs} Year"),
        ("CURRENT STREAK", f"🔥 {current_streak} Days"),
        ("LONGEST STREAK", f"⚡ {longest_streak} Days"),
    ]

    card_width = 240
    card_height = 36
    start_x = padding_x
    card_y = header_bar_height + 12

    for idx, (label, val) in enumerate(stats):
        cx = start_x + (idx * (card_width + 15))
        svg_parts.append(f'<rect class="stat-box" x="{cx}" y="{card_y}" width="{card_width}" height="{card_height}" />')
        svg_parts.append(f'<text class="stat-label" x="{cx + 12}" y="{card_y + 15}">{label}</text>')
        svg_parts.append(f'<text class="stat-val" x="{cx + 12}" y="{card_y + 30}">{val}</text>')

    # Day of week labels on left (Mon, Wed, Fri)
    day_labels = [(1, "Mon"), (3, "Wed"), (5, "Fri")]
    for row_idx, label in day_labels:
        ly = grid_start_y + (row_idx * step) + 9
        svg_parts.append(f'<text class="lbl" x="{padding_x - 24}" y="{ly}">{label}</text>')

    # Month Labels (Top of grid)
    month_y = grid_start_y - 10
    for col_idx, m_name in month_labels:
        mx = padding_x + (col_idx * step)
        svg_parts.append(f'<text class="lbl" x="{mx}" y="{month_y}">{m_name}</text>')

    # Grid Cells
    for cell in grid_cells:
        c = cell["col"]
        r = cell["row"]
        level = min(4, max(0, cell["level"]))
        fill_color = COLOR_MAP.get(level, COLOR_MAP[0])
        stroke_color = STROKE_MAP.get(level, STROKE_MAP[0])

        cx = padding_x + (c * step)
        cy = grid_start_y + (r * step)

        svg_parts.append(
            f'<rect class="cell d-{c}-{r}" x="{cx}" y="{cy}" width="{cell_size}" height="{cell_size}" rx="2" fill="{fill_color}" stroke="{stroke_color}" stroke-width="0.5" />'
        )

    # Footer Legend (Less -> More)
    footer_y = grid_start_y + grid_height + 22
    legend_end_x = width - padding_x
    legend_start_x = legend_end_x - 145

    svg_parts.append(f'<text class="lbl" x="{legend_start_x - 30}" y="{footer_y + 9}">Less</text>')
    for l_idx in range(5):
        lx = legend_start_x + (l_idx * 15)
        l_fill = COLOR_MAP[l_idx]
        l_stroke = STROKE_MAP[l_idx]
        svg_parts.append(
            f'<rect x="{lx}" y="{footer_y}" width="11" height="11" rx="2" fill="{l_fill}" stroke="{l_stroke}" stroke-width="0.5" />'
        )
    svg_parts.append(f'<text class="lbl" x="{legend_start_x + 80}" y="{footer_y + 9}">More</text>')

    svg_parts.append("</svg>")

    # Write output SVG
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))

    print(f"[render_heatmap_svg] Generated contribution heatmap SVG: {output_path}")


def main() -> None:
    """Main rendering entrypoint."""
    data = load_contributions_data(INPUT_JSON)
    generate_heatmap_svg(data, OUTPUT_SVG)


if __name__ == "__main__":
    main()
