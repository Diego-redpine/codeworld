# CodeWorld v2 — Red Pine Kingdom Design

**Date:** February 28, 2026
**Author:** Diego + Claude

## Summary

CodeWorld evolves from a generic project visualizer into a Red Pine business growth simulator. Red Pine OS is the central kingdom. Revenue drives visual progression. Customers become buildings. AI agents are visible workers. The town grows as the business grows.

## 1. World Model

- **Red Pine is the center.** No grid system. One organic kingdom growing outward.
- **Each Red Pine customer = a building** inside the kingdom, matched to their business type (9 template families → 9 building sprites).
- **Platform subsystems = districts:**
  - Forge = codebase/dashboard
  - Market = portal/marketplace
  - Library = docs/onboarding
  - Watchtower = COO + AI agents
  - Comm Tower = unified inbox/SMS/email
- **AI agents = visible walking NPCs** — COO, Receptionist, Content Writer, Review Manager, Route Planner.
- **Future projects** (Car Buddy, etc.) = satellite settlements in surrounding wilderness.

## 2. Age Progression System

Revenue-driven continuous visual evolution. Not discrete jumps — gradual interpolation.

| Milestone | Revenue | HQ Building | Visual Style |
|-----------|---------|-------------|-------------|
| Settlement | $0 | Log cabin | Dirt paths, wooden fences, campfire |
| Village | $1,000/mo | Stone manor | Cobblestone forming, market stalls, well |
| Town | $5,000/mo | Castle | Full cobblestone, districts, wall segments |
| City | $10,000/mo | Grand castle | Paved roads, full walls, towers |
| Capital | $20,000/mo | Fortress + walls | Brick roads, wide boulevards, gardens |
| Kingdom | $30,000/mo | Fortress + spires | Advanced structures, busy districts |
| Metropolis | $100,000/mo | Castle + modern tower | Skyscrapers, lit streets, dense urban |

At any revenue value, the visual is interpolated:
- At $600/mo (60% to Village): 60% of paths are cobblestone, stone foundations appearing, cabin has construction scaffolding.
- Elements have individual `age_threshold` values and fade/build in over a range.

Construction animations visible during transitions:
- Scaffolding on upgrading buildings
- Worker NPCs building
- Dust particles
- Buildings "rise" from foundation → walls → roof

## 3. Animation & Liveliness (Pokemon Red/Blue level)

### Ambient (always running)
- Water: 4-frame shimmer cycle (400ms)
- Smoke: braille pattern particles rising from chimneys
- Flags/banners: 2-frame wave on castle/watchtower
- Trees: 2-frame canopy sway (2s cycle)
- Flowers: subtle color pulse
- Torches/lanterns: 3-frame flicker
- Birds: tiny 2px sprites flying across sky (occasional)
- Clouds: slow drift across top

### NPCs
- Walk on paths between buildings (pathfinding on path network)
- Idle: stand near buildings, turn to face different directions
- Working: arm-movement animation at target building
- Enter buildings: walk to door, disappear, reappear
- Scaled with revenue (more NPCs = more life)
- Color-coded by role (COO = blue, Receptionist = green, etc.)

### Construction
- Scaffolding sprites on upgrading buildings
- Tiny worker NPCs with hammer animation
- Dust particles at construction sites

## 4. Data Architecture

### Config (config.toml)
```toml
[redpine]
supabase_url = ""
supabase_key = ""
revenue = 0         # manual fallback
customers = 0       # manual fallback

[display]
side_mode = false
theme = "cozy"
```

### Data Flow
1. Startup: try Supabase → query businesses table
2. Every 30s: re-poll for updated counts
3. Revenue: from Stripe/billing table or manual config
4. No credentials → graceful fallback to config values
5. Claude transcripts: still from ~/.claude/projects/ (local)

### Supabase Queries
- `SELECT count(*) FROM businesses` → customer count → building count
- `SELECT business_type, name FROM businesses` → building sprites + labels
- Revenue: billing/subscriptions table or manual

## 5. Layout

### Full Mode (standalone)
- Left panel (28 cols): stats, resources, action log, building list
- Right panel (rest): town pixel art grid

### Side Mode (--side, for tmux split with Claude Code)
- No left panel — grid takes full width
- Compact 1-2 line stats bar at bottom
- Town name, POP, REV, AGE indicator

### tmux Setup
```
Claude Code (left) | CodeWorld --side (right)
```

## 6. Pixel Art Upgrade

### Bigger Sprites
- Buildings: 12×14+ pixels (was 7×8)
- Trees: 6×12 (was 3×8)
- Agents: 4×6 (was 3×4)
- HQ: 16×18+ (scales with age)

### Customer Building Types (9 families)
- Beauty → small shop with striped awning
- Restaurant → tavern with smoke
- Fitness → gym with weights in window
- Home Services → workshop with truck
- Professional → office with columns
- Creative → studio with art sign
- Education → schoolhouse with bell
- Automotive → garage with open bay
- Retail → storefront with display

### Terrain Variety
- 8+ grass variants (was 3)
- Path tiles: cracks, edges, intersections
- Water: shoreline, ripples, deep/shallow
- Seasonal decorations possible

### HQ Evolution (6 sprites)
Each hand-crafted, largest building in town:
1. Log cabin (Settlement)
2. Stone manor (Village)
3. Castle (Town)
4. Grand castle (City)
5. Fortress with walls (Capital)
6. Castle + modern tower (Metropolis)

## 7. Keybindings
- `w` — toggle world/town view
- `r` — refresh data
- `q` — quit
- Arrow keys — navigate world map
- Enter — select town from world view

## 8. Dependencies
- Python 3.11+
- Textual 8.0+
- supabase-py (optional, for live data)
- No other external deps

## 9. Revenue Milestones (from Red Pine Brain)
- Survival: 8 customers = ~$400/mo
- Freedom: 30 customers = ~$1,500/mo
- Scale: 100 customers = ~$5,000/mo
- These map directly to Settlement → Village → Town transitions
