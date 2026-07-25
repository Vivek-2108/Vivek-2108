#!/usr/bin/env python3
"""
scripts/prep_photo.py

Pipeline to process profile image for ASCII art generation:
1. Removes background using rembg.
2. Composites subject over a solid white background.
3. Enhances contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization).
4. Saves processed grayscale image to assets/prepared.png.
"""

import io
import sys
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
from rembg import remove

# Define directory constants relative to repository root
ROOT_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = ROOT_DIR / "assets" / "profile.jpg"
OUTPUT_PATH = ROOT_DIR / "assets" / "prepared.png"


def prepare_photo(input_path: Path, output_path: Path) -> None:
    """Preprocess image with background removal, compositing, and CLAHE contrast enhancement."""
    # Support .png, .jpg, .jpeg automatically
    if not input_path.exists():
        for ext in [".png", ".jpeg", ".jpg"]:
            alt_path = input_path.with_suffix(ext)
            if alt_path.exists():
                input_path = alt_path
                break

    if not input_path.exists():
        print(f"Error: Input photo file '{input_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    print(f"[prep_photo] Loading input image: {input_path}")
    with open(input_path, "rb") as f:
        input_bytes = f.read()

    print("[prep_photo] Removing background with rembg...")
    output_bytes = remove(input_bytes)

    # Load PNG with transparency into PIL
    img_rgba = Image.open(io.BytesIO(output_bytes)).convert("RGBA")

    # Create solid white background and composite subject over it
    background = Image.new("RGBA", img_rgba.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(background, img_rgba).convert("L")  # Grayscale

    # Convert PIL grayscale image to NumPy array for OpenCV CLAHE processing
    gray_array = np.array(composited)

    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) for crisp edges
    print("[prep_photo] Enhancing contrast using CLAHE...")
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    enhanced_array = clahe.apply(gray_array)

    # Save output image
    output_path.parent.mkdir(parents=True, exist_ok=True)
    enhanced_img = Image.fromarray(enhanced_array)
    enhanced_img.save(output_path, "PNG")
    print(f"[prep_photo] Prepared photo saved successfully: {output_path}")


if __name__ == "__main__":
    prepare_photo(INPUT_PATH, OUTPUT_PATH)
