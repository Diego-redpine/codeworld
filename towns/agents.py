"""Agent sprite animation and movement system.

Agents are little pixel-art characters that walk between buildings
in the town when Claude performs tool calls.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field

try:
    from assets.sprites import AGENT_VARIANTS, AGENT_V2_VARIANTS, ROLE_TO_VARIANT, Sprite
except ImportError:
    from assets.sprites import AGENT_VARIANTS, Sprite
    AGENT_V2_VARIANTS = AGENT_VARIANTS
    ROLE_TO_VARIANT = {}


@dataclass
class Agent:
    """A walking agent sprite in the town."""

    # Position in pixel coordinates
    x: float
    y: float

    # Target position (building they're walking to)
    target_x: float = 0
    target_y: float = 0

    # State
    state: str = "idle"  # "idle", "walking", "working"
    work_timer: int = 0  # ticks remaining for work animation
    idle_timer: int = 0  # ticks before picking a new destination

    # Appearance
    variant: int = 0     # index into AGENT_VARIANTS
    facing_right: bool = True
    use_v2_sprites: bool = True  # use larger v2 sprites

    # Animation
    anim_frame: int = 0
    anim_tick: int = 0

    # Speed (pixels per tick)
    speed: float = 0.8

    # Identity
    session_id: str = ""
    name: str = "Agent"

    # v2: Role system
    role: str = "villager"  # "coo", "receptionist", "content_writer", "review_manager", "route_planner", "villager", "worker"

    # v2: Path-based movement
    path_waypoints: list[tuple[float, float]] = field(default_factory=list)
    current_waypoint: int = 0

    # v2: Building interaction
    inside_building: bool = False
    inside_timer: int = 0

    def get_sprite(self) -> Sprite:
        """Get the current animation frame sprite."""
        if self.use_v2_sprites:
            variants = AGENT_V2_VARIANTS
            # Use role-specific variant if available
            role_idx = ROLE_TO_VARIANT.get(self.role, self.variant % len(variants))
            sprites = variants[role_idx % len(variants)]
        else:
            sprites = AGENT_VARIANTS[self.variant % len(AGENT_VARIANTS)]

        if self.state == "walking":
            frames = sprites["walk"]
        elif self.state == "working":
            frames = sprites["work"]
        else:
            frames = sprites["idle"]
        return frames[self.anim_frame % len(frames)]

    def tick(self):
        """Update agent state for one animation tick."""
        # Building interaction — agent is inside, count down
        if self.inside_building:
            self.inside_timer -= 1
            if self.inside_timer <= 0:
                self.inside_building = False
            return  # don't move or animate while inside

        self.anim_tick += 1

        # Advance animation frame every 3 ticks
        if self.anim_tick % 3 == 0:
            self.anim_frame += 1

        if self.state == "walking":
            if self.path_waypoints and self.current_waypoint < len(self.path_waypoints):
                self._move_along_path()
            else:
                self._move_toward_target()
        elif self.state == "working":
            self.work_timer -= 1
            if self.work_timer <= 0:
                self.state = "idle"
                self.idle_timer = random.randint(5, 20)
        elif self.state == "idle":
            self.idle_timer -= 1
            if self.idle_timer <= 0:
                # Wander randomly nearby, clamped to reasonable bounds
                self.target_x = max(2, min(200, self.x + random.uniform(-20, 20)))
                self.target_y = max(2, min(100, self.y + random.uniform(-10, 10)))
                self.path_waypoints.clear()
                self.current_waypoint = 0
                self.state = "walking"

    def _move_along_path(self):
        """Follow waypoints to target."""
        wx, wy = self.path_waypoints[self.current_waypoint]
        dx = wx - self.x
        dy = wy - self.y
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist < self.speed:
            # Reached current waypoint
            self.x = wx
            self.y = wy
            self.current_waypoint += 1
            self.facing_right = dx > 0 if abs(dx) > 0.1 else self.facing_right

            # Check if all waypoints exhausted
            if self.current_waypoint >= len(self.path_waypoints):
                self.path_waypoints.clear()
                self.current_waypoint = 0
                # Now move directly to final target
                self._move_toward_target()
            return

        # Move toward current waypoint
        nx, ny = dx / dist, dy / dist
        self.x += nx * self.speed
        self.y += ny * self.speed
        self.facing_right = dx > 0

    def _move_toward_target(self):
        """Move toward the target position."""
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist < self.speed:
            # Arrived at target
            self.x = self.target_x
            self.y = self.target_y
            if self.work_timer > 0:
                self.state = "working"
            else:
                self.state = "idle"
                self.idle_timer = random.randint(5, 20)
            return

        # Normalize and move
        nx, ny = dx / dist, dy / dist
        self.x += nx * self.speed
        self.y += ny * self.speed
        self.facing_right = dx > 0

    def send_to(self, x: float, y: float, work_ticks: int = 8, waypoints: list[tuple[float, float]] | None = None):
        """Send the agent to a building position to do work."""
        self.target_x = x
        self.target_y = y
        self.work_timer = work_ticks
        self.state = "walking"
        if waypoints:
            self.path_waypoints = list(waypoints)
            self.current_waypoint = 0
        else:
            self.path_waypoints.clear()
            self.current_waypoint = 0

    def enter_building(self, ticks: int = 15):
        """Agent disappears into a building for N ticks."""
        self.inside_building = True
        self.inside_timer = ticks


@dataclass
class Particle:
    """A small animated particle effect (smoke, sparkle, heart, dust)."""
    x: float
    y: float
    dx: float = 0       # velocity x
    dy: float = -0.3    # velocity y (default: float upward)
    life: int = 12       # ticks before removal
    max_life: int = 12
    particle_type: str = "smoke"  # "smoke", "sparkle", "heart", "dust"
    color_idx: int = 0

    def tick(self):
        """Update particle position and lifetime."""
        self.x += self.dx
        self.y += self.dy
        self.life -= 1
        # Change color as it ages
        progress = 1.0 - (self.life / self.max_life)
        self.color_idx = min(3, int(progress * 4))


class AgentManager:
    """Manages all agents and particles in a town."""

    def __init__(self):
        self.agents: list[Agent] = []
        self.particles: list[Particle] = []
        self._next_variant = 0

    def spawn_agent(self, x: float, y: float, session_id: str = "", use_v2: bool = True) -> Agent:
        """Create a new agent at a position."""
        agent = Agent(
            x=x, y=y,
            variant=self._next_variant,
            session_id=session_id,
            name=f"Agent {len(self.agents) + 1}",
            idle_timer=random.randint(3, 10),
            use_v2_sprites=use_v2,
        )
        self._next_variant = (self._next_variant + 1) % max(len(AGENT_VARIANTS), len(AGENT_V2_VARIANTS))
        self.agents.append(agent)
        return agent

    def spawn_role_agent(self, role: str, x: float, y: float) -> Agent:
        """Spawn an agent with a specific role (uses role-specific sprite)."""
        variant_idx = ROLE_TO_VARIANT.get(role, self._next_variant)
        agent = Agent(
            x=x, y=y,
            variant=variant_idx,
            role=role,
            name=f"{role.replace('_', ' ').title()}",
            idle_timer=random.randint(3, 10),
            use_v2_sprites=True,
        )
        self.agents.append(agent)
        return agent

    def spawn_particle(
        self, x: float, y: float, particle_type: str = "smoke",
        dx: float = 0, dy: float = -0.3, life: int = 12,
    ) -> Particle:
        """Create a new particle at a position."""
        p = Particle(
            x=x + random.uniform(-0.5, 0.5),
            y=y,
            dx=dx + random.uniform(-0.1, 0.1),
            dy=dy,
            life=life,
            max_life=life,
            particle_type=particle_type,
        )
        self.particles.append(p)
        return p

    def spawn_construction_dust(self, x: float, y: float):
        """Spawn dust particles at a construction site."""
        for _ in range(random.randint(3, 5)):
            self.spawn_particle(
                x + random.uniform(-2, 2),
                y + random.uniform(-1, 1),
                particle_type="dust",
                dx=random.uniform(-0.3, 0.3),
                dy=random.uniform(-0.5, -0.1),
                life=random.randint(6, 12),
            )

    def tick(self):
        """Update all agents and particles."""
        for agent in self.agents:
            agent.tick()

        for particle in self.particles:
            particle.tick()

        # Remove dead particles
        self.particles = [p for p in self.particles if p.life > 0]

    def get_agent_by_session(self, session_id: str) -> Agent | None:
        """Find an agent by its Claude session ID."""
        for agent in self.agents:
            if agent.session_id == session_id:
                return agent
        return None

    def get_agent_by_role(self, role: str) -> Agent | None:
        """Find an agent by its role."""
        for agent in self.agents:
            if agent.role == role:
                return agent
        return None

    def ensure_min_agents(self, count: int, center_x: float, center_y: float):
        """Ensure at least N agents exist (for visual liveliness)."""
        while len(self.agents) < count:
            x = center_x + random.uniform(-15, 15)
            y = center_y + random.uniform(-8, 8)
            self.spawn_agent(x, y)
