#!/usr/bin/env python3
"""
scripts/make_info_card.py

Generates a Neofetch-style terminal info card as an SVG document (`info-card.svg`).
Features line-by-line slide & fade animations, color badges, and customizable profile data dictionary.
"""

import sys
import xml.sax.saxutils as xml_escape
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_SVG = ROOT_DIR / "info-card.svg"

# Profile Data Dictionary - Modify fields here to customize your Neofetch Card!
PROFILE_DATA = {
    "whoami": "vivekjadhav07",
    "name": "Vivek Jadhav",
    "role": "Full Stack & Android Developer",
    "education": "Information Technology / CS",
    "location": "India",
    "stack": {
        "Languages": "Java, Python, JavaScript, SQL",
        "Backend": "Java, Node.js, Express, Firebase",
        "Frontend": "Angular, React, HTML5, CSS3",
        "DevOps": "Git, GitHub Actions, Vercel",
        "Databases": "MySQL, MongoDB, Supabase",
        "Tools": "Figma, Canva, Postman, VS Code",
    },
    "achievements": "Building scalable web apps & real-world projects",
    "building": "Interactive web tools & DSA problem solving",
}


def generate_info_card_svg(data: dict, output_path: Path) -> None:
    """Generate Neofetch terminal card SVG with CSS staggered fade-in animations."""
    # Build list of lines to render
    lines = []
    
    # Header command
    lines.append(("cmd", "$ whoami"))
    lines.append(("separator", "----------------------------------------"))
    
    # Core fields
    lines.append(("key_val", ("Name", data.get("name", ""))))
    lines.append(("key_val", ("Role", data.get("role", ""))))
    lines.append(("key_val", ("Education", data.get("education", ""))))
    lines.append(("key_val", ("Location", data.get("location", ""))))
    lines.append(("separator", ""))
    
    # Stack section
    lines.append(("section", "STACK"))
    stack = data.get("stack", {})
    for category, skills in stack.items():
        lines.append(("sub_key_val", (category, skills)))
        
    lines.append(("separator", ""))
    # Additional metadata
    lines.append(("key_val", ("Achievements", data.get("achievements", ""))))
    lines.append(("key_val", ("Building", data.get("building", ""))))
    
    # Terminal color blocks row at bottom
    lines.append(("color_blocks", ""))

    # Layout measurements
    width = 460
    header_height = 36
    padding_x = 22
    padding_y = 16
    line_height = 20

    calc_height = header_height + padding_y * 2 + (len(lines) * line_height) + 10
    height = int(calc_height)

    # Delay per line for staggered animation
    delay_step = 0.05

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
    
    # Text styles
    svg_parts.append("    .txt { font-family: 'Fira Code', monospace; font-size: 12px; }")
    svg_parts.append("    .cmd { fill: #58a6ff; font-weight: 700; }")
    svg_parts.append("    .sep { fill: #30363d; }")
    svg_parts.append("    .key { fill: #79c0ff; font-weight: 600; }")
    svg_parts.append("    .sub-key { fill: #d2a8ff; font-weight: 600; }")
    svg_parts.append("    .val { fill: #c9d1d9; }")
    svg_parts.append("    .section-head { fill: #ffa657; font-weight: 700; letter-spacing: 1px; }")
    
    # Animation keyframes: fade-in and slight slide up
    svg_parts.append("    .line-anim { opacity: 0; animation: slideFadeIn 0.35s ease-out forwards; }")
    svg_parts.append("    @keyframes slideFadeIn {")
    svg_parts.append("      0% { opacity: 0; transform: translateY(6px); }")
    svg_parts.append("      100% { opacity: 1; transform: translateY(0); }")
    svg_parts.append("    }")
    
    # Delays
    for idx in range(len(lines)):
        delay = round(idx * delay_step, 3)
        svg_parts.append(f"    .l-{idx} {{ animation-delay: {delay}s; }}")
        
    svg_parts.append("  </style>")
    svg_parts.append("</defs>")

    # Background frame
    svg_parts.append(f'<rect class="bg" width="{width}" height="{height}" />')
    
    # Header bar
    svg_parts.append(f'<rect class="header" width="{width}" height="{header_height}" />')
    svg_parts.append('<circle class="dot-red" cx="18" cy="18" r="5" />')
    svg_parts.append('<circle class="dot-yellow" cx="34" cy="18" r="5" />')
    svg_parts.append('<circle class="dot-green" cx="50" cy="18" r="5" />')
    
    window_title = xml_escape.escape("vivekjadhav07@terminal:~ $ neofetch")
    svg_parts.append(f'<text class="title" x="68" y="22">{window_title}</text>')

    # Content Rendering
    start_y = header_height + padding_y + 12
    for idx, (line_type, content) in enumerate(lines):
        y_pos = start_y + (idx * line_height)
        
        if line_type == "cmd":
            escaped = xml_escape.escape(str(content))
            svg_parts.append(
                f'<text class="txt cmd line-anim l-{idx}" x="{padding_x}" y="{y_pos}">{escaped}</text>'
            )
        elif line_type == "separator":
            escaped = xml_escape.escape(str(content))
            svg_parts.append(
                f'<text class="txt sep line-anim l-{idx}" x="{padding_x}" y="{y_pos}">{escaped}</text>'
            )
        elif line_type == "section":
            escaped = xml_escape.escape(str(content))
            svg_parts.append(
                f'<text class="txt section-head line-anim l-{idx}" x="{padding_x}" y="{y_pos}"> {escaped}</text>'
            )
        elif line_type in ("key_val", "sub_key_val"):
            key, val = content
            escaped_key = xml_escape.escape(f"{key}:")
            escaped_val = xml_escape.escape(str(val))
            
            key_class = "key" if line_type == "key_val" else "sub-key"
            x_offset = padding_x if line_type == "key_val" else padding_x + 10
            val_x = x_offset + (len(key) * 8.5) + 18
            
            svg_parts.append(
                f'<g class="line-anim l-{idx}">'
                f'<text class="txt {key_class}" x="{x_offset}" y="{y_pos}">{escaped_key}</text>'
                f'<text class="txt val" x="{val_x:.1f}" y="{y_pos}">{escaped_val}</text>'
                f'</g>'
            )
        elif line_type == "color_blocks":
            # Render terminal color palette bar
            colors = ["#ff5f56", "#ffbd2e", "#27c93f", "#58a6ff", "#bc8cff", "#39d353", "#f0883e"]
            block_group = [f'<g class="line-anim l-{idx}">']
            block_width = 24
            block_height = 10
            for c_idx, hex_color in enumerate(colors):
                bx = padding_x + (c_idx * (block_width + 6))
                block_group.append(
                    f'<rect x="{bx}" y="{y_pos - 8}" width="{block_width}" height="{block_height}" rx="2" fill="{hex_color}" />'
                )
            block_group.append("</g>")
            svg_parts.append("".join(block_group))

    svg_parts.append("</svg>")

    # Save SVG
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))

    print(f"[make_info_card] Neofetch info card SVG saved to: {output_path}")


def main() -> None:
    """Main function to create Neofetch Info Card SVG."""
    generate_info_card_svg(PROFILE_DATA, OUTPUT_SVG)


if __name__ == "__main__":
    main()
