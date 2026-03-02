# CodeWorld — Cozy Terminal Town Visualizer

Turn your coding sessions into watching cozy pixel-art villages grow.

Each project folder becomes a town. Buildings appear as your codebase grows.
Claude agents walk between buildings as they work in real time.

## Quick Start

```bash
cd codeworld
source .venv/bin/activate
python main.py
```

## Usage

```bash
# Visualize current directory
python main.py

# Visualize a specific project
python main.py /path/to/project

# Start in world map view
python main.py --world

# Narrow mode for tmux side pane
python main.py --side
```

## Keybindings

| Key     | Action                          |
|---------|---------------------------------|
| `w`     | Toggle World Map / Town View    |
| `r`     | Refresh metrics now             |
| `q`     | Quit                            |
| `←` `→` | Navigate towns (world view)     |
| `Enter` | Select town (world view)        |

## How It Works

- **Files + folders** determine which buildings exist
- **Git history** creates sparkle particles (happiness)
- **Claude Code transcripts** spawn walking agent sprites
- **Day/night cycle** based on your real local time

## Building Types

| Folder         | Building    |
|----------------|-------------|
| `src/`, `app/` | Castle      |
| `docs/`        | Library     |
| `tests/`       | Tavern      |
| `frontend/`    | Market      |
| `data/`, `db/` | Garden      |
| `build/`       | Forge       |
| `api/`         | Watchtower  |
| `utils/`       | Well        |

## Config

Edit `config.toml` to add project paths manually:

```toml
projects = [
  "/Users/you/code/my-project",
  "/Users/you/code/another-project",
]
```

Without config, CodeWorld auto-discovers all projects from `~/.claude/projects/`.

## Tech Stack

- Python 3.11+
- [Textual](https://github.com/Textualize/textual) — TUI framework
- Half-block Unicode pixel art (no images, no emojis)

## Credits

- Textual framework: https://github.com/Textualize/textual
- Claude Code: https://github.com/anthropics/claude-code
- Inspired by: Microtown, Stardew Valley, Outlanders, Kingdom

## License

MIT
