#!/usr/bin/env python3
"""
scripts/make_ascii_svg.py

Converts assets/prepared.png (or fallback assets/profile.jpg) into a monochrome ASCII art SVG
with self-typing row-by-row reveal animations, terminal aesthetic, and cursor effect.
Outputs to ascii.svg in the repository root.
"""

import sys
import xml.sax.saxutils as xml_escape
from pathlib import Path
import numpy as np
from PIL import Image

# Directory paths
ROOT_DIR = Path(__file__).resolve().parent.parent
PREPARED_PATH = ROOT_DIR / "assets" / "prepared.png"
FALLBACK_PATH = ROOT_DIR / "assets" / "profile.jpg"
OUTPUT_SVG = ROOT_DIR / "ascii.svg"

# ASCII ramp - dark to light characters for dark background
# ASCII_RAMP = " .:-=+*#%@"
ASCII_RAMP = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

# Configuration defaults
DEFAULT_CHAR_WIDTH = 58  # Characters wide
ASPECT_RATIO_CORRECTION = 0.52  # Monospace height/width ratio adjustment


def image_to_ascii(img: Image.Image, width: int = DEFAULT_CHAR_WIDTH) -> list[str]:
    """Convert a PIL Image to a list of ASCII strings."""
    # Convert image to grayscale
    gray_img = img.convert("L")
    
    # Calculate height maintaining aspect ratio
    orig_w, orig_h = gray_img.size
    aspect = orig_h / orig_w
    height = int(width * aspect * ASPECT_RATIO_CORRECTION)
    
    # Resize image
    resized_img = gray_img.resize((width, height), Image.Resampling.LANCZOS)
    pixels = np.array(resized_img)
    
    # Map pixel values (0-255) to ASCII character ramp
    num_chars = len(ASCII_RAMP)
    ascii_rows = []
    for row in pixels:
        line_chars = []
        for val in row:
            # Map dark pixels to sparse characters, light pixels to dense characters
            idx = int((val / 255.0) * (num_chars - 1))
            line_chars.append(ASCII_RAMP[idx])
        ascii_rows.append("".join(line_chars))
        
    return ascii_rows


def generate_ascii_svg(ascii_lines: list[str], output_path: Path) -> None:
    """Generate SVG document with dark terminal frame and row-by-row CSS typing animation."""
    num_rows = len(ascii_lines)
    max_cols = max(len(line) for line in ascii_lines) if ascii_lines else 0

    # Layout constants
    font_size = 11
    char_width = 6.6
    line_height = 12.5
    padding_x = 24
    header_height = 36
    padding_y = 18

    calc_width = int(max_cols * char_width + padding_x * 2)
    calc_height = int(num_rows * line_height + header_height + padding_y * 2)
    
    width = max(440, calc_width)
    height = calc_height

    # Total animation duration
    delay_per_row = 0.05  # Seconds between row reveals
    total_anim_time = round(num_rows * delay_per_row + 0.5, 2)

    # Build animated SVG XML
    svg_parts = []
    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">'
    )
    svg_parts.append("<defs>")
    svg_parts.append("  <style>")
    svg_parts.append("    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&amp;display=swap');")
    svg_parts.append("    .bg { fill: #0d1117; rx: 10px; ry: 10px; stroke: #30363d; stroke-width: 1px; }")
    svg_parts.append("    .header { fill: #161b22; rx: 10px; ry: 10px; }")
    svg_parts.append("    .title { font-family: 'Fira Code', monospace; font-size: 11px; fill: #8b949e; font-weight: 600; }")
    svg_parts.append("    .dot-red { fill: #ff5f56; }")
    svg_parts.append("    .dot-yellow { fill: #ffbd2e; }")
    svg_parts.append("    .dot-green { fill: #27c93f; }")
    svg_parts.append("    .ascii-text { font-family: 'Fira Code', 'Courier New', monospace; font-size: 11px; fill: #39d353; white-space: pre; }")
    
    # CSS Animation Keyframes
    svg_parts.append("    .line { opacity: 0; animation: typeRow 0.1s ease-out forwards; }")
    svg_parts.append("    @keyframes typeRow {")
    svg_parts.append("      0% { opacity: 0; clip-path: inset(0 100% 0 0); }")
    svg_parts.append("      100% { opacity: 1; clip-path: inset(0 0 0 0); }")
    svg_parts.append("    }")
    
    # Cursor Animation
    svg_parts.append("    .cursor { fill: #39d353; animation: blink 0.8s step-end infinite; }")
    svg_parts.append("    @keyframes blink { 50% { opacity: 0; } }")
    
    # Generate line-specific delay CSS rules
    for idx in range(num_rows):
        delay = round(idx * delay_per_row, 3)
        svg_parts.append(f"    .l-{idx} {{ animation-delay: {delay}s; }}")
        
    svg_parts.append("  </style>")
    svg_parts.append("</defs>")

    # Outer Container Frame
    svg_parts.append(f'<rect class="bg" width="{width}" height="{height}" />')
    
    # Terminal Header Bar
    svg_parts.append(f'<rect class="header" width="{width}" height="{header_height}" />')
    # Header Buttons
    svg_parts.append('<circle class="dot-red" cx="18" cy="18" r="5" />')
    svg_parts.append('<circle class="dot-yellow" cx="34" cy="18" r="5" />')
    svg_parts.append('<circle class="dot-green" cx="50" cy="18" r="5" />')
    # Terminal Title Text
    title_str = xml_escape.escape("vivekjadhav07@terminal:~ $ cat profile_portrait.txt")
    svg_parts.append(f'<text class="title" x="68" y="22">{title_str}</text>')

    # ASCII Text Lines Rendering
    start_y = header_height + padding_y + 8
    for idx, raw_line in enumerate(ascii_lines):
        y_pos = start_y + (idx * line_height)
        escaped_line = xml_escape.escape(raw_line)
        svg_parts.append(
            f'<text class="ascii-text line l-{idx}" x="{padding_x}" y="{y_pos:.1f}">{escaped_line}</text>'
        )

    # Terminal Cursor at the end of ASCII output
    cursor_y = start_y + ((num_rows - 1) * line_height)
    last_line_len = len(ascii_lines[-1]) if ascii_lines else 0
    cursor_x = padding_x + (last_line_len * char_width) + 4
    svg_parts.append(
        f'<rect class="cursor line l-{num_rows - 1}" x="{cursor_x:.1f}" y="{cursor_y - 9:.1f}" width="7" height="11" />'
    )

    svg_parts.append("</svg>")

    # Write SVG output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))

    print(f"[make_ascii_svg] Generated ASCII SVG saved to: {output_path}")


def main() -> None:
    """Main execution entrypoint for ASCII SVG creation."""
    target_img_path = PREPARED_PATH if PREPARED_PATH.exists() else FALLBACK_PATH
    if not target_img_path.exists():
        print(f"Error: Neither '{PREPARED_PATH}' nor '{FALLBACK_PATH}' exists.", file=sys.stderr)
        sys.exit(1)

    print(f"[make_ascii_svg] Loading image from: {target_img_path}")
    img = Image.open(target_img_path)
    
    ascii_rows = image_to_ascii(img, width=DEFAULT_CHAR_WIDTH)
    generate_ascii_svg(ascii_rows, OUTPUT_SVG)


if __name__ == "__main__":
    main()
