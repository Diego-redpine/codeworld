"""Red Pine business metrics and codebase stats."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime, timedelta

# Directories to always skip during codebase scan
SKIP_DIRS = {
    ".git", ".svn", ".hg",
    "node_modules", ".next", "__pycache__", ".pytest_cache",
    "venv", ".venv", "env", ".env",
    ".tox", ".mypy_cache", ".ruff_cache",
    "dist", "build", ".build", "out", "target",
    ".cache", ".parcel-cache", ".turbo",
    "vendor", "Pods", ".gradle",
    "coverage", ".nyc_output",
    ".idea", ".vscode",
    ".DS_Store",
}

CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs",
    ".go", ".rs", ".c", ".cpp", ".h", ".hpp",
    ".java", ".kt", ".kts", ".scala",
    ".rb", ".php", ".swift", ".m", ".mm",
    ".css", ".scss", ".sass", ".less",
    ".html", ".htm", ".xml", ".svg",
    ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg",
    ".md", ".mdx", ".txt", ".rst",
    ".sh", ".bash", ".zsh", ".fish",
    ".sql", ".graphql", ".gql",
    ".vue", ".svelte", ".astro",
    ".lua", ".ex", ".exs", ".erl",
    ".tf", ".hcl",
    ".dockerfile", ".docker-compose",
    ".env.example", ".gitignore", ".eslintrc",
    "Makefile", "Dockerfile", "Gemfile", "Rakefile",
}

BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".webp",
    ".mp3", ".mp4", ".wav", ".ogg", ".webm", ".avi",
    ".zip", ".tar", ".gz", ".bz2", ".xz", ".7z", ".rar",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx",
    ".exe", ".dll", ".so", ".dylib", ".o", ".a",
    ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".sqlite", ".db",
    ".pyc", ".pyo", ".class", ".jar",
}

# Revenue milestones for age progression
MILESTONES = [
    (0, "Settlement"),
    (1000, "Village"),
    (5000, "Town"),
    (10000, "City"),
    (20000, "Capital"),
    (30000, "Kingdom"),
    (100000, "Metropolis"),
]


@dataclass
class CustomerRecord:
    """A Red Pine customer business."""
    business_id: str
    business_type: str  # "beauty", "restaurant", "fitness", etc.
    name: str
    status: str  # "active", "inactive"
    created_at: str


@dataclass
class RedPineMetrics:
    """Red Pine business metrics -- revenue drives age progression."""
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
    def age_milestone(self) -> str:
        """Current milestone name based on revenue."""
        result = MILESTONES[0][1]
        for threshold, name in MILESTONES:
            if self.revenue >= threshold:
                result = name
            else:
                break
        return result

    @property
    def age_progress(self) -> float:
        """Progress (0.0-1.0) from current milestone to next."""
        current_threshold = 0
        next_threshold = MILESTONES[-1][0]
        for i, (threshold, _) in enumerate(MILESTONES):
            if self.revenue >= threshold:
                current_threshold = threshold
                if i + 1 < len(MILESTONES):
                    next_threshold = MILESTONES[i + 1][0]
                else:
                    return 1.0  # max milestone reached
            else:
                break
        span = next_threshold - current_threshold
        if span <= 0:
            return 1.0
        return min(1.0, (self.revenue - current_threshold) / span)

    @property
    def population(self) -> int:
        """Kingdom population: customers + agents + base villagers."""
        base = 5  # minimum villagers
        return base + self.customer_count + self.active_agents

    @property
    def milestone_index(self) -> int:
        """Index into MILESTONES list for current milestone."""
        idx = 0
        for i, (threshold, _) in enumerate(MILESTONES):
            if self.revenue >= threshold:
                idx = i
            else:
                break
        return idx


def scan_codebase(project_path: str) -> dict:
    """Scan Red Pine codebase for file/LOC stats. Returns dict with codebase_files, codebase_loc."""
    root = Path(project_path)
    if not root.exists():
        return {"codebase_files": 0, "codebase_loc": 0}

    total_files = 0
    total_loc = 0

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            ext = os.path.splitext(fname)[1].lower()
            if ext in BINARY_EXTENSIONS:
                continue
            total_files += 1
            if ext in CODE_EXTENSIONS or fname in CODE_EXTENSIONS:
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        total_loc += sum(1 for _ in f)
                except (OSError, UnicodeDecodeError):
                    pass

    return {"codebase_files": total_files, "codebase_loc": total_loc}


def get_git_info(project_path: str) -> dict:
    """Get git stats for Red Pine codebase."""
    result = {}
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=project_path, capture_output=True, timeout=5,
        ).check_returncode()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return result

    try:
        out = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=project_path, capture_output=True, text=True, timeout=5,
        )
        result["branch"] = out.stdout.strip()
    except Exception:
        pass

    try:
        since = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        out = subprocess.run(
            ["git", "rev-list", "--count", f"--since={since}", "HEAD"],
            cwd=project_path, capture_output=True, text=True, timeout=10,
        )
        result["commits_30d"] = int(out.stdout.strip())
    except Exception:
        result["commits_30d"] = 0

    return result


# ---------------------------------------------------------------------------
# Backward-compatibility aliases
# These keep existing imports in towns/town.py and main.py working until
# Task 5 migrates them to the new names.
# ---------------------------------------------------------------------------

# FolderMetrics is removed but referenced by towns/town.py — provide a stub
@dataclass
class FolderMetrics:
    """Deprecated: kept for backward compatibility."""
    name: str = ""
    path: str = ""
    file_count: int = 0
    loc: int = 0
    last_modified: float = 0


# ProjectMetrics alias — old code can still do `from towns.metrics import ProjectMetrics`
class ProjectMetrics(RedPineMetrics):
    """Deprecated: backward-compat alias for RedPineMetrics.

    Adds shim attributes that old town.py / main.py code expects.
    """
    def __init__(self, path: str = "", name: str = "", **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self.name = name
        self.total_files = kwargs.get("codebase_files", 0)
        self.total_loc = kwargs.get("codebase_loc", 0)
        self.total_dirs = 0
        self.folders: list[FolderMetrics] = []
        self.recent_commits = kwargs.get("git_commits_30d", 0)
        self.last_commit_time = ""
        self.session_minutes = 0

    @property
    def happiness(self) -> float:
        """0.0 to 1.0 based on recent activity."""
        base = min(1.0, self.recent_commits / 30) if self.recent_commits else 0.0
        return max(0.1, base)

    @property
    def tier(self) -> int:
        """Town tier based on file count."""
        if self.total_files >= 400:
            return 4
        elif self.total_files >= 150:
            return 3
        elif self.total_files >= 50:
            return 2
        else:
            return 1


def scan_project(project_path: str) -> ProjectMetrics:
    """Backward-compat wrapper: scans codebase and returns a ProjectMetrics."""
    root = Path(project_path)
    stats = scan_codebase(project_path)
    git_info = get_git_info(project_path)

    return ProjectMetrics(
        path=project_path,
        name=root.name,
        codebase_files=stats["codebase_files"],
        codebase_loc=stats["codebase_loc"],
        git_commits_30d=git_info.get("commits_30d", 0),
        git_branch=git_info.get("branch", ""),
    )


def quick_file_count(project_path: str) -> int:
    """Fast file count without full scan."""
    count = 0
    root = Path(project_path)
    if not root.exists():
        return 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in BINARY_EXTENSIONS:
                count += 1
    return count
