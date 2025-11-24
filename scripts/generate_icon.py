#!/usr/bin/env python3
"""Generate simple project icons (PNG) from a project name.

Creates a set of square PNGs at common icon sizes in an output directory.
Background color is derived deterministically from the project name.
The icon contains the project's initials centered.

Usage: python3 scripts/generate_icon.py "Project Name" --out path/to/outdir
"""

from __future__ import annotations

import hashlib
import os
import sys
import argparse
import colorsys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def initials(name: str) -> str:
    parts = [p for p in name.strip().split() if p]
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[1][0]).upper()


def color_from_name(name: str) -> tuple[int, int, int]:
    h = hashlib.sha1(name.encode("utf8")).hexdigest()
    # take part of hash to produce a hue
    hv = int(h[:8], 16) % 360
    # convert hue to rgb via hsv with moderate saturation/value
    r, g, b = colorsys.hsv_to_rgb(hv / 360.0, 0.55, 0.95)
    return (int(r * 255), int(g * 255), int(b * 255))


SIZES = [1024, 512, 256, 192, 128, 96, 64, 48, 32, 24, 16]


def load_font(size: int) -> ImageFont.FreeTypeFont:
    # Try to load a common TTF; fall back to default if not present
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()


def generate_icon(name: str, outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    text = initials(name)
    bg = color_from_name(name)
    for size in SIZES:
        img = Image.new("RGBA", (size, size), bg + (255,))
        draw = ImageDraw.Draw(img)

        # font size tuned to image size
        font_size = int(size * 0.42)
        font = load_font(font_size)

        # measure text and draw centered
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
        except Exception:
            try:
                w, h = font.getsize(text)
            except Exception:
                w, h = (size * 0.5, size * 0.5)
        x = (size - w) / 2
        y = (size - h) / 2 - int(size * 0.03)

        # text color: choose white or dark depending on bg brightness
        brightness = (bg[0] * 0.299 + bg[1] * 0.587 + bg[2] * 0.114)
        text_color = (255, 255, 255) if brightness < 200 else (24, 24, 24)

        draw.text((x, y), text, font=font, fill=text_color)

        outpath = outdir / f"icon_{size}x{size}.png"
        img.save(outpath, optimize=True)

    # Save a simple manifest / preview
    try:
        preview = Image.open(outdir / f"icon_{SIZES[1]}x{SIZES[1]}.png")
        preview.save(outdir / "icon.png")
    except Exception:
        pass


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Generate project icons from name")
    p.add_argument("name", help="Project name (used to derive colors and initials)")
    p.add_argument("--out", "-o", required=True, help="Output directory for icons")
    args = p.parse_args(argv)

    outdir = Path(args.out)
    generate_icon(args.name, outdir)
    print(f"Generated icons for '{args.name}' in {outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
