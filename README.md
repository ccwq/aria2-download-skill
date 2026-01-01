# aria2-download (Agent Skills Compatible)

[中文说明](./README.zh-cn.md)

High-performance parallel downloader Skill for Agent skills compatible tools. It uses `aria2c` (multi-connection + resume + proxy) to replace `curl`/`wget` when your network is slow or you need to speed up large file downloads.

## What this Skill does

- Parallel download by default (`--split=16`, `--max-connection-per-server=16`)
- Cross-platform bundled `aria2c` binaries (Windows/Linux/macOS)
- Resume supported (`--continue=true` by default)
- Proxy supported via `--all-proxy`
- Advanced options passthrough to `aria2c` via `--`

## Use in Agent skills compatible tools

In your Agent skills compatible tool's chat interface:

- List skills: `/skills`
- Explicit call: mention the skill name `aria2-download` (or type `$` to select it)

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

### Using Skills (2 ways)
- Explicit: mention the skill name (or type `$` to select)
- Implicit: Your Agent skills compatible tool may auto-enable a skill when your request matches the skill `description`

## Common Issues

- `aria2c not found`: ensure bundled binaries exist, or install system `aria2` and make `aria2c` available in `PATH`.
- Permission denied on Linux/macOS: the script will `chmod 755` the bundled binary, but your filesystem may block it.
- TLS failures: try `--no-check-certificate` only when you fully trust the source.
