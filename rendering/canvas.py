"""Pixel canvas that renders to half-block Unicode characters.

Each terminal character cell represents 2 vertical pixels using the ▀ character
with foreground color = top pixel and background color = bottom pixel.
This effectively doubles the vertical resolution.
"""
from __future__ import annotations

import struct

from rich.text import Text
from rich.style import Style

from assets.palettes import Color


class PixelCanvas:
    """A 2D pixel buffer with dual storage for fast TUI and web rendering.

    Internally maintains both:
    - pixels: list[list[Color|None]] for TUI half-block rendering
    - _rgb: flat bytearray for ultra-fast WebSocket serialization
    """

    def __init__(self, width: int, height: int, bg: Color = (16, 16, 24)):
        self.width = width
        self.height = height if height % 2 == 0 else height + 1
        self.bg = bg
        self.pixels: list[list[Color | None]] = [
            [None] * width for _ in range(self.height)
        ]
        # Flat RGB buffer: 4-byte header + W*H*3 bytes
        size = 4 + self.width * self.height * 3
        self._rgb = bytearray(size)
        struct.pack_into('>HH', self._rgb, 0, self.width, self.height)
        # Pre-fill with bg color
        br, bg_g, bb = bg
        for i in range(self.width * self.height):
            off = 4 + i * 3
            self._rgb[off] = br
            self._rgb[off + 1] = bg_g
            self._rgb[off + 2] = bb
        self._stride = self.width * 3
        self._style_cache: dict[tuple, Style] = {}

    def clear(self, bg: Color | None = None):
        """Clear the canvas to background color."""
        fill = bg if bg is not None else None
        c = self.bg if fill is None else fill
        br, bg_g, bb = c
        for y in range(self.height):
            for x in range(self.width):
                self.pixels[y][x] = fill
        # Clear flat buffer
        for i in range(self.width * self.height):
            off = 4 + i * 3
            self._rgb[off] = br
            self._rgb[off + 1] = bg_g
            self._rgb[off + 2] = bb

    def copy_from(self, other: "PixelCanvas"):
        """Fast copy of all pixels from another canvas of the same size."""
        for y in range(self.height):
            self.pixels[y][:] = other.pixels[y][:]
        # Bulk copy flat buffer (C-level memcpy)
        self._rgb[4:] = other._rgb[4:]

    def fill_rect(self, x: int, y: int, w: int, h: int, color: Color):
        """Fill a rectangle with a solid color."""
        r, g, b = color
        for py in range(max(0, y), min(self.height, y + h)):
            for px in range(max(0, x), min(self.width, x + w)):
                self.pixels[py][px] = color
                off = 4 + (py * self.width + px) * 3
                self._rgb[off] = r
                self._rgb[off + 1] = g
                self._rgb[off + 2] = b

    def set_pixel(self, x: int, y: int, color: Color | None):
        """Set a single pixel (bounds-checked)."""
        if 0 <= x < self.width and 0 <= y < self.height and color is not None:
            self.pixels[y][x] = color
            off = 4 + (y * self.width + x) * 3
            self._rgb[off] = color[0]
            self._rgb[off + 1] = color[1]
            self._rgb[off + 2] = color[2]

    def get_pixel(self, x: int, y: int) -> Color | None:
        """Get a pixel color (bounds-checked)."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.pixels[y][x]
        return None

    def draw_sprite(self, sprite: list[list[Color | None]], x: int, y: int):
        """Draw a sprite (2D pixel array) at position, respecting transparency."""
        w = self.width
        h = self.height
        rgb = self._rgb
        pixels = self.pixels
        for sy, row in enumerate(sprite):
            py = y + sy
            if py < 0 or py >= h:
                continue
            prow = pixels[py]
            base_off = 4 + py * w * 3
            for sx, color in enumerate(row):
                if color is not None:
                    px = x + sx
                    if 0 <= px < w:
                        prow[px] = color
                        off = base_off + px * 3
                        rgb[off] = color[0]
                        rgb[off + 1] = color[1]
                        rgb[off + 2] = color[2]

    def draw_sprite_flipped(self, sprite: list[list[Color | None]], x: int, y: int):
        """Draw a sprite horizontally flipped."""
        w = self.width
        h = self.height
        rgb = self._rgb
        pixels = self.pixels
        for sy, row in enumerate(sprite):
            py = y + sy
            if py < 0 or py >= h:
                continue
            prow = pixels[py]
            base_off = 4 + py * w * 3
            rlen = len(row)
            for sx in range(rlen):
                color = row[rlen - 1 - sx]
                if color is not None:
                    px = x + sx
                    if 0 <= px < w:
                        prow[px] = color
                        off = base_off + px * 3
                        rgb[off] = color[0]
                        rgb[off + 1] = color[1]
                        rgb[off + 2] = color[2]

    def apply_tint(self, tint: Color, amount: float):
        """Apply a color tint to all non-None pixels."""
        if amount <= 0:
            return
        tr, tg, tb = tint
        for y in range(self.height):
            for x in range(self.width):
                c = self.pixels[y][x]
                if c is not None:
                    nc = (
                        int(c[0] + (tr - c[0]) * amount),
                        int(c[1] + (tg - c[1]) * amount),
                        int(c[2] + (tb - c[2]) * amount),
                    )
                    self.pixels[y][x] = nc
                    off = 4 + (y * self.width + x) * 3
                    self._rgb[off] = nc[0]
                    self._rgb[off + 1] = nc[1]
                    self._rgb[off + 2] = nc[2]

    def _get_style(self, top: Color | None, bot: Color | None) -> Style:
        """Get or create a cached Style for a pixel pair."""
        bg = self.bg
        tc = top if top is not None else bg
        bc = bot if bot is not None else bg
        key = (tc, bc)
        if key not in self._style_cache:
            self._style_cache[key] = Style(
                color=f"#{tc[0]:02x}{tc[1]:02x}{tc[2]:02x}",
                bgcolor=f"#{bc[0]:02x}{bc[1]:02x}{bc[2]:02x}",
            )
        return self._style_cache[key]

    def render(self) -> Text:
        """Render the canvas to a Rich Text object using half-block characters."""
        parts: list[tuple[str, Style]] = []
        bg = self.bg
        pixels = self.pixels
        h = self.height
        w = self.width

        for y in range(0, h, 2):
            if y > 0:
                parts.append(("\n", Style.null()))
            prev_style = None
            run = []
            for x in range(w):
                tc = pixels[y][x] or bg
                bc = pixels[y + 1][x] if y + 1 < h else None
                bc = bc or bg
                style = self._get_style(tc, bc)
                if style is prev_style:
                    run.append("▀")
                else:
                    if run:
                        parts.append(("".join(run), prev_style))
                    run = ["▀"]
                    prev_style = style
            if run:
                parts.append(("".join(run), prev_style))

        text = Text()
        for chunk, style in parts:
            text.append(chunk, style)
        return text

    def to_rgb_bytes(self) -> bytes:
        """Serialize canvas to binary RGB for WebSocket streaming.

        Format: 4-byte header (uint16 width, uint16 height, big-endian)
        followed by W*H*3 bytes of RGB data, row-major.

        This is now O(1) — just returns the pre-built flat buffer.
        """
        return bytes(self._rgb)

    @property
    def char_height(self) -> int:
        """Height in terminal character rows."""
        return self.height // 2

    @property
    def char_width(self) -> int:
        """Width in terminal character columns."""
        return self.width
