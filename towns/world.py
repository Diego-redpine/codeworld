"""World map — zoomed-out view showing all project towns.

Each town is rendered as a tiny cluster of blocks on a large green landscape.
"""
from __future__ import annotations

import hashlib
import math
import random

from rendering.canvas import PixelCanvas
from assets import palettes
from assets.sprites import TILE_GRASS_VARIANTS
from towns.town import Town


class WorldMap:
    """Zoomed-out view showing multiple project towns."""

    def __init__(self, towns: list[Town]):
        self.towns = towns
        self.selected_idx = 0
        self.anim_tick = 0

    @property
    def selected_town(self) -> Town | None:
        if 0 <= self.selected_idx < len(self.towns):
            return self.towns[self.selected_idx]
        return None

    def select_next(self):
        if self.towns:
            self.selected_idx = (self.selected_idx + 1) % len(self.towns)

    def select_prev(self):
        if self.towns:
            self.selected_idx = (self.selected_idx - 1) % len(self.towns)

    def select_by_path(self, path: str):
        """Select the town matching a project path."""
        for i, town in enumerate(self.towns):
            if town.project_path == path:
                self.selected_idx = i
                return

    def draw(self, canvas: PixelCanvas, tick: int = 0):
        """Draw the world map onto a canvas."""
        self.anim_tick = tick
        canvas.clear()

        # ── Ground ──
        rng = random.Random(42)
        for y in range(0, canvas.height, 2):
            for x in range(canvas.width):
                variant = rng.choice(TILE_GRASS_VARIANTS)
                canvas.set_pixel(x, y, variant[0][0])
                if y + 1 < canvas.height:
                    canvas.set_pixel(x, y + 1, variant[1][0])

        if not self.towns:
            return

        # ── Calculate town positions ──
        positions = self._calculate_positions(canvas.width, canvas.height)

        # ── Draw each town as a mini cluster ──
        for i, (town, (tx, ty)) in enumerate(zip(self.towns, positions)):
            selected = (i == self.selected_idx)
            self._draw_mini_town(canvas, town, tx, ty, selected, tick)

    def _calculate_positions(
        self, width: int, height: int,
    ) -> list[tuple[int, int]]:
        """Calculate positions for each town on the world map."""
        n = len(self.towns)
        positions = []

        if n == 1:
            positions.append((width // 2, height // 2))
        elif n <= 4:
            # Grid layout
            cols = min(n, 2)
            rows = math.ceil(n / cols)
            cell_w = width // (cols + 1)
            cell_h = height // (rows + 1)
            for i in range(n):
                col = i % cols
                row = i // cols
                x = cell_w * (col + 1)
                y = cell_h * (row + 1)
                positions.append((x, y))
        else:
            # Circular layout with some jitter
            rng = random.Random(99)
            cx, cy = width // 2, height // 2
            radius_x = width // 3
            radius_y = height // 3
            for i in range(n):
                angle = (2 * math.pi * i / n) - math.pi / 2
                x = int(cx + math.cos(angle) * radius_x + rng.randint(-3, 3))
                y = int(cy + math.sin(angle) * radius_y + rng.randint(-2, 2))
                positions.append((x, y))

        return positions

    def _draw_mini_town(
        self, canvas: PixelCanvas, town: Town,
        cx: int, cy: int, selected: bool, tick: int,
    ):
        """Draw a tiny representation of a town."""
        tier = town.metrics.tier
        rng = random.Random(hash(town.project_path))

        # Town size based on tier
        if tier >= 4:
            size = 4
        elif tier >= 3:
            size = 3
        elif tier >= 2:
            size = 2
        else:
            size = 1

        # Draw mini buildings as colored blocks
        colors_roof = [
            palettes.ROOF_RED, palettes.ROOF_BLUE,
            palettes.ROOF_THATCH, palettes.ROOF_GREEN,
        ]
        colors_wall = [palettes.WOOD, palettes.STONE, palettes.WOOD_PLANK]

        # Ground patch (lighter area for the town)
        for dy in range(-size - 2, size + 3):
            for dx in range(-size - 2, size + 3):
                canvas.set_pixel(cx + dx, cy + dy, palettes.GRASS_LIGHT)

        # Mini buildings
        n_buildings = min(len(town.buildings), size * 3 + 2)
        for i in range(n_buildings):
            angle = rng.uniform(0, 2 * math.pi)
            dist = rng.uniform(0, size * 1.5)
            bx = int(cx + math.cos(angle) * dist)
            by = int(cy + math.sin(angle) * dist)

            roof = rng.choice(colors_roof)
            wall = rng.choice(colors_wall)

            # 2-pixel tall building (1 char)
            canvas.set_pixel(bx, by, roof)
            canvas.set_pixel(bx, by + 1, wall)
            if rng.random() > 0.5:
                canvas.set_pixel(bx + 1, by, roof)
                canvas.set_pixel(bx + 1, by + 1, wall)

        # Draw a tree or two
        for _ in range(size):
            tx = cx + rng.randint(-size - 1, size + 1)
            ty = cy + rng.randint(-size - 1, size + 1)
            canvas.set_pixel(tx, ty, palettes.GRASS_DARK)
            canvas.set_pixel(tx, ty + 1, palettes.LOG)

        # Selection highlight — pulsing border
        if selected:
            pulse = abs((tick % 20) - 10) / 10.0
            border_color = palettes.lerp_color(
                palettes.UI_ACCENT, palettes.UI_GOLD, pulse,
            )
            r = size + 3
            for dx in range(-r, r + 1):
                canvas.set_pixel(cx + dx, cy - r, border_color)
                canvas.set_pixel(cx + dx, cy + r, border_color)
            for dy in range(-r, r + 1):
                canvas.set_pixel(cx - r, cy + dy, border_color)
                canvas.set_pixel(cx + r, cy + dy, border_color)

        # Town name label — we'll draw this as part of the UI, not pixels
        # (Textual overlay handles text labels better)

    def tick(self):
        """Advance world map animations."""
        self.anim_tick += 1
