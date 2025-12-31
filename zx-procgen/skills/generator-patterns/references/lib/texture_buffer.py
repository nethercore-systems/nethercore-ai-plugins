#!/usr/bin/env python3
"""Texture buffer class for procedural texture generation.

Copy this file to your project's generator/lib/ folder.

Requires: pip install pillow numpy pyfastnoiselite
"""
import numpy as np
from PIL import Image
from typing import Tuple, Optional

# Try to import FastNoiseLite (optional but recommended)
try:
    from pyfastnoiselite import FastNoiseLite, NoiseType
    HAS_NOISE = True
except ImportError:
    HAS_NOISE = False
    print("Warning: pyfastnoiselite not installed. Noise functions unavailable.")


Color = Tuple[int, int, int, int]  # RGBA


class TextureBuffer:
    """Buffer for procedural texture generation using PIL + NumPy."""

    def __init__(self, width: int, height: int):
        """Create a new texture buffer.

        Args:
            width: Texture width in pixels
            height: Texture height in pixels
        """
        self.width = width
        self.height = height
        self.data = np.zeros((height, width, 4), dtype=np.uint8)
        self.data[:, :, 3] = 255  # Default opaque

    # === Pixel Access ===

    def get(self, x: int, y: int) -> Color:
        """Get pixel color at (x, y)."""
        return tuple(self.data[y % self.height, x % self.width])

    def set(self, x: int, y: int, color: Color):
        """Set pixel color at (x, y)."""
        self.data[y % self.height, x % self.width] = color

    # === Fill Operations ===

    def fill(self, color: Color):
        """Fill entire buffer with a color."""
        self.data[:, :] = color

    def fill_rect(self, x: int, y: int, w: int, h: int, color: Color):
        """Fill a rectangle with a color."""
        x1, y1 = max(0, x), max(0, y)
        x2, y2 = min(self.width, x + w), min(self.height, y + h)
        self.data[y1:y2, x1:x2] = color

    # === Drawing ===

    def draw_line(self, x1: int, y1: int, x2: int, y2: int,
                  color: Color, width: int = 1):
        """Draw a line using Bresenham's algorithm."""
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            # Draw point with width
            for ox in range(-width // 2, width // 2 + 1):
                for oy in range(-width // 2, width // 2 + 1):
                    self.set(x1 + ox, y1 + oy, color)

            if x1 == x2 and y1 == y2:
                break

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    # === Noise ===

    def add_perlin_noise(self, scale: float = 0.1, intensity: int = 50,
                         seed: int = 42, blend_mode: str = 'add'):
        """Add Perlin noise to the texture.

        Args:
            scale: Noise frequency (smaller = larger features)
            intensity: Noise strength (0-255)
            seed: Random seed
            blend_mode: 'add', 'subtract', 'multiply', or 'overlay'
        """
        if not HAS_NOISE:
            print("Noise not available. Install pyfastnoiselite.")
            return

        noise = FastNoiseLite(seed)
        noise.noise_type = NoiseType.NoiseType_Perlin
        noise.frequency = scale

        noise_data = np.zeros((self.height, self.width), dtype=np.float32)
        for y in range(self.height):
            for x in range(self.width):
                noise_data[y, x] = noise.get_noise(x, y)

        # Normalize to 0-1
        noise_data = (noise_data + 1) / 2

        # Apply to RGB channels based on blend mode
        for c in range(3):
            channel = self.data[:, :, c].astype(np.float32)
            noise_scaled = noise_data * intensity

            if blend_mode == 'add':
                channel = channel + noise_scaled
            elif blend_mode == 'subtract':
                channel = channel - noise_scaled
            elif blend_mode == 'multiply':
                channel = channel * (noise_data * 0.5 + 0.5)
            elif blend_mode == 'overlay':
                mask = channel < 128
                channel[mask] = 2 * channel[mask] * noise_data[mask]
                channel[~mask] = 1 - 2 * (1 - channel[~mask]) * (1 - noise_data[~mask])

            self.data[:, :, c] = np.clip(channel, 0, 255).astype(np.uint8)

    def add_simplex_noise(self, scale: float = 0.1, intensity: int = 50,
                          seed: int = 42, octaves: int = 1):
        """Add simplex noise with optional octaves (FBM)."""
        if not HAS_NOISE:
            return

        noise = FastNoiseLite(seed)
        noise.noise_type = NoiseType.NoiseType_OpenSimplex2

        if octaves > 1:
            noise.fractal_type = 1  # FBM
            noise.fractal_octaves = octaves

        noise.frequency = scale

        for y in range(self.height):
            for x in range(self.width):
                n = (noise.get_noise(x, y) + 1) / 2  # 0-1
                for c in range(3):
                    val = self.data[y, x, c] + int(n * intensity)
                    self.data[y, x, c] = max(0, min(255, val))

    # === Blending ===

    def blend(self, other: 'TextureBuffer', mode: str = 'normal',
              opacity: float = 1.0):
        """Blend another texture onto this one.

        Args:
            other: Source texture buffer
            mode: 'normal', 'multiply', 'add', 'overlay'
            opacity: Blend opacity (0-1)
        """
        src = other.data.astype(np.float32) / 255
        dst = self.data.astype(np.float32) / 255

        if mode == 'normal':
            result = src
        elif mode == 'multiply':
            result = src * dst
        elif mode == 'add':
            result = src + dst
        elif mode == 'overlay':
            mask = dst < 0.5
            result = np.where(mask, 2 * dst * src, 1 - 2 * (1 - dst) * (1 - src))
        else:
            result = src

        # Apply opacity
        result = dst * (1 - opacity) + result * opacity
        self.data = (np.clip(result, 0, 1) * 255).astype(np.uint8)

    # === I/O ===

    def save(self, path: str):
        """Save texture to file."""
        img = Image.fromarray(self.data, 'RGBA')
        img.save(path)
        print(f"Saved: {path}")

    def save_rgb(self, path: str):
        """Save texture as RGB (no alpha)."""
        img = Image.fromarray(self.data[:, :, :3], 'RGB')
        img.save(path)
        print(f"Saved: {path}")

    @classmethod
    def from_image(cls, path: str) -> 'TextureBuffer':
        """Load texture from an image file."""
        img = Image.open(path).convert('RGBA')
        buf = cls(img.width, img.height)
        buf.data = np.array(img)
        return buf

    # === Utilities ===

    def copy(self) -> 'TextureBuffer':
        """Create a copy of this buffer."""
        new_buf = TextureBuffer(self.width, self.height)
        new_buf.data = self.data.copy()
        return new_buf

    def resize(self, width: int, height: int) -> 'TextureBuffer':
        """Resize texture (returns new buffer)."""
        img = Image.fromarray(self.data, 'RGBA')
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        new_buf = TextureBuffer(width, height)
        new_buf.data = np.array(img)
        return new_buf

    def make_seamless(self, blend_width: int = 32):
        """Make texture seamlessly tileable by blending edges."""
        for y in range(self.height):
            for x in range(blend_width):
                t = x / blend_width
                # Blend left-right
                left = self.data[y, x].astype(np.float32)
                right = self.data[y, self.width - blend_width + x].astype(np.float32)
                blended = left * t + right * (1 - t)
                self.data[y, x] = blended.astype(np.uint8)
                self.data[y, self.width - blend_width + x] = blended.astype(np.uint8)

        for x in range(self.width):
            for y in range(blend_width):
                t = y / blend_width
                # Blend top-bottom
                top = self.data[y, x].astype(np.float32)
                bottom = self.data[self.height - blend_width + y, x].astype(np.float32)
                blended = top * t + bottom * (1 - t)
                self.data[y, x] = blended.astype(np.uint8)
                self.data[self.height - blend_width + y, x] = blended.astype(np.uint8)
