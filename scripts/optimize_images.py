#!/usr/bin/env python3
"""Batch-optimize product images to WebP at 85% quality, max 1200px wide."""

import os
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PRODUCTS_DIR = ROOT / "public" / "images" / "products"
MAX_WIDTH = 1200
QUALITY = 85


def optimize_one(jpg_path: Path):
    webp_path = jpg_path.with_suffix(".webp")
    original_bytes = jpg_path.stat().st_size

    with Image.open(jpg_path) as im:
        im = im.convert("RGB")
        if im.width > MAX_WIDTH:
            new_height = int(im.height * (MAX_WIDTH / im.width))
            im = im.resize((MAX_WIDTH, new_height), Image.LANCZOS)
        im.save(webp_path, "WEBP", quality=QUALITY, method=6)

    new_bytes = webp_path.stat().st_size
    return original_bytes, new_bytes


def main():
    if not PRODUCTS_DIR.exists():
        print(f"ERROR: {PRODUCTS_DIR} does not exist", file=sys.stderr)
        sys.exit(1)

    jpgs = sorted(PRODUCTS_DIR.glob("*.jpg"))
    if not jpgs:
        print("No .jpg files found")
        return

    print(f"Optimizing {len(jpgs)} images...")
    total_orig = 0
    total_new = 0
    for jpg in jpgs:
        try:
            orig, new = optimize_one(jpg)
            total_orig += orig
            total_new += new
            savings_pct = (1 - new / orig) * 100 if orig else 0
            print(f"  {jpg.name}: {orig/1024:.0f} KB -> {new/1024:.0f} KB ({savings_pct:.1f}% smaller)")
        except Exception as e:
            print(f"  {jpg.name}: FAILED ({e})", file=sys.stderr)

    print()
    print(f"Total original:  {total_orig/1024/1024:.2f} MB ({total_orig:,} bytes)")
    print(f"Total optimized: {total_new/1024/1024:.2f} MB ({total_new:,} bytes)")
    if total_orig:
        print(f"Savings:         {(total_orig - total_new)/1024/1024:.2f} MB ({(1 - total_new/total_orig)*100:.1f}%)")


if __name__ == "__main__":
    main()
