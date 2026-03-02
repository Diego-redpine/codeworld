# CodeWorld v2 — Red Pine Kingdom Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Transform CodeWorld from a generic project visualizer into a Red Pine business growth simulator where the kingdom grows as the business grows.

**Architecture:** Single Textual app with Supabase data layer (graceful fallback to config). Revenue drives age progression (7 milestones). Each customer = a building. AI agents are visible NPCs. All sprites upgraded to larger, more detailed pixel art.

**Tech Stack:** Python 3.14, Textual 8.0, supabase-py (optional), half-block Unicode rendering

**Parallelization Note:** Tasks 1-4 are independent and can run simultaneously. Task 5 depends on 1-4. Task 6 depends on 5.

---

### Task 1: Data Layer — RedPineMetrics + Supabase Connection

**Files:**
- Rewrite: `towns/metrics.py`
- Modify: `config.toml`
- Create: `towns/supabase_client.py`

**What to build:**

Replace `ProjectMetrics` with `RedPineMetrics`:
```python
@dataclass
class CustomerRecord:
    business_id: str
    business_type: str  # "beauty", "restaurant", "fitness", etc.
    name: str
    status: str  # "active", "inactive"
    created_at: str

@dataclass
class RedPineMetrics:
    revenue: float = 0.0          # monthly recurring revenue
    customer_count: int = 0
    customers: list[CustomerRecord] = field(default_factory=list)
    active_agents: int = 0        # AI agent subscriptions
    total_tool_calls: int = 0     # from Claude transcripts
    codebase_files: int = 0       # from redpine-os scan
    codebase_loc: int = 0
    git_commits_30d: int = 0
    git_branch: str = ""
    age_days: int = 0

    @property
    def age_milestone(self) -> str: ...  # Settlement/Village/Town/etc.

    @property
    def age_progress(self) -> float: ...  # 0.0-1.0 within current milestone

    @property
    def population(self) -> int: ...  # customers + agents + base
```

Age milestone calculation:
```python
MILESTONES = [
    (0, "Settlement"), (1000, "Village"), (5000, "Town"),
    (10000, "City"), (20000, "Capital"), (30000, "Kingdom"),
    (100000, "Metropolis"),
]
```

`age_progress` returns 0.0-1.0 showing how far between current and next milestone. At $600, that's 0.6 progress from Settlement→Village.

Create `towns/supabase_client.py`:
```python
class RedPineDataSource:
    """Fetches Red Pine business data from Supabase with local fallback."""

    def __init__(self, url: str | None, key: str | None, fallback: dict):
        # If url/key provided, connect. Otherwise use fallback dict.

    async def fetch_metrics(self) -> RedPineMetrics:
        # Query Supabase for customers and revenue
        # Fall back to config values if connection fails

    def _query_customers(self) -> list[CustomerRecord]: ...
    def _query_revenue(self) -> float: ...
```

Keep `scan_project()` but simplify — only used for Red Pine's own codebase stats (files, LOC, git). Remove folder metrics, tier system, population formula.

Update `config.toml`:
```toml
[redpine]
supabase_url = ""
supabase_key = ""
project_path = "/Users/Diego21/redpine-os"
revenue = 0
customers = 0

[display]
side_mode = false
theme = "cozy"
```

**Acceptance:** `RedPineMetrics` correctly calculates `age_milestone` and `age_progress` for any revenue value. Supabase client falls back to config when no credentials.

---

### Task 2: Pixel Art — Bigger Sprites + 9 Customer Buildings + 6 HQ Variants

**Files:**
- Rewrite: `assets/sprites.py` (expand significantly)
- Modify: `assets/palettes.py` (add colors)

**What to build:**

Add new palette colors for customer building types and NPC roles:
```python
# Customer building accents
SALON_PINK = (228, 148, 178)
SALON_STRIPE = (178, 68, 108)
RESTAURANT_WARM = (198, 128, 52)
GYM_BLUE = (52, 128, 198)
# ... etc for 9 types

# NPC role colors
COO_CAPE = (52, 82, 168)       # blue cape/accent
RECEPTIONIST_APRON = (52, 148, 78)  # green
CONTENT_SHIRT = (198, 128, 52)      # orange
REVIEW_VEST = (178, 52, 52)         # red
ROUTE_SASH = (128, 52, 168)         # purple
```

Create 9 customer building sprites at 10-12 wide × 10-12 tall:
- `BUILDING_BEAUTY` — striped awning (pink/white), small shop window
- `BUILDING_RESTAURANT` — warm-colored, chimney with smoke slot, outdoor tables
- `BUILDING_FITNESS` — wider, blue accent, dumbbell shapes in window
- `BUILDING_HOME_SERVICES` — workshop shape, truck parked beside (3px vehicle)
- `BUILDING_PROFESSIONAL` — columns at entrance, clean stone
- `BUILDING_CREATIVE` — asymmetric roof, paintbrush/camera sign (colored window)
- `BUILDING_EDUCATION` — bell tower, wide door, small playground area
- `BUILDING_AUTOMOTIVE` — garage with open bay door (dark interior), car shape inside
- `BUILDING_RETAIL` — large front window (display items as colored pixels)

Create 6 HQ building sprites, progressively larger:
- `HQ_CABIN` — 8×8 pixels, log cabin with chimney, simple peaked roof
- `HQ_MANOR` — 12×12 pixels, stone foundation, two stories, dormers
- `HQ_CASTLE` — 14×14 pixels, twin towers, central gate, flag on top
- `HQ_GRAND_CASTLE` — 16×16 pixels, wider castle, buttresses, multiple windows
- `HQ_FORTRESS` — 18×16 pixels, surrounding wall segments, watchtowers at corners
- `HQ_METROPOLIS` — 18×18 pixels, castle base with modern spire/tower rising from center

Enlarge existing agents from 3×4 to 4×6:
```python
def make_agent_v2(hair, shirt, role_accent):
    """Larger agent with role-identifying accent color."""
    # 4 wide × 6 tall
    idle = [
        [_, HD, HD, _],
        [SK, SH, SH, SK],
        [_, RC, RC, _],   # RC = role_accent color (cape/apron/vest)
        [_, SH, SH, _],
        [BT, _, _, BT],
        [_, _, _, _],
    ]
    # walk_1, walk_2, work_1, work_2 similarly
```

Add ambient sprites:
- `CLOUD` — 5×2 pixels, white/light gray wisps
- `BIRD_FRAMES` — 2 frames of 3×2 pixel bird
- `TORCH_FRAMES` — 3 frames of 2×4 flickering torch
- `FLAG_FRAMES` — 2 frames of 3×3 flag waving
- `SCAFFOLDING` — 6×8 pixel construction scaffolding overlay
- `CONSTRUCTION_WORKER` — agent variant with hammer

Update `BUILDING_REGISTRY` and add `BUSINESS_TYPE_TO_BUILDING`:
```python
BUSINESS_TYPE_TO_BUILDING = {
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
```

**Acceptance:** All sprites render correctly on a test canvas without row-width inconsistencies. Each business type has a visually distinct building.

---

### Task 3: Agent System — Roles, Pathfinding, Animation Upgrade

**Files:**
- Modify: `towns/agents.py`

**What to build:**

Add role system to Agent:
```python
@dataclass
class Agent:
    # ... existing fields ...
    role: str = "villager"  # "coo", "receptionist", "content_writer", "review_manager", "route_planner", "villager", "worker"

    # New: path-based movement
    path_waypoints: list[tuple[float, float]] = field(default_factory=list)
    current_waypoint: int = 0

    # New: building interaction
    inside_building: bool = False
    inside_timer: int = 0
```

Add path-based movement: agents walk along a list of waypoints (path tiles) instead of straight-line:
```python
def _move_along_path(self):
    """Follow waypoints to target."""
    if self.current_waypoint >= len(self.path_waypoints):
        self._move_toward_target()  # fallback: direct movement
        return
    wx, wy = self.path_waypoints[self.current_waypoint]
    # Move toward current waypoint, advance when reached
```

Add building entry/exit:
```python
def enter_building(self, ticks: int = 15):
    """Agent disappears into a building."""
    self.inside_building = True
    self.inside_timer = ticks

def tick(self):
    if self.inside_building:
        self.inside_timer -= 1
        if self.inside_timer <= 0:
            self.inside_building = False
        return  # don't draw while inside
    # ... rest of tick
```

Add NPC spawning by role in AgentManager:
```python
def spawn_role_agent(self, role: str, x: float, y: float) -> Agent:
    """Spawn an agent with a specific role (uses role-specific sprite)."""
```

Add construction particles to AgentManager:
```python
def spawn_construction_dust(self, x: float, y: float):
    """Spawn dust particles at a construction site."""
```

**Acceptance:** Agents walk along path waypoints. Agents have visible role distinctions. Building entry/exit works (agent disappears/reappears).

---

### Task 4: Town Rewrite — Red Pine Kingdom

**Files:**
- Rewrite: `towns/town.py`
- Delete or gut: `towns/world.py` (consolidate into town.py if needed)

**What to build:**

New `Kingdom` class replacing `Town`:
```python
class Kingdom:
    """The Red Pine kingdom — grows based on real business data."""

    def __init__(self, metrics: RedPineMetrics):
        self.metrics = metrics
        self.hq: Building | None = None
        self.customer_buildings: list[Building] = []
        self.district_buildings: list[Building] = []  # Forge, Market, Library, etc.
        self.decorations: list[tuple[int, int, Sprite]] = []
        self.path_network: list[tuple[int, int]] = []  # connected path tiles
        self.water_tiles: list[tuple[int, int]] = []
        self.agent_manager = AgentManager()
        self.construction_sites: list[ConstructionSite] = []
        self.ambient_objects: list[AmbientObject] = []  # clouds, birds, torches
```

Age-interpolated rendering:
```python
def _get_hq_sprite(self) -> Sprite:
    """Return the HQ sprite based on current revenue milestone."""
    milestone = self.metrics.age_milestone
    return HQ_SPRITES[milestone]

def _get_path_style(self) -> str:
    """Return path type based on age progress."""
    progress = self.metrics.revenue
    if progress < 500: return "dirt"
    elif progress < 1000: return "partial_cobble"  # mix of dirt and stone
    elif progress < 5000: return "cobblestone"
    elif progress < 10000: return "paved"
    else: return "brick"
```

Customer building placement:
```python
def _place_customer_buildings(self):
    """Place a building for each Red Pine customer."""
    for customer in self.metrics.customers:
        btype = BUSINESS_TYPE_TO_BUILDING.get(customer.business_type, "hut")
        sprite = CUSTOMER_BUILDING_REGISTRY[btype]["sprite"]
        # Place in expanding ring around HQ
        # Older customers closer to center, newer ones on periphery
```

Construction system:
```python
@dataclass
class ConstructionSite:
    x: int
    y: int
    target_sprite: Sprite
    progress: float = 0.0  # 0.0 = foundation, 1.0 = complete

    def get_current_sprite(self) -> Sprite:
        if self.progress < 0.3: return FOUNDATION_SPRITE
        elif self.progress < 0.7: return SCAFFOLDING_SPRITE
        else: return self.target_sprite  # mostly done
```

Layer rendering order:
1. Ground (grass, varies by age)
2. Water
3. Paths (type depends on age)
4. Decorations (trees, flowers — more variety with age)
5. Construction sites (scaffolding + workers)
6. Buildings (HQ + districts + customer buildings)
7. Agents (NPCs walking)
8. Ambient (clouds, birds at top)
9. Particles (smoke, sparkle, dust)
10. Day/night tint

District buildings (always present, represent Red Pine subsystems):
```python
DISTRICTS = {
    "forge": {"name": "The Forge", "desc": "Dashboard & Codebase"},
    "market": {"name": "Market Square", "desc": "Portal & Marketplace"},
    "library": {"name": "Grand Library", "desc": "Docs & Onboarding"},
    "watchtower": {"name": "Watchtower", "desc": "COO & AI Agents"},
    "comm_tower": {"name": "Signal Tower", "desc": "Communications"},
}
```

Ambient animation system:
```python
@dataclass
class AmbientObject:
    x: float
    y: float
    obj_type: str  # "cloud", "bird", "torch", "flag"
    frame: int = 0
    speed: float = 0.2

    def tick(self): ...
    def get_sprite(self) -> Sprite: ...
```

**Acceptance:** Kingdom renders with HQ at center, district buildings around it, customer buildings in expanding rings. Age milestone visually changes terrain and HQ sprite. Ambient animations run continuously.

---

### Task 5: App Integration — Wire Everything Together

**Files:**
- Modify: `main.py`
- Modify: `towns/transcript_watcher.py` (simplify)

**Depends on:** Tasks 1-4

**What to build:**

Replace `CodeWorldApp` internals:
- Remove `_discover_and_load_projects()` → replace with `_init_kingdom()`
- Replace `self.towns` dict with single `self.kingdom: Kingdom`
- Add `self.data_source: RedPineDataSource` for Supabase polling
- Update timer callbacks to poll Supabase every 30s

Update `StatsPanel` for Red Pine metrics:
```python
# Show: Revenue, Customers, Age, Population, AI Agents active
# Resource bars: Revenue progress to next milestone, customer growth
# Activity log: recent Claude actions + Supabase events
```

Simplify `transcript_watcher.py`:
- Only watch Red Pine's own Claude project dir
- Keep tool action → building routing (still useful for Claude agent visualization)
- Remove multi-project discovery

Add `--side` mode:
```python
# In CSS, when side_mode:
#   Hide stats-panel
#   Show compact bottom bar instead
#   Town grid takes full width
```

Update `config.toml` loading:
```python
def load_config():
    config = tomllib.load(...)
    redpine = config.get("redpine", {})
    return {
        "supabase_url": redpine.get("supabase_url", ""),
        "supabase_key": redpine.get("supabase_key", ""),
        "project_path": redpine.get("project_path", ""),
        "revenue_fallback": redpine.get("revenue", 0),
        "customers_fallback": redpine.get("customers", 0),
        "side_mode": config.get("display", {}).get("side_mode", False),
    }
```

**Acceptance:** App starts, shows Red Pine kingdom, stats panel shows revenue/age/customers. `--side` flag works for tmux layout.

---

### Task 6: Polish — Test, Tune, Visual Quality

**Files:** All files (bug fixes, visual tweaks)

**Depends on:** Task 5

**What to do:**
- Run the full app and verify all animations play
- Tune animation speeds (water shimmer, smoke rise, agent walk speed)
- Verify age progression looks correct at various revenue values
- Test Supabase fallback (run without credentials)
- Test `--side` mode at narrow widths (40-60 cols)
- Fix any sprite rendering artifacts
- Ensure day/night cycle looks good at all hours
- Verify construction animations trigger on age transitions
- Check agent pathfinding doesn't walk through buildings
- Performance: ensure 400ms frame budget is met even with many agents/particles

---

## Dependency Graph

```
Task 1 (Data Layer) ──┐
Task 2 (Sprites)   ───┤
Task 3 (Agents)    ───┼── Task 5 (Integration) ── Task 6 (Polish)
Task 4 (Kingdom)   ───┘
```

Tasks 1-4 are fully independent. Task 5 merges them. Task 6 is final polish.

## Estimated Effort

| Task | Lines Changed | Complexity |
|------|---------------|-----------|
| 1. Data Layer | ~300 new/rewritten | Medium |
| 2. Sprites | ~600 new | High (art design) |
| 3. Agents | ~100 modified | Medium |
| 4. Kingdom | ~500 rewritten | High (core logic) |
| 5. Integration | ~200 modified | Medium |
| 6. Polish | ~100 tweaks | Low |
| **Total** | **~1,800** | |
