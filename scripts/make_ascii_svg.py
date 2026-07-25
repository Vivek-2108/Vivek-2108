#!/usr/bin/env python3
"""
scripts/make_ascii_svg.py

Converts an input profile image into monochrome ASCII text,
and generates a self-typing SVG animation (`ascii.svg`).
"""

import sys
import xml.sax.saxutils as xml_escape
from pathlib import Path
from PIL import Image
from config import ASCII_SVG, ASSETS_DIR, GITHUB_USERNAME

PREPARED_IMAGE = ASSETS_DIR / "prepared.png"

ASCII_RAMP = " .:-=+*#%@"
DEFAULT_CHAR_WIDTH = 58
ASPECT_CORRECTION = 0.55


def image_to_ascii_lines(image_path: Path, num_cols: int = DEFAULT_CHAR_WIDTH) -> list[str]:
    """Load image, resize with aspect ratio correction, map to ASCII ramp characters."""
    if not image_path.is_file():
        print(f"Error: Input image file not found at: {image_path}", file=sys.stderr)
        sys.exit(1)

    img = Image.open(image_path).convert("L")
    w, h = img.size

    num_rows = int((h / w) * num_cols * ASPECT_CORRECTION)
    img_resized = img.resize((num_cols, num_rows), Image.Resampling.LANCZOS)
    pixels = list(img_resized.getdata())

    ramp_len = len(ASCII_RAMP)
    ascii_lines = []

    for r in range(num_rows):
        row_chars = []
        for c in range(num_cols):
            val = pixels[r * num_cols + c]
            char_idx = int((val / 255.0) * (ramp_len - 1))
            row_chars.append(ASCII_RAMP[char_idx])
        ascii_lines.append("".join(row_chars))

    return ascii_lines


def generate_ascii_svg(ascii_lines: list[str], output_path: Path = ASCII_SVG) -> None:
    """Embed ASCII lines inside terminal container SVG with staggered row-by-row typing animation."""
    if not ascii_lines:
        return

    num_rows = len(ascii_lines)

    char_width_px = 7.2
    line_height = 12.5
    header_height = 36
    padding_x = 18
    padding_y = 16

    content_w = int(DEFAULT_CHAR_WIDTH * char_width_px)
    content_h = int(num_rows * line_height)

    width = content_w + (padding_x * 2) + 4
    height = header_height + content_h + (padding_y * 2) + 6

    row_delay_step = 0.05
    typing_duration = 0.15

    svg_parts = []
    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">'
    )
    svg_parts.append("<defs>")
    svg_parts.append("  <style>")
    svg_parts.append("    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&amp;display=swap');")
    svg_parts.append("    .bg { fill: #0d1117; rx: 10px; ry: 10px; stroke: #30363d; stroke-width: 1px; }")
    svg_parts.append("    .header { fill: #161b22; rx: 10px; ry: 10px; }")
    svg_parts.append("    .title { font-family: 'Fira Code', monospace; font-size: 11px; fill: #8b949e; font-weight: 600; }")
    svg_parts.append("    .dot-red { fill: #ff5f56; }")
    svg_parts.append("    .dot-yellow { fill: #ffbd2e; }")
    svg_parts.append("    .dot-green { fill: #27c93f; }")
    
    svg_parts.append("    .ascii-text { font-family: 'Fira Code', monospace; font-size: 10.5px; fill: #39d353; font-weight: 600; white-space: pre; }")
    
    svg_parts.append("    .line { opacity: 0; animation: typeRow 0.15s ease-out forwards; }")
    svg_parts.append("    @keyframes typeRow {")
    svg_parts.append("      0% { opacity: 0; transform: translateX(-4px); }")
    svg_parts.append("      100% { opacity: 1; transform: translateX(0); }")
    svg_parts.append("    }")

    for r_idx in range(num_rows):
        delay = round(r_idx * row_delay_step, 3)
        svg_parts.append(f"    .l-{r_idx} {{ animation-delay: {delay}s; }}")

    total_anim_time = round((num_rows * row_delay_step) + typing_duration, 2)
    svg_parts.append("    .cursor { fill: #39d353; opacity: 0; animation: blinkCursor 0.8s step-end infinite; }")
    svg_parts.append(f"    .cursor-active {{ animation-delay: {total_anim_time}s; opacity: 1; }}")
    svg_parts.append("    @keyframes blinkCursor { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }")

    svg_parts.append("  </style>")
    svg_parts.append("</defs>")

    svg_parts.append(f'<rect class="bg" width="{width}" height="{height}" />')
    svg_parts.append(f'<rect class="header" width="{width}" height="{header_height}" />')
    svg_parts.append('<circle class="dot-red" cx="18" cy="18" r="5" />')
    svg_parts.append('<circle class="dot-yellow" cx="34" cy="18" r="5" />')
    svg_parts.append('<circle class="dot-green" cx="50" cy="18" r="5" />')

    title_str = xml_escape.escape(f"{GITHUB_USERNAME}@terminal:~ $ cat profile_portrait.txt")
    svg_parts.append(f'<text class="title" x="68" y="22">{title_str}</text>')

    start_y = header_height + padding_y + 8
    for idx, raw_line in enumerate(ascii_lines):
        y_pos = start_y + (idx * line_height)
        escaped_line = xml_escape.escape(raw_line)
        svg_parts.append(
            f'<text class="ascii-text line l-{idx}" x="{padding_x}" y="{y_pos:.1f}">{escaped_line}</text>'
        )

    cursor_y = start_y + ((num_rows - 1) * line_height)
    svg_parts.append(
        f'<rect class="cursor cursor-active" x="{padding_x}" y="{cursor_y - 9:.1f}" width="7" height="11" />'
    )

    svg_parts.append("</svg>")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))

    print(f"[make_ascii_svg] Generated ASCII SVG saved to: {output_path}")


def main() -> None:
    """Main entry point to build ASCII portrait SVG."""
    print(f"[make_ascii_svg] Loading image from: {PREPARED_IMAGE}")
    lines = image_to_ascii_lines(PREPARED_IMAGE, DEFAULT_CHAR_WIDTH)
    generate_ascii_svg(lines, ASCII_SVG)


if __name__ == "__main__":
    main()
