#!/usr/bin/env python3
"""Sprite generation utilities.

Copy this file to your project's generator/lib/ folder.

Requires: pip install pillow numpy
"""
import numpy as np
from PIL import Image
from typing import Tuple, List, Dict

Color = Tuple[int, int, int, int]  # RGBA


# === Common Palettes ===

PALETTES: Dict[str, List[Color]] = {
    'pico8': [
        (0, 0, 0, 255),        # black
        (29, 43, 83, 255),     # dark blue
        (126, 37, 83, 255),    # dark purple
        (0, 135, 81, 255),     # dark green
        (171, 82, 54, 255),    # brown
        (95, 87, 79, 255),     # dark gray
        (194, 195, 199, 255),  # light gray
        (255, 241, 232, 255),  # white
        (255, 0, 77, 255),     # red
        (255, 163, 0, 255),    # orange
        (255, 236, 39, 255),   # yellow
        (0, 228, 54, 255),     # green
        (41, 173, 255, 255),   # blue
        (131, 118, 156, 255),  # lavender
        (255, 119, 168, 255),  # pink
        (255, 204, 170, 255),  # peach
    ],
    'nes': [
        (0, 0, 0, 255),        # black
        (252, 252, 252, 255),  # white
        (248, 56, 0, 255),     # red
        (0, 168, 0, 255),      # green
        (0, 88, 248, 255),     # blue
        (248, 184, 0, 255),    # yellow
        (148, 148, 148, 255),  # gray
        (0, 168, 68, 255),     # dark green
    ],
    'gameboy': [
        (15, 56, 15, 255),     # darkest
        (48, 98, 48, 255),     # dark
        (139, 172, 15, 255),   # light
        (155, 188, 15, 255),   # lightest
    ],
    'grayscale': [
        (0, 0, 0, 255),
        (85, 85, 85, 255),
        (170, 170, 170, 255),
        (255, 255, 255, 255),
    ],
}


def get_palette(name: str) -> List[Color]:
    """Get a named palette."""
    return PALETTES.get(name, PALETTES['pico8'])


# === Color Quantization ===

def find_nearest_color(color: Color, palette: List[Color]) -> Color:
    """Find the nearest color in a palette using Euclidean distance."""
    min_dist = float('inf')
    nearest = palette[0]

    for p in palette:
        dist = sum((a - b) ** 2 for a, b in zip(color[:3], p[:3]))
        if dist < min_dist:
            min_dist = dist
            nearest = p

    return nearest


def quantize_image(img: np.ndarray, palette: List[Color]) -> np.ndarray:
    """Quantize an image to a palette."""
    result = np.zeros_like(img)

    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            result[y, x] = find_nearest_color(tuple(img[y, x]), palette)

    return result


# === Dithering ===

BAYER_2X2 = np.array([
    [0, 2],
    [3, 1],
]) / 4

BAYER_4X4 = np.array([
    [0, 8, 2, 10],
    [12, 4, 14, 6],
    [3, 11, 1, 9],
    [15, 7, 13, 5],
]) / 16

BAYER_8X8 = np.array([
    [0, 32, 8, 40, 2, 34, 10, 42],
    [48, 16, 56, 24, 50, 18, 58, 26],
    [12, 44, 4, 36, 14, 46, 6, 38],
    [60, 28, 52, 20, 62, 30, 54, 22],
    [3, 35, 11, 43, 1, 33, 9, 41],
    [51, 19, 59, 27, 49, 17, 57, 25],
    [15, 47, 7, 39, 13, 45, 5, 37],
    [63, 31, 55, 23, 61, 29, 53, 21],
]) / 64


def bayer_dither(img: np.ndarray, palette: List[Color],
                 matrix: np.ndarray = BAYER_4X4,
                 spread: float = 0.5) -> np.ndarray:
    """Apply ordered Bayer dithering."""
    result = np.zeros_like(img)
    h, w = img.shape[:2]
    mh, mw = matrix.shape

    for y in range(h):
        for x in range(w):
            threshold = (matrix[y % mh, x % mw] - 0.5) * spread * 255
            dithered = tuple(
                max(0, min(255, int(img[y, x, c] + threshold)))
                for c in range(3)
            ) + (img[y, x, 3],)
            result[y, x] = find_nearest_color(dithered, palette)

    return result


def floyd_steinberg_dither(img: np.ndarray, palette: List[Color]) -> np.ndarray:
    """Apply Floyd-Steinberg error diffusion dithering."""
    result = img.astype(np.float32).copy()
    h, w = img.shape[:2]

    for y in range(h):
        for x in range(w):
            old_pixel = result[y, x].copy()
            new_pixel = np.array(find_nearest_color(tuple(old_pixel.astype(int)), palette))
            result[y, x] = new_pixel

            error = old_pixel - new_pixel

            # Distribute error
            if x + 1 < w:
                result[y, x + 1] += error * 7 / 16
            if y + 1 < h:
                if x > 0:
                    result[y + 1, x - 1] += error * 3 / 16
                result[y + 1, x] += error * 5 / 16
                if x + 1 < w:
                    result[y + 1, x + 1] += error * 1 / 16

    return np.clip(result, 0, 255).astype(np.uint8)


# === Sprite Sheet Utilities ===

def create_sprite_sheet(sprites: List[np.ndarray],
                        columns: int = 4) -> np.ndarray:
    """Combine sprites into a sprite sheet.

    Args:
        sprites: List of sprite images (must be same size)
        columns: Number of columns in the sheet

    Returns:
        Combined sprite sheet as numpy array
    """
    if not sprites:
        raise ValueError("No sprites provided")

    sprite_h, sprite_w = sprites[0].shape[:2]
    rows = (len(sprites) + columns - 1) // columns

    sheet = np.zeros((rows * sprite_h, columns * sprite_w, 4), dtype=np.uint8)

    for i, sprite in enumerate(sprites):
        row = i // columns
        col = i % columns
        y = row * sprite_h
        x = col * sprite_w
        sheet[y:y + sprite_h, x:x + sprite_w] = sprite

    return sheet


def split_sprite_sheet(sheet: np.ndarray, sprite_width: int,
                       sprite_height: int) -> List[np.ndarray]:
    """Split a sprite sheet into individual sprites."""
    sprites = []
    rows = sheet.shape[0] // sprite_height
    cols = sheet.shape[1] // sprite_width

    for row in range(rows):
        for col in range(cols):
            y = row * sprite_height
            x = col * sprite_width
            sprite = sheet[y:y + sprite_height, x:x + sprite_width]
            sprites.append(sprite)

    return sprites


# === Outline & Effects ===

def add_outline(img: np.ndarray, color: Color = (0, 0, 0, 255),
                width: int = 1) -> np.ndarray:
    """Add an outline around non-transparent pixels."""
    h, w = img.shape[:2]
    result = np.zeros((h + width * 2, w + width * 2, 4), dtype=np.uint8)

    # Draw outline
    for dy in range(-width, width + 1):
        for dx in range(-width, width + 1):
            if dx == 0 and dy == 0:
                continue
            for y in range(h):
                for x in range(w):
                    if img[y, x, 3] > 0:  # Has alpha
                        ny, nx = y + dy + width, x + dx + width
                        if result[ny, nx, 3] == 0:
                            result[ny, nx] = color

    # Draw original sprite on top
    result[width:h + width, width:w + width] = img

    return result


def flip_horizontal(img: np.ndarray) -> np.ndarray:
    """Flip sprite horizontally."""
    return np.fliplr(img)


def flip_vertical(img: np.ndarray) -> np.ndarray:
    """Flip sprite vertically."""
    return np.flipud(img)


# === I/O ===

def save_sprite(img: np.ndarray, path: str):
    """Save sprite to file."""
    Image.fromarray(img, 'RGBA').save(path)
    print(f"Saved: {path}")


def load_sprite(path: str) -> np.ndarray:
    """Load sprite from file."""
    return np.array(Image.open(path).convert('RGBA'))
