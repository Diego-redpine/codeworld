"""Color palettes for CodeWorld retro pixel art.

Based on the Endesga 32 palette by ENDESGA (https://lospec.com/palette-list/endesga-32)
with derived shades for game-specific elements. This gives a cohesive, professional
pixel art look where every color belongs together.
"""

# Type alias for RGB tuples
Color = tuple[int, int, int]

# ═══════════════════════════════════════════════════════════
# ENDESGA 32 BASE PALETTE
# ═══════════════════════════════════════════════════════════
# Reference colors from the palette (used to derive game colors)
_E_MAROON     = (190, 74, 47)    # #be4a2f
_E_BROWN      = (215, 118, 67)   # #d77643
_E_SAND       = (234, 212, 170)  # #ead4aa
_E_TAN        = (228, 166, 114)  # #e4a672
_E_BARK       = (184, 111, 80)   # #b86f50
_E_DARK_BROWN = (115, 62, 57)    # #733e39
_E_BLACKISH   = (62, 39, 49)     # #3e2731
_E_DARK_RED   = (162, 38, 51)    # #a22633
_E_RED        = (228, 59, 68)    # #e43b44
_E_ORANGE     = (247, 118, 34)   # #f77622
_E_YELLOW_O   = (254, 174, 52)   # #feae34
_E_YELLOW     = (254, 231, 97)   # #fee761
_E_GREEN      = (99, 199, 77)    # #63c74d
_E_MED_GREEN  = (62, 137, 72)    # #3e8948
_E_DARK_GREEN = (38, 92, 66)     # #265c42
_E_DARKEST_GR = (25, 60, 62)     # #193c3e
_E_DARK_BLUE  = (18, 78, 137)    # #124e89
_E_BLUE       = (0, 153, 219)    # #0099db
_E_CYAN       = (44, 232, 245)   # #2ce8f5
_E_WHITE      = (255, 255, 255)  # #ffffff
_E_LIGHT_GRAY = (192, 203, 220)  # #c0cbdc
_E_MED_GRAY   = (139, 155, 180)  # #8b9bb4
_E_DARK_GRAY  = (90, 105, 136)   # #5a6988
_E_DARKER     = (58, 68, 102)    # #3a4466
_E_NEAR_BLACK = (38, 43, 68)     # #262b44
_E_BLACKEST   = (24, 20, 37)     # #181425
_E_HOT_RED    = (255, 0, 68)     # #ff0044
_E_PURPLE     = (104, 56, 108)   # #68386c
_E_PINK       = (181, 80, 136)   # #b55088
_E_CORAL      = (246, 117, 122)  # #f6757a
_E_SKIN       = (232, 183, 150)  # #e8b796
_E_SKIN_DARK  = (194, 133, 105)  # #c28569

# ═══════════════════════════════════════════════════════════
# GAME COLORS — derived from Endesga 32
# ═══════════════════════════════════════════════════════════

# ── Greens (grass, foliage) ──────────────────────────────
GRASS_DARK = _E_DARK_GREEN       # (38, 92, 66) — base ground
GRASS = _E_MED_GREEN             # (62, 137, 72) — main grass
GRASS_MID = (50, 115, 69)        # midpoint of dark↔main
GRASS_LIGHT = _E_GREEN           # (99, 199, 77) — highlight
GRASS_HIGHLIGHT = (130, 215, 100) # derived brighter
MEADOW = (72, 155, 80)           # slightly brighter than GRASS

# ── Browns (paths, wood, earth) ──────────────────────────
DIRT = _E_BARK                   # (184, 111, 80)
DIRT_DARK = _E_DARK_BROWN        # (115, 62, 57)
DIRT_LIGHT = _E_TAN              # (228, 166, 114)
WOOD = _E_BARK                   # (184, 111, 80)
WOOD_DARK = _E_DARK_BROWN        # (115, 62, 57)
WOOD_LIGHT = _E_BROWN            # (215, 118, 67)
WOOD_PLANK = _E_BROWN            # (215, 118, 67)
LOG = (95, 58, 42)               # between dark_brown and blackish

# ── Stone / Gray ─────────────────────────────────────────
STONE = _E_MED_GRAY              # (139, 155, 180)
STONE_DARK = _E_DARK_GRAY        # (90, 105, 136)
STONE_LIGHT = _E_LIGHT_GRAY      # (192, 203, 220)
STONE_ACCENT = _E_DARKER         # (58, 68, 102)
COBBLE = (115, 130, 158)         # between dark_gray and med_gray
COBBLE_LIGHT = (155, 168, 195)   # between med_gray and light_gray

# ── Roofs ────────────────────────────────────────────────
ROOF_RED = _E_MAROON             # (190, 74, 47)
ROOF_RED_DARK = _E_DARK_RED      # (162, 38, 51)
ROOF_RED_LIGHT = _E_RED          # (228, 59, 68)
ROOF_BLUE = _E_DARK_BLUE         # (18, 78, 137)
ROOF_BLUE_DARK = (12, 58, 110)   # derived darker
ROOF_BLUE_LIGHT = _E_BLUE        # (0, 153, 219)
ROOF_THATCH = _E_TAN             # (228, 166, 114)
ROOF_THATCH_DARK = _E_BARK       # (184, 111, 80)
ROOF_THATCH_LIGHT = _E_SAND      # (234, 212, 170)
ROOF_GREEN = _E_MED_GREEN        # (62, 137, 72)
ROOF_GREEN_DARK = _E_DARK_GREEN  # (38, 92, 66)
ROOF_PURPLE = _E_PURPLE          # (104, 56, 108)
ROOF_PURPLE_DARK = (78, 42, 82)  # derived darker

# ── Water ────────────────────────────────────────────────
WATER_DEEP = (12, 58, 110)       # darker than dark_blue
WATER = _E_DARK_BLUE             # (18, 78, 137)
WATER_LIGHT = _E_BLUE            # (0, 153, 219)
WATER_HIGHLIGHT = _E_CYAN        # (44, 232, 245)
WATER_SHIMMER = (140, 238, 248)  # lighter cyan
WATER_FOAM = (200, 245, 250)     # near-white cyan

# ── Windows / Light ──────────────────────────────────────
WINDOW_GLOW = _E_YELLOW_O        # (254, 174, 52) — warm glow
WINDOW_BRIGHT = _E_YELLOW        # (254, 231, 97)
WINDOW = _E_ORANGE               # (247, 118, 34) — warm window
WINDOW_DARK = _E_MAROON          # (190, 74, 47)
LAMP = _E_YELLOW_O               # (254, 174, 52)
LANTERN = _E_ORANGE              # (247, 118, 34)

# ── Flowers ──────────────────────────────────────────────
FLOWER_RED = _E_RED              # (228, 59, 68)
FLOWER_YELLOW = _E_YELLOW        # (254, 231, 97)
FLOWER_BLUE = _E_BLUE            # (0, 153, 219)
FLOWER_PINK = _E_PINK            # (181, 80, 136)
FLOWER_WHITE = _E_WHITE          # (255, 255, 255)
FLOWER_PURPLE = _E_PURPLE        # (104, 56, 108)

# ── Agents / Characters ─────────────────────────────────
SKIN = _E_SKIN                   # (232, 183, 150)
SKIN_DARK = _E_SKIN_DARK         # (194, 133, 105)
HAIR_BROWN = _E_DARK_BROWN       # (115, 62, 57)
HAIR_DARK = _E_BLACKISH          # (62, 39, 49)
HAIR_BLONDE = _E_SAND            # (234, 212, 170)
SHIRT_BLUE = _E_DARK_BLUE        # (18, 78, 137)
SHIRT_RED = _E_DARK_RED          # (162, 38, 51)
SHIRT_GREEN = _E_MED_GREEN       # (62, 137, 72)
SHIRT_PURPLE = _E_PURPLE         # (104, 56, 108)
PANTS = _E_DARKER                # (58, 68, 102)
PANTS_BROWN = _E_DARK_BROWN      # (115, 62, 57)
BOOTS = _E_BLACKISH              # (62, 39, 49)

# ── UI / Night ───────────────────────────────────────────
UI_BG = _E_BLACKEST              # (24, 20, 37)
UI_BG_LIGHT = _E_NEAR_BLACK      # (38, 43, 68)
UI_BORDER = _E_DARKER            # (58, 68, 102)
UI_BORDER_HIGHLIGHT = _E_DARK_GRAY  # (90, 105, 136)
UI_TEXT = _E_LIGHT_GRAY          # (192, 203, 220)
UI_TEXT_DIM = _E_MED_GRAY        # (139, 155, 180)
UI_ACCENT = _E_BLUE              # (0, 153, 219)
UI_GOLD = _E_YELLOW_O            # (254, 174, 52)
UI_GREEN = _E_GREEN              # (99, 199, 77)
UI_RED = _E_RED                  # (228, 59, 68)

NIGHT_SKY = (18, 16, 30)         # near blackest
NIGHT_TINT = _E_BLACKEST         # (24, 20, 37)
STAR = _E_YELLOW                 # (254, 231, 97)
STAR_DIM = _E_SAND               # (234, 212, 170)
MOON = _E_SAND                   # (234, 212, 170)

# ── Smoke / Particles ────────────────────────────────────
SMOKE = _E_MED_GRAY              # (139, 155, 180)
SMOKE_LIGHT = _E_LIGHT_GRAY      # (192, 203, 220)
SMOKE_DARK = _E_DARK_GRAY        # (90, 105, 136)
SPARKLE = _E_YELLOW              # (254, 231, 97)
HEART = _E_RED                   # (228, 59, 68)

# ── Special ──────────────────────────────────────────────
SHADOW = _E_NEAR_BLACK           # (38, 43, 68)
TRANSPARENT = None
_ = None  # shorthand for transparent in sprite defs

# ── Customer Building Accents ──────────────────────────
SALON_PINK = _E_CORAL            # (246, 117, 122)
SALON_STRIPE = _E_PINK           # (181, 80, 136)
RESTAURANT_WARM = _E_ORANGE      # (247, 118, 34)
RESTAURANT_CHIMNEY = _E_DARK_BROWN  # (115, 62, 57)
GYM_BLUE = _E_BLUE               # (0, 153, 219)
GYM_STEEL = _E_LIGHT_GRAY        # (192, 203, 220)
HOME_OLIVE = (85, 128, 72)       # between med_green and dark_green
HOME_TRUCK = _E_DARK_BLUE        # (18, 78, 137)
OFFICE_MARBLE = _E_LIGHT_GRAY    # (192, 203, 220)
OFFICE_COLUMN = _E_MED_GRAY      # (139, 155, 180)
STUDIO_ORANGE = _E_ORANGE        # (247, 118, 34)
STUDIO_TEAL = _E_DARKEST_GR     # (25, 60, 62) — teal accent
SCHOOL_CREAM = _E_SAND           # (234, 212, 170)
SCHOOL_BRICK = _E_MAROON         # (190, 74, 47)
GARAGE_DARK = _E_NEAR_BLACK      # (38, 43, 68)
GARAGE_METAL = _E_MED_GRAY       # (139, 155, 180)
RETAIL_DISPLAY = _E_CYAN         # (44, 232, 245)
RETAIL_AWNING = _E_DARK_GREEN    # (38, 92, 66)

# ── NPC Role Colors ────────────────────────────────────
COO_CAPE = _E_DARK_BLUE          # (18, 78, 137)
RECEPTIONIST_APRON = _E_MED_GREEN   # (62, 137, 72)
CONTENT_SHIRT = _E_ORANGE        # (247, 118, 34)
REVIEW_VEST = _E_DARK_RED        # (162, 38, 51)
ROUTE_SASH = _E_PURPLE           # (104, 56, 108)
WORKER_HELMET = _E_YELLOW_O      # (254, 174, 52)

# ── Construction ───────────────────────────────────────
SCAFFOLD_WOOD = _E_BROWN         # (215, 118, 67)
SCAFFOLD_ROPE = _E_BARK          # (184, 111, 80)
FOUNDATION = _E_DARK_GRAY        # (90, 105, 136)

# ── Street Furniture ──────────────────────────────────
BENCH_WOOD = _E_BROWN            # (215, 118, 67)
BENCH_DARK = _E_DARK_BROWN       # (115, 62, 57)
TRASHCAN = _E_DARK_GRAY          # (90, 105, 136)
TRASHCAN_LID = _E_MED_GRAY       # (139, 155, 180)
POT_TERRACOTTA = _E_MAROON       # (190, 74, 47)
POT_DARK = _E_DARK_BROWN         # (115, 62, 57)
SIGN_WOOD = _E_BROWN             # (215, 118, 67)


def lerp_color(a: Color, b: Color, t: float) -> Color:
    """Linearly interpolate between two colors."""
    return (
        int(a[0] + (b[0] - a[0]) * t),
        int(a[1] + (b[1] - a[1]) * t),
        int(a[2] + (b[2] - a[2]) * t),
    )


def tint_color(color: Color | None, tint: Color, amount: float) -> Color | None:
    """Apply a color tint to a pixel."""
    if color is None:
        return None
    return lerp_color(color, tint, amount)


def night_tint(color: Color | None, amount: float = 0.4) -> Color | None:
    """Apply night-time blue tint."""
    return tint_color(color, (20, 20, 50), amount)


def dawn_tint(color: Color | None, amount: float = 0.2) -> Color | None:
    """Apply warm dawn tint."""
    return tint_color(color, (60, 40, 20), amount)


def get_time_tint(hour: int):
    """Return (tint_color, tint_amount) for a given hour."""
    if 6 <= hour < 8:    # dawn
        return (80, 60, 30), 0.15
    elif 8 <= hour < 17:  # day
        return None, 0.0
    elif 17 <= hour < 19:  # dusk
        return (70, 40, 20), 0.2
    elif 19 <= hour < 21:  # evening
        return (30, 20, 50), 0.3
    else:                  # night
        return (15, 15, 40), 0.45
