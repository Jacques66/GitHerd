# GitHerd

**Real-time Git branch synchronizer**

Keep multiple Git branches aligned in real-time. Ideal for parallel AI coding sessions (Claude Code, Cursor, Copilot) or any workflow with multiple active branches.

## Features

- 🔄 **Real-time polling** — Configurable interval per repo (default 60s)
- ⚡ **Auto fast-forward** — Single branch ahead? Sync automatically
- 🔀 **Smart merge detection** — Multiple branches? Check for disjoint files
- 🔔 **Sound notification** — Know instantly when commits arrive
- 🗑 **Branch cleanup** — Delete branches from the UI
- 📌 **Always on top** — Never lose sight of your sync status
- 📂 **Multi-repo support** — Manage multiple repositories in tabs
- 💾 **Session persistence** — Repos are remembered between sessions
- ⚙️ **GUI configuration** — Edit settings without touching config files
- 🔍 **Auto-detection** — Remote and main branch detected automatically

## How it works

| Situation | Action |
|-----------|--------|
| Nothing to do | 🟢 Idle |
| Local main ahead | Auto push |
| Branches behind main | Auto push to sync |
| 1 branch ahead (no divergence) | Fast-forward + push |
| 1+ diverged branch, disjoint files | 🟡 Merge button |
| 1+ diverged branch, common files | 🔴 STOP |
| 2+ branches ahead, disjoint files | 🟡 Merge button |
| 2+ branches ahead, common files | 🔴 STOP |
| Git error (remote not found, etc.) | 🔴 Tab disabled |

**Deterministic. No heuristics. No magic.**

## Installation
```bash
git clone https://github.com/Jacques66/GitHerd.git
```

## Usage

Simply run GitHerd from anywhere:
```bash
python /path/to/GitHerd/githerd.py
```

Or add GitHerd to your PATH and run:
```bash
githerd
```

### Adding repositories

1. Click **"➕ Ajouter un repo"** to open the folder selector
2. Select a Git repository folder
3. Remote and main branch are **auto-detected**
4. A `githerd.toml` config file is created with detected values
5. A new tab opens with that repository

### Managing tabs

- **Right-click** on a tab to close it
- Repositories are saved automatically and restored on next launch
- Each tab has its own polling, status, and log

### Configuration

#### Global settings (☰ menu in bottom bar)

| Setting | Description |
|---------|-------------|
| Git binary | Path to git executable (default: `git`) |
| Font zoom | UI font scale factor (default: `1.6`) |

Stored in `~/.config/githerd/settings.json`

#### Per-repo settings (☰ menu in each tab)

| Setting | Description |
|---------|-------------|
| Remote | Git remote name (auto-detected) |
| Main branch | Main branch name (auto-detected) |
| Branch prefix | Prefix of branches to track (default: `claude/`) |
| Interval | Polling interval in seconds (default: `60`) |

Stored in `<repo>/githerd.toml`

### Config file format

```toml
[git]
remote = "origin"
main_branch = "main"
branch_prefix = "claude/"

[sync]
interval_seconds = 60
```

### Persistence

| File | Content |
|------|---------|
| `~/.config/githerd/repos.json` | List of open repositories |
| `~/.config/githerd/settings.json` | Global settings |
| `<repo>/githerd.toml` | Per-repo settings |

## Requirements

- Python 3.11+
- tkinter (usually included with Python)
- Git

### Optional (Linux)

- `wmctrl` — For always-on-top window
- `pulseaudio-utils` — For sound notifications
```bash
sudo apt install wmctrl pulseaudio-utils
```

## Error handling

If Git is not functional in a repository (wrong remote, network error, etc.):

- The tab shows 🔴 **ERREUR — Git non fonctionnel**
- Polling and Sync buttons are **disabled**
- You can still access **Configuration** to fix settings
- After saving new settings, Git health is re-checked

## Why GitHerd?

When running multiple AI coding sessions (or multiple developers) on the same repository, branches can quickly diverge. Manual synchronization is tedious and error-prone.

GitHerd watches your branches and:
- **Automatically syncs** when safe (single branch, fast-forward possible)
- **Alerts you immediately** when intervention is needed
- **Helps you merge safely** when files don't overlap

Catch divergences early (a few commits) instead of late (dozens of conflicts).

## License

MIT — Copyright (c) 2025 InZeMobile

## Author

Jacques Lovi. - [InZeMobile](https://github.com/Jacques66)
