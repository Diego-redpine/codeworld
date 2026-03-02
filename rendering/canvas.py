"""Pixel canvas that renders to half-block Unicode characters.

Each terminal character cell represents 2 vertical pixels using the ▀ character
with foreground color = top pixel and background color = bottom pixel.
This effectively doubles the vertical resolution.
"""
from __future__ import annotations

from rich.text import Text
from rich.style import Style

from assets.palettes import Color


class PixelCanvas:
    """A 2D pixel buffer that composites to half-block terminal characters."""

    def __init__(self, width: int, height: int, bg: Color = (16, 16, 24)):
        """Create a pixel canvas.

        Args:
            width: Width in pixels (= terminal columns).
            height: Height in pixels (should be even; = terminal rows * 2).
            bg: Background color for empty pixels.
        """
        self.width = width
        self.height = height if height % 2 == 0 else height + 1
        self.bg = bg
        self.pixels: list[list[Color | None]] = [
            [None] * width for _ in range(self.height)
        ]
        self._style_cache: dict[tuple, Style] = {}

    def clear(self, bg: Color | None = None):
        """Clear the canvas to background color."""
        fill = bg if bg is not None else None
        for y in range(self.height):
            for x in range(self.width):
                self.pixels[y][x] = fill

    def fill_rect(self, x: int, y: int, w: int, h: int, color: Color):
        """Fill a rectangle with a solid color."""
        for py in range(max(0, y), min(self.height, y + h)):
            for px in range(max(0, x), min(self.width, x + w)):
                self.pixels[py][px] = color

    def set_pixel(self, x: int, y: int, color: Color | None):
        """Set a single pixel (bounds-checked)."""
        if 0 <= x < self.width and 0 <= y < self.height and color is not None:
            self.pixels[y][x] = color

    def get_pixel(self, x: int, y: int) -> Color | None:
        """Get a pixel color (bounds-checked)."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.pixels[y][x]
        return None

    def draw_sprite(self, sprite: list[list[Color | None]], x: int, y: int):
        """Draw a sprite (2D pixel array) at position, respecting transparency."""
        for sy, row in enumerate(sprite):
            for sx, color in enumerate(row):
                if color is not None:
                    px, py = x + sx, y + sy
                    if 0 <= px < self.width and 0 <= py < self.height:
                        self.pixels[py][px] = color

    def draw_sprite_flipped(self, sprite: list[list[Color | None]], x: int, y: int):
        """Draw a sprite horizontally flipped."""
        for sy, row in enumerate(sprite):
            flipped = list(reversed(row))
            for sx, color in enumerate(flipped):
                if color is not None:
                    px, py = x + sx, y + sy
                    if 0 <= px < self.width and 0 <= py < self.height:
                        self.pixels[py][px] = color

    def apply_tint(self, tint: Color, amount: float):
        """Apply a color tint to all non-None pixels."""
        if amount <= 0:
            return
        for y in range(self.height):
            for x in range(self.width):
                c = self.pixels[y][x]
                if c is not None:
                    self.pixels[y][x] = (
                        int(c[0] + (tint[0] - c[0]) * amount),
                        int(c[1] + (tint[1] - c[1]) * amount),
                        int(c[2] + (tint[2] - c[2]) * amount),
                    )

    def _get_style(self, top: Color | None, bot: Color | None) -> Style:
        """Get or create a cached Style for a pixel pair."""
        bg = self.bg
        # Determine effective colors
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
        """Render the canvas to a Rich Text object using half-block characters.

        Batches consecutive pixels with the same style into single appends
        for significantly fewer Text.append() calls.
        """
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
        """Serialize the canvas to binary RGB for WebSocket streaming.

        Format: 4-byte header (uint16 width, uint16 height, big-endian)
        followed by W*H*3 bytes of RGB data, row-major.
        None pixels use the background color.
        """
        import struct
        bg = self.bg
        w, h = self.width, self.height
        buf = bytearray(4 + w * h * 3)
        struct.pack_into('>HH', buf, 0, w, h)
        idx = 4
        for y in range(h):
            row = self.pixels[y]
            for x in range(w):
                c = row[x] if row[x] is not None else bg
                buf[idx] = c[0]
                buf[idx + 1] = c[1]
                buf[idx + 2] = c[2]
                idx += 3
        return bytes(buf)

    @property
    def char_height(self) -> int:
        """Height in terminal character rows."""
        return self.height // 2

    @property
    def char_width(self) -> int:
        """Width in terminal character columns."""
        return self.width
