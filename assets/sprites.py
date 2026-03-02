"""Hand-crafted pixel art sprites for CodeWorld.

Each sprite is a 2D list of Color tuples or None (transparent).
Sprites are designed at the "effective pixel" level — each pixel
maps to one half of a terminal character cell via the half-block renderer.
"""
from __future__ import annotations

from assets.palettes import (
    _,
    GRASS, GRASS_DARK, GRASS_LIGHT, GRASS_MID, GRASS_HIGHLIGHT, MEADOW,
    DIRT, DIRT_DARK, DIRT_LIGHT,
    WOOD, WOOD_DARK, WOOD_LIGHT, WOOD_PLANK, LOG,
    STONE, STONE_DARK, STONE_LIGHT, STONE_ACCENT, COBBLE, COBBLE_LIGHT,
    ROOF_RED, ROOF_RED_DARK, ROOF_RED_LIGHT,
    ROOF_BLUE, ROOF_BLUE_DARK, ROOF_BLUE_LIGHT,
    ROOF_THATCH, ROOF_THATCH_DARK, ROOF_THATCH_LIGHT,
    ROOF_GREEN, ROOF_GREEN_DARK,
    ROOF_PURPLE, ROOF_PURPLE_DARK,
    WATER_DEEP, WATER, WATER_LIGHT, WATER_HIGHLIGHT, WATER_SHIMMER,
    WINDOW_GLOW, WINDOW_BRIGHT, WINDOW, WINDOW_DARK,
    LAMP, LANTERN,
    FLOWER_RED, FLOWER_YELLOW, FLOWER_BLUE, FLOWER_PINK, FLOWER_WHITE, FLOWER_PURPLE,
    SKIN, SKIN_DARK, HAIR_BROWN, HAIR_DARK, HAIR_BLONDE,
    SHIRT_BLUE, SHIRT_RED, SHIRT_GREEN, SHIRT_PURPLE,
    PANTS, PANTS_BROWN, BOOTS,
    SMOKE, SMOKE_LIGHT, SMOKE_DARK,
    SPARKLE, HEART,
    SHADOW,
    Color,
    SALON_PINK, SALON_STRIPE,
    RESTAURANT_WARM, RESTAURANT_CHIMNEY,
    GYM_BLUE, GYM_STEEL,
    HOME_OLIVE, HOME_TRUCK,
    OFFICE_MARBLE, OFFICE_COLUMN,
    STUDIO_ORANGE, STUDIO_TEAL,
    SCHOOL_CREAM, SCHOOL_BRICK,
    GARAGE_DARK, GARAGE_METAL,
    RETAIL_DISPLAY, RETAIL_AWNING,
    COO_CAPE, RECEPTIONIST_APRON, CONTENT_SHIRT, REVIEW_VEST, ROUTE_SASH, WORKER_HELMET,
    SCAFFOLD_WOOD, SCAFFOLD_ROPE, FOUNDATION,
    UI_GOLD,
    BENCH_WOOD, BENCH_DARK, TRASHCAN, TRASHCAN_LID,
    POT_TERRACOTTA, POT_DARK, SIGN_WOOD,
)

# Type alias
Sprite = list[list[Color | None]]

# Outline color for all sprites
OL_C = (24, 20, 37)  # near-black outline (Endesga blackest)


# ═══════════════════════════════════════════════════════════
# TERRAIN TILES (1x2 pixels = 1 terminal character)
# ═══════════════════════════════════════════════════════════

TILE_GRASS_VARIANTS = [
    [[GRASS], [GRASS_DARK]],
    [[GRASS_MID], [GRASS]],
    [[GRASS], [GRASS_MID]],
    [[GRASS_LIGHT], [GRASS]],
    [[GRASS_MID], [GRASS_DARK]],
    [[MEADOW], [GRASS]],
    [[GRASS], [MEADOW]],
    [[GRASS_DARK], [GRASS_MID]],
]

TILE_DIRT = [[DIRT], [DIRT_DARK]]
TILE_DIRT_LIGHT = [[DIRT_LIGHT], [DIRT]]
TILE_PATH_H = [[DIRT], [DIRT_LIGHT]]
TILE_PATH_V = [[DIRT_LIGHT], [DIRT]]
TILE_COBBLE = [[COBBLE], [COBBLE_LIGHT]]

TILE_WATER_FRAMES = [
    [[WATER], [WATER_DEEP]],
    [[WATER_LIGHT], [WATER]],
    [[WATER], [WATER_LIGHT]],
    [[WATER_DEEP], [WATER]],
]

TILE_WATER_SHIMMER_FRAMES = [
    [[WATER_HIGHLIGHT], [WATER_LIGHT]],
    [[WATER_SHIMMER], [WATER_HIGHLIGHT]],
    [[WATER_LIGHT], [WATER]],
    [[WATER], [WATER_LIGHT]],
]


# ═══════════════════════════════════════════════════════════
# TREES (various sizes)
# ═══════════════════════════════════════════════════════════

# Pine tree — 12 wide x 19 tall — lush conical pine with 4 green shades + dark outline
GD = GRASS_DARK
GN = (25, 60, 50)    # darkest pine (Endesga darkest green)
GP = (38, 92, 66)    # pine green (Endesga dark green)
GL = (62, 137, 72)   # light pine (Endesga med green)
GH = (99, 199, 77)   # pine highlight (Endesga bright green)
TK = LOG             # trunk
TB2 = (75, 48, 35)   # bark highlight (lighter brown)
_TO = OL_C           # tree outline for crisp edges

TREE_PINE: Sprite = [
    [_, _, _, _, _, _, _TO, _, _, _, _, _],
    [_, _, _, _, _, _TO, GH, _TO, _, _, _, _],
    [_, _, _, _, _TO, GH, GL, GH, _TO, _, _, _],
    [_, _, _, _TO, GH, GL, GP, GL, GH, _TO, _, _],
    [_, _, _TO, GH, GL, GP, GN, GP, GL, GH, _TO, _],
    [_, _TO, GH, GL, GP, GN, GP, GN, GP, GL, GH, _TO],
    [_, _, _, _TO, GL, GP, GN, GP, GL, _TO, _, _],
    [_, _, _TO, GH, GL, GP, GN, GP, GL, GH, _TO, _],
    [_, _TO, GH, GL, GP, GN, GL, GP, GN, GL, GH, _TO],
    [_TO, GH, GL, GP, GN, GP, GN, GP, GN, GP, GL, _TO],
    [_, _, _TO, GL, GP, GN, GP, GN, GP, GL, _TO, _],
    [_, _TO, GH, GL, GP, GN, GL, GP, GN, GL, GH, _TO],
    [_TO, GH, GL, GP, GN, GP, GN, GP, GN, GP, GL, _TO],
    [_TO, GL, GP, GN, GP, GL, GP, GN, GP, GL, GP, _TO],
    [_, _TO, GL, GP, GN, GP, GN, GP, GN, GP, _TO, _],
    [_, _, _, _, _TO, TK, TK, _TO, _, _, _, _],
    [_, _, _, _, _TO, TK, TB2, _TO, _, _, _, _],
    [_, _, _, _, _TO, TK, TK, _TO, _, _, _, _],
    [_, _, _, _, GN, GN, GN, GN, _, _, _, _],
]

# Oak tree — 14 wide x 16 tall — big bushy oak with round canopy, 4 shades + outline
OD = (25, 60, 50)    # dark oak leaf (Endesga darkest green)
OG = (38, 92, 66)    # oak green (Endesga dark green)
# Note: OL is used for outline in villagers, so use O_L for oak light
O_L = (62, 137, 72)  # light oak leaf (Endesga med green)
OH = (99, 199, 77)   # oak highlight (Endesga bright green)

TREE_OAK: Sprite = [
    [_, _, _, _, _, _TO, OH, O_L, _TO, _, _, _, _, _],
    [_, _, _, _TO, OH, OG, O_L, OG, OH, _TO, _, _, _, _],
    [_, _, _TO, OG, OH, OG, OD, OG, OH, OG, _TO, _, _, _],
    [_, _TO, OG, OD, OG, OH, OG, OH, OG, OD, OG, _TO, _, _],
    [_TO, OG, OD, OG, O_L, OG, OD, OG, O_L, OG, OD, OG, _TO, _],
    [_TO, OD, OG, O_L, OG, OD, OG, OD, OG, O_L, OG, OD, _TO, _],
    [_TO, OG, O_L, OG, OD, OG, O_L, OG, OD, OG, O_L, OG, _TO, _],
    [_TO, OD, OG, O_L, OG, O_L, OG, O_L, OG, O_L, OG, OD, _TO, _],
    [_TO, OG, OD, OG, O_L, OG, OD, OG, O_L, OG, OD, OG, _TO, _],
    [_, _TO, OG, OD, OG, OH, OG, OH, OG, OD, OG, _TO, _, _],
    [_, _, _TO, OG, O_L, OG, OD, OG, O_L, OG, _TO, _, _, _],
    [_, _, _, _TO, OG, O_L, OG, O_L, OG, _TO, _, _, _, _],
    [_, _, _, _, _, _TO, TK, TK, _TO, _, _, _, _, _],
    [_, _, _, _, _, _TO, TK, TB2, _TO, _, _, _, _, _],
    [_, _, _, _, _, _TO, TK, TK, _TO, _, _, _, _, _],
    [_, _, _, _, _, GN, GN, GN, GN, _, _, _, _, _],
]

# Willow tree — 12 wide x 18 tall (weeping willow with droopy branches)
WL_D = (38, 92, 66)   # willow dark (Endesga dark green)
WL_G = (62, 137, 72)  # willow green (Endesga med green)
WL_L = (99, 199, 77)  # willow light (Endesga bright green)
WL_N = (25, 60, 50)   # willow darkest

TREE_WILLOW: Sprite = [
    [_, _, _, _, WL_G, WL_L, WL_G, WL_L, _, _, _, _],
    [_, _, _, WL_G, WL_D, WL_L, WL_G, WL_D, WL_G, _, _, _],
    [_, _, WL_L, WL_D, WL_G, WL_L, WL_D, WL_G, WL_L, WL_D, _, _],
    [_, WL_G, WL_D, WL_G, WL_L, WL_D, WL_G, WL_L, WL_D, WL_G, WL_L, _],
    [WL_L, WL_D, WL_G, WL_L, WL_N, WL_G, WL_N, WL_L, WL_G, WL_D, WL_G, WL_L],
    [WL_D, WL_G, WL_L, WL_D, WL_G, WL_L, WL_G, WL_D, WL_L, WL_G, WL_D, WL_G],
    [WL_G, WL_L, WL_D, WL_G, WL_D, WL_G, WL_D, WL_G, WL_D, WL_L, WL_G, WL_D],
    [WL_D, WL_G, _, WL_D, _, TK, TK, _, WL_G, _, WL_D, WL_G],
    [WL_G, _, WL_D, _, _, TK, TK, _, _, WL_D, _, WL_D],
    [WL_D, _, WL_G, _, _, TK, TK, _, _, WL_G, _, WL_G],
    [_, WL_G, _, WL_D, _, TK, TK, _, WL_D, _, WL_G, _],
    [_, WL_D, _, WL_G, _, TK, TK, _, WL_G, _, WL_D, _],
    [_, _, WL_G, _, WL_D, TK, TK, WL_D, _, WL_G, _, _],
    [_, _, WL_D, _, _, TK, TK, _, _, WL_D, _, _],
    [_, _, _, WL_G, _, TK, TK, _, WL_G, _, _, _],
    [_, _, _, _, _, TK, TK, _, _, _, _, _],
    [_, _, _, _, _, TK, TK, _, _, _, _, _],
    [_, _, _, _, GN, GN, GN, GN, _, _, _, _],
]

# Maple tree — 10 wide x 14 tall (autumn-colored, bigger canopy) + outline
MP_R = (228, 59, 68)   # maple red (Endesga red)
MP_O = (247, 118, 34)  # maple orange (Endesga orange)
MP_Y = (254, 174, 52)  # maple yellow (Endesga yellow-orange)
MP_D = (162, 38, 51)   # maple dark (Endesga dark red)

TREE_MAPLE: Sprite = [
    [_, _, _, _TO, MP_Y, MP_R, _TO, _, _, _],
    [_, _, _TO, MP_Y, MP_O, MP_Y, MP_R, _TO, _, _],
    [_, _TO, MP_D, MP_R, MP_Y, MP_O, MP_D, MP_R, _TO, _],
    [_TO, MP_O, MP_Y, MP_D, MP_R, MP_Y, MP_O, MP_Y, MP_D, _TO],
    [_TO, MP_R, MP_O, MP_R, MP_Y, MP_O, MP_D, MP_R, MP_O, _TO],
    [_TO, MP_D, MP_Y, MP_O, MP_D, MP_R, MP_Y, MP_D, MP_R, _TO],
    [_TO, MP_O, MP_D, MP_R, MP_Y, MP_O, MP_D, MP_R, MP_O, _TO],
    [_, _TO, MP_R, MP_O, MP_D, MP_Y, MP_R, MP_O, _TO, _],
    [_, _, _TO, MP_D, MP_R, MP_D, MP_O, _TO, _, _],
    [_, _, _, _TO, MP_D, MP_O, _TO, _, _, _],
    [_, _, _, _, _TO, TK, _TO, _, _, _],
    [_, _, _, _, _TO, TB2, _TO, _, _, _],
    [_, _, _, _, _TO, TK, _TO, _, _, _],
    [_, _, _, _, GN, GN, GN, _, _, _],
]

# Bush — 7 wide x 5 tall — lush round bush
BD = (25, 60, 50)     # bush dark (Endesga darkest green)
BG = (38, 92, 66)     # bush green (Endesga dark green)
BL = (62, 137, 72)    # bush light (Endesga med green)
BH = (99, 199, 77)    # bush highlight

BUSH: Sprite = [
    [_, _, BG, BH, BL, _, _],
    [_, BG, BL, BG, BH, BG, _],
    [BG, BD, BG, BL, BG, BD, BG],
    [BD, BG, BD, BG, BD, BG, BD],
    [_, BD, BG, BD, BG, BD, _],
]

# Bush with berries — 7 wide x 5 tall
BY = (228, 59, 68)  # berry red (Endesga red)

BUSH_BERRY: Sprite = [
    [_, _, BG, BY, BL, _, _],
    [_, BG, BY, BG, BH, BY, _],
    [BG, BY, BG, BL, BY, BD, BG],
    [BD, BG, BY, BG, BD, BY, BD],
    [_, BD, BG, BD, BG, BD, _],
]

# Small bush / shrub — 2 wide x 2 tall
SHRUB: Sprite = [
    [BG, BL],
    [BD, BG],
]

# Tall grass — 3 wide x 4 tall
TG = GRASS_HIGHLIGHT
TGD = GRASS_MID

TALL_GRASS: Sprite = [
    [_, TG, _],
    [TG, TGD, TG],
    [TGD, TG, TGD],
    [GRASS, GRASS_MID, GRASS],
]


# ═══════════════════════════════════════════════════════════
# FLOWERS (scattered decoration)
# ═══════════════════════════════════════════════════════════

FLOWER_SPRITES = [
    # Red flower — 3×4 (row-doubled for half-block crispness)
    [[_, FLOWER_RED, _], [_, FLOWER_RED, _], [FLOWER_RED, FLOWER_YELLOW, FLOWER_RED], [GRASS, GRASS_MID, GRASS]],
    # Yellow flower — 3×4
    [[_, FLOWER_YELLOW, _], [_, FLOWER_YELLOW, _], [FLOWER_YELLOW, FLOWER_RED, FLOWER_YELLOW], [GRASS_MID, GRASS, GRASS_MID]],
    # Blue flower — 3×4
    [[_, FLOWER_BLUE, _], [_, FLOWER_BLUE, _], [FLOWER_BLUE, FLOWER_WHITE, FLOWER_BLUE], [GRASS, GRASS_MID, GRASS]],
    # Pink flower — 3×4
    [[_, FLOWER_PINK, _], [_, FLOWER_PINK, _], [FLOWER_PINK, FLOWER_YELLOW, FLOWER_PINK], [GRASS_MID, GRASS, GRASS_MID]],
    # White flower — 3×4
    [[FLOWER_WHITE, _, FLOWER_WHITE], [FLOWER_WHITE, _, FLOWER_WHITE], [_, FLOWER_YELLOW, _], [GRASS, GRASS_MID, GRASS]],
    # Purple flower — 3×4
    [[_, FLOWER_PURPLE, _], [_, FLOWER_PURPLE, _], [FLOWER_PURPLE, FLOWER_PINK, FLOWER_PURPLE], [GRASS, GRASS_MID, GRASS]],
]

# Rock — small (3×4, row-doubled for half-block crispness)
RK_D = STONE_DARK
RK = STONE
RK_L = STONE_LIGHT
ROCK_SMALL: Sprite = [
    [_, RK, _],
    [_, RK, _],
    [RK_D, RK_L, RK],
    [_, RK_D, _],
]

# Rock — large (5×4)
ROCK_LARGE: Sprite = [
    [_, RK, RK_L, RK, _],
    [RK_D, RK, RK_L, RK, RK_D],
    [RK, RK_D, RK, RK_D, RK],
    [_, RK_D, RK, RK_D, _],
]

# Tree stump (3×4, row-doubled for half-block crispness)
STUMP: Sprite = [
    [_, LOG, _],
    [_, LOG, _],
    [LOG, WOOD_DARK, LOG],
    [_, LOG, _],
]

# Log on ground (5×2)
FALLEN_LOG: Sprite = [
    [LOG, WOOD, LOG, WOOD, LOG],
    [WOOD_DARK, LOG, WOOD_DARK, LOG, WOOD_DARK],
]


# ═══════════════════════════════════════════════════════════
# DECORATION SPRITES (barrels, crates, market stalls, etc.)
# ═══════════════════════════════════════════════════════════

# ── Barrel (5w × 6h) — wooden barrel with metal bands ──
_BRL_W = WOOD_PLANK
_BRL_D = WOOD_DARK
_BRL_L = WOOD_LIGHT
_BRL_M = STONE_DARK  # metal band

BARREL: Sprite = [
    [_, OL_C, _BRL_W, OL_C, _],
    [OL_C, _BRL_L, _BRL_W, _BRL_D, OL_C],
    [OL_C, _BRL_M, _BRL_M, _BRL_M, OL_C],
    [OL_C, _BRL_W, _BRL_D, _BRL_W, OL_C],
    [OL_C, _BRL_M, _BRL_M, _BRL_M, OL_C],
    [_, OL_C, _BRL_D, OL_C, _],
]

# ── Crate (5w × 5h) — wooden shipping crate ──
_CR_W = WOOD_PLANK
_CR_D = WOOD_DARK
_CR_L = WOOD_LIGHT

CRATE: Sprite = [
    [OL_C, OL_C, OL_C, OL_C, OL_C],
    [OL_C, _CR_W, _CR_D, _CR_W, OL_C],
    [OL_C, _CR_D, _CR_L, _CR_D, OL_C],
    [OL_C, _CR_W, _CR_D, _CR_W, OL_C],
    [OL_C, OL_C, OL_C, OL_C, OL_C],
]

# ── Crate Stack (6w × 8h) — two crates stacked ──
CRATE_STACK: Sprite = [
    [_, OL_C, OL_C, OL_C, OL_C, _],
    [_, OL_C, _CR_L, _CR_D, OL_C, _],
    [_, OL_C, _CR_D, _CR_L, OL_C, _],
    [_, OL_C, OL_C, OL_C, OL_C, _],
    [OL_C, OL_C, OL_C, OL_C, OL_C, OL_C],
    [OL_C, _CR_W, _CR_D, _CR_W, _CR_D, OL_C],
    [OL_C, _CR_D, _CR_L, _CR_D, _CR_L, OL_C],
    [OL_C, OL_C, OL_C, OL_C, OL_C, OL_C],
]

# ── Market Stall (12w × 8h) — open stall with striped awning ──
_MS_AW = ROOF_RED
_MS_AD = ROOF_RED_DARK
_MS_AL = ROOF_RED_LIGHT
_MS_PL = WOOD_PLANK
_MS_PD = WOOD_DARK
_MS_GD = WINDOW_GLOW  # goods on display

MARKET_STALL: Sprite = [
    [OL_C, _MS_AW, _MS_AD, _MS_AL, _MS_AW, _MS_AD, _MS_AL, _MS_AW, _MS_AD, _MS_AL, _MS_AW, OL_C],
    [OL_C, _MS_AD, _MS_AW, _MS_AD, _MS_AL, _MS_AW, _MS_AD, _MS_AL, _MS_AW, _MS_AD, _MS_AL, OL_C],
    [_MS_PD, _, _, _, _, _, _, _, _, _, _, _MS_PD],
    [_MS_PL, _, _, _, _, _, _, _, _, _, _, _MS_PL],
    [_MS_PD, _, _, _, _, _, _, _, _, _, _, _MS_PD],
    [_MS_PL, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _MS_PL],
    [_MS_PD, OL_C, _MS_GD, _CR_W, _MS_GD, _CR_D, _MS_GD, _CR_W, _MS_GD, _CR_D, OL_C, _MS_PD],
    [_MS_PL, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _MS_PL],
]

# ── Lamp Post (3w × 8h) — iron lamp with warm glow ──
_LP_I = STONE_DARK   # iron
_LP_G = WINDOW_GLOW  # glow
_LP_B = WINDOW_BRIGHT # bright

LAMP_POST: Sprite = [
    [_, _LP_B, _],
    [_LP_G, _LP_B, _LP_G],
    [_, _LP_G, _],
    [OL_C, _LP_I, OL_C],
    [_, _LP_I, _],
    [_, _LP_I, _],
    [_, _LP_I, _],
    [_, OL_C, _],
]

# ── Sign Post (5w × 7h) — wooden sign on a post ──
_SG_W = WOOD_PLANK
_SG_D = WOOD_DARK
_SG_L = WOOD_LIGHT

SIGN_POST: Sprite = [
    [OL_C, OL_C, OL_C, OL_C, OL_C],
    [OL_C, _SG_L, _SG_W, _SG_D, OL_C],
    [OL_C, _SG_D, _SG_W, _SG_L, OL_C],
    [OL_C, OL_C, OL_C, OL_C, OL_C],
    [_, _, _SG_D, _, _],
    [_, _, _SG_D, _, _],
    [_, _, OL_C, _, _],
]

# ── Well (improved, 7w × 8h) — stone well with rope and bucket ──
_WL_S = STONE
_WL_SD = STONE_DARK
_WL_SL = STONE_LIGHT
_WL_WB = WATER_LIGHT
_WL_R = WOOD_DARK  # rope

WELL_SPRITE: Sprite = [
    [_, _, _WL_R, OL_C, _WL_R, _, _],
    [_, _, _, OL_C, _, _, _],
    [_, OL_C, _WL_SD, _WL_S, _WL_SD, OL_C, _],
    [OL_C, _WL_SD, _WL_WB, _WL_WB, _WL_WB, _WL_SD, OL_C],
    [OL_C, _WL_S, _WL_WB, _WL_WB, _WL_WB, _WL_S, OL_C],
    [OL_C, _WL_SL, _WL_WB, _WL_WB, _WL_WB, _WL_SL, OL_C],
    [_, OL_C, _WL_S, _WL_S, _WL_S, OL_C, _],
    [_, _, OL_C, OL_C, OL_C, _, _],
]

# ── Fence Variants ──
# Stone fence (3w × 4h)
FENCE_STONE: Sprite = [
    [_, STONE_DARK, _],
    [STONE, STONE, STONE],
    [STONE_DARK, STONE, STONE_DARK],
    [_, STONE_DARK, _],
]

# Wooden fence with cross (3w × 4h)
FENCE_WOOD: Sprite = [
    [_, WOOD_DARK, _],
    [WOOD_PLANK, WOOD_DARK, WOOD_PLANK],
    [WOOD_DARK, WOOD_PLANK, WOOD_DARK],
    [_, WOOD_DARK, _],
]

# ── Flower Bed (6w × 3h) — dense flower planting ──
FLOWER_BED: Sprite = [
    [FLOWER_RED, GRASS_LIGHT, FLOWER_YELLOW, GRASS_LIGHT, FLOWER_BLUE, FLOWER_PINK],
    [GRASS, FLOWER_PINK, GRASS, FLOWER_RED, GRASS, FLOWER_YELLOW],
    [DIRT_LIGHT, DIRT, DIRT_LIGHT, DIRT, DIRT_LIGHT, DIRT],
]

# ── Bench (5w × 3h) — wooden park bench ──
_BN_W = BENCH_WOOD
_BN_D = BENCH_DARK

BENCH: Sprite = [
    [OL_C, _BN_W, _BN_W, _BN_W, OL_C],
    [OL_C, _BN_D, _BN_W, _BN_D, OL_C],
    [_BN_D, _, _, _, _BN_D],
]

# ── Trash Can (2w × 4h) — metal bin ──
_TC = TRASHCAN
_TL = TRASHCAN_LID

TRASH_CAN: Sprite = [
    [_TL, _TL],
    [OL_C, OL_C],
    [_TC, _TC],
    [OL_C, OL_C],
]

# ── Potted Plant (3w × 4h) — terracotta pot with plant ──
_PT_T = POT_TERRACOTTA
_PT_D = POT_DARK
_PT_G = GRASS_LIGHT
_PT_GD = GRASS

POTTED_PLANT: Sprite = [
    [_, _PT_G, _],
    [_PT_GD, _PT_G, _PT_GD],
    [OL_C, _PT_T, OL_C],
    [_, _PT_D, _],
]

# ── Street Sign (1w × 5h) — thin post with sign ──
_SSG = SIGN_WOOD

STREET_SIGN: Sprite = [
    [_SSG],
    [OL_C],
    [OL_C],
    [OL_C],
    [OL_C],
]


# ═══════════════════════════════════════════════════════════
# BUILDINGS
# ═══════════════════════════════════════════════════════════

# ── Basic Hut (11 wide x 14 tall) — bigger cottage with more detail ──
# Peaked roof with shingles, visible window frames, detailed door
RR = ROOF_RED
RD = ROOF_RED_DARK
RL = ROOF_RED_LIGHT
WW = WOOD_PLANK
WD = WOOD_DARK
WL = WOOD_LIGHT
WG = WINDOW_GLOW
DR = WOOD_DARK        # door

HUT: Sprite = [
    [_, _, _, _, _, OL_C, _, _, _, _, _],
    [_, _, _, _, OL_C, RD, OL_C, _, _, _, _],
    [_, _, _, OL_C, RD, RR, RL, OL_C, _, _, _],
    [_, _, OL_C, RR, RL, RR, RL, RR, OL_C, _, _],
    [_, OL_C, RD, RR, RL, RR, RL, RR, RD, OL_C, _],
    [OL_C, RR, RL, RR, RL, RR, RL, RR, RL, RR, OL_C],
    [OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C],
    [OL_C, WW, WD, WW, WW, WW, WW, WW, WD, WW, OL_C],
    [OL_C, WW, WG, WG, WW, WW, WW, WG, WG, WW, OL_C],
    [OL_C, WW, WG, WG, WW, WW, WW, WG, WG, WW, OL_C],
    [OL_C, WW, WD, WD, WW, WW, WW, WD, WD, WW, OL_C],
    [OL_C, WW, WW, WW, WW, DR, WW, WW, WW, WW, OL_C],
    [OL_C, WW, WW, WW, WW, DR, WW, WW, WW, WW, OL_C],
    [OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C],
]

# ── Farm House (13 wide x 14 tall) — bigger farmhouse with detail ──
RT = ROOF_THATCH
RTD = ROOF_THATCH_DARK
RTL = ROOF_THATCH_LIGHT

FARM: Sprite = [
    [_, _, _, _, _, _, OL_C, _, _, _, _, _, _],
    [_, _, _, _, _, OL_C, RTD, OL_C, _, _, _, _, _],
    [_, _, _, _, OL_C, RT, RTL, RT, OL_C, _, _, _, _],
    [_, _, _, OL_C, RTD, RT, RTL, RT, RTD, OL_C, _, _, _],
    [_, _, OL_C, RT, RTL, RT, RTL, RT, RTL, RT, OL_C, _, _],
    [_, OL_C, RTD, RT, RTL, RT, RTL, RT, RTL, RT, RTD, OL_C, _],
    [OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C],
    [OL_C, WW, WD, WW, WW, WW, WW, WW, WW, WW, WD, WW, OL_C],
    [OL_C, WW, WG, WG, WW, WW, WW, WW, WW, WG, WG, WW, OL_C],
    [OL_C, WW, WG, WG, WW, WW, WW, WW, WW, WG, WG, WW, OL_C],
    [OL_C, WW, WD, WD, WW, WW, WW, WW, WW, WD, WD, WW, OL_C],
    [OL_C, WW, WW, WW, DR, DR, WW, WG, WG, WW, WW, WW, OL_C],
    [OL_C, WW, WW, WW, DR, DR, WW, WG, WG, WW, WW, WW, OL_C],
    [OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C],
]

# ── Library (16 wide x 14 tall) ─────────────────────────
# Grand stone library with blue roof, arched windows, bookshelves visible
RB = ROOF_BLUE
RBD = ROOF_BLUE_DARK
RBL = ROOF_BLUE_LIGHT
SS = STONE
SD = STONE_DARK
SL = STONE_LIGHT

LIBRARY: Sprite = [
    [_, _, _, _, _, _, _, OL_C, OL_C, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, OL_C, RBD, RBL, OL_C, _, _, _, _, _, _],
    [_, _, _, _, _, OL_C, RB, RBL, RB, RBD, OL_C, _, _, _, _, _],
    [_, _, _, _, OL_C, RB, RBL, RB, RBL, RB, RBD, OL_C, _, _, _, _],
    [_, _, _, OL_C, RBD, RB, RBL, RB, RBL, RB, RBL, RB, OL_C, _, _, _],
    [_, _, OL_C, RB, RBL, RB, RBL, RB, RBL, RB, RBL, RB, RBD, OL_C, _, _],
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
    [_, _, OL_C, SS, SD, SS, SS, SS, SS, SS, SS, SS, SS, OL_C, _, _],
    [_, _, OL_C, SS, WG, WG, SS, SL, SS, SL, SS, WG, WG, OL_C, _, _],
    [_, _, OL_C, SS, WG, WG, SS, SL, SS, SL, SS, WG, WG, OL_C, _, _],
    [_, _, OL_C, SS, SD, SD, SS, SS, SS, SS, SS, SD, SD, OL_C, _, _],
    [_, _, OL_C, SS, SS, SS, SS, SD, DR, SD, SS, SS, SS, OL_C, _, _],
    [_, _, OL_C, SS, SS, SS, SS, SD, DR, SD, SS, SS, SS, OL_C, _, _],
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
]

# ── Forge / Workshop (16 wide x 14 tall) ────────────────
# Stone building with chimney, smoke, anvil area, warm glow
CH = STONE_DARK       # chimney
FL = LANTERN          # forge flame

FORGE: Sprite = [
    [_, _, _, _, _, _, _, _, _, _, _, _, _, OL_C, OL_C, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, OL_C, OL_C, _],
    [_, _, _, _, _, _, _, OL_C, OL_C, _, _, _, OL_C, CH, OL_C, _],
    [_, _, _, _, _, _, OL_C, RD, RR, OL_C, _, _, OL_C, CH, OL_C, _],
    [_, _, _, _, _, OL_C, RR, RL, RR, RD, OL_C, _, OL_C, SD, OL_C, _],
    [_, _, _, _, OL_C, RR, RL, RR, RL, RR, RD, OL_C, _, _, _, _],
    [_, _, _, OL_C, RD, RL, RR, RL, RR, RL, RR, RD, OL_C, _, _, _],
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
    [_, _, OL_C, SS, SD, SS, SS, SS, SS, SS, SS, SS, SD, OL_C, _, _],
    [_, _, OL_C, SS, FL, FL, SS, SS, SS, SS, WG, WG, SS, OL_C, _, _],
    [_, _, OL_C, SS, FL, FL, SS, SS, SS, SS, WG, WG, SS, OL_C, _, _],
    [_, _, OL_C, SS, SD, SD, SS, SS, SS, SS, SD, SD, SS, OL_C, _, _],
    [_, _, OL_C, SS, SS, SS, SS, SD, DR, SD, SS, SS, SS, OL_C, _, _],
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
]

# ── Market Square (18 wide x 12 tall) ───────────────────
# Wide market building with striped awning, display counter, goods
AW = ROOF_RED          # awning
AWD = ROOF_RED_DARK
AWL = ROOF_RED_LIGHT
PL = WOOD_PLANK        # post/pillar
CR = ROOF_THATCH_LIGHT  # crate

MARKET: Sprite = [
    [_, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _],
    [_, OL_C, AW, AWD, AW, AWL, AW, AWD, AW, AWL, AW, AWD, AW, AWL, AW, AWD, OL_C, _],
    [_, OL_C, AWD, AW, AWL, AW, AWD, AW, AWL, AW, AWD, AW, AWL, AW, AWD, AW, OL_C, _],
    [_, OL_C, PL, _, _, _, _, PL, _, _, _, _, PL, _, _, _, OL_C, _],
    [_, OL_C, PL, WW, WD, WW, WW, PL, WW, WW, WD, WW, PL, WW, WD, WW, OL_C, _],
    [_, OL_C, PL, WW, WG, WG, WW, PL, WW, WG, WG, WW, PL, WW, WG, WW, OL_C, _],
    [_, OL_C, PL, WW, WG, WG, WW, PL, WW, WG, WG, WW, PL, WW, WG, WW, OL_C, _],
    [_, OL_C, PL, WW, WD, WD, WW, PL, WW, WD, WD, WW, PL, WW, WD, WW, OL_C, _],
    [_, OL_C, PL, CR, CR, _, _, PL, _, _, CR, CR, PL, _, CR, CR, OL_C, _],
    [_, OL_C, PL, CR, WG, _, _, PL, _, _, WG, CR, PL, _, WG, CR, OL_C, _],
    [_, OL_C, WW, WD, WW, WD, WW, WD, WW, WD, WW, WD, WW, WD, WW, WD, OL_C, _],
    [_, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _],
]

# ── Tavern (16 wide x 14 tall) ──────────────────────────
# Warm wooden tavern with thatch roof, sign, glowing windows, chimney
SG = WOOD_LIGHT        # sign

TAVERN: Sprite = [
    [_, _, _, _, _, _, _, _, _, _, _, _, _, OL_C, OL_C, _],
    [_, _, _, _, _, _, _, OL_C, OL_C, _, _, _, _, OL_C, OL_C, _],
    [_, _, _, _, _, _, OL_C, RTD, RT, OL_C, _, _, OL_C, SD, OL_C, _],
    [_, _, _, _, _, OL_C, RT, RTL, RT, RTD, OL_C, _, _, _, _, _],
    [_, _, _, _, OL_C, RTD, RT, RTL, RT, RTL, RT, OL_C, _, _, _, _],
    [_, _, _, OL_C, RT, RTL, RT, RTL, RT, RTL, RT, RTD, OL_C, _, _, _],
    [_, _, OL_C, RTD, RT, RTL, RT, RTL, RT, RTL, RT, RTL, RT, OL_C, _, _],
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
    [_, _, OL_C, WW, WD, WW, WW, SG, SG, SG, WW, WW, WD, OL_C, _, _],
    [_, _, OL_C, WW, WG, WG, WW, SG, WD, SG, WW, WG, WG, OL_C, _, _],
    [_, _, OL_C, WW, WG, WG, WW, WW, WW, WW, WW, WG, WG, OL_C, _, _],
    [_, _, OL_C, WW, WD, WD, WW, WW, WW, WW, WW, WD, WD, OL_C, _, _],
    [_, _, OL_C, WW, WW, WW, WW, DR, DR, WW, WG, WG, WW, OL_C, _, _],
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
]

# ── Garden / Fields (9 wide x 6 tall) ───────────────────
# Open plot with crops and flowers
CRP1 = (62, 137, 72)   # crop green (Endesga med green)
CRP2 = (99, 199, 77)   # crop light (Endesga bright green)
CRP3 = (38, 92, 66)    # crop dark (Endesga dark green)
SOIL = (115, 62, 57)   # tilled soil (Endesga dark brown)

GARDEN: Sprite = [
    [WD, WW, WD, WW, WD, WW, WD, WW, WD],
    [CRP1, SOIL, CRP2, SOIL, CRP3, SOIL, CRP1, SOIL, CRP2],
    [CRP2, SOIL, CRP1, SOIL, CRP2, SOIL, CRP3, SOIL, CRP1],
    [CRP3, SOIL, CRP2, SOIL, CRP1, SOIL, CRP2, SOIL, CRP3],
    [CRP1, SOIL, CRP3, SOIL, CRP2, SOIL, CRP1, SOIL, CRP2],
    [WD, WW, WD, WW, WD, WW, WD, WW, WD],
]

# ── Tower (10 wide x 16 tall) ───────────────────────────
# Tall narrow stone watchtower with lookout platform, windows, flag
FL_R = ROOF_RED  # flag

TOWER: Sprite = [
    [_, _, _, _, FL_R, FL_R, _, _, _, _],
    [_, _, _, _, OL_C, OL_C, _, _, _, _],
    [_, OL_C, OL_C, OL_C, SD, SL, OL_C, OL_C, OL_C, _],
    [_, OL_C, SS, SL, SS, SS, SL, SS, OL_C, _],
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
    [_, _, OL_C, SS, SD, SS, SD, OL_C, _, _],
    [_, _, OL_C, SS, WG, WG, SS, OL_C, _, _],
    [_, _, OL_C, SS, SD, SD, SS, OL_C, _, _],
    [_, _, OL_C, SS, SS, SS, SS, OL_C, _, _],
    [_, _, OL_C, SS, WG, WG, SS, OL_C, _, _],
    [_, _, OL_C, SS, SD, SD, SS, OL_C, _, _],
    [_, _, OL_C, SS, SS, SS, SS, OL_C, _, _],
    [_, _, OL_C, SS, WG, WG, SS, OL_C, _, _],
    [_, _, OL_C, SS, SD, SD, SS, OL_C, _, _],
    [_, _, OL_C, SS, DR, DR, SS, OL_C, _, _],
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
]

# ── Castle (13 wide x 12 tall) ──────────────────────────
# Grand main building with twin towers
TW = STONE_ACCENT     # tower stone
TB = STONE_DARK        # tower battlement

CASTLE: Sprite = [
    [TB, _, TB, _, _, _, _, _, _, _, TB, _, TB],
    [SS, TB, SS, _, _, RD, _, _, _, SS, TB, SS, _],
    [SS, SD, SS, _, RD, RR, RD, _, SS, SD, SS, _, _],
    [SS, WG, SS, RD, RR, RL, RR, RD, SS, WG, SS, _, _],
    [SS, SD, SS, SS, SS, SS, SS, SS, SS, SD, SS, _, _],
    [SS, WG, SS, SS, WG, SS, WG, SS, SS, WG, SS, _, _],
    [SS, SD, SS, SS, SD, SS, SD, SS, SS, SD, SS, _, _],
    [SS, WG, SS, SS, WG, SS, WG, SS, SS, WG, SS, _, _],
    [SS, SD, SS, SS, SD, SS, SD, SS, SS, SD, SS, _, _],
    [SS, SS, SS, SS, SD, DR, SD, SS, SS, SS, SS, _, _],
    [SS, SS, SS, SS, SD, DR, SD, SS, SS, SS, SS, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _],
]

# ── Well (5 wide x 6 tall) ──────────────────────────────
WS = STONE_LIGHT       # well stone
WB = WATER_LIGHT       # well water

WELL: Sprite = [
    [_, WD, WL, WD, _],
    [_, _, WD, _, _],
    [_, SD, SS, SD, _],
    [SD, WB, WB, WB, SD],
    [SS, WB, WB, WB, SS],
    [_, SS, SS, SS, _],
]

# ── Windmill (7 wide x 12 tall) ─────────────────────────
BL_W = WOOD_LIGHT      # blade
BL_D = WOOD_DARK       # blade dark

WINDMILL_FRAMES: list[Sprite] = [
    # Frame 0 — blades at +
    [
        [_, _, _, BL_W, _, _, _],
        [_, _, _, BL_W, _, _, _],
        [_, _, _, BL_D, _, _, _],
        [BL_D, BL_W, BL_W, WD, BL_W, BL_W, BL_D],
        [_, _, _, BL_D, _, _, _],
        [_, _, _, BL_W, _, _, _],
        [_, _, RTD, RT, RTD, _, _],
        [_, RTD, RT, RTL, RT, RTD, _],
        [_, SS, SD, SS, SD, SS, _],
        [_, SS, WG, SS, WG, SS, _],
        [_, SS, SD, DR, SD, SS, _],
        [_, SS, SD, DR, SD, SS, _],
    ],
    # Frame 1 — blades at x
    [
        [_, BL_D, _, _, _, BL_W, _],
        [_, _, BL_W, _, BL_D, _, _],
        [_, _, _, BL_D, _, _, _],
        [_, _, _, WD, _, _, _],
        [_, _, _, BL_D, _, _, _],
        [_, BL_W, _, _, _, BL_D, _],
        [BL_D, _, RTD, RT, RTD, _, BL_W],
        [_, RTD, RT, RTL, RT, RTD, _],
        [_, SS, SD, SS, SD, SS, _],
        [_, SS, WG, SS, WG, SS, _],
        [_, SS, SD, DR, SD, SS, _],
        [_, SS, SD, DR, SD, SS, _],
    ],
]

# ── Bridge segment (5 wide x 4 tall) ────────────────────
BRIDGE: Sprite = [
    [WD, WW, WW, WW, WD],
    [WW, DIRT, DIRT, DIRT, WW],
    [WW, DIRT_LIGHT, DIRT, DIRT_LIGHT, WW],
    [WD, WW, WW, WW, WD],
]

# ── Fence segment (3 wide x 4 tall, row-doubled for half-block crispness) ────
FENCE_H: Sprite = [
    [_, WD, _],
    [WW, WW, WW],
    [WW, WW, WW],
    [_, WD, _],
]

FENCE_POST: Sprite = [
    [WD],
    [WW],
    [WW],
    [WD],
]


# ═══════════════════════════════════════════════════════════
# CUSTOMER BUILDING SPRITES (v2 — larger, more detailed)
# ═══════════════════════════════════════════════════════════

# ── Beauty Shop (18w × 16h) — pink/purple barber pole, mirror sign ──
SP = SALON_PINK
SS_S = SALON_STRIPE  # renamed to avoid conflict with SS (STONE)
_PUR = ROOF_PURPLE   # purple accent
_PPD = ROOF_PURPLE_DARK

BUILDING_BEAUTY: Sprite = [
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
    [_, _, OL_C, SP, SS_S, SP, SS_S, SP, SS_S, SP, SS_S, SP, SS_S, SP, SS_S, SP, SS_S, OL_C, _, _],
    [_, _, OL_C, SS_S, SP, SS_S, SP, SS_S, SP, SS_S, SP, SS_S, SP, SS_S, SP, SS_S, SP, OL_C, _, _],
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
    [_, _, OL_C, WW, WD, WW, WW, WW, WW, WW, WW, WW, WW, WW, WW, WD, WW, OL_C, _, _],
    [_, _, OL_C, WW, WG, WG, WG, WW, _PUR, OL_C, _PUR, WW, WG, WG, WG, WW, WW, OL_C, _, _],
    [_, _, OL_C, WW, WG, WG, WG, WW, OL_C, SP, OL_C, WW, WG, WG, WG, WW, WW, OL_C, _, _],
    [_, _, OL_C, WW, WG, WG, WG, WW, _PUR, OL_C, _PUR, WW, WG, WG, WG, WW, WW, OL_C, _, _],
    [_, _, OL_C, WW, WD, WD, WD, WW, WW, WW, WW, WW, WD, WD, WD, WW, WW, OL_C, _, _],
    [_, _, OL_C, WW, WW, WW, WW, WW, WW, WW, WW, WW, WW, WW, WW, WW, WW, OL_C, _, _],
    [_, _, OL_C, WW, SP, SS_S, SP, WW, WW, DR, DR, WW, WW, SP, SS_S, SP, WW, OL_C, _, _],
    [_, _, OL_C, WW, SS_S, SP, SS_S, WW, WW, DR, DR, WW, WW, SS_S, SP, SS_S, WW, OL_C, _, _],
    [_, _, OL_C, WW, SP, SS_S, SP, WW, WW, WW, WW, WW, WW, SP, SS_S, SP, WW, OL_C, _, _],
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
]

# ── Restaurant (16w × 16h) — red awning, chimney with smoke pixels ──
RW = RESTAURANT_WARM
RC_C = RESTAURANT_CHIMNEY
_SMK = SMOKE_LIGHT   # smoke from chimney

BUILDING_RESTAURANT: Sprite = [
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, OL_C, _SMK, _, _],
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, RC_C, OL_C, _, _],
    [_, _, OL_C, RD, RR, RR, RL, RR, RR, RL, RR, RR, RL, RR, RD, OL_C, RC_C, OL_C, _, _],
    [_, _, OL_C, RR, RL, RR, RL, RR, RL, RR, RL, RR, RL, RR, RR, OL_C, _, _, _, _],
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _, _, _],
    [_, _, OL_C, WW, WD, WW, WW, WW, WW, WW, WW, WW, WW, WD, WW, OL_C, _, _, _, _],
    [_, _, OL_C, WW, WG, WG, WW, RW, RW, RW, WW, WW, WG, WG, WW, OL_C, _, _, _, _],
    [_, _, OL_C, WW, WG, WG, WW, RW, WG, RW, WW, WW, WG, WG, WW, OL_C, _, _, _, _],
    [_, _, OL_C, WW, WD, WD, WW, WW, WW, WW, WW, WW, WD, WD, WW, OL_C, _, _, _, _],
    [_, _, OL_C, WW, WW, WW, WW, WW, WW, WW, WW, WW, WW, WW, WW, OL_C, _, _, _, _],
    [_, _, OL_C, WW, WW, WW, DR, DR, WW, WG, WG, WG, WW, WW, WW, OL_C, _, _, _, _],
    [_, _, OL_C, WW, WW, WW, DR, DR, WW, WG, WG, WG, WW, WW, WW, OL_C, _, _, _, _],
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, RW, _, _, RW, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, WD, _, _, WD, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
]

# ── Gym / Fitness (18w × 16h) — blue accents, dumbbell sign ──
GB = GYM_BLUE
GS = GYM_STEEL

BUILDING_FITNESS: Sprite = [
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
    [_, _, OL_C, GB, GB, GB, GB, GB, GB, GB, GB, GB, GB, GB, GB, GB, GB, OL_C, _, _],
    [_, _, OL_C, GB, GS, GS, GB, GB, GB, GB, GB, GB, GB, GS, GS, GB, GB, OL_C, _, _],
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
    [_, _, OL_C, SS, SD, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SD, SS, OL_C, _, _],
    [_, _, OL_C, SS, GS, GS, SS, GS, OL_C, OL_C, OL_C, GS, SS, GS, GS, SS, SS, OL_C, _, _],
    [_, _, OL_C, SS, GS, GS, SS, SS, SS, GB, SS, SS, SS, GS, GS, SS, SS, OL_C, _, _],
    [_, _, OL_C, SS, SD, SD, SS, GS, OL_C, OL_C, OL_C, GS, SS, SD, SD, SS, SS, OL_C, _, _],
    [_, _, OL_C, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, OL_C, _, _],
    [_, _, OL_C, SS, WG, WG, SS, SS, SS, SS, SS, SS, SS, SS, WG, WG, SS, OL_C, _, _],
    [_, _, OL_C, SS, WG, WG, SS, SS, SS, SS, SS, SS, SS, SS, WG, WG, SS, OL_C, _, _],
    [_, _, OL_C, SS, SD, SD, SS, SS, DR, DR, DR, DR, SS, SS, SD, SD, SS, OL_C, _, _],
    [_, _, OL_C, SS, SS, SS, SS, SS, DR, DR, DR, DR, SS, SS, SS, SS, SS, OL_C, _, _],
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
]

# ── Home Services / Workshop (11w × 10h) ───────────────
HO = HOME_OLIVE
HT = HOME_TRUCK

BUILDING_HOME_SERVICES: Sprite = [
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _, _, _],
    [_, _, OL_C, HO, HO, HO, HO, HO, HO, HO, HO, HO, HO, HO, HO, OL_C, _, _, _, _],
    [_, _, OL_C, HO, HO, HO, HO, HO, HO, HO, HO, HO, HO, HO, HO, OL_C, _, _, _, _],
    [_, _, OL_C, WW, WD, WW, WW, WW, WW, WW, WW, WW, WD, WW, WW, OL_C, _, _, _, _],
    [_, _, OL_C, WW, WG, WG, WW, WW, WW, WW, WW, WW, WG, WG, WW, OL_C, _, _, _, _],
    [_, _, OL_C, WW, WG, WG, WW, WW, WW, WW, WW, WW, WG, WG, WW, OL_C, _, _, _, _],
    [_, _, OL_C, WW, WD, WD, WW, WW, WW, WW, WW, WW, WD, WD, WW, OL_C, _, _, _, _],
    [_, _, OL_C, WW, WW, WW, WW, WW, WW, WW, WW, WW, WW, WW, WW, OL_C, _, _, _, _],
    [_, _, OL_C, WW, WW, WW, DR, DR, DR, WW, WW, WW, WW, WW, WW, OL_C, _, _, _, _],
    [_, _, OL_C, WW, WW, WW, DR, DR, DR, WW, WW, WW, WW, WW, WW, OL_C, HT, HT, _, _],
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, HT, HT, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, HT, HT, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, SD, SD, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
]

# ── Professional Office (10w × 11h) ───────────────────
OM = OFFICE_MARBLE
OC = OFFICE_COLUMN

BUILDING_PROFESSIONAL: Sprite = [
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
    [_, _, OL_C, SS, SS, SD, SS, SS, SS, SS, SS, SS, SS, SD, SS, SS, SS, OL_C, _, _],
    [_, _, OL_C, OC, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, OC, OL_C, _, _],
    [_, _, OL_C, OC, SS, WG, WG, SS, SS, SS, SS, SS, SS, WG, WG, SS, OC, OL_C, _, _],
    [_, _, OL_C, OC, SS, WG, WG, SS, SS, SS, SS, SS, SS, WG, WG, SS, OC, OL_C, _, _],
    [_, _, OL_C, OC, SS, SD, SD, SS, SS, SS, SS, SS, SS, SD, SD, SS, OC, OL_C, _, _],
    [_, _, OL_C, OC, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, OC, OL_C, _, _],
    [_, _, OL_C, OC, SS, WG, WG, SS, SS, SS, SS, SS, SS, WG, WG, SS, OC, OL_C, _, _],
    [_, _, OL_C, OC, SS, WG, WG, SS, SS, SS, SS, SS, SS, WG, WG, SS, OC, OL_C, _, _],
    [_, _, OL_C, OC, SS, SD, SD, SS, SS, SS, SS, SS, SS, SD, SD, SS, OC, OL_C, _, _],
    [_, _, OL_C, OC, SS, SS, SS, SS, SD, DR, DR, SD, SS, SS, SS, SS, OC, OL_C, _, _],
    [_, _, OL_C, OC, SS, SS, SS, SS, SD, DR, DR, SD, SS, SS, SS, SS, OC, OL_C, _, _],
    [_, _, OL_C, OM, OM, OM, OM, OM, OM, OM, OM, OM, OM, OM, OM, OM, OM, OL_C, _, _],
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
]

# ── Creative Studio (10w × 10h) ───────────────────────
SO = STUDIO_ORANGE
ST_T = STUDIO_TEAL

BUILDING_CREATIVE: Sprite = [
    [_, _, _, _, _, _, _, _, OL_C, OL_C, OL_C, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, OL_C, RD, RR, RD, OL_C, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, OL_C, RR, RL, RR, RL, RR, OL_C, _, _, _, _, _, _, _],
    [_, _, _, _, _, OL_C, RR, RL, RR, RL, RR, RL, RR, OL_C, _, _, _, _, _, _],
    [_, _, OL_C, OL_C, OL_C, RD, RL, RR, RL, RR, RL, RR, RD, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
    [_, _, OL_C, WW, WD, WW, WW, WW, WW, WW, WW, WW, WW, WW, WD, WW, WW, OL_C, _, _],
    [_, _, OL_C, WW, ST_T, ST_T, ST_T, WW, WW, WW, WW, SO, SO, SO, WW, WW, WW, OL_C, _, _],
    [_, _, OL_C, WW, ST_T, ST_T, ST_T, WW, WW, WW, WW, SO, SO, SO, WW, WW, WW, OL_C, _, _],
    [_, _, OL_C, WW, WD, WD, WD, WW, WW, WW, WW, WD, WD, WD, WW, WW, WW, OL_C, _, _],
    [_, _, OL_C, WW, WW, WW, WW, WW, WW, WW, WW, WW, WW, WW, WW, WW, WW, OL_C, _, _],
    [_, _, OL_C, WW, WW, WW, WW, WW, WW, DR, DR, WW, WW, WW, WW, WW, WW, OL_C, _, _],
    [_, _, OL_C, WW, WW, WW, WW, WW, WW, DR, DR, WW, WW, WW, WW, WW, WW, OL_C, _, _],
    [_, _, OL_C, WW, SO, ST_T, WW, WW, WW, WW, WW, WW, WW, WW, ST_T, SO, WW, OL_C, _, _],
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
]

# ── School / Education (12w × 11h) ────────────────────
SB = SCHOOL_BRICK
SC = SCHOOL_CREAM

BUILDING_EDUCATION: Sprite = [
    [_, _, _, _, _, _, _, _, _, WG, WG, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, SD, SD, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, OL_C, SB, SB, OL_C, _, _, _, _, _, _, _, _],
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, SB, SC, SB, SB, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
    [_, _, OL_C, SB, SC, SB, SC, SB, SB, SC, SB, SB, SC, SB, SC, SB, SB, OL_C, _, _],
    [_, _, OL_C, SB, SB, SB, SB, SB, SB, SB, SB, SB, SB, SB, SB, SB, SB, OL_C, _, _],
    [_, _, OL_C, SB, WG, WG, SB, SB, SB, SB, SB, SB, SB, SB, WG, WG, SB, OL_C, _, _],
    [_, _, OL_C, SB, WG, WG, SB, SB, SB, SB, SB, SB, SB, SB, WG, WG, SB, OL_C, _, _],
    [_, _, OL_C, SB, SD, SD, SB, SB, SB, SB, SB, SB, SB, SB, SD, SD, SB, OL_C, _, _],
    [_, _, OL_C, SB, SB, SB, SB, SB, SB, SB, SB, SB, SB, SB, SB, SB, SB, OL_C, _, _],
    [_, _, OL_C, SB, SB, SB, SB, DR, DR, DR, DR, SB, SB, SB, SB, SB, SB, OL_C, _, _],
    [_, _, OL_C, SB, SB, SB, SB, DR, DR, DR, DR, SB, SB, SB, SB, SB, SB, OL_C, _, _],
    [_, _, OL_C, SB, SC, SC, SB, SB, SB, SB, SB, SB, SB, SB, SC, SC, SB, OL_C, _, _],
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
]

# ── Automotive / Garage (12w × 10h) ───────────────────
GK = GARAGE_DARK
GM = GARAGE_METAL

BUILDING_AUTOMOTIVE: Sprite = [
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
    [_, _, OL_C, GM, GM, GM, GM, GM, GM, GM, GM, GM, GM, GM, GM, GM, GM, OL_C, _, _],
    [_, _, OL_C, GM, SD, SD, SD, SD, SD, SD, SD, SD, SD, SD, SD, SD, GM, OL_C, _, _],
    [_, _, OL_C, SS, SD, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SD, SS, OL_C, _, _],
    [_, _, OL_C, SS, WG, WG, SS, SS, SS, SS, SS, SS, SS, SS, WG, WG, SS, OL_C, _, _],
    [_, _, OL_C, SS, SD, SD, SS, SS, SS, SS, SS, SS, SS, SS, SD, SD, SS, OL_C, _, _],
    [_, _, OL_C, SS, SS, SS, GK, GK, GK, GK, GK, GK, GK, SS, SS, SS, SS, OL_C, _, _],
    [_, _, OL_C, SS, SS, SS, GK, GK, GK, GK, GK, GK, GK, SS, SS, SS, SS, OL_C, _, _],
    [_, _, OL_C, SS, SS, SS, GK, RD, RD, RD, RD, RD, GK, SS, SS, SS, SS, OL_C, _, _],
    [_, _, OL_C, SS, SS, SS, GK, SD, SD, SD, SD, SD, GK, SS, SS, SS, SS, OL_C, _, _],
    [_, _, OL_C, SS, SS, SS, GK, GK, GK, GK, GK, GK, GK, SS, SS, DR, SS, OL_C, _, _],
    [_, _, OL_C, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, DR, SS, OL_C, _, _],
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
]

# ── Retail / Storefront (11w × 10h) ───────────────────
RD_D = RETAIL_DISPLAY
RA = RETAIL_AWNING

BUILDING_RETAIL: Sprite = [
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
    [_, _, OL_C, RA, RA, RA, RA, RA, RA, RA, RA, RA, RA, RA, RA, RA, RA, OL_C, _, _],
    [_, _, OL_C, RA, RD_D, RA, RD_D, RA, RD_D, RA, RD_D, RA, RD_D, RA, RD_D, RA, RA, OL_C, _, _],
    [_, _, OL_C, WW, WD, WW, WW, WW, WW, WW, WW, WW, WW, WW, WW, WD, WW, OL_C, _, _],
    [_, _, OL_C, WW, RD_D, RD_D, RD_D, WW, WW, WW, WW, RD_D, RD_D, RD_D, WW, WW, WW, OL_C, _, _],
    [_, _, OL_C, WW, RD_D, WG, RD_D, WW, WW, WW, WW, RD_D, WG, RD_D, WW, WW, WW, OL_C, _, _],
    [_, _, OL_C, WW, RD_D, WG, RD_D, WW, WW, WW, WW, RD_D, WG, RD_D, WW, WW, WW, OL_C, _, _],
    [_, _, OL_C, WW, RD_D, RD_D, RD_D, WW, WW, WW, WW, RD_D, RD_D, RD_D, WW, WW, WW, OL_C, _, _],
    [_, _, OL_C, WW, WD, WD, WD, WW, WW, WW, WW, WD, WD, WD, WW, WW, WW, OL_C, _, _],
    [_, _, OL_C, WW, WW, WW, WW, WW, WW, DR, DR, WW, WW, WW, WW, WW, WW, OL_C, _, _],
    [_, _, OL_C, WW, WW, WW, WW, WW, WW, DR, DR, WW, WW, WW, WW, WW, WW, OL_C, _, _],
    [_, _, OL_C, WW, WW, WW, WW, WW, WW, WW, WW, WW, WW, WW, WW, WW, WW, OL_C, _, _],
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
]


# ═══════════════════════════════════════════════════════════
# HQ BUILDING SPRITES (6 stages of evolution)
# ═══════════════════════════════════════════════════════════

# ── HQ Cabin (8w × 8h) — Settlement ───────────────────
HQ_CABIN: Sprite = [
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, OL_C, OL_C, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, OL_C, OL_C, _, _, _],
    [_, _, _, _, _, _, _, _, OL_C, OL_C, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, OL_C, RTD, RT, OL_C, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, OL_C, RT, RTL, RT, RTD, OL_C, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, OL_C, RTD, RT, RTL, RT, RTD, RT, OL_C, _, _, _, _, _, _, _],
    [_, _, _, _, OL_C, RT, RTL, RT, RTL, RT, RTL, RT, RTD, OL_C, _, _, _, _, _, _],
    [_, _, _, OL_C, RTD, RT, RTL, RT, RTL, RT, RTL, RT, RTD, RT, OL_C, _, _, _, _, _],
    [_, _, OL_C, RT, RTL, RT, RTL, RT, RTL, RT, RTL, RT, RTL, RT, RTD, OL_C, _, _, _, _],
    [_, _, OL_C, WW, WD, WW, WW, WW, WW, WW, WW, WW, WW, WD, WW, OL_C, _, _, _, _],
    [_, _, OL_C, WW, WG, WG, WW, WW, WW, WW, WW, WW, WG, WG, WW, OL_C, OL_C, OL_C, _, _],
    [_, _, OL_C, WW, WG, WG, WW, WW, WW, WW, WW, WW, WG, WG, WW, OL_C, WW, OL_C, _, _],
    [_, _, OL_C, WW, WD, WD, WW, WW, DR, DR, WW, WW, WD, WD, WW, OL_C, WW, OL_C, _, _],
    [_, _, OL_C, WW, WW, WW, WW, WW, DR, DR, WW, WW, WW, WW, WW, WD, WW, OL_C, _, _],
    [_, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
]

# ── HQ Manor (22w × 20h) — Village (sill rows doubled) ─
HQ_MANOR: Sprite = [
    [_, _, _, _, _, _, _, _, _, OL_C, OL_C, OL_C, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, OL_C, RD, RR, RD, OL_C, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, OL_C, RR, RL, RR, RL, RR, OL_C, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, OL_C, RR, RL, RR, RL, RR, RL, RR, OL_C, _, _, _, _, _, _, _],
    [_, _, _, _, _, OL_C, RD, RL, RR, RL, RR, RL, RR, RD, RR, OL_C, _, _, _, _, _, _],
    [_, _, _, _, OL_C, RR, RL, RR, RL, RR, RL, RR, RL, RR, RL, RR, OL_C, _, _, _, _, _],
    [_, _, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _, _, _],
    [_, _, _, OL_C, SS, SD, SS, SS, SS, SS, SS, SS, SS, SS, SS, SD, SS, OL_C, _, _, _, _],
    [_, _, _, OL_C, SS, WG, WG, SS, SL, SS, SS, SL, SS, SS, WG, WG, SS, OL_C, _, _, _, _],
    [_, _, _, OL_C, SS, WG, WG, SS, SL, SS, SS, SL, SS, SS, WG, WG, SS, OL_C, _, _, _, _],
    [_, _, _, OL_C, SS, SD, SD, SS, SS, SS, SS, SS, SS, SS, SD, SD, SS, OL_C, _, _, _, _],
    [_, _, _, OL_C, SS, SD, SD, SS, SS, SS, SS, SS, SS, SS, SD, SD, SS, OL_C, _, _, _, _],
    [_, _, _, OL_C, SS, WG, WG, SS, SS, SS, SS, SS, SS, SS, WG, WG, SS, OL_C, _, _, _, _],
    [_, _, _, OL_C, SS, WG, WG, SS, SS, SS, SS, SS, SS, SS, WG, WG, SS, OL_C, _, _, _, _],
    [_, _, _, OL_C, SS, SD, SD, SS, SD, DR, DR, SD, SS, SS, SD, SD, SS, OL_C, _, _, _, _],
    [_, _, _, OL_C, SS, SS, SS, SS, SD, DR, DR, SD, SS, SS, SS, SS, SS, OL_C, _, _, _, _],
    [_, _, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
]

# ── HQ Castle (14w × 14h) — Town ──────────────────────
HQ_CASTLE: Sprite = [
    [_, OL_C, TB, OL_C, TB, OL_C, _, _, _, _, _, _, _, _, _, _, _, _, _, _, OL_C, TB, OL_C, TB, OL_C, _],
    [_, OL_C, SS, TB, SS, OL_C, _, _, _, _, _, _, _, _, _, _, _, _, _, _, OL_C, SS, TB, SS, OL_C, _],
    [_, OL_C, SS, SD, SS, OL_C, _, _, _, _, _, OL_C, OL_C, OL_C, _, _, _, _, _, _, OL_C, SS, SD, SS, OL_C, _],
    [_, OL_C, SS, WG, SS, OL_C, _, _, _, _, OL_C, RD, RR, RD, OL_C, _, _, _, _, _, OL_C, SS, WG, SS, OL_C, _],
    [_, OL_C, SS, SD, SS, OL_C, _, _, _, OL_C, RR, RL, RR, RL, RR, OL_C, _, _, _, _, OL_C, SS, SD, SS, OL_C, _],
    [_, OL_C, SS, WG, SS, OL_C, _, _, OL_C, RR, RL, RR, RL, RR, RL, RR, OL_C, _, _, _, OL_C, SS, WG, SS, OL_C, _],
    [_, OL_C, SS, SD, SS, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, SS, SD, SS, OL_C, _],
    [_, OL_C, SS, WG, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, WG, SS, OL_C, _],
    [_, OL_C, SS, SD, SS, SS, WG, WG, SS, SS, WG, SS, SS, WG, SS, SS, WG, WG, SS, SS, SS, SS, SD, SS, OL_C, _],
    [_, OL_C, SS, WG, SS, SS, WG, WG, SS, SS, SD, SS, SS, SD, SS, SS, WG, WG, SS, SS, SS, SS, WG, SS, OL_C, _],
    [_, OL_C, SS, SD, SS, SS, SD, SD, SS, SS, WG, SS, SS, WG, SS, SS, SD, SD, SS, SS, SS, SS, SD, SS, OL_C, _],
    [_, OL_C, SS, WG, SS, SS, WG, WG, SS, SS, SD, SS, SS, SD, SS, SS, WG, WG, SS, SS, SS, SS, WG, SS, OL_C, _],
    [_, OL_C, SS, SD, SS, SS, SD, SD, SS, SS, SS, SS, SS, SS, SS, SS, SD, SD, SS, SS, SS, SS, SD, SS, OL_C, _],
    [_, OL_C, SS, WG, SS, SS, SS, SS, SS, SS, SD, DR, DR, SD, SS, SS, SS, SS, SS, SS, SS, SS, WG, SS, OL_C, _],
    [_, OL_C, SS, SS, SS, SS, SS, SS, SS, SS, SD, DR, DR, SD, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, OL_C, _],
    [_, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
]

# ── HQ Grand Castle (28w × 22h) — City ────────────────
HQ_GRAND_CASTLE: Sprite = [
    [OL_C, TB, OL_C, TB, OL_C, _, _, _, _, _, _, _, _, OL_C, FL_R, FL_R, OL_C, _, _, _, _, _, _, OL_C, TB, OL_C, TB, OL_C],
    [OL_C, SS, TB, SS, OL_C, _, _, _, _, _, _, _, OL_C, TB, OL_C, TB, OL_C, _, _, _, _, _, _, OL_C, SS, TB, SS, OL_C],
    [OL_C, SS, SD, SS, OL_C, _, _, _, _, _, _, _, OL_C, SS, TB, SS, OL_C, _, _, _, _, _, _, OL_C, SS, SD, SS, OL_C],
    [OL_C, SS, WG, SS, OL_C, _, _, _, _, _, _, _, OL_C, SS, SD, SS, OL_C, _, _, _, _, _, _, OL_C, SS, WG, SS, OL_C],
    [OL_C, SS, SD, SS, OL_C, _, _, _, _, _, _, _, OL_C, SS, WG, SS, OL_C, _, _, _, _, _, _, OL_C, SS, SD, SS, OL_C],
    [OL_C, SS, WG, SS, OL_C, _, _, _, OL_C, OL_C, OL_C, OL_C, OL_C, SS, SD, SS, OL_C, OL_C, OL_C, OL_C, _, _, _, OL_C, SS, WG, SS, OL_C],
    [OL_C, SS, SD, SS, OL_C, _, _, OL_C, RD, RR, RL, RR, RL, RR, RL, RR, RL, RR, RD, OL_C, _, _, _, OL_C, SS, SD, SS, OL_C],
    [OL_C, SS, WG, SS, OL_C, _, OL_C, RR, RL, RR, RL, RR, RL, RR, RL, RR, RL, RR, RL, RR, OL_C, _, _, OL_C, SS, WG, SS, OL_C],
    [OL_C, SS, SD, SS, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, SS, SD, SS, OL_C],
    [OL_C, SS, WG, SS, SS, SS, SL, SS, SS, SS, SL, SS, SS, SS, SS, SL, SS, SS, SS, SL, SS, SS, SS, SS, SS, WG, SS, OL_C],
    [OL_C, SS, SD, SS, SS, WG, WG, SS, SS, WG, WG, SS, WG, WG, SS, WG, WG, SS, SS, WG, WG, SS, SS, SS, SS, SD, SS, OL_C],
    [OL_C, SS, WG, SS, SS, WG, WG, SS, SS, WG, WG, SS, WG, WG, SS, WG, WG, SS, SS, WG, WG, SS, SS, SS, SS, WG, SS, OL_C],
    [OL_C, SS, SD, SS, SS, SD, SD, SS, SS, SD, SD, SS, SD, SD, SS, SD, SD, SS, SS, SD, SD, SS, SS, SS, SS, SD, SS, OL_C],
    [OL_C, SS, WG, SS, SS, WG, WG, SS, SS, WG, WG, SS, WG, WG, SS, WG, WG, SS, SS, WG, WG, SS, SS, SS, SS, WG, SS, OL_C],
    [OL_C, SS, SD, SS, SS, WG, WG, SS, SS, WG, WG, SS, WG, WG, SS, WG, WG, SS, SS, WG, WG, SS, SS, SS, SS, SD, SS, OL_C],
    [OL_C, SS, WG, SS, SS, SD, SD, SS, SS, SD, SD, SS, SD, SD, SS, SD, SD, SS, SS, SD, SD, SS, SS, SS, SS, WG, SS, OL_C],
    [OL_C, SS, SD, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SD, SS, OL_C],
    [OL_C, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SD, SD, DR, DR, SD, SD, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, OL_C],
    [OL_C, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SD, SD, DR, DR, SD, SD, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, OL_C],
    [OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
]

# ── HQ Fortress (30w × 24h) — Capital ─────────────────
SA = STONE_ACCENT      # iron / portcullis accent
CB = COBBLE            # cobble stone
LP = LAMP              # torch flame
LN = LANTERN           # torch glow

HQ_FORTRESS: Sprite = [
    [OL_C, TB, OL_C, TB, OL_C, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, OL_C, TB, OL_C, TB, OL_C],
    [OL_C, SS, TB, SS, OL_C, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, OL_C, SS, TB, SS, OL_C],
    [OL_C, SS, SD, SS, OL_C, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, OL_C, SS, SD, SS, OL_C],
    [OL_C, SS, WG, SS, OL_C, _, _, _, _, _, _, _, _, OL_C, OL_C, OL_C, OL_C, _, _, _, _, _, _, _, _, OL_C, SS, WG, SS, OL_C],
    [OL_C, SS, SD, SS, OL_C, _, _, _, _, _, _, _, OL_C, RBD, RB, RB, RBD, OL_C, _, _, _, _, _, _, _, OL_C, SS, SD, SS, OL_C],
    [OL_C, SS, LP, SS, OL_C, _, _, _, _, _, _, OL_C, RBD, RB, RBL, RB, RBD, RB, OL_C, _, _, _, _, _, _, OL_C, SS, LP, SS, OL_C],
    [OL_C, SS, SD, SS, OL_C, _, _, _, _, _, OL_C, RB, RBL, RB, RBL, RB, RBL, RB, RBD, OL_C, _, _, _, _, _, OL_C, SS, SD, SS, OL_C],
    [OL_C, SS, WG, SS, OL_C, _, _, _, _, OL_C, RBD, RB, RBL, RB, RBL, RB, RBL, RB, RBD, RB, OL_C, _, _, _, _, OL_C, SS, WG, SS, OL_C],
    [OL_C, SS, SD, SS, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, SS, SD, SS, OL_C],
    [OL_C, SS, WG, SS, SD, SS, SS, CB, SS, SS, SL, SS, SS, SS, SS, SS, SS, SS, SS, SL, SS, SS, CB, SS, SS, SD, SS, WG, SS, OL_C],
    [OL_C, SS, SD, SS, SD, SS, WG, WG, SS, SS, SD, SS, WG, WG, SS, SS, WG, WG, SS, SD, SS, SS, WG, WG, SS, SD, SS, SD, SS, OL_C],
    [OL_C, SS, WG, SS, SD, SS, WG, WG, SS, SS, SD, SS, WG, WG, SS, SS, WG, WG, SS, SD, SS, SS, WG, WG, SS, SD, SS, WG, SS, OL_C],
    [OL_C, SS, SD, SS, SD, SS, SD, SD, SS, SS, SD, SS, SD, SD, SS, SS, SD, SD, SS, SD, SS, SS, SD, SD, SS, SD, SS, SD, SS, OL_C],
    [OL_C, SS, WG, SS, SD, SS, WG, WG, SS, SS, SD, SS, WG, WG, SS, SS, WG, WG, SS, SD, SS, SS, WG, WG, SS, SD, SS, WG, SS, OL_C],
    [OL_C, SS, SD, SS, SD, SS, WG, WG, SS, SS, SD, SS, WG, WG, SS, SS, WG, WG, SS, SD, SS, SS, WG, WG, SS, SD, SS, SD, SS, OL_C],
    [OL_C, SS, WG, SS, SD, SS, SD, SD, SS, SS, SD, SS, SD, SD, SS, SS, SD, SD, SS, SD, SS, SS, SD, SD, SS, SD, SS, WG, SS, OL_C],
    [OL_C, SS, SD, SS, SD, SS, SS, SS, SS, SS, SD, SS, SS, SS, SS, SS, SS, SS, SS, SD, SS, SS, SS, SS, SS, SD, SS, SD, SS, OL_C],
    [OL_C, SS, LP, SS, SD, SS, SS, SS, SS, SS, SS, SS, SA, SA, SA, SA, SA, SA, SS, SS, SS, SS, SS, SS, SS, SD, SS, LP, SS, OL_C],
    [OL_C, SS, SS, SS, SD, SS, SS, SS, SS, SS, SS, SS, SA, SD, SD, SD, SD, SA, SS, SS, SS, SS, SS, SS, SS, SD, SS, SS, SS, OL_C],
    [OL_C, SS, SS, SS, SD, SS, SS, SS, SS, SS, SS, SS, SA, SD, SD, SD, SD, SA, SS, SS, SS, SS, SS, SS, SS, SD, SS, SS, SS, OL_C],
    [OL_C, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SA, SD, SD, SD, SD, SA, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, SS, OL_C],
    [OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
]

# ── HQ Metropolis (32w × 26h) — Kingdom/Metropolis ────
# The ultimate city HQ with modern spire, glass facade, gold trim
MW = (139, 155, 180)   # modern wall (Endesga med gray)
MG = (90, 105, 136)    # modern glass (Endesga dark gray)
ML = (192, 203, 220)   # modern light (Endesga light gray)
AU = UI_GOLD           # gold accent
WN = WINDOW_BRIGHT     # bright window glass
OM = OFFICE_MARBLE     # marble facade

HQ_METROPOLIS: Sprite = [
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, OL_C, AU, AU, OL_C, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, OL_C, ML, ML, OL_C, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, OL_C, MG, MW, MG, OL_C, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, OL_C, MW, MG, MW, OL_C, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, OL_C, MG, MW, MG, OL_C, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, OL_C, MW, WN, MG, WN, MW, OL_C, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, OL_C, MW, MG, WN, MW, WN, MG, MW, OL_C, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, MW, WN, MG, MW, MG, WN, MW, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _, _, _, _, _],
    [_, _, _, _, _, OL_C, RD, RR, RL, RR, RL, OL_C, MW, MG, WN, MW, WN, MG, MW, OL_C, RL, RR, RL, RR, RD, OL_C, _, _, _, _, _, _],
    [_, _, _, _, OL_C, RR, RL, RR, RL, RR, RL, OL_C, AU, MW, MG, MW, MG, MW, AU, OL_C, RR, RL, RR, RL, RR, RL, OL_C, _, _, _, _, _],
    [_, _, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _, _, _],
    [_, _, _, OL_C, OM, SL, SS, OM, SL, SS, OM, SS, SL, OM, SS, SS, SS, OM, SL, SS, OM, SS, SL, OM, SS, SL, OM, OL_C, _, _, _, _],
    [_, _, _, OL_C, OM, WN, WN, SS, WG, WG, SS, SS, WN, WN, MG, MW, MG, WN, WN, SS, SS, WG, WG, SS, WN, WN, OM, OL_C, _, _, _, _],
    [_, _, _, OL_C, OM, WN, WN, SS, WG, WG, SS, SS, WN, WN, MG, MW, MG, WN, WN, SS, SS, WG, WG, SS, WN, WN, OM, OL_C, _, _, _, _],
    [_, _, _, OL_C, OM, SD, SD, SS, SD, SD, SS, SS, SD, SD, SD, AU, SD, SD, SD, SS, SS, SD, SD, SS, SD, SD, OM, OL_C, _, _, _, _],
    [_, _, _, OL_C, OM, WG, WG, SS, WN, WN, SS, SS, WG, WG, MG, MW, MG, WG, WG, SS, SS, WN, WN, SS, WG, WG, OM, OL_C, _, _, _, _],
    [_, _, _, OL_C, OM, WG, WG, SS, WN, WN, SS, SS, WG, WG, MG, MW, MG, WG, WG, SS, SS, WN, WN, SS, WG, WG, OM, OL_C, _, _, _, _],
    [_, _, _, OL_C, OM, SD, SD, SS, SD, SD, SS, SS, SD, SD, SD, AU, SD, SD, SD, SS, SS, SD, SD, SS, SD, SD, OM, OL_C, _, _, _, _],
    [_, _, _, OL_C, OM, WG, WG, SS, WN, WN, SS, SS, WG, WG, MG, MW, MG, WG, WG, SS, SS, WN, WN, SS, WG, WG, OM, OL_C, _, _, _, _],
    [_, _, _, OL_C, OM, WG, WG, SS, WN, WN, SS, SS, WG, WG, MG, MW, MG, WG, WG, SS, SS, WN, WN, SS, WG, WG, OM, OL_C, _, _, _, _],
    [_, _, _, OL_C, OM, SD, SD, SS, SS, SS, SS, SS, SS, SS, SS, AU, SS, SS, SS, SS, SS, SS, SS, SS, SD, SD, OM, OL_C, _, _, _, _],
    [_, _, _, OL_C, OM, SS, SS, SS, SS, SS, SS, SS, SD, AU, DR, DR, DR, DR, AU, SD, SS, SS, SS, SS, SS, SS, OM, OL_C, _, _, _, _],
    [_, _, _, OL_C, OM, SS, SS, SS, SS, SS, SS, SS, SD, AU, DR, DR, DR, DR, AU, SD, SS, SS, SS, SS, SS, SS, OM, OL_C, _, _, _, _],
    [_, _, _, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, OL_C, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
    [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
]


# ═══════════════════════════════════════════════════════════
# VILLAGER SPRITES (7 wide x 10 tall) — chunky RPG-style pixel art
# Inspired by Pixel Agents — clear readable characters with distinct
# hair, face, shirt, pants, boots and dark outline.
# ═══════════════════════════════════════════════════════════

# Eye color for all villagers (tiny dark dots on face)
_EYE = (24, 20, 37)  # same as outline — reads as pupils
# Mouth/skin shadow for face detail
_MOUTH = (194, 133, 105)  # skin dark — reads as mouth


def _hair_hi(hair: Color) -> Color:
    """Compute a highlight shade for hair (lighter by ~30%)."""
    return (min(255, hair[0] + 40), min(255, hair[1] + 40), min(255, hair[2] + 40))


def _hair_sh(hair: Color) -> Color:
    """Compute a shadow shade for hair (darker by ~25%)."""
    return (max(0, hair[0] - 30), max(0, hair[1] - 30), max(0, hair[2] - 30))


def _shirt_hi(shirt: Color) -> Color:
    """Shirt highlight — lighter by ~35 per channel."""
    return (min(255, shirt[0] + 35), min(255, shirt[1] + 35), min(255, shirt[2] + 35))


def _shirt_sh(shirt: Color) -> Color:
    """Shirt shadow — darker by ~30 per channel."""
    return (max(0, shirt[0] - 30), max(0, shirt[1] - 30), max(0, shirt[2] - 30))


def _pants_hi(pants: Color) -> Color:
    """Pants highlight."""
    return (min(255, pants[0] + 25), min(255, pants[1] + 25), min(255, pants[2] + 25))


def _boot_hi(boot: Color) -> Color:
    """Boot highlight."""
    return (min(255, boot[0] + 30), min(255, boot[1] + 30), min(255, boot[2] + 30))


def make_villager(
    hair: Color, skin: Color, shirt: Color, pants: Color,
    accent: Color | None = None,
    hat: Color | None = None,
) -> dict[str, list[Sprite]]:
    """Create a 7x12 defined RPG villager sprite with full dark outline.

    Design reference: Pixel Agents by @Amank1412 — chunky, readable
    characters with clear head/body/legs and bold colors.
    7 wide x 12 tall for more detail — proportioned next to 14-20px buildings.

    Every pixel is intentional. Features:
      - Row 0-2: hair with 2 shades (highlight top, shadow sides)
      - Row 3: face — skin, 2 visible eye dots, mouth dot
      - Row 4-6: shirt with highlight, base, shadow (3 colors)
      - Row 7-8: pants with 2 shades
      - Row 9-10: boots with highlight
      - Row 11: ground shadow line
      - Full #181425 outline on ALL exterior edges
    """
    OL = OL_C   # dark outline
    HD = hair
    HH = _hair_hi(hair)   # hair highlight
    HS = _hair_sh(hair)    # hair shadow
    SK = skin
    EY = _EYE   # eyes
    MT = _MOUTH  # mouth / skin shadow
    SH = shirt
    SHH = _shirt_hi(shirt)  # shirt highlight
    SHS = _shirt_sh(shirt)  # shirt shadow
    RC = accent if accent is not None else shirt
    PT = pants
    PTH = _pants_hi(pants)  # pants highlight
    BT = BOOTS
    BTH = _boot_hi(BT)      # boot highlight
    HT = hat

    # ── IDLE: standing still, arms at sides ──
    idle: Sprite = [
        [_, _, OL, HH, OL, _, _],        # hair crown highlight
        [_, OL, HH, HD, HH, OL, _],      # hair — highlight edges, base center
        [_, OL, HS, HD, HS, OL, _],       # hair lower — shadow sides
        [_, OL, SK, EY, SK, OL, _],       # face: skin-eye-eye-skin — 2 eyes merge to center
        [_, OL, SHH, RC, SHH, OL, _],    # shirt collar highlight + accent
        [_, OL, SH, SH, SH, OL, _],      # shirt torso base
        [_, OL, SHS, SH, SHS, OL, _],    # shirt lower shadow / belt
        [_, OL, PTH, PT, PTH, OL, _],    # pants upper — highlight edges
        [_, OL, PT, OL, PT, OL, _],       # pants lower — center gap for legs
        [_, OL, BTH, _, BTH, OL, _],     # boots with highlight
        [_, OL, BT, _, BT, OL, _],       # boot soles
        [_, _, OL, _, OL, _, _],          # ground contact shadow
    ]

    # ── WALK FRAME 1: left leg forward, right arm forward ──
    walk_1: Sprite = [
        [_, _, OL, HH, OL, _, _],        # hair highlight
        [_, OL, HH, HD, HH, OL, _],      # hair
        [_, OL, HS, HD, HS, OL, _],       # hair shadow
        [_, OL, SK, EY, SK, OL, _],       # face
        [_, OL, SHH, RC, SHH, OL, _],    # shirt collar
        [_, SK, SH, SH, SH, OL, _],      # right arm back (skin pixel left)
        [_, OL, SHS, SH, SHS, SK, _],    # left arm forward + shirt shadow
        [_, OL, PTH, PT, PTH, OL, _],    # pants
        [_, PT, OL, _, OL, PT, _],        # stride — legs apart
        [OL, BTH, _, _, _, BTH, OL],     # feet wide stride + highlight
        [OL, BT, _, _, _, BT, OL],       # boot soles
        [OL, _, _, _, _, _, OL],          # ground contact
    ]

    # ── WALK FRAME 2: right leg forward, left arm forward ──
    walk_2: Sprite = [
        [_, _, OL, HH, OL, _, _],        # hair highlight
        [_, OL, HH, HD, HH, OL, _],      # hair
        [_, OL, HS, HD, HS, OL, _],       # hair shadow
        [_, OL, SK, EY, SK, OL, _],       # face
        [_, OL, SHH, RC, SHH, OL, _],    # shirt collar
        [_, OL, SH, SH, SH, SK, _],      # left arm back
        [_, SK, SHS, SH, SHS, OL, _],    # right arm forward + shirt shadow
        [_, OL, PTH, PT, PTH, OL, _],    # pants
        [_, PT, OL, _, OL, PT, _],        # stride (mirrored)
        [OL, BTH, _, _, _, BTH, OL],     # feet stride + highlight
        [OL, BT, _, _, _, BT, OL],       # boot soles
        [_, OL, _, _, _, OL, _],          # ground contact
    ]

    # ── WORK FRAME 1: right arm raised (hammering/typing) ──
    work_1: Sprite = [
        [_, _, OL, HH, OL, _, _],        # hair highlight
        [_, OL, HH, HD, HH, OL, _],      # hair
        [_, OL, HS, HD, HS, OL, _],       # hair shadow
        [_, OL, SK, EY, SK, OL, _],       # face
        [_, OL, SHH, RC, SH, SK, _],     # shirt + right arm up
        [_, OL, SH, SH, SH, OL, SK],    # torso + raised hand
        [_, OL, SHS, SH, SHS, OL, _],    # shirt lower shadow
        [_, OL, PTH, PT, PTH, OL, _],    # pants
        [_, OL, PT, OL, PT, OL, _],       # pants lower
        [_, OL, BTH, _, BTH, OL, _],     # boots highlight
        [_, OL, BT, _, BT, OL, _],       # boot soles
        [_, _, OL, _, OL, _, _],          # ground
    ]

    # ── WORK FRAME 2: both arms out (carrying/gesturing) ──
    work_2: Sprite = [
        [_, _, OL, HH, OL, _, _],        # hair highlight
        [_, OL, HH, HD, HH, OL, _],      # hair
        [_, OL, HS, HD, HS, OL, _],       # hair shadow
        [_, OL, SK, EY, SK, OL, _],       # face
        [SK, OL, SHH, RC, SHH, OL, SK], # both arms out + highlight
        [_, OL, SH, SH, SH, OL, _],      # torso
        [_, OL, SHS, SH, SHS, OL, _],    # shirt lower shadow
        [_, OL, PTH, PT, PTH, OL, _],    # pants
        [_, OL, PT, OL, PT, OL, _],       # pants lower
        [_, OL, BTH, _, BTH, OL, _],     # boots highlight
        [_, OL, BT, _, BT, OL, _],       # boot soles
        [_, _, OL, _, OL, _, _],          # ground
    ]

    # Optional hat overrides top three rows (hair rows)
    if HT is not None:
        for frame in [idle, walk_1, walk_2, work_1, work_2]:
            frame[0] = [_, OL, HT, HT, HT, OL, _]   # hat top
            frame[1] = [OL, HT, HT, HT, HT, HT, OL] # hat brim wide
            frame[2] = [_, OL, HD, HD, HD, OL, _]     # hair peek below hat

    return {
        "idle": [idle],
        "walk": [walk_1, walk_2],
        "work": [work_1, work_2],
    }


VILLAGER_VARIANTS = [
    # ── Role agents (indices 0-4) ──
    make_villager(HAIR_BROWN, SKIN, SHIRT_BLUE, PANTS, accent=COO_CAPE),           # 0: COO
    make_villager(HAIR_DARK, SKIN, SHIRT_GREEN, PANTS, accent=RECEPTIONIST_APRON),  # 1: Receptionist
    make_villager(HAIR_BLONDE, SKIN, SHIRT_RED, PANTS, accent=CONTENT_SHIRT),      # 2: Content Writer
    make_villager(HAIR_BROWN, SKIN, SHIRT_RED, PANTS, accent=REVIEW_VEST),         # 3: Review Manager
    make_villager(HAIR_DARK, SKIN, SHIRT_PURPLE, PANTS, accent=ROUTE_SASH),        # 4: Route Planner
    # ── Townspeople / customers (indices 5-11) ──
    make_villager(HAIR_BLONDE, SKIN, SHIRT_BLUE, PANTS_BROWN),                     # 5: Villager A
    make_villager(HAIR_BROWN, SKIN, SHIRT_GREEN, PANTS),                           # 6: Villager B
    make_villager(HAIR_DARK, SKIN_DARK, SHIRT_RED, PANTS_BROWN),                   # 7: Villager C
    make_villager(HAIR_BLONDE, SKIN_DARK, SHIRT_PURPLE, PANTS),                    # 8: Villager D
    make_villager(HAIR_BROWN, SKIN, WOOD_PLANK, PANTS_BROWN, hat=WORKER_HELMET),   # 9: Worker w/ hat
    make_villager(HAIR_DARK, SKIN, SHIRT_BLUE, PANTS, accent=ROOF_THATCH),         # 10: Shopkeeper
    make_villager(HAIR_BLONDE, SKIN, SHIRT_GREEN, PANTS_BROWN, accent=DIRT),       # 11: Farmer
]

# Backward compatibility -- agents.py imports this
AGENT_V2_VARIANTS = VILLAGER_VARIANTS


# ═══════════════════════════════════════════════════════════
# AGENT SPRITES v2 (4 wide × 6 tall)
# ═══════════════════════════════════════════════════════════

def make_agent_v2(hair: Color, shirt: Color, role_accent: Color | None = None) -> dict[str, list[Sprite]]:
    """Create a larger agent sprite set with optional role-identifying accent."""
    HD = hair
    SH = shirt
    SK = SKIN
    BT = BOOTS
    PT = PANTS
    RC = role_accent if role_accent is not None else shirt

    idle: Sprite = [
        [_, HD, HD, _],
        [HD, SK, SK, HD],
        [_, SH, SH, _],
        [_, RC, RC, _],
        [_, PT, PT, _],
        [BT, _, _, BT],
    ]

    walk_1: Sprite = [
        [_, HD, HD, _],
        [HD, SK, SK, HD],
        [_, SH, SH, _],
        [_, RC, RC, _],
        [_, PT, PT, _],
        [_, BT, BT, _],
    ]

    walk_2: Sprite = [
        [_, HD, HD, _],
        [HD, SK, SK, HD],
        [_, SH, SH, _],
        [_, RC, RC, _],
        [_, PT, PT, _],
        [BT, _, _, BT],
    ]

    work_1: Sprite = [
        [_, HD, HD, _],
        [HD, SK, SK, HD],
        [SH, SH, SH, _],
        [_, RC, RC, _],
        [_, PT, PT, _],
        [BT, _, _, BT],
    ]

    work_2: Sprite = [
        [_, HD, HD, _],
        [HD, SK, SK, HD],
        [_, SH, SH, SH],
        [_, RC, RC, _],
        [_, PT, PT, _],
        [BT, _, _, BT],
    ]

    return {
        "idle": [idle],
        "walk": [walk_1, walk_2],
        "work": [work_1, work_2],
    }


# Pre-built v2 agent variants (legacy — kept for reference, superseded by VILLAGER_VARIANTS)
_AGENT_V2_VARIANTS_LEGACY = [
    make_agent_v2(HAIR_BROWN, SHIRT_BLUE, COO_CAPE),           # COO
    make_agent_v2(HAIR_DARK, SHIRT_GREEN, RECEPTIONIST_APRON),  # Receptionist
    make_agent_v2(HAIR_BLONDE, SHIRT_RED, CONTENT_SHIRT),       # Content Writer
    make_agent_v2(HAIR_BROWN, SHIRT_RED, REVIEW_VEST),          # Review Manager
    make_agent_v2(HAIR_DARK, SHIRT_PURPLE, ROUTE_SASH),         # Route Planner
    make_agent_v2(HAIR_BLONDE, SHIRT_BLUE),                     # Villager
    make_agent_v2(HAIR_BROWN, SHIRT_GREEN),                     # Villager
    make_agent_v2(HAIR_DARK, SHIRT_RED),                        # Villager
]

ROLE_TO_VARIANT = {
    "coo": 0,
    "receptionist": 1,
    "content_writer": 2,
    "review_manager": 3,
    "route_planner": 4,
    "villager": 5,
    "worker": 6,
}


# ═══════════════════════════════════════════════════════════
# AMBIENT SPRITES
# ═══════════════════════════════════════════════════════════

CL_W = (255, 255, 255)  # cloud white (Endesga white)
CL_G = (192, 203, 220)  # cloud gray (Endesga light gray)

CLOUD: Sprite = [
    [_, _, CL_G, CL_W, CL_W, CL_G, _, _],
    [_, _, CL_G, CL_W, CL_W, CL_G, _, _],
    [_, CL_G, CL_W, CL_W, CL_W, CL_W, CL_G, _],
    [CL_G, CL_W, CL_W, CL_G, CL_W, CL_W, CL_W, CL_G],
]

BR_B = (62, 39, 49)  # bird dark (Endesga blackish)
BR_L = (115, 62, 57) # bird light (Endesga dark brown)
BIRD_FRAMES: list[Sprite] = [
    [[_, BR_B, _, BR_B], [_, BR_B, _, BR_B], [BR_B, BR_L, BR_B, _], [_, BR_B, _, _]],
    [[BR_B, _, BR_B, _], [BR_B, _, BR_B, _], [_, BR_L, _, BR_B], [_, BR_B, _, _]],
]

TF_Y = LANTERN
TF_R = (232, 128, 32)
TF_O = (248, 188, 52)

TORCH_FRAMES: list[Sprite] = [
    [[_, TF_Y], [_, TF_R], [WD, WD], [WD, WD]],
    [[TF_O, _], [TF_Y, _], [WD, WD], [WD, WD]],
    [[_, TF_R], [TF_O, _], [WD, WD], [WD, WD]],
]

FL_W = ROOF_RED  # flag color
FL_D = ROOF_RED_DARK

FLAG_FRAMES: list[Sprite] = [
    [[FL_W, FL_W, FL_D], [FL_W, FL_W, FL_D], [FL_D, FL_W, _], [SD, _, _]],
    [[FL_D, FL_W, FL_W], [FL_D, FL_W, FL_W], [_, FL_D, FL_W], [SD, _, _]],
]

# Scaffolding (6w × 8h)
SW_S = SCAFFOLD_WOOD
SR = SCAFFOLD_ROPE

SCAFFOLDING: Sprite = [
    [SW_S, _, _, _, _, SW_S],
    [SW_S, SR, _, _, SR, SW_S],
    [SW_S, SW_S, SW_S, SW_S, SW_S, SW_S],
    [SW_S, _, _, _, _, SW_S],
    [SW_S, _, SR, SR, _, SW_S],
    [SW_S, SW_S, SW_S, SW_S, SW_S, SW_S],
    [SW_S, _, _, _, _, SW_S],
    [SW_S, _, _, _, _, SW_S],
]

# Foundation (generic, used during construction)
FN = FOUNDATION
FOUNDATION_SPRITE: Sprite = [
    [FN, FN, FN, FN, FN, FN, FN, FN],
    [FN, SD, FN, FN, FN, FN, SD, FN],
    [FN, FN, FN, FN, FN, FN, FN, FN],
    [FN, FN, FN, FN, FN, FN, FN, FN],
]


# ═══════════════════════════════════════════════════════════
# CUSTOMER BUILDING REGISTRY (v2)
# ═══════════════════════════════════════════════════════════

CUSTOMER_BUILDING_REGISTRY: dict[str, dict] = {
    "beauty_shop": {"sprite": BUILDING_BEAUTY, "name": "Beauty Shop", "desc": "Salon & Beauty"},
    "restaurant": {"sprite": BUILDING_RESTAURANT, "name": "Restaurant", "desc": "Food & Dining"},
    "gym": {"sprite": BUILDING_FITNESS, "name": "Gym", "desc": "Fitness Center"},
    "workshop": {"sprite": BUILDING_HOME_SERVICES, "name": "Workshop", "desc": "Home Services"},
    "office": {"sprite": BUILDING_PROFESSIONAL, "name": "Office", "desc": "Professional Services"},
    "studio": {"sprite": BUILDING_CREATIVE, "name": "Studio", "desc": "Creative Services"},
    "school": {"sprite": BUILDING_EDUCATION, "name": "School", "desc": "Education"},
    "garage": {"sprite": BUILDING_AUTOMOTIVE, "name": "Garage", "desc": "Automotive"},
    "storefront": {"sprite": BUILDING_RETAIL, "name": "Storefront", "desc": "Retail"},
}

BUSINESS_TYPE_TO_BUILDING: dict[str, str] = {
    "beauty": "beauty_shop",
    "restaurant": "restaurant",
    "fitness": "gym",
    "home_services": "workshop",
    "professional": "office",
    "creative": "studio",
    "education": "school",
    "automotive": "garage",
    "retail": "storefront",
}

HQ_SPRITES: dict[str, Sprite] = {
    "Settlement": HQ_CABIN,
    "Village": HQ_MANOR,
    "Town": HQ_CASTLE,
    "City": HQ_GRAND_CASTLE,
    "Capital": HQ_FORTRESS,
    "Kingdom": HQ_FORTRESS,   # same as Capital for now
    "Metropolis": HQ_METROPOLIS,
}


# ═══════════════════════════════════════════════════════════
# AGENT SPRITES (3 wide x 4 tall)
# ═══════════════════════════════════════════════════════════

def make_agent(hair: Color, shirt: Color) -> dict[str, list[Sprite]]:
    """Create a full agent sprite set with given colors."""
    HD = hair
    SH = shirt
    SK = SKIN
    BT = BOOTS
    PT = PANTS

    idle: Sprite = [
        [_, HD, _],
        [SK, SH, SK],
        [_, SH, _],
        [BT, _, BT],
    ]

    walk_1: Sprite = [
        [_, HD, _],
        [SK, SH, SK],
        [_, SH, _],
        [_, BT, BT],
    ]

    walk_2: Sprite = [
        [_, HD, _],
        [SK, SH, SK],
        [_, SH, _],
        [BT, BT, _],
    ]

    work_1: Sprite = [
        [_, HD, _],
        [SH, SH, SK],
        [_, SH, _],
        [BT, _, BT],
    ]

    work_2: Sprite = [
        [_, HD, _],
        [SK, SH, SH],
        [_, SH, _],
        [BT, _, BT],
    ]

    return {
        "idle": [idle],
        "walk": [walk_1, walk_2],
        "work": [work_1, work_2],
    }


# Pre-built agent variants
AGENT_VARIANTS = [
    make_agent(HAIR_BROWN, SHIRT_BLUE),
    make_agent(HAIR_DARK, SHIRT_RED),
    make_agent(HAIR_BLONDE, SHIRT_GREEN),
    make_agent(HAIR_BROWN, SHIRT_PURPLE),
    make_agent(HAIR_DARK, SHIRT_BLUE),
    make_agent(HAIR_BLONDE, SHIRT_RED),
]


# ═══════════════════════════════════════════════════════════
# PARTICLES (tiny animated effects)
# ═══════════════════════════════════════════════════════════

SMOKE_PARTICLES = [
    [[SMOKE_DARK]],
    [[SMOKE]],
    [[SMOKE_LIGHT]],
    [[_]],  # fade out
]

SPARKLE_PARTICLES = [
    [[SPARKLE]],
    [[WINDOW_BRIGHT]],
    [[WINDOW_GLOW]],
    [[_]],
]

HEART_PARTICLES = [
    [[HEART]],
    [[HEART]],
    [[_]],
]


# ═══════════════════════════════════════════════════════════
# BUILDING REGISTRY — maps folder names to buildings
# ═══════════════════════════════════════════════════════════

BUILDING_REGISTRY: dict[str, dict] = {
    "castle": {"sprite": CASTLE, "name": "Castle", "desc": "Main project root"},
    "hut": {"sprite": HUT, "name": "Cottage", "desc": "Small module"},
    "farm": {"sprite": FARM, "name": "Farmhouse", "desc": "Data / storage"},
    "library": {"sprite": LIBRARY, "name": "Library", "desc": "Documentation"},
    "forge": {"sprite": FORGE, "name": "Forge", "desc": "Build / tools"},
    "market": {"sprite": MARKET, "name": "Market", "desc": "Frontend / UI"},
    "tavern": {"sprite": TAVERN, "name": "Tavern", "desc": "Tests"},
    "garden": {"sprite": GARDEN, "name": "Garden", "desc": "Config / data"},
    "tower": {"sprite": TOWER, "name": "Watchtower", "desc": "CI / Deploy"},
    "well": {"sprite": WELL, "name": "Well", "desc": "Utils"},
    "windmill": {"sprite": WINDMILL_FRAMES[0], "name": "Windmill", "desc": "Processing"},
}

# Folder name -> building type mapping
FOLDER_TO_BUILDING: dict[str, str] = {
    "src": "castle",
    "app": "castle",
    "lib": "library",
    "docs": "library",
    "documentation": "library",
    "tests": "tavern",
    "test": "tavern",
    "spec": "tavern",
    "__tests__": "tavern",
    "data": "garden",
    "db": "garden",
    "database": "garden",
    "migrations": "garden",
    "frontend": "market",
    "client": "market",
    "ui": "market",
    "components": "market",
    "pages": "market",
    "views": "market",
    "public": "market",
    "static": "market",
    "build": "forge",
    "dist": "forge",
    "tools": "forge",
    "scripts": "forge",
    "config": "garden",
    "utils": "well",
    "helpers": "well",
    "common": "well",
    "shared": "well",
    "api": "tower",
    "server": "tower",
    "backend": "tower",
    "services": "tower",
    "deploy": "tower",
    "ci": "tower",
    ".github": "tower",
    "assets": "windmill",
    "media": "windmill",
    "models": "farm",
    "schemas": "farm",
    "types": "farm",
}
