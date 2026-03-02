"""Red Pine Kingdom — the central town that grows with the business.

Revenue drives visual progression. Each customer is a building.
AI agents are visible NPCs. The kingdom grows as Red Pine grows.
"""
from __future__ import annotations

import hashlib
import random
import math
from dataclasses import dataclass, field

from rendering.canvas import PixelCanvas
from assets import palettes
from assets.sprites import (
    Sprite,
    TILE_GRASS_VARIANTS, TILE_WATER_FRAMES, TILE_WATER_SHIMMER_FRAMES,
    TILE_DIRT, TILE_PATH_H, TILE_COBBLE,
    TREE_PINE, TREE_OAK, BUSH, SHRUB, TALL_GRASS,
    FLOWER_SPRITES,
    HUT, FARM, LIBRARY, FORGE, MARKET, TAVERN, TOWER, WELL,
    CASTLE, WINDMILL_FRAMES,
    BRIDGE, FENCE_H, FENCE_POST, GARDEN,
    BUILDING_REGISTRY, FOLDER_TO_BUILDING,
    SMOKE_PARTICLES, SPARKLE_PARTICLES, HEART_PARTICLES,
)
from towns.agents import AgentManager, Agent, Particle

# Safe imports for v2 sprites (may not exist until Task 2 completes)
try:
    from assets.sprites import (
        CUSTOMER_BUILDING_REGISTRY, BUSINESS_TYPE_TO_BUILDING, HQ_SPRITES,
        BUILDING_BEAUTY, BUILDING_RESTAURANT, BUILDING_FITNESS,
        BUILDING_HOME_SERVICES, BUILDING_PROFESSIONAL, BUILDING_CREATIVE,
        BUILDING_EDUCATION, BUILDING_AUTOMOTIVE, BUILDING_RETAIL,
        HQ_CABIN, HQ_MANOR, HQ_CASTLE as HQ_CASTLE_SPRITE,
        HQ_GRAND_CASTLE, HQ_FORTRESS, HQ_METROPOLIS,
        CLOUD, BIRD_FRAMES, TORCH_FRAMES, FLAG_FRAMES,
        SCAFFOLDING, FOUNDATION_SPRITE,
    )
    HAS_V2_SPRITES = True
except ImportError:
    HAS_V2_SPRITES = False
    CUSTOMER_BUILDING_REGISTRY = {}
    BUSINESS_TYPE_TO_BUILDING = {}
    HQ_SPRITES = {}

# Safe imports for landscape sprites
try:
    from assets.sprites import TREE_WILLOW, TREE_MAPLE, BUSH_BERRY, ROCK_SMALL, ROCK_LARGE, STUMP, FALLEN_LOG
    HAS_LANDSCAPE_SPRITES = True
except ImportError:
    HAS_LANDSCAPE_SPRITES = False

# Safe imports for decoration sprites (barrels, crates, market stalls, etc.)
try:
    from assets.sprites import (
        BARREL, CRATE, CRATE_STACK, MARKET_STALL, LAMP_POST,
        SIGN_POST, WELL_SPRITE, FENCE_STONE, FENCE_WOOD, FLOWER_BED,
    )
    HAS_DECORATION_SPRITES = True
except ImportError:
    HAS_DECORATION_SPRITES = False

# Safe import for v2 metrics
try:
    from towns.metrics import RedPineMetrics
except ImportError:
    RedPineMetrics = None


# District buildings — represent Red Pine subsystems
DISTRICTS = {
    "forge": {"name": "The Forge", "desc": "Dashboard & Codebase", "building": "forge"},
    "market": {"name": "Market Square", "desc": "Portal & Marketplace", "building": "market"},
    "library": {"name": "Grand Library", "desc": "Docs & Onboarding", "building": "library"},
    "watchtower": {"name": "Watchtower", "desc": "COO & AI Agents", "building": "tower"},
    "comm_tower": {"name": "Signal Tower", "desc": "Communications", "building": "tavern"},
}


@dataclass
class Building:
    """A placed building in the kingdom."""
    x: int
    y: int
    building_type: str
    folder: str = ""
    name: str = ""
    loc: int = 0
    file_count: int = 0
    sprite: Sprite = field(default_factory=list)
    is_hq: bool = False
    is_district: bool = False
    is_customer: bool = False
    customer_type: str = ""  # "beauty", "restaurant", etc.

    @property
    def width(self) -> int:
        return len(self.sprite[0]) if self.sprite else 0

    @property
    def height(self) -> int:
        return len(self.sprite) if self.sprite else 0

    @property
    def center_x(self) -> float:
        return self.x + self.width / 2

    @property
    def center_y(self) -> float:
        return self.y + self.height / 2


@dataclass
class ConstructionSite:
    """A building under construction."""
    x: int
    y: int
    target_sprite: Sprite
    progress: float = 0.0  # 0.0 = foundation, 1.0 = complete
    name: str = ""

    def get_current_sprite(self) -> Sprite:
        if not HAS_V2_SPRITES:
            return self.target_sprite
        if self.progress < 0.3:
            return FOUNDATION_SPRITE
        elif self.progress < 0.7:
            return SCAFFOLDING
        else:
            return self.target_sprite

    def tick(self):
        """Advance construction progress."""
        self.progress = min(1.0, self.progress + 0.005)

    @property
    def complete(self) -> bool:
        return self.progress >= 1.0


@dataclass
class AmbientObject:
    """A floating ambient decoration (cloud, bird, torch, flag)."""
    x: float
    y: float
    obj_type: str  # "cloud", "bird", "torch", "flag"
    frame: int = 0
    speed: float = 0.2
    anim_tick: int = 0

    def tick(self):
        self.anim_tick += 1
        if self.obj_type == "cloud":
            self.x += self.speed
        elif self.obj_type == "bird":
            self.x += self.speed * 1.5
            if self.anim_tick % 4 == 0:
                self.frame = 1 - self.frame
        elif self.obj_type in ("torch", "flag"):
            if self.anim_tick % 5 == 0:
                self.frame = (self.frame + 1) % 3 if self.obj_type == "torch" else (self.frame + 1) % 2

    def get_sprite(self) -> Sprite | None:
        if not HAS_V2_SPRITES:
            return None
        if self.obj_type == "cloud":
            return CLOUD
        elif self.obj_type == "bird":
            return BIRD_FRAMES[self.frame % len(BIRD_FRAMES)]
        elif self.obj_type == "torch":
            return TORCH_FRAMES[self.frame % len(TORCH_FRAMES)]
        elif self.obj_type == "flag":
            return FLAG_FRAMES[self.frame % len(FLAG_FRAMES)]
        return None


class Kingdom:
    """The Red Pine kingdom — grows based on real business data."""

    def __init__(self, metrics=None):
        # Accept either RedPineMetrics or legacy ProjectMetrics
        self.metrics = metrics
        self.hq: Building | None = None
        self.customer_buildings: list[Building] = []
        self.district_buildings: list[Building] = []
        self.buildings: list[Building] = []  # all buildings combined
        self.decoration_sprites: list[tuple[int, int, Sprite]] = []
        self.path_tiles: list[tuple[int, int]] = []
        self.water_tiles: list[tuple[int, int]] = []
        self.agent_manager = AgentManager()
        self.construction_sites: list[ConstructionSite] = []
        self.ambient_objects: list[AmbientObject] = []
        self.fence_tiles: list[tuple[int, int]] = []
        self.shore_tiles: list[tuple[int, int]] = []
        self.anim_tick = 0

        # Canvas dimensions — balanced for dense RPG town feel
        self.canvas_w = 192
        self.canvas_h = 120

        # Seed for consistent layout
        self._rng = random.Random(42)
        self._layout_dirty = True

        # For backward compat with Town interface
        self.project_path = ""
        self.name = "Red Pine Kingdom"

    def _get_revenue(self) -> float:
        """Get revenue from metrics (works with both old and new metrics)."""
        if self.metrics is None:
            return 0.0
        if hasattr(self.metrics, 'revenue'):
            return self.metrics.revenue
        return 0.0

    def _get_milestone(self) -> str:
        """Get age milestone name."""
        if self.metrics and hasattr(self.metrics, 'age_milestone'):
            return self.metrics.age_milestone
        return "Settlement"

    def _get_milestone_progress(self) -> float:
        """Get progress within current milestone (0.0-1.0)."""
        if self.metrics and hasattr(self.metrics, 'age_progress'):
            return self.metrics.age_progress
        return 0.0

    def _get_customers(self) -> list:
        """Get customer list from metrics, with placeholder fallback.

        Always generates a minimum number of buildings so the kingdom
        looks alive even without live Supabase data.
        """
        if self.metrics and hasattr(self.metrics, 'customers') and self.metrics.customers:
            return self.metrics.customers

        # Determine count from metrics or config
        count = 0
        if self.metrics and hasattr(self.metrics, 'customer_count'):
            count = self.metrics.customer_count
        elif isinstance(self.metrics, dict):
            count = int(self.metrics.get('customers', 0))

        # Always show at least some buildings based on milestone
        milestone_minimums = {
            "Settlement": 6, "Village": 10, "Town": 15,
            "City": 20, "Capital": 25, "Metropolis": 30,
        }
        milestone = self._get_milestone()
        minimum = milestone_minimums.get(milestone, 6)
        count = max(count, minimum)

        btypes = ["beauty", "restaurant", "fitness", "home_services",
                   "professional", "creative", "education", "automotive", "retail"]

        class _Placeholder:
            def __init__(self, i, btype):
                self.business_type = btype
                self.name = f"{btype.replace('_', ' ').title()} #{i+1}"

        return [_Placeholder(i, btypes[i % len(btypes)]) for i in range(count)]

    def update_metrics(self, metrics):
        """Update metrics and mark layout for refresh if milestone changed."""
        old_milestone = self._get_milestone()
        self.metrics = metrics
        if self._get_milestone() != old_milestone:
            self._layout_dirty = True

    def generate_layout(self, width: int, height: int):
        """Generate the kingdom layout."""
        self.canvas_w = width
        self.canvas_h = height
        self.buildings.clear()
        self.customer_buildings.clear()
        self.district_buildings.clear()
        self.decoration_sprites.clear()
        self.water_tiles.clear()
        self.path_tiles.clear()
        self.fence_tiles.clear()
        self.shore_tiles.clear()
        self.construction_sites.clear()
        self.ambient_objects.clear()

        rng = self._rng
        rng.seed(42)  # consistent layout

        cx, cy = width // 2, height // 2

        # ── Place HQ at center ──
        self._place_hq(cx, cy)

        # ── Place district buildings in inner ring ──
        self._place_districts(cx, cy)

        # ── Place customer buildings in expanding rings ──
        self._place_customer_buildings(cx, cy)

        # ── Combine all buildings ──
        if self.hq:
            self.buildings = [self.hq] + self.district_buildings + self.customer_buildings
        else:
            self.buildings = self.district_buildings + self.customer_buildings

        # ── Generate water for higher milestones ──
        revenue = self._get_revenue()
        if revenue >= 5000 and width > 40:
            self._generate_river(width, height)

        # ── Generate paths ──
        self._generate_paths()

        # ── Scatter decorations ──
        self._scatter_trees(width, height)
        self._scatter_flowers(width, height)
        self._scatter_decorations(width, height)

        # ── Place fences near buildings ──
        self._scatter_fences(width, height)

        # ── Spawn ambient objects ──
        self._spawn_ambient(width, height)

        # ── Ensure agents ──
        pop = 3
        if self.metrics and hasattr(self.metrics, 'population'):
            pop = min(self.metrics.population, 8)
        self.agent_manager.ensure_min_agents(max(2, pop), cx, cy)

        # ── Spawn role agents ──
        self._spawn_role_agents(cx, cy)

        self._layout_dirty = False

    def _place_hq(self, cx: int, cy: int):
        """Place the HQ building at center, sized by milestone."""
        milestone = self._get_milestone()

        if HAS_V2_SPRITES and milestone in HQ_SPRITES:
            sprite = HQ_SPRITES[milestone]
        else:
            sprite = CASTLE  # fallback

        sw = len(sprite[0]) if sprite else 13
        sh = len(sprite) if sprite else 12

        self.hq = Building(
            x=cx - sw // 2,
            y=cy - sh // 2,
            building_type="hq",
            name=f"Red Pine HQ ({milestone})",
            sprite=sprite,
            is_hq=True,
        )

    def _place_districts(self, cx: int, cy: int):
        """Place district buildings in inner ring around HQ."""
        rng = self._rng
        district_items = list(DISTRICTS.items())
        placed_rects = []

        # HQ rect
        if self.hq:
            placed_rects.append((self.hq.x - 2, self.hq.y - 2, self.hq.width + 4, self.hq.height + 4))

        for i, (key, info) in enumerate(district_items):
            btype = info["building"]
            reg = BUILDING_REGISTRY.get(btype)
            if not reg:
                continue
            sprite = reg["sprite"]
            sw = len(sprite[0]) if sprite else 9
            sh = len(sprite) if sprite else 10

            angle = (2 * math.pi * i / len(district_items)) + rng.uniform(-0.2, 0.2)
            radius = max(sw, sh) * 1.8 + rng.uniform(-2, 3)
            bx = int(cx + math.cos(angle) * radius) - sw // 2
            by = int(cy + math.sin(angle) * radius * 0.6) - sh // 2

            bx = max(2, min(self.canvas_w - sw - 2, bx))
            by = max(2, min(self.canvas_h - sh - 2, by))

            for _ in range(20):
                if not self._overlaps(bx, by, sw, sh, placed_rects):
                    break
                bx += rng.randint(-3, 3)
                by += rng.randint(-2, 2)
                bx = max(2, min(self.canvas_w - sw - 2, bx))
                by = max(2, min(self.canvas_h - sh - 2, by))

            building = Building(
                x=bx, y=by,
                building_type=btype,
                name=info["name"],
                sprite=sprite,
                is_district=True,
            )
            self.district_buildings.append(building)
            placed_rects.append((bx - 2, by - 2, sw + 4, sh + 4))

    def _place_customer_buildings(self, cx: int, cy: int):
        """Place a building for each Red Pine customer."""
        customers = self._get_customers()
        if not customers and not HAS_V2_SPRITES:
            return

        # Cap buildings based on canvas area — allow more buildings with bigger canvas
        max_buildings = (self.canvas_w * self.canvas_h) // 250
        if len(customers) > max_buildings:
            customers = customers[:max_buildings]

        rng = self._rng
        placed_rects = []

        # Existing building rects
        if self.hq:
            placed_rects.append((self.hq.x - 2, self.hq.y - 2, self.hq.width + 4, self.hq.height + 4))
        for b in self.district_buildings:
            placed_rects.append((b.x - 2, b.y - 2, b.width + 4, b.height + 4))

        for i, customer in enumerate(customers):
            btype_key = "hut"
            sprite = HUT

            if HAS_V2_SPRITES:
                cust_type = customer.business_type if hasattr(customer, 'business_type') else "other"
                btype_key = BUSINESS_TYPE_TO_BUILDING.get(cust_type, "beauty_shop")
                reg = CUSTOMER_BUILDING_REGISTRY.get(btype_key)
                if reg:
                    sprite = reg["sprite"]

            sw = len(sprite[0]) if sprite else 10
            sh = len(sprite) if sprite else 10

            # Place in expanding rings — older customers closer to center
            # Some extra spacing so decorations fit between buildings
            ring = (i // 8) + 2  # 8 buildings per ring
            angle = (i * 2.3 + rng.uniform(-0.4, 0.4))
            radius = ring * max(sw, sh) * 1.2 + rng.uniform(-3, 4)
            bx = int(cx + math.cos(angle) * radius) - sw // 2
            by = int(cy + math.sin(angle) * radius * 0.55) - sh // 2

            bx = max(2, min(self.canvas_w - sw - 2, bx))
            by = max(2, min(self.canvas_h - sh - 2, by))

            for _ in range(20):
                if not self._overlaps(bx, by, sw, sh, placed_rects):
                    break
                bx += rng.randint(-3, 3)
                by += rng.randint(-2, 2)
                bx = max(2, min(self.canvas_w - sw - 2, bx))
                by = max(2, min(self.canvas_h - sh - 2, by))

            cust_name = customer.name if hasattr(customer, 'name') else f"Customer {i+1}"
            building = Building(
                x=bx, y=by,
                building_type=btype_key,
                name=cust_name,
                sprite=sprite,
                is_customer=True,
                customer_type=customer.business_type if hasattr(customer, 'business_type') else "",
            )
            self.customer_buildings.append(building)
            placed_rects.append((bx - 2, by - 2, sw + 4, sh + 4))

    def _overlaps(self, x, y, w, h, rects):
        for rx, ry, rw, rh in rects:
            if x < rx + rw and x + w > rx and y < ry + rh and y + h > ry:
                return True
        return False

    def _get_path_style(self) -> str:
        """Return path type based on revenue."""
        revenue = self._get_revenue()
        if revenue < 500:
            return "dirt"
        elif revenue < 1000:
            return "partial_cobble"
        elif revenue < 5000:
            return "cobblestone"
        elif revenue < 10000:
            return "paved"
        else:
            return "brick"

    def _generate_river(self, width: int, height: int):
        """Generate a river with natural sandy/dirt bank edges."""
        rng = self._rng
        y = height // 2 + rng.randint(-height // 6, height // 6)
        river_width = rng.randint(3, 5)
        self.shore_tiles: list[tuple[int, int]] = []

        for x in range(0, width):
            y += rng.choice([-1, 0, 0, 0, 0, 1])
            y = max(4, min(height - 6, y))
            # Main water body
            for dy in range(river_width):
                self.water_tiles.append((x, y + dy))
            # Shore/bank tiles on edges (sand/dirt transition)
            self.shore_tiles.append((x, y - 1))
            self.shore_tiles.append((x, y - 2))
            self.shore_tiles.append((x, y + river_width))
            self.shore_tiles.append((x, y + river_width + 1))

    def _generate_paths(self):
        """Generate wide paths between buildings with organic routing."""
        if not self.buildings or len(self.buildings) < 2:
            return
        hq = self.buildings[0]
        ccx = int(hq.center_x)
        ccy = int(hq.y + hq.height + 2)

        path_set = set()
        building_pixels = set()
        for b in self.buildings:
            for by in range(b.y - 1, b.y + b.height + 1):
                for bx in range(b.x - 1, b.x + b.width + 1):
                    building_pixels.add((bx, by))

        # Path width: 6-8px for main roads — wide visible roads like RPG towns
        half_w = 3

        for building in self.buildings[1:]:
            bx = int(building.center_x)
            by = int(building.y + building.height + 2)
            x, y = bx, by

            # Walk horizontal then vertical — wide roads
            while x != ccx:
                for d in range(-half_w, half_w + 1):
                    if (x, y + d) not in building_pixels:
                        path_set.add((x, y + d))
                x += 1 if x < ccx else -1
            while y != ccy:
                for d in range(-half_w, half_w + 1):
                    if (x + d, y) not in building_pixels:
                        path_set.add((x + d, y))
                y += 1 if y < ccy else -1

        self.path_tiles = list(path_set)

    def _scatter_trees(self, width: int, height: int):
        """Scatter trees, rocks, stumps densely with edge border for forest feel."""
        rng = self._rng

        # Build sprite lists with varieties
        big_trees = [TREE_PINE, TREE_PINE, TREE_OAK, TREE_OAK]
        small_plants = [BUSH, BUSH, SHRUB, TALL_GRASS]
        if HAS_LANDSCAPE_SPRITES:
            big_trees.extend([TREE_WILLOW, TREE_MAPLE])
            small_plants.extend([BUSH_BERRY, ROCK_SMALL, ROCK_LARGE, STUMP, FALLEN_LOG])

        all_trees = big_trees + small_plants

        # Build occupied set from buildings, water, paths
        occupied = set()
        for b in self.buildings:
            for bx in range(b.x - 3, b.x + b.width + 3):
                for by in range(b.y - 2, b.y + b.height + 2):
                    occupied.add((bx, by))
        for wx, wy in self.water_tiles:
            occupied.add((wx, wy))
        for px, py in self.path_tiles:
            for d in range(-1, 2):
                occupied.add((px + d, py))
                occupied.add((px, py + d))

        def _try_place(sprite, tx, ty):
            sw = len(sprite[0])
            sh = len(sprite)
            if tx < 0 or ty < 0 or tx + sw >= width or ty + sh >= height:
                return False
            for sx in range(tx - 1, tx + sw + 1):
                for sy in range(ty - 1, ty + sh + 1):
                    if (sx, sy) in occupied:
                        return False
            self.decoration_sprites.append((tx, ty, sprite))
            for sx in range(tx - 1, tx + sw + 1):
                for sy in range(ty - 1, ty + sh + 1):
                    occupied.add((sx, sy))
            return True

        # ── Edge border: dense tree line around all edges ──
        # Thinner border to leave more room for town interior
        border_depth = max(8, min(width, height) // 7)

        # Pass 1: systematic grid placement along edges (high success rate)
        for sprite in [TREE_PINE, TREE_OAK] * 2:
            sw = len(sprite[0])
            sh = len(sprite)
            # Top edge
            for tx in range(0, width - sw, sw + 1):
                for ty in range(0, border_depth, sh + 1):
                    s = rng.choice(big_trees)
                    _try_place(s, tx + rng.randint(-1, 1), ty + rng.randint(-1, 1))
            # Bottom edge
            for tx in range(0, width - sw, sw + 1):
                for ty in range(height - border_depth, height - sh, sh + 1):
                    s = rng.choice(big_trees)
                    _try_place(s, tx + rng.randint(-1, 1), ty + rng.randint(-1, 1))
            # Left edge
            for ty in range(0, height - sh, sh + 1):
                for tx in range(0, border_depth, sw + 1):
                    s = rng.choice(big_trees)
                    _try_place(s, tx + rng.randint(-1, 1), ty + rng.randint(-1, 1))
            # Right edge
            for ty in range(0, height - sh, sh + 1):
                for tx in range(width - border_depth, width - sw, sw + 1):
                    s = rng.choice(big_trees)
                    _try_place(s, tx + rng.randint(-1, 1), ty + rng.randint(-1, 1))

        # Pass 2: fill gaps in border with bushes and small trees
        edge_fill = (width + height) * 3
        for _ in range(edge_fill):
            sprite = rng.choice(small_plants + big_trees)
            sw = len(sprite[0])
            sh = len(sprite)
            side = rng.randint(0, 3)
            if side == 0:
                tx, ty = rng.randint(0, width - sw), rng.randint(0, border_depth)
            elif side == 1:
                tx, ty = rng.randint(0, width - sw), rng.randint(max(0, height - border_depth - sh), max(1, height - sh))
            elif side == 2:
                tx, ty = rng.randint(0, border_depth), rng.randint(0, max(1, height - sh))
            else:
                tx, ty = rng.randint(max(0, width - border_depth - sw), max(1, width - sw)), rng.randint(0, max(1, height - sh))
            _try_place(sprite, tx, ty)

        # ── Interior trees — dense scatter ──
        tree_count = 120 + len(self.customer_buildings) * 6
        tree_count = min(tree_count, 400)
        for _ in range(tree_count):
            sprite = rng.choice(all_trees)
            sw = len(sprite[0])
            sh = len(sprite)
            tx = rng.randint(border_depth, max(border_depth + 1, width - sw - border_depth))
            ty = rng.randint(border_depth, max(border_depth + 1, height - sh - border_depth))
            _try_place(sprite, tx, ty)

        # ── Small plants gap-fill everywhere ──
        for _ in range(tree_count):
            sprite = rng.choice(small_plants)
            sw = len(sprite[0])
            sh = len(sprite)
            tx = rng.randint(1, max(2, width - sw - 1))
            ty = rng.randint(1, max(2, height - sh - 1))
            _try_place(sprite, tx, ty)

    def _scatter_flowers(self, width: int, height: int):
        """Scatter flowers and small decorations generously across the map."""
        rng = self._rng
        flower_count = 40 + len(self.customer_buildings) * 4
        flower_count = min(flower_count, 150)

        occupied = set()
        for b in self.buildings:
            for bx in range(b.x - 1, b.x + b.width + 1):
                for by in range(b.y - 1, b.y + b.height + 1):
                    occupied.add((bx, by))
        for wx, wy in self.water_tiles:
            occupied.add((wx, wy))
        for px, py in self.path_tiles:
            occupied.add((px, py))
        # Also skip existing decorations
        for dx, dy, ds in self.decoration_sprites:
            sw = len(ds[0]) if ds and ds[0] else 1
            sh = len(ds) if ds else 1
            for sx in range(dx, dx + sw):
                for sy in range(dy, dy + sh):
                    occupied.add((sx, sy))

        for _ in range(flower_count):
            sprite = rng.choice(FLOWER_SPRITES)
            sw = len(sprite[0]) if sprite and sprite[0] else 1
            sh = len(sprite) if sprite else 1
            fx = rng.randint(1, max(2, width - sw - 1))
            fy = rng.randint(1, max(2, height - sh - 1))
            if (fx, fy) not in occupied:
                self.decoration_sprites.append((fx, fy, sprite))
                for sx in range(fx, fx + sw):
                    for sy in range(fy, fy + sh):
                        occupied.add((sx, sy))

    def _scatter_decorations(self, width: int, height: int):
        """Scatter barrels, crates, market stalls, lamp posts, signs, wells near buildings.

        This creates the dense, populated RPG town feel with props everywhere.
        """
        if not HAS_DECORATION_SPRITES:
            return

        rng = self._rng

        # Build occupied set
        occupied = set()
        for b in self.buildings:
            for bx in range(b.x - 1, b.x + b.width + 1):
                for by in range(b.y - 1, b.y + b.height + 1):
                    occupied.add((bx, by))
        for wx, wy in self.water_tiles:
            occupied.add((wx, wy))
        for px, py in self.path_tiles:
            occupied.add((px, py))
        for dx, dy, ds in self.decoration_sprites:
            sw = len(ds[0]) if ds and ds[0] else 1
            sh = len(ds) if ds else 1
            for sx in range(dx, dx + sw):
                for sy in range(dy, dy + sh):
                    occupied.add((sx, sy))

        def _try_place_deco(sprite, tx, ty):
            sw = len(sprite[0])
            sh = len(sprite)
            if tx < 0 or ty < 0 or tx + sw >= width or ty + sh >= height:
                return False
            for sx in range(tx, tx + sw):
                for sy in range(ty, ty + sh):
                    if (sx, sy) in occupied:
                        return False
            self.decoration_sprites.append((tx, ty, sprite))
            for sx in range(tx - 1, tx + sw + 1):
                for sy in range(ty - 1, ty + sh + 1):
                    occupied.add((sx, sy))
            return True

        # ── Place barrels and crates next to buildings ──
        small_props = [BARREL, CRATE, CRATE_STACK]
        for building in self.buildings:
            # Try 2-3 props per building
            for _ in range(rng.randint(1, 3)):
                prop = rng.choice(small_props)
                sw = len(prop[0])
                sh = len(prop)
                # Place near building edges
                side = rng.choice(["right", "left", "bottom"])
                if side == "right":
                    tx = building.x + building.width + 1
                    ty = building.y + rng.randint(0, max(0, building.height - sh))
                elif side == "left":
                    tx = building.x - sw - 1
                    ty = building.y + rng.randint(0, max(0, building.height - sh))
                else:
                    tx = building.x + rng.randint(0, max(0, building.width - sw))
                    ty = building.y + building.height + 1
                _try_place_deco(prop, tx, ty)

        # ── Place lamp posts along paths ──
        path_list = self.path_tiles
        if path_list:
            lamp_count = min(len(path_list) // 40, 20)
            for i in range(lamp_count):
                idx = (i * 41 + 17) % len(path_list)
                px, py = path_list[idx]
                # Try to place next to path
                for offset in [(3, 0), (-3, 0), (0, -3), (0, 3)]:
                    if _try_place_deco(LAMP_POST, px + offset[0], py + offset[1]):
                        break

        # ── Place sign posts at road junctions ──
        sign_count = min(len(self.buildings) // 3, 8)
        for i in range(sign_count):
            if i < len(self.buildings):
                b = self.buildings[i]
                # Place near building entrance
                tx = b.x + b.width // 2 + rng.choice([-4, 4])
                ty = b.y + b.height + 2
                _try_place_deco(SIGN_POST, tx, ty)

        # ── Place flower beds near district buildings ──
        for building in self.district_buildings[:4]:
            # Flower beds in front of district buildings
            tx = building.x + rng.randint(0, max(0, building.width - 6))
            ty = building.y + building.height + 2
            _try_place_deco(FLOWER_BED, tx, ty)

        # ── Place a market stall near the market building ──
        for building in self.buildings:
            if building.building_type == "market":
                tx = building.x + building.width + 3
                ty = building.y + rng.randint(0, max(0, building.height - 8))
                _try_place_deco(MARKET_STALL, tx, ty)
                # Second stall
                tx2 = building.x - 14
                ty2 = building.y + rng.randint(0, max(0, building.height - 8))
                _try_place_deco(MARKET_STALL, tx2, ty2)

        # ── Place a well in the town center ──
        if self.hq:
            well_x = self.hq.x + self.hq.width + 4
            well_y = self.hq.y + self.hq.height // 2
            _try_place_deco(WELL_SPRITE, well_x, well_y)

        # ── Scatter extra barrels and crates randomly in town area ──
        for _ in range(30):
            prop = rng.choice(small_props)
            sw = len(prop[0])
            sh = len(prop)
            tx = rng.randint(10, max(11, width - sw - 10))
            ty = rng.randint(10, max(11, height - sh - 10))
            _try_place_deco(prop, tx, ty)

    def _scatter_fences(self, width: int, height: int):
        """Place fence segments near buildings and along path edges."""
        rng = self._rng
        path_set = set(self.path_tiles)

        for building in self.customer_buildings[:12]:
            # Place a short fence run in front of or beside each building
            side = rng.choice(["bottom", "left", "right"])
            if side == "bottom":
                fy = building.y + building.height + 1
                fx_start = building.x - 1
                for i in range(building.width + 2):
                    fx = fx_start + i
                    if 0 <= fx < width and 0 <= fy < height and (fx, fy) not in path_set:
                        self.fence_tiles.append((fx, fy))
            elif side == "left":
                fx = building.x - 2
                fy_start = building.y
                for i in range(min(building.height, 6)):
                    fy = fy_start + i
                    if 0 <= fx < width and 0 <= fy < height and (fx, fy) not in path_set:
                        self.fence_tiles.append((fx, fy))
            else:
                fx = building.x + building.width + 1
                fy_start = building.y
                for i in range(min(building.height, 6)):
                    fy = fy_start + i
                    if 0 <= fx < width and 0 <= fy < height and (fx, fy) not in path_set:
                        self.fence_tiles.append((fx, fy))

    def _spawn_ambient(self, width: int, height: int):
        """Spawn ambient objects — clouds, birds, torches, flags."""
        rng = self._rng
        # More clouds
        for _ in range(rng.randint(3, 6)):
            self.ambient_objects.append(AmbientObject(
                x=rng.uniform(-10, width),
                y=rng.uniform(0, 6),
                obj_type="cloud",
                speed=rng.uniform(0.03, 0.1),
            ))

        # More birds
        for _ in range(rng.randint(1, 3)):
            self.ambient_objects.append(AmbientObject(
                x=rng.uniform(-5, width // 2),
                y=rng.uniform(1, 8),
                obj_type="bird",
                speed=rng.uniform(0.15, 0.3),
            ))

        # Torches on HQ for Town+ milestones
        revenue = self._get_revenue()
        if revenue >= 5000 and self.hq:
            self.ambient_objects.append(AmbientObject(
                x=self.hq.x - 1, y=self.hq.y + self.hq.height - 4,
                obj_type="torch",
            ))
            self.ambient_objects.append(AmbientObject(
                x=self.hq.x + self.hq.width, y=self.hq.y + self.hq.height - 4,
                obj_type="torch",
            ))

        # Flags on HQ for City+
        if revenue >= 10000 and self.hq:
            self.ambient_objects.append(AmbientObject(
                x=self.hq.x + self.hq.width // 2, y=self.hq.y - 2,
                obj_type="flag",
            ))

    def _spawn_role_agents(self, cx: int, cy: int):
        """Spawn named role agents near relevant district buildings."""
        roles = ["coo", "receptionist", "content_writer", "review_manager", "route_planner"]
        active_agents = 0
        if self.metrics and hasattr(self.metrics, 'active_agents'):
            active_agents = self.metrics.active_agents

        # Spawn at least some role agents even without active subscriptions
        for i, role in enumerate(roles[:max(2, active_agents)]):
            # Find a district building to spawn near
            if i < len(self.district_buildings):
                b = self.district_buildings[i]
                x, y = b.center_x + self._rng.uniform(-3, 3), b.y + b.height
            else:
                x, y = cx + self._rng.uniform(-10, 10), cy + self._rng.uniform(-5, 5)
            self.agent_manager.spawn_role_agent(role, x, y)

        # Spawn townsfolk proportional to milestone — near buildings for organic spread
        townsfolk_counts = {
            "Settlement": 5, "Village": 8, "Town": 12,
            "City": 16, "Capital": 20, "Metropolis": 25,
        }
        milestone = self._get_milestone()
        n_townsfolk = townsfolk_counts.get(milestone, 3)
        all_buildings = self.buildings
        for i in range(n_townsfolk):
            # Spawn near a random building to spread them across the town
            if all_buildings:
                b = all_buildings[i % len(all_buildings)]
                vx = b.center_x + self._rng.uniform(-12, 12)
                vy = b.y + b.height + self._rng.uniform(0, 6)
            else:
                vx = cx + self._rng.uniform(-50, 50)
                vy = cy + self._rng.uniform(-25, 25)
            agent = self.agent_manager.spawn_agent(vx, vy, use_v2=True)
            agent.variant = 5 + (i % 7)  # cycle through townspeople variants (5-11)

    def draw(self, canvas: PixelCanvas, tick: int = 0):
        """Draw the entire kingdom onto a pixel canvas."""
        if self._layout_dirty or not self.buildings:
            self.generate_layout(canvas.width, canvas.height)

        canvas.clear()

        # ── Layer 0: Ground ──
        self._draw_ground(canvas)

        # ── Layer 0b: Town clearing — dirt/stone under buildings ──
        self._draw_town_clearing(canvas)

        # ── Layer 1: Shore/banks (sand transition before water) ──
        self._draw_shore(canvas)

        # ── Layer 1b: Water ──
        self._draw_water(canvas, tick)

        # ── Layer 2: Paths ──
        self._draw_paths(canvas)

        # ── Layer 3: Decorations (trees, flowers, rocks) ──
        for dx, dy, sprite in self.decoration_sprites:
            canvas.draw_sprite(sprite, dx, dy)

        # ── Layer 3b: Fences ──
        self._draw_fences(canvas)

        # ── Layer 4: Construction sites ──
        for site in self.construction_sites:
            sprite = site.get_current_sprite()
            canvas.draw_sprite(sprite, site.x, site.y)

        # ── Layer 4b: Building shadows (drawn before buildings) ──
        self._draw_building_shadows(canvas)

        # ── Layer 5: Buildings ──
        for building in self.buildings:
            if building.building_type == "windmill":
                frame = (tick // 6) % len(WINDMILL_FRAMES)
                canvas.draw_sprite(WINDMILL_FRAMES[frame], building.x, building.y)
            else:
                canvas.draw_sprite(building.sprite, building.x, building.y)

        # ── Layer 6: Agents ──
        for agent in self.agent_manager.agents:
            if agent.inside_building:
                continue
            sprite = agent.get_sprite()
            ax, ay = int(agent.x), int(agent.y)
            if agent.facing_right:
                canvas.draw_sprite(sprite, ax, ay)
            else:
                canvas.draw_sprite_flipped(sprite, ax, ay)
            # Bright marker dot above agent head for visibility
            sw = len(sprite[0]) if sprite else 3
            marker_x = ax + sw // 2
            marker_y = ay - 1
            if 0 <= marker_x < canvas.width and 0 <= marker_y < canvas.height:
                canvas.set_pixel(marker_x, marker_y, palettes.WINDOW_BRIGHT)

        # ── Layer 7: Ambient objects ──
        for amb in self.ambient_objects:
            sprite = amb.get_sprite()
            if sprite:
                canvas.draw_sprite(sprite, int(amb.x), int(amb.y))

        # ── Layer 8: Particles ──
        self._draw_particles(canvas)

        # ── Layer 9: Day/night tint ──
        from datetime import datetime
        hour = datetime.now().hour
        tint_info = palettes.get_time_tint(hour)
        if tint_info[0] is not None:
            canvas.apply_tint(tint_info[0], tint_info[1])

    def _draw_ground(self, canvas: PixelCanvas):
        """Draw rich, varied ground with organic grass patches.

        Uses layered patches at different scales for a lush, natural look.
        All patches are cell-aligned (even y) for clean half-block rendering.
        """
        base = palettes.GRASS_DARK
        mid = palettes.GRASS_MID
        main_g = palettes.GRASS
        light = palettes.GRASS_LIGHT
        highlight = palettes.GRASS_HIGHLIGHT
        meadow = palettes.MEADOW

        w, h = canvas.width, canvas.height

        # Solid base — dark green foundation
        canvas.fill_rect(0, 0, w, h, base)

        rng = random.Random(42)

        # Layer 1: Large organic patches of mid-green (5-10px blobs)
        # These create the broad terrain variation visible in RPG games
        n_large = (w * h) // 50
        for _ in range(n_large):
            cx = rng.randint(0, w - 1)
            cy = (rng.randint(0, max(1, h // 2 - 1))) * 2
            radius = rng.randint(3, 7)
            color = rng.choice([mid, mid, main_g, meadow])
            # Circular blob with jitter
            for _ in range(radius * radius):
                dx = rng.randint(-radius, radius)
                dy = rng.randint(-radius, radius)
                if dx * dx + dy * dy <= radius * radius:
                    px = cx + dx
                    py = ((cy + dy) // 2) * 2  # cell-align
                    if 0 <= px < w and 0 <= py < h - 1:
                        canvas.set_pixel(px, py, color)
                        canvas.set_pixel(px, py + 1, color)

        # Layer 2: Medium patches of lighter greens (2-4px)
        n_med = (w * h) // 80
        for _ in range(n_med):
            cx = rng.randint(0, w - 1)
            cy = (rng.randint(0, max(1, h // 2 - 1))) * 2
            size = rng.randint(2, 4)
            color = rng.choice([main_g, light, meadow, mid])
            for dy in range(0, size * 2, 2):
                for dx in range(size):
                    px, py = cx + dx, cy + dy
                    if 0 <= px < w and 0 <= py < h - 1:
                        canvas.set_pixel(px, py, color)
                        canvas.set_pixel(px, py + 1, color)

        # Layer 3: Small highlight specks (1-2px) for shimmer
        n_small = (w * h) // 120
        for _ in range(n_small):
            px = rng.randint(0, w - 1)
            py = (rng.randint(0, max(1, h // 2 - 1))) * 2
            color = rng.choice([light, highlight, meadow])
            canvas.set_pixel(px, py, color)
            canvas.set_pixel(px, py + 1, color)

        # Layer 4: Tiny dirt specks for texture (scattered soil)
        n_dirt = (w * h) // 300
        for _ in range(n_dirt):
            px = rng.randint(0, w - 1)
            py = (rng.randint(0, max(1, h // 2 - 1))) * 2
            canvas.set_pixel(px, py, palettes.DIRT_LIGHT)
            canvas.set_pixel(px, py + 1, palettes.DIRT_LIGHT)

    def _draw_town_clearing(self, canvas: PixelCanvas):
        """Draw dirt/stone clearings around buildings for a town-square feel.

        In RPG references, the area around buildings is cleared earth, not
        wild grass. This creates visual separation between town and wilderness.
        """
        dirt = palettes.DIRT
        dirt_l = palettes.DIRT_LIGHT
        dirt_d = palettes.DIRT_DARK

        for building in self.buildings:
            # Padding around each building footprint
            pad = 3 if building.is_hq else 2
            x0 = building.x - pad
            y0 = building.y - pad
            x1 = building.x + building.width + pad
            y1 = building.y + building.height + pad

            for py in range(max(0, y0), min(canvas.height, y1)):
                for px in range(max(0, x0), min(canvas.width, x1)):
                    # Inner area = solid dirt, outer ring = mixed
                    inner = (building.x - 1 <= px <= building.x + building.width and
                             building.y - 1 <= py <= building.y + building.height)
                    if inner:
                        canvas.set_pixel(px, py, dirt)
                    else:
                        # Feathered edge: mix of dirt and grass
                        v = ((px * 7 + py * 13) * 2654435761) >> 16
                        if v % 3 == 0:
                            canvas.set_pixel(px, py, dirt_l)
                        elif v % 3 == 1:
                            canvas.set_pixel(px, py, dirt_d)
                        # else: leave as grass for organic edge

    def _draw_shore(self, canvas: PixelCanvas):
        """Draw sandy/dirt shore tiles along river banks."""
        if not self.shore_tiles:
            return
        water_set = set(self.water_tiles)
        for sx, sy in self.shore_tiles:
            if (sx, sy) not in water_set and 0 <= sx < canvas.width and 0 <= sy < canvas.height:
                # Alternate between sand and dirt for natural look
                if (sx + sy) % 3 == 0:
                    canvas.set_pixel(sx, sy, palettes.DIRT_LIGHT)
                else:
                    canvas.set_pixel(sx, sy, palettes.DIRT)

    def _draw_water(self, canvas: PixelCanvas, tick: int):
        for wx, wy in self.water_tiles:
            frame_idx = (tick // 4 + wx + wy) % len(TILE_WATER_FRAMES)
            tile = TILE_WATER_FRAMES[frame_idx]
            canvas.set_pixel(wx, wy, tile[0][0])
            if wy + 1 < canvas.height:
                canvas.set_pixel(wx, wy + 1, tile[1][0])
            if (wx + wy * 3) % 7 == 0:
                shimmer = TILE_WATER_SHIMMER_FRAMES[frame_idx]
                canvas.set_pixel(wx, wy, shimmer[0][0])

    def _draw_paths(self, canvas: PixelCanvas):
        """Draw paths with warm, high-contrast colors that stand out on grass."""
        water_set = set(self.water_tiles)
        path_set = set(self.path_tiles)
        path_style = self._get_path_style()

        # Use warm tan/sand tones for maximum contrast against green grass
        # These are the colors RPG games use for visible paths
        sand = (234, 212, 170)      # bright sand highlight
        tan = palettes.DIRT_LIGHT   # (228, 166, 114) warm tan
        dirt = palettes.DIRT        # (184, 111, 80) medium brown
        dark = palettes.DIRT_DARK   # (115, 62, 57) dark border

        if path_style == "dirt":
            main_c, light_c, edge_c = tan, sand, dirt
        elif path_style in ("partial_cobble", "cobblestone"):
            main_c, light_c, edge_c = palettes.COBBLE_LIGHT, sand, palettes.COBBLE
        elif path_style == "paved":
            main_c, light_c, edge_c = palettes.STONE_LIGHT, (220, 225, 240), palettes.STONE
        else:  # brick
            main_c, light_c, edge_c = tan, sand, dirt

        for px, py in self.path_tiles:
            if (px, py) in water_set:
                continue
            # Check if edge of path (adjacent to non-path = border)
            is_edge = any((px + dx, py + dy) not in path_set
                         for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)])
            if is_edge:
                # Dark border for definition against grass
                canvas.set_pixel(px, py, dark)
            elif (px + py) % 4 == 0:
                canvas.set_pixel(px, py, light_c)
            elif (px * 3 + py * 7) % 5 == 0:
                canvas.set_pixel(px, py, edge_c)
            else:
                canvas.set_pixel(px, py, main_c)

    def _draw_building_shadows(self, canvas: PixelCanvas):
        """Draw a subtle drop shadow for depth — blends with grass."""
        # Use a very dark green that blends with the grass base
        sc = (28, 62, 48)  # dark shadow green
        for building in self.buildings:
            # Bottom shadow (2px below)
            sy = building.y + building.height
            for sx in range(building.x + 1, building.x + building.width + 2):
                canvas.set_pixel(sx, sy, sc)
                if sy + 1 < canvas.height:
                    canvas.set_pixel(sx, sy + 1, sc)
            # Right shadow (1px wide)
            sx = building.x + building.width
            for sy2 in range(building.y + 1, building.y + building.height + 2):
                canvas.set_pixel(sx, sy2, sc)
                if sx + 1 < canvas.width:
                    canvas.set_pixel(sx + 1, sy2, sc)

    def _draw_fences(self, canvas: PixelCanvas):
        """Draw fence tiles as simple wood-colored pixels."""
        for fx, fy in self.fence_tiles:
            canvas.set_pixel(fx, fy, palettes.WOOD)
            if fy + 1 < canvas.height:
                canvas.set_pixel(fx, fy + 1, palettes.WOOD_DARK)

    def _draw_particles(self, canvas: PixelCanvas):
        for p in self.agent_manager.particles:
            px, py = int(p.x), int(p.y)
            if p.particle_type == "smoke":
                colors = [palettes.SMOKE_DARK, palettes.SMOKE, palettes.SMOKE_LIGHT, None]
            elif p.particle_type == "sparkle":
                colors = [palettes.SPARKLE, palettes.WINDOW_BRIGHT, palettes.WINDOW_GLOW, None]
            elif p.particle_type == "heart":
                colors = [palettes.HEART, palettes.HEART, None, None]
            elif p.particle_type == "dust":
                colors = [palettes.DIRT, palettes.DIRT_LIGHT, palettes.SMOKE_LIGHT, None]
            else:
                colors = [palettes.SMOKE, None, None, None]

            color = colors[min(p.color_idx, len(colors) - 1)]
            if color is not None:
                canvas.set_pixel(px, py, color)

    def to_scene_manifest(self) -> dict:
        """Return JSON-serializable scene state for the interactive web app."""
        metrics_data = {}
        if self.metrics:
            metrics_data = {
                "revenue": getattr(self.metrics, 'revenue', 0),
                "customers": getattr(self.metrics, 'customer_count', 0),
                "population": getattr(self.metrics, 'population', 0),
                "age_days": getattr(self.metrics, 'age_days', 0),
                "codebase_files": getattr(self.metrics, 'codebase_files', 0),
                "codebase_loc": getattr(self.metrics, 'codebase_loc', 0),
                "git_branch": getattr(self.metrics, 'git_branch', ""),
                "git_commits_30d": getattr(self.metrics, 'git_commits_30d', 0),
                "active_agents": getattr(self.metrics, 'active_agents', 0),
                "total_tool_calls": getattr(self.metrics, 'total_tool_calls', 0),
            }

        return {
            "type": "scene",
            "tick": self.anim_tick,
            "milestone": self._get_milestone(),
            "milestone_progress": self._get_milestone_progress(),
            "metrics": metrics_data,
            "canvas": {"width": self.canvas_w, "height": self.canvas_h},
            "buildings": [
                {
                    "x": b.x, "y": b.y, "w": b.width, "h": b.height,
                    "type": b.building_type,
                    "name": b.name or b.building_type.replace("_", " ").title(),
                    "is_hq": b.is_hq,
                    "is_district": b.is_district,
                    "is_customer": b.is_customer,
                    "customer_type": b.customer_type,
                }
                for b in self.buildings
            ],
            "agents": [
                {
                    "x": round(a.x, 1), "y": round(a.y, 1),
                    "role": a.role, "name": a.name,
                    "state": a.state, "variant": a.variant,
                    "inside_building": a.inside_building,
                    "facing_right": a.facing_right,
                }
                for a in self.agent_manager.agents
                if not a.inside_building
            ],
        }

    def tick(self):
        """Advance all animations by one tick."""
        self.anim_tick += 1
        self.agent_manager.tick()

        # Tick construction sites
        for site in self.construction_sites:
            site.tick()
            # Spawn dust at active construction sites
            if self.anim_tick % 10 == 0 and not site.complete:
                self.agent_manager.spawn_construction_dust(site.x + 3, site.y + 2)

        # Remove completed construction
        self.construction_sites = [s for s in self.construction_sites if not s.complete]

        # Tick ambient objects
        for amb in self.ambient_objects:
            amb.tick()

        # Respawn clouds/birds that go off screen
        self.ambient_objects = [
            a for a in self.ambient_objects
            if not (a.obj_type in ("cloud", "bird") and a.x > self.canvas_w + 20)
        ]
        if self.anim_tick % 40 == 0:
            rng = self._rng
            if sum(1 for a in self.ambient_objects if a.obj_type == "cloud") < 3:
                self.ambient_objects.append(AmbientObject(
                    x=-10, y=rng.uniform(0, 4),
                    obj_type="cloud", speed=rng.uniform(0.05, 0.15),
                ))

        # Smoke from HQ chimney (for Town+ milestone)
        if self.anim_tick % 8 == 0 and self.hq and self._get_revenue() >= 5000:
            self.agent_manager.spawn_particle(
                self.hq.x + self.hq.width // 2, self.hq.y - 1,
                "smoke", dx=0.1, dy=-0.4, life=15,
            )

        # Sparkles near HQ based on progress
        if self.anim_tick % 20 == 0 and self._get_milestone_progress() > 0.5:
            rng = self._rng
            if self.hq:
                self.agent_manager.spawn_particle(
                    self.hq.center_x + rng.uniform(-3, 3), self.hq.y - 1,
                    "sparkle", dy=-0.3, life=10,
                )

    def handle_action(self, action_type: str, session_id: str = ""):
        """Handle a Claude action by sending an agent to the relevant building."""
        agent = self.agent_manager.get_agent_by_session(session_id)
        if agent is None and len(self.agent_manager.agents) > 0:
            agent = self._rng.choice(self.agent_manager.agents)
        if agent is None:
            return

        target_building = None
        for b in self.buildings:
            if b.building_type == action_type:
                target_building = b
                break
        if target_building is None and self.buildings:
            target_building = self.buildings[0]
        if target_building:
            agent.send_to(
                target_building.center_x - 1,
                target_building.y + target_building.height - 1,
                work_ticks=8,
            )

    def get_building_at(self, px: int, py: int) -> Building | None:
        for b in self.buildings:
            if b.x <= px < b.x + b.width and b.y <= py < b.y + b.height:
                return b
        return None


# ── Backward compatibility alias ──
Town = Kingdom
