# aria2-download (Codex Skill)

[中文说明](./README.zh-cn.md)

High-performance parallel downloader Skill for Codex CLI. It uses `aria2c` (multi-connection + resume + proxy) to replace `curl`/`wget` when your network is slow or you need to speed up large file downloads.

## What this Skill does

- Parallel download by default (`--split=16`, `--max-connection-per-server=16`)
- Cross-platform bundled `aria2c` binaries (Windows/Linux/macOS)
- Resume supported (`--continue=true` by default)
- Proxy supported via `--all-proxy`
- Advanced options passthrough to `aria2c` via `--`

## Prerequisites

- Codex CLI installed (for Skill usage)
- Python 3.8+ (to run `scripts/download.py`)
- `aria2c`:
  - Bundled under `assets/bin/**` (preferred)
  - Falls back to system `aria2c` if the bundled binary is unavailable

## Install

### 1) Install Codex CLI (npm)

Prerequisite: Node.js + npm (recommended: Node.js 18+).

```bash
npm i -g @openai/codex@latest
codex --version
```

First run:

```bash
codex
```

### 2) Install this Skill

Pick one directory (any is fine) and place this repo folder under it:

- Current project: `$CWD/.codex/skills/aria2-download/`
- Repo root: `$REPO_ROOT/.codex/skills/aria2-download/`
- User global: `$CODEX_HOME/skills/aria2-download/` (default `~/.codex/skills`)

After installing, restart `codex`, then type `/skills` to verify it is discovered.

### 3) (Optional) Install via `skill-installer`

If you already have the `skill-installer` system skill available in Codex, you can also ask it to install this repository as a skill (from a GitHub repo/path). After installation, restart `codex`.

## Use in Codex

In Codex chat:

- List skills: `/skills`
- Explicitly call: mention the skill name `aria2-download` (or type `$` to select it)

Example prompts:

- “Use `aria2-download` to download https://example.com/bigfile.zip”
- “Use `aria2-download` to download URL to `my-downloads/` with proxy `http://127.0.0.1:7890`”

## Use the script directly (without Codex)

Basic:

```bash
python scripts/download.py https://example.com/bigfile.zip
```

Custom output dir / proxy:

```bash
python scripts/download.py https://example.com/bigfile.zip -d download-aria-skill --proxy http://127.0.0.1:7890
```

Passthrough extra `aria2c` options:

```bash
python scripts/download.py https://example.com/bigfile.zip -- --max-tries=0 --retry-wait=3
```

## Install common tools

### Install Git

- https://git-scm.com/downloads

### Install Python

- Windows: https://www.python.org/downloads/ (or Microsoft Store)
- macOS: `brew install python`
- Linux (Ubuntu/Debian): `sudo apt-get update && sudo apt-get install -y python3 python3-pip`

### Install aria2 (optional fallback)

- Windows (Chocolatey): `choco install aria2`
- Windows (Scoop): `scoop install aria2`
- macOS (Homebrew): `brew install aria2`
- Linux (Ubuntu/Debian): `sudo apt-get install -y aria2`
- Arch: `sudo pacman -S aria2`

Common `aria2c` usage:

```bash
aria2c -x 16 -s 16 -c https://example.com/bigfile.zip
```

## Manual install / create your own Skill

1. Choose a location: `$CWD/.codex/skills`, `$REPO_ROOT/.codex/skills`, or `$CODEX_HOME/skills`
2. Create a folder like `.../.codex/skills/my-skill/`
3. Add `.../.codex/skills/my-skill/SKILL.md` with at least a YAML header containing `name` and `description`
4. Restart `codex`, then use `/skills` to confirm it is loaded

## Triggering Skills (2 ways)

- Explicit: mention the skill name (or type `$` to select)
- Implicit: Codex may auto-enable a skill when your request matches the skill `description`

## Project layout

- `SKILL.md`: Skill metadata + usage details for Codex
- `scripts/download.py`: main entry to run `aria2c`
- `assets/bin/**`: bundled `aria2c` binaries for Windows/Linux/macOS

## Troubleshooting

- `aria2c not found`: ensure bundled binaries exist, or install system `aria2` and make `aria2c` available in `PATH`.
- Permission denied on Linux/macOS: the script will `chmod 755` the bundled binary, but your filesystem may block it.
- TLS failures: try `--no-check-certificate` only when you fully trust the source.
