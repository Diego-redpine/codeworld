"""Watch Claude Code transcript files for live agent activity.

Transcripts are stored at ~/.claude/projects/<encoded-path>/*.jsonl
Each line is a JSON event with type, tool_name, content, etc.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class AgentAction:
    """A parsed action from a Claude transcript."""
    timestamp: str
    action_type: str       # "edit", "read", "bash", "write", "search", etc.
    target: str            # file path or command
    description: str       # human-readable summary
    session_id: str = ""
    agent_id: str = ""     # for sub-agents
    is_subagent: bool = False


# Map Claude tool names to human-readable actions and building types
TOOL_MAP = {
    "Edit": ("edited", "forge"),
    "Write": ("wrote", "forge"),
    "Read": ("read", "library"),
    "Bash": ("ran command at", "forge"),
    "Grep": ("searched", "library"),
    "Glob": ("found files in", "library"),
    "WebFetch": ("fetched from", "market"),
    "WebSearch": ("searched web at", "market"),
    "Agent": ("dispatched agent from", "tower"),
    "NotebookEdit": ("edited notebook at", "library"),
    "TodoWrite": ("updated tasks at", "tower"),
    "AskUserQuestion": ("asked question at", "tavern"),
}


def encode_project_path(project_path: str) -> str:
    """Encode a project path to match Claude's folder naming convention."""
    return project_path.replace("/", "-")


def find_claude_project_dir(project_path: str) -> Path | None:
    """Find the Claude projects directory for a given project path."""
    claude_dir = Path.home() / ".claude" / "projects"
    if not claude_dir.exists():
        return None

    encoded = encode_project_path(project_path)
    target = claude_dir / encoded
    if target.exists():
        return target
    return None


def decode_project_path(encoded_name: str) -> str:
    """Decode a Claude project folder name back to a filesystem path.

    Claude encodes paths by replacing / with -.
    e.g., -Users-Diego21-redpine-os -> /Users/Diego21/redpine-os

    Since folder names can contain hyphens, we greedily match the shortest
    segment at each level that exists as a directory, then treat the
    remainder as the final path component.
    """
    parts = encoded_name.lstrip("-").split("-")
    current = "/"
    i = 0

    while i < len(parts):
        matched = False
        for end in range(i + 1, len(parts) + 1):
            segment = "-".join(parts[i:end])
            candidate = os.path.join(current, segment)

            if end == len(parts):
                # Last possible segment — use it regardless
                current = candidate
                i = end
                matched = True
                break

            if os.path.isdir(candidate):
                current = candidate
                i = end
                matched = True
                break

        if not matched:
            current = os.path.join(current, "-".join(parts[i:]))
            break

    return current


def discover_all_projects() -> list[dict]:
    """Discover all projects from ~/.claude/projects/."""
    claude_dir = Path.home() / ".claude" / "projects"
    if not claude_dir.exists():
        return []

    projects = []
    for entry in claude_dir.iterdir():
        if entry.is_dir() and entry.name.startswith("-"):
            decoded_path = decode_project_path(entry.name)
            actual_path = Path(decoded_path)

            # Count transcript files
            jsonl_files = list(entry.glob("*.jsonl"))

            projects.append({
                "path": str(actual_path),
                "name": actual_path.name,
                "claude_dir": str(entry),
                "session_count": len(jsonl_files),
                "exists": actual_path.exists(),
            })

    return projects


class TranscriptWatcher:
    """Watches Claude transcript files for a project."""

    def __init__(self, project_path: str):
        self.project_path = project_path
        self.claude_dir = find_claude_project_dir(project_path)
        self._file_positions: dict[str, int] = {}
        self._latest_file: str | None = None
        self.actions: list[AgentAction] = []
        self.active_sessions: set[str] = set()
        self.total_tool_calls: int = 0

    def _find_latest_transcript(self) -> str | None:
        """Find the most recently modified .jsonl file."""
        if self.claude_dir is None:
            return None
        jsonl_files = list(Path(self.claude_dir).glob("*.jsonl"))
        if not jsonl_files:
            return None
        return str(max(jsonl_files, key=lambda f: f.stat().st_mtime))

    def _find_all_recent_transcripts(self, max_age_hours: int = 24) -> list[str]:
        """Find all transcript files modified in the last N hours."""
        if self.claude_dir is None:
            return []
        cutoff = time.time() - (max_age_hours * 3600)
        jsonl_files = []
        for f in Path(self.claude_dir).glob("*.jsonl"):
            try:
                if f.stat().st_mtime > cutoff:
                    jsonl_files.append(str(f))
            except OSError:
                pass
        return jsonl_files

    def poll(self) -> list[AgentAction]:
        """Poll for new transcript events. Returns new actions since last poll."""
        new_actions = []

        # Watch the latest transcript file
        latest = self._find_latest_transcript()
        if latest is None:
            return new_actions

        # Also check recent transcripts for sub-agent counting
        recent_files = self._find_all_recent_transcripts(max_age_hours=1)

        for fpath in recent_files:
            last_pos = self._file_positions.get(fpath, 0)
            try:
                file_size = os.path.getsize(fpath)
                if file_size <= last_pos:
                    continue

                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    f.seek(last_pos)
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        action = self._parse_line(line)
                        if action:
                            new_actions.append(action)
                            self.total_tool_calls += 1

                    self._file_positions[fpath] = f.tell()

            except (OSError, json.JSONDecodeError):
                pass

        # Track active sessions
        self.active_sessions = set()
        for fpath in self._find_all_recent_transcripts(max_age_hours=1):
            session_id = Path(fpath).stem
            # Check if file was modified in last 5 minutes
            try:
                if time.time() - os.path.getmtime(fpath) < 300:
                    self.active_sessions.add(session_id)
            except OSError:
                pass

        self.actions.extend(new_actions)
        # Keep only last 50 actions
        if len(self.actions) > 50:
            self.actions = self.actions[-50:]

        return new_actions

    def _parse_line(self, line: str) -> AgentAction | None:
        """Parse a single JSONL line into an AgentAction."""
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            return None

        msg_type = data.get("type", "")

        # Look for assistant messages with tool use
        if msg_type == "assistant":
            message = data.get("message", {})
            content = message.get("content", [])
            session_id = data.get("sessionId", "")

            for block in content if isinstance(content, list) else []:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    tool_name = block.get("name", "")
                    tool_input = block.get("input", {})
                    return self._make_action(tool_name, tool_input, session_id, data)

        return None

    def _make_action(
        self, tool_name: str, tool_input: dict, session_id: str, raw: dict
    ) -> AgentAction | None:
        """Create an AgentAction from a tool call."""
        tool_info = TOOL_MAP.get(tool_name)
        if tool_info is None:
            return None

        verb, building = tool_info
        timestamp = raw.get("timestamp", "")

        # Build description
        target = ""
        if tool_name in ("Edit", "Read", "Write"):
            target = tool_input.get("file_path", "unknown")
            # Shorten to filename
            target = os.path.basename(target)
            desc = f"Agent {verb} {target}"
        elif tool_name == "Bash":
            cmd = tool_input.get("command", "")
            # Truncate long commands
            target = cmd[:40] + "..." if len(cmd) > 40 else cmd
            desc = f"Agent {verb} {target}"
        elif tool_name in ("Grep", "Glob"):
            pattern = tool_input.get("pattern", "")
            target = pattern
            desc = f"Agent {verb} '{pattern}'"
        elif tool_name == "Agent":
            desc = "Agent dispatched sub-agent"
            target = "sub-agent"
        else:
            desc = f"Agent {verb} {tool_name}"
            target = tool_name

        # Check if this is from a sub-agent file
        is_subagent = "agent-" in os.path.basename(raw.get("sessionId", ""))

        return AgentAction(
            timestamp=timestamp,
            action_type=building,
            target=target,
            description=desc,
            session_id=session_id,
            is_subagent=is_subagent,
        )

    @property
    def active_agent_count(self) -> int:
        """Number of currently active Claude sessions."""
        return len(self.active_sessions)

    def get_recent_actions(self, count: int = 5) -> list[AgentAction]:
        """Get the N most recent actions."""
        return self.actions[-count:]

    def count_total_tool_calls(self) -> int:
        """Count total tool calls across all transcripts."""
        if self.claude_dir is None:
            return 0

        count = 0
        for fpath in Path(self.claude_dir).glob("*.jsonl"):
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if '"tool_use"' in line:
                            count += 1
            except OSError:
                pass
        return count
