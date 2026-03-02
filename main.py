#!/usr/bin/env python3
"""CodeWorld v2 — Red Pine Kingdom Visualizer.

Watch the Red Pine kingdom grow as the business grows.
Revenue drives age progression. Customers become buildings.
AI agents are visible NPCs walking between districts.
"""
from __future__ import annotations

import argparse
import sys
import os
from pathlib import Path
from datetime import datetime

# Ensure the codeworld package root is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from textual.app import App, ComposeResult
from textual.widgets import Static, Footer
from textual.containers import Horizontal, Container
from textual.reactive import reactive
from textual.binding import Binding

from rich.text import Text
from rich.style import Style

from rendering.canvas import PixelCanvas
from rendering.web_renderer import WebRenderer
from towns.town import Kingdom
from towns.metrics import RedPineMetrics, scan_codebase, get_git_info
from towns.supabase_client import RedPineDataSource, load_env_from_project
from towns.transcript_watcher import TranscriptWatcher
from towns.agents import AgentManager
from assets import palettes


# ═══════════════════════════════════════════════════════════
# WIDGETS
# ═══════════════════════════════════════════════════════════

class KingdomGridWidget(Static):
    """The main pixel-art rendering surface for the kingdom."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kingdom: Kingdom | None = None
        self.canvas: PixelCanvas | None = None
        self.tick_count = 0

    def set_kingdom(self, kingdom: Kingdom):
        self.kingdom = kingdom
        self.canvas = None

    def on_resize(self, event):
        self.canvas = None

    def update_frame(self, tick: int):
        self.tick_count = tick
        if self.kingdom:
            self.kingdom.tick()
        self.refresh()

    def render(self):
        if self.kingdom is None:
            return Text("No kingdom loaded", style="dim")

        size = self.size
        if size.width < 4 or size.height < 2:
            return Text("")

        pw = size.width
        ph = size.height * 2  # half-block = 2 pixels per row
        if self.canvas is None or self.canvas.width != pw or self.canvas.height != ph:
            self.canvas = PixelCanvas(pw, ph, bg=palettes.GRASS_DARK)
            self.kingdom._layout_dirty = True

        self.kingdom.draw(self.canvas, tick=self.tick_count)
        return self.canvas.render()


class StatsPanel(Static):
    """Left sidebar showing Red Pine kingdom stats."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.metrics: RedPineMetrics | None = None
        self.actions: list[str] = []
        self.tool_calls: int = 0
        self.active_agents: int = 0

    def update_data(
        self,
        metrics: RedPineMetrics | None = None,
        actions: list[str] | None = None,
        tool_calls: int = 0,
        active_agents: int = 0,
    ):
        if metrics is not None:
            self.metrics = metrics
        if actions is not None:
            self.actions = actions[-7:]
        self.tool_calls = tool_calls
        self.active_agents = active_agents
        self.refresh()

    def render(self):
        t = Text()

        # ── Header ──
        t.append("  ░▒▓", Style(color="#4a7c3f"))
        t.append(" RED PINE ", Style(color="#e8c84a", bold=True))
        t.append("▓▒░\n", Style(color="#4a7c3f"))
        t.append("  ─────────────────\n", Style(color="#3c3c50"))

        if self.metrics is None:
            t.append("\n  Loading...\n", Style(color="#808090"))
            return t

        m = self.metrics

        # ── Age & Milestone ──
        t.append(f"\n  {m.age_milestone}\n", Style(color="#64b4ff", bold=True))

        # Revenue
        revenue_str = f"${m.revenue:,.0f}/mo"
        t.append(f"  REV {revenue_str}\n", Style(color="#e8c84a", bold=True))

        # Progress bar to next milestone
        progress_bar = self._bar(int(m.age_progress * 100), 100, width=10)
        t.append(f"  {progress_bar} {int(m.age_progress * 100)}%\n", Style(color="#5a9c4e"))

        t.append("  ─────────────────\n", Style(color="#3c3c50"))

        # ── Customers ──
        t.append("\n  KINGDOM\n", Style(color="#c0c0d0", bold=True))

        t.append(f"  CUSTOMERS ", Style(color="#c0c0d0"))
        t.append(f"{m.customer_count}\n", Style(color="#64b4ff", bold=True))

        t.append(f"  POP ", Style(color="#c0c0d0"))
        t.append(f"{m.population}\n", Style(color="#64b4ff"))

        t.append(f"  AI AGENTS ", Style(color="#c0c0d0"))
        t.append(f"{self.active_agents}\n", Style(color="#e8c84a"))

        t.append("  ─────────────────\n", Style(color="#3c3c50"))

        # ── Codebase ──
        t.append("\n  CODEBASE\n", Style(color="#c0c0d0", bold=True))

        bar_f = self._bar(m.codebase_files, 1000)
        t.append("  ", Style())
        t.append("█", Style(color="#8b6914"))
        t.append(f" Files {m.codebase_files:>5}", Style(color="#c8b070"))
        t.append(f" {bar_f}\n", Style(color="#8b6914"))

        bar_l = self._bar(m.codebase_loc, 50000)
        t.append("  ", Style())
        t.append("█", Style(color="#7a7a7a"))
        t.append(f" LOC  {m.codebase_loc:>6}", Style(color="#a0a0a8"))
        t.append(f" {bar_l}\n", Style(color="#7a7a7a"))

        if m.git_branch:
            t.append(f"  branch: {m.git_branch}\n", Style(color="#5a9c4e"))

        bar_c = self._bar(m.git_commits_30d, 100)
        t.append("  ", Style())
        t.append("█", Style(color="#daa520"))
        t.append(f" Commits {m.git_commits_30d:>3}", Style(color="#e8c84a"))
        t.append(f" {bar_c}\n", Style(color="#daa520"))

        t.append("  ─────────────────\n", Style(color="#3c3c50"))

        # ── Tool Calls ──
        bar_t = self._bar(self.tool_calls, 500)
        t.append(f"\n  TOOLS {self.tool_calls:>5}", Style(color="#c0c0d0"))
        t.append(f" {bar_t}\n", Style(color="#daa520"))

        t.append("  ─────────────────\n", Style(color="#3c3c50"))

        # ── Activity Log ──
        t.append("\n  ACTIVITY\n", Style(color="#c0c0d0", bold=True))
        if self.actions:
            for action in self.actions[-5:]:
                if len(action) > 26:
                    action = action[:23] + "..."
                t.append(f"  > {action}\n", Style(color="#808090"))
        else:
            t.append("  > Quiet...\n", Style(color="#505060"))

        t.append("  ─────────────────\n", Style(color="#3c3c50"))

        # ── Time ──
        now = datetime.now()
        hour = now.hour
        if 6 <= hour < 12:
            tod = "Morning"
        elif 12 <= hour < 17:
            tod = "Afternoon"
        elif 17 <= hour < 21:
            tod = "Evening"
        else:
            tod = "Night"
        t.append(f"\n  {now.strftime('%H:%M')} {tod}\n", Style(color="#505060"))

        return t

    @staticmethod
    def _bar(value: int, max_val: int, width: int = 6) -> str:
        ratio = min(1.0, value / max_val) if max_val > 0 else 0
        filled = int(ratio * width)
        return "█" * filled + "░" * (width - filled)


class CompactStatsBar(Static):
    """Compact 1-line stats bar for --side mode."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.metrics: RedPineMetrics | None = None

    def update_data(self, metrics: RedPineMetrics | None = None):
        if metrics is not None:
            self.metrics = metrics
        self.refresh()

    def render(self):
        if self.metrics is None:
            return Text("  Red Pine Kingdom  |  Loading...", style="dim")

        m = self.metrics
        t = Text()
        t.append(" RED PINE ", Style(color="#e8c84a", bold=True))
        t.append(f" {m.age_milestone} ", Style(color="#64b4ff"))
        t.append(f" ${m.revenue:,.0f}/mo ", Style(color="#5a9c4e"))
        t.append(f" POP {m.population} ", Style(color="#808090"))
        t.append(f" CUST {m.customer_count} ", Style(color="#c0c0d0"))
        return t


# ═══════════════════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════════════════

class CodeWorldApp(App):
    """CodeWorld v2 — Red Pine Kingdom Visualizer."""

    CSS = """
    Screen {
        background: #10101a;
    }

    #main-container {
        width: 100%;
        height: 100%;
    }

    #stats-panel {
        width: 28;
        min-width: 24;
        max-width: 32;
        background: #10101a;
        border-right: solid #3c3c50;
        padding: 0;
        overflow-y: auto;
    }

    #kingdom-grid {
        width: 1fr;
        height: 100%;
        background: #0a0a14;
    }

    #kingdom-view {
        width: 100%;
        height: 100%;
    }

    #compact-stats {
        height: 1;
        background: #10101a;
        border-top: solid #3c3c50;
        display: none;
    }

    Footer {
        background: #10101a;
        color: #808090;
    }

    .side-mode #stats-panel {
        display: none;
    }

    .side-mode #compact-stats {
        display: block;
    }
    """

    BINDINGS = [
        Binding("r", "refresh_metrics", "Refresh", show=True),
        Binding("q", "quit", "Quit", show=True),
    ]

    def __init__(
        self,
        config: dict | None = None,
        side_mode: bool = False,
    ):
        super().__init__()
        self._config = config or {}
        self._side_mode = side_mode

        # Red Pine data
        self.kingdom: Kingdom | None = None
        self.data_source: RedPineDataSource | None = None
        self.watcher: TranscriptWatcher | None = None
        self.web_renderer: WebRenderer | None = None
        self.tick_count = 0

    def compose(self) -> ComposeResult:
        with Horizontal(id="main-container"):
            yield StatsPanel(id="stats-panel")
            with Container(id="kingdom-view"):
                yield KingdomGridWidget(id="kingdom-grid")
        yield CompactStatsBar(id="compact-stats")
        yield Footer()

    def on_mount(self):
        """Initialize kingdom and start timers."""
        if self._side_mode:
            self.add_class("side-mode")

        self._init_kingdom()

        # Animation timer (500ms — smoother at this rendering load)
        self.set_interval(0.5, self._tick_animation)

        # Metrics polling timer (30s for Supabase, 5s for codebase)
        self.set_interval(30.0, self._tick_supabase)
        self.set_interval(5.0, self._tick_codebase)

        # Transcript polling timer (2 seconds)
        self.set_interval(2.0, self._tick_transcripts)

        # Browser-based pixel renderer
        web_cfg = self._config.get("web", {})
        if web_cfg.get("enabled", True):
            port = int(web_cfg.get("port", 8765))
            open_browser = web_cfg.get("open_browser", True)
            self.web_renderer = WebRenderer(port=port)
            self.web_renderer.start(open_browser=open_browser)

    def _init_kingdom(self):
        """Initialize the Red Pine kingdom from config + Supabase."""
        redpine = self._config.get("redpine", {})

        # Resolve Supabase credentials: explicit config > auto-discover from project .env
        sb_url = redpine.get("supabase_url") or None
        sb_key = redpine.get("supabase_key") or None

        if not sb_url or not sb_key:
            project_path = redpine.get("project_path", "")
            if project_path and Path(project_path).exists():
                discovered = load_env_from_project(project_path)
                if not sb_url and "url" in discovered:
                    sb_url = discovered["url"]
                if not sb_key and "key" in discovered:
                    sb_key = discovered["key"]

        # Create Supabase data source
        self.data_source = RedPineDataSource(
            url=sb_url,
            key=sb_key,
            fallback={
                "revenue": redpine.get("revenue", 0),
                "customers": redpine.get("customers", 0),
            },
        )

        # Fetch initial metrics
        metrics = self.data_source.fetch_metrics_sync()

        # Scan Red Pine codebase if path provided
        project_path = redpine.get("project_path", "")
        if project_path and Path(project_path).exists():
            codebase = scan_codebase(project_path)
            metrics.codebase_files = codebase["codebase_files"]
            metrics.codebase_loc = codebase["codebase_loc"]

            git = get_git_info(project_path)
            metrics.git_branch = git.get("branch", "")
            metrics.git_commits_30d = git.get("commits_30d", 0)

            # Watch transcripts for this project
            self.watcher = TranscriptWatcher(project_path)

        # Create kingdom
        self.kingdom = Kingdom(metrics=metrics)
        self.kingdom.name = "Red Pine Kingdom"

        # Set on widget
        grid = self.query_one("#kingdom-grid", KingdomGridWidget)
        grid.set_kingdom(self.kingdom)

        self._update_stats()

    def _update_stats(self):
        """Update the stats panel with current metrics."""
        if not self.kingdom:
            return

        recent = []
        tool_calls = 0
        active = 0
        if self.watcher:
            recent = [a.description for a in self.watcher.get_recent_actions(7)]
            tool_calls = self.watcher.total_tool_calls
            active = self.watcher.active_agent_count

        if self._side_mode:
            bar = self.query_one("#compact-stats", CompactStatsBar)
            bar.update_data(metrics=self.kingdom.metrics)
        else:
            panel = self.query_one("#stats-panel", StatsPanel)
            panel.update_data(
                metrics=self.kingdom.metrics,
                actions=recent,
                tool_calls=tool_calls,
                active_agents=active,
            )

    def _tick_animation(self):
        """Animation tick — 500ms."""
        self.tick_count += 1
        if self.kingdom:
            self.kingdom.tick()
        try:
            grid = self.query_one("#kingdom-grid", KingdomGridWidget)
            grid.update_frame(self.tick_count)
            # Stream frame to browser renderer
            if self.web_renderer and grid.canvas:
                self.web_renderer.send_frame(grid.canvas.to_rgb_bytes())
                if self.kingdom:
                    self.web_renderer.send_scene(self.kingdom.to_scene_manifest())
        except Exception:
            pass  # widget may be gone during teardown

    def _tick_supabase(self):
        """Poll Supabase for updated customer/revenue data (every 30s)."""
        if not self.data_source or not self.kingdom:
            return

        new_metrics = self.data_source.fetch_metrics_sync()

        # Preserve codebase stats from last scan
        old = self.kingdom.metrics
        if old and hasattr(old, 'codebase_files'):
            new_metrics.codebase_files = old.codebase_files
            new_metrics.codebase_loc = old.codebase_loc
            new_metrics.git_branch = old.git_branch
            new_metrics.git_commits_30d = old.git_commits_30d

        self.kingdom.update_metrics(new_metrics)
        self._update_stats()

    def _tick_codebase(self):
        """Poll codebase for file/LOC stats (every 5s)."""
        if not self.kingdom or not self.kingdom.metrics:
            return

        redpine = self._config.get("redpine", {})
        project_path = redpine.get("project_path", "")
        if not project_path or not Path(project_path).exists():
            return

        codebase = scan_codebase(project_path)
        self.kingdom.metrics.codebase_files = codebase["codebase_files"]
        self.kingdom.metrics.codebase_loc = codebase["codebase_loc"]

        git = get_git_info(project_path)
        self.kingdom.metrics.git_branch = git.get("branch", "")
        self.kingdom.metrics.git_commits_30d = git.get("commits_30d", 0)

        self._update_stats()

    def _tick_transcripts(self):
        """Transcript polling — every 2 seconds."""
        if not self.watcher or not self.kingdom:
            return

        new_actions = self.watcher.poll()
        for action in new_actions:
            self.kingdom.handle_action(
                action.action_type,
                session_id=action.session_id,
            )

        if self.kingdom.metrics:
            self.kingdom.metrics.total_tool_calls = self.watcher.total_tool_calls
            self.kingdom.metrics.active_agents = self.watcher.active_agent_count

        self._update_stats()

    def on_unmount(self):
        """Clean up the web renderer on exit."""
        if self.web_renderer:
            self.web_renderer.stop()

    # ── Actions ──

    def action_refresh_metrics(self):
        self._tick_supabase()
        self._tick_codebase()
        self.notify("Metrics refreshed", timeout=2)


# ═══════════════════════════════════════════════════════════
# CLI ENTRY POINT
# ═══════════════════════════════════════════════════════════

def load_config() -> dict:
    """Load config.toml if it exists."""
    config_path = Path(__file__).parent / "config.toml"
    if config_path.exists():
        try:
            import tomllib
            with open(config_path, "rb") as f:
                return tomllib.load(f)
        except Exception:
            pass
    return {}


def run_headless(config: dict, revenue_override=None, customers_override=None):
    """Run Kingdom + WebRenderer without Textual TUI.

    Used by the web app and VS Code extension.
    """
    import asyncio
    import signal
    import time

    redpine = config.get("redpine", {})

    # Apply overrides
    if revenue_override is not None:
        redpine["revenue"] = revenue_override
    if customers_override is not None:
        redpine["customers"] = customers_override

    # Resolve Supabase credentials
    sb_url = redpine.get("supabase_url") or None
    sb_key = redpine.get("supabase_key") or None

    if not sb_url or not sb_key:
        project_path = redpine.get("project_path", "")
        if project_path and Path(project_path).exists():
            discovered = load_env_from_project(project_path)
            if not sb_url and "url" in discovered:
                sb_url = discovered["url"]
            if not sb_key and "key" in discovered:
                sb_key = discovered["key"]

    # Create data source
    data_source = RedPineDataSource(
        url=sb_url,
        key=sb_key,
        fallback={
            "revenue": redpine.get("revenue", 0),
            "customers": redpine.get("customers", 0),
        },
    )

    # Fetch initial metrics (use fallback first, then async update from Supabase)
    from towns.metrics import RedPineMetrics
    metrics = RedPineMetrics()
    metrics.revenue = redpine.get("revenue", 0)
    metrics.customer_count = redpine.get("customers", 0)

    # Apply CLI overrides
    if revenue_override is not None:
        metrics.revenue = revenue_override
    if customers_override is not None:
        metrics.customer_count = customers_override

    # Scan codebase (defer heavy git scan to background thread)
    project_path = redpine.get("project_path", "")
    watcher = None
    if project_path and Path(project_path).exists():
        watcher = TranscriptWatcher(project_path)

    # Create kingdom
    kingdom = Kingdom(metrics=metrics)
    kingdom.name = "Red Pine Kingdom"

    # Create canvas — spacious enough for 15+ buildings + forests
    canvas = PixelCanvas(256, 160)

    # Start web renderer
    web_cfg = config.get("web", {})
    port = int(web_cfg.get("port", 8765))
    host = web_cfg.get("host", "0.0.0.0")
    renderer = WebRenderer(host=host, port=port)
    renderer.start(open_browser=False)

    print(f"CodeWorld headless server running on http://{host}:{port}")
    print("Press Ctrl+C to stop")

    # Animation tick counter
    tick = 0
    running = True

    def handle_signal(sig, frame):
        nonlocal running
        running = False

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    # Timers for polling
    last_supabase = 0
    last_codebase = 0
    last_transcript = 0

    # Background I/O threads — never block the render loop
    import threading
    _pending_metrics = None
    _pending_codebase = None
    _io_lock = threading.Lock()

    def _bg_fetch_supabase():
        nonlocal _pending_metrics
        try:
            m = data_source.fetch_metrics_sync()
            with _io_lock:
                _pending_metrics = m
        except Exception:
            pass

    def _bg_scan_codebase():
        nonlocal _pending_codebase
        try:
            cb = scan_codebase(project_path)
            git = get_git_info(project_path)
            with _io_lock:
                _pending_codebase = (cb, git)
        except Exception:
            pass

    # Kick off initial fetches in background immediately
    threading.Thread(target=_bg_fetch_supabase, daemon=True).start()
    if project_path:
        threading.Thread(target=_bg_scan_codebase, daemon=True).start()

    try:
        while running:
            now = time.monotonic()

            # Animation tick
            tick += 1
            kingdom.tick()
            kingdom.draw(canvas, tick)
            renderer.send_frame(canvas.to_rgb_bytes())
            # Send scene manifest less often (every 10th frame) — it's metadata
            if tick % 10 == 0:
                renderer.send_scene(kingdom.to_scene_manifest())

            # Apply pending background results (non-blocking)
            with _io_lock:
                if _pending_metrics is not None:
                    new_metrics = _pending_metrics
                    _pending_metrics = None
                    if kingdom.metrics:
                        new_metrics.codebase_files = kingdom.metrics.codebase_files
                        new_metrics.codebase_loc = kingdom.metrics.codebase_loc
                        new_metrics.git_branch = kingdom.metrics.git_branch
                        new_metrics.git_commits_30d = kingdom.metrics.git_commits_30d
                    kingdom.update_metrics(new_metrics)
                    if revenue_override is not None:
                        kingdom.metrics.revenue = revenue_override
                    if customers_override is not None:
                        kingdom.metrics.customer_count = customers_override

                if _pending_codebase is not None:
                    cb, git = _pending_codebase
                    _pending_codebase = None
                    kingdom.metrics.codebase_files = cb["codebase_files"]
                    kingdom.metrics.codebase_loc = cb["codebase_loc"]
                    kingdom.metrics.git_branch = git.get("branch", "")
                    kingdom.metrics.git_commits_30d = git.get("commits_30d", 0)

            # Schedule background Supabase polling (30s)
            if now - last_supabase > 30:
                last_supabase = now
                threading.Thread(target=_bg_fetch_supabase, daemon=True).start()

            # Schedule background codebase scanning (60s)
            if project_path and now - last_codebase > 60:
                last_codebase = now
                threading.Thread(target=_bg_scan_codebase, daemon=True).start()

            # Transcript polling (2s — lightweight file check, OK on main thread)
            if watcher and now - last_transcript > 2:
                last_transcript = now
                try:
                    new_actions = watcher.poll()
                    for action in new_actions:
                        kingdom.handle_action(
                            action.action_type,
                            session_id=action.session_id,
                        )
                    if kingdom.metrics:
                        kingdom.metrics.total_tool_calls = watcher.total_tool_calls
                        kingdom.metrics.active_agents = watcher.active_agent_count
                except Exception:
                    pass

            time.sleep(0.05)  # Target ~10 FPS server-side, browser receives ~6
    finally:
        renderer.stop()
        print("\nCodeWorld stopped.")


def main():
    parser = argparse.ArgumentParser(
        description="CodeWorld v2 — Red Pine Kingdom Visualizer",
    )
    parser.add_argument(
        "--side", action="store_true",
        help="Compact side-pane mode for tmux splits",
    )
    parser.add_argument(
        "--headless", action="store_true",
        help="Run WebSocket server only (no terminal UI, for web app / VS Code extension)",
    )
    parser.add_argument(
        "--revenue", type=float, default=None,
        help="Override revenue value (for testing age progression)",
    )
    parser.add_argument(
        "--customers", type=int, default=None,
        help="Override customer count (for testing)",
    )
    args = parser.parse_args()

    # Load config
    config = load_config()

    # CLI overrides
    if args.revenue is not None:
        config.setdefault("redpine", {})["revenue"] = args.revenue
    if args.customers is not None:
        config.setdefault("redpine", {})["customers"] = args.customers

    if args.headless:
        run_headless(
            config,
            revenue_override=args.revenue,
            customers_override=args.customers,
        )
        return

    # Side mode from config or CLI
    side_mode = args.side or config.get("display", {}).get("side_mode", False)

    app = CodeWorldApp(
        config=config,
        side_mode=side_mode,
    )
    app.run()


if __name__ == "__main__":
    main()
