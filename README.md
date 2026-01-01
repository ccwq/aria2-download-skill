# aria2-download (Agent Skills Compatible)

[中文说明](./README.zh-cn.md)

High-performance parallel downloader Skill for Agent skills compatible tools. It uses `aria2c` (multi-connection + resume + proxy) to replace `curl`/`wget` when your network is slow or you need to speed up large file downloads.

## What this Skill does

- Parallel download by default (`--split=16`, `--max-connection-per-server=16`)
- Cross-platform bundled `aria2c` binaries (Windows/Linux/macOS)
- Resume supported (`--continue=true` by default)
- Proxy supported via `--all-proxy`
- Advanced options passthrough to `aria2c` via `--`

## Prerequisites

- Agent skills compatible tool installed (for Skill usage)
- Python 3.8+ (to run `scripts/download.py`)
- `aria2c`:
  - Bundled under `assets/bin/**` (preferred)
  - Falls back to system `aria2c` if the bundled binary is unavailable

## Install

### 1) Install Agent skills compatible tool

Prerequisite: Node.js + npm (recommended: Node.js 18+).

```bash
npm i -g @anthropic-ai/cli@latest
anthropic --version
```

First run:

```bash
anthropic
```

### 2) Install this Skill

Pick one directory (any is fine) and place this repo folder under it:

- Current project: `$CWD/.anthropic/skills/aria2-download/`
- Repo root: `$REPO_ROOT/.anthropic/skills/aria2-download/`
- User global: `$ANTHROPIC_HOME/skills/aria2-download/` (default `~/.anthropic/skills`)

After installing, restart your Agent skills compatible tool, then type `/skills` to verify it is discovered.

### 3) (Optional) Install via `skill-installer`

If you already have the `skill-installer` system skill available in your Agent skills compatible tool, you can also ask it to install this repository as a skill (from a GitHub repo/path). After installation, restart your tool.

## Use in Agent skills compatible tools

In your Agent skills compatible tool's chat interface:

- List skills: `/skills`
- Explicitly call: mention the skill name `aria2-download` (or type `$` to select it)

Example prompts:

- "Use `aria2-download` to download https://example.com/bigfile.zip"
- "Use `aria2-download` to download URL to `my-downloads/` with proxy `http://127.0.0.1:7890`"

## Use the script directly (without Agent skills compatible tools)

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

1. Choose a location: `$CWD/.anthropic/skills`, `$REPO_ROOT/.anthropic/skills`, or `$ANTHROPIC_HOME/skills`
2. Create a folder like `.../.anthropic/skills/my-skill/`
3. Add `.../.anthropic/skills/my-skill/SKILL.md` with at least a YAML header containing `name` and `description`
4. Restart your Agent skills compatible tool, then use `/skills` to confirm it is loaded

## Triggering Skills (2 ways)

- Explicit: mention the skill name (or type `$` to select)
- Implicit: Your Agent skills compatible tool may auto-enable a skill when your request matches the skill `description`

## Project layout

- `SKILL.md`: Skill metadata + usage details
- `scripts/download.py`: main entry to run `aria2c`
- `assets/bin/**`: bundled `aria2c` binaries for Windows/Linux/macOS

## Supported Tools

### Claude Code

**Installing this Skill**:
1. Clone or download this repository
2. Copy the entire `aria2-download` folder to:
   - Project directory: `$CWD/.anthropic/skills/`
   - Global directory: `~/.anthropic/skills/`
3. Restart Claude Code
4. Verify installation: Type `/skills` to see if `aria2-download` appears

**Usage**:
- List skills: `/skills`
- Explicit call: Mention "aria2-download" in your prompt
- Example: "Use aria2-download to download https://example.com/bigfile.zip"

### iFlow (阿里心流)

**Installing this Skill**:

**Method 1: CLI (Recommended)**
```bash
iflow agent add aria2-download --scope project
# or for global use:
iflow agent add aria2-download --scope global
```

**Method 2: Manual**
1. Clone or download this repository
2. Copy the entire `aria2-download` folder to:
   - Project directory: `$CWD/.iflow/skills/`
   - Global directory: `~/.iflow/skills/`
3. Restart iFlow
4. Verify installation: Type `/skills` to see if `aria2-download` appears

**Usage**:
- List skills: `/skills`
- Explicit call: Mention "aria2-download" in your prompt
- Example: "Use aria2-download to download https://example.com/bigfile.zip"

### Gemini CLI

**Installing this Skill**:
1. Clone or download this repository
2. Copy the entire `aria2-download` folder to your skills directory (e.g., `~/.gemini/skills/` or `$CWD/.gemini/skills/`)
3. **Important**: Configure `gemini-extension.json` (usually in `~/.gemini/extensions/skillz/`) to include the absolute path to your skills directory in the `args` section.
   ```json
   "args": ["skillz@latest", "/absolute/path/to/.gemini/skills", "--verbose"]
   ```
4. Restart Gemini CLI
5. Verify installation: Type `/skills` to see if `aria2-download` appears

**Usage**:
- List skills: `/skills`
- Explicit call: Mention "aria2-download" in your prompt
- Example: "Use aria2-download to download https://example.com/bigfile.zip"

## Troubleshooting

- `aria2c not found`: ensure bundled binaries exist, or install system `aria2` and make `aria2c` available in `PATH`.
- Permission denied on Linux/macOS: the script will `chmod 755` the bundled binary, but your filesystem may block it.
- TLS failures: try `--no-check-certificate` only when you fully trust the source.
