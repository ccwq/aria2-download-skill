---
name: aria2-download
description: 高性能并行下载工具。在网络环境较差或需要加速下载大文件时，使用 aria2 代替标准的 curl/wget。内置 Windows、Linux、macOS 的 aria2c 可执行文件，支持多线程加速、断点续传及代理配置。默认下载到当前工作目录下的 download-aria-skill 文件夹中。
---

# aria2 下载器

此 Skill 用于在弱网环境下提升下载速度：使用 `aria2c` 的多连接并发替代 `curl` / `wget`。

## 核心功能

1. **多线程加速**：默认使用 16 连接并行下载（`--split=16` / `--max-connection-per-server=16`）。
2. **跨平台内置**：仅保留各平台“可直接运行”的 `aria2c` 最终产物（无源码/无额外附件）。
3. **断点续传**：`aria2c` 原生支持断点续传。
4. **代理支持**：支持 `http://` / `https://` / `socks5://` 等代理（通过 `--all-proxy`）。

## 使用方法

### 基础下载

告知 agent 需要下载的链接，Skill 会调用 `scripts/download.py` 下载到当前工作目录下的 `./download-aria-skill/`。

### 指定目录或代理

你可以明确要求：使用 aria2 下载 `URL` 到 `目录` 并使用代理 `PROXY`。

## 所有可用参数（本 Skill 支持）

以下为 `scripts/download.py` 支持的全部参数（为减少错误，已内置常用默认值）。如需更高级的 aria2 选项，可使用“参数透传”（见文末）。

必填：
- `URL`：要下载的链接

路径与输出：
- `-d, --dir OUTPUT_DIR`：输出目录（默认：`download-aria-skill`）
- `-o, --out OUT`：输出文件名（可选，等价 aria2c 的 `--out`）

代理：
- `--proxy PROXY`：代理地址（可选，等价 aria2c 的 `--all-proxy`）
  - 示例：`http://127.0.0.1:7890`、`socks5://127.0.0.1:1080`

性能（并发/分段）：
- `-x, --max-connection-per-server N`：单服务器最大连接数（默认：`16`）
- `-s, --split N`：分段数（默认：`16`）
- `-k, --min-split-size SIZE`：最小分段大小（默认：`1M`，可用 `K/M/G`）

行为控制：
- `-c, --continue`：启用断点续传（默认启用）
- `--no-continue`：禁用断点续传
- `--allow-overwrite`：允许覆盖同名文件（默认：关闭）
- `--check-certificate`：启用 TLS 证书校验（默认启用）
- `--no-check-certificate`：禁用 TLS 证书校验（不建议，必要时再用）
- `--file-allocation {none,prealloc,trunc,falloc}`：文件预分配方式（默认：`none`）

请求相关：
- `--user-agent UA`：自定义 User-Agent（默认使用 Chrome UA）
- `--referer URL`：自定义 Referer
- `-H, --header "K: V"`：自定义请求头（可重复）
  - 示例：`-H "Authorization: Bearer xxx" -H "Cookie: a=b"`

参数透传（高级用法）：
- `--`：分隔符，后面的所有参数会“原样”透传给 `aria2c`
  - 示例：`python scripts/download.py URL -- --max-tries=0 --retry-wait=3`

## assets 结构（当前 Skill 目录内）

- Windows：`assets/bin/windows/aria2c.exe`
- Linux：`assets/bin/linux/aria2c`
- macOS：
  - Apple Silicon：`assets/bin/macos/arm64/aria2c`
  - Intel：`assets/bin/macos/x86_64/aria2c`

## 注意事项

- 默认输出目录是“当前工作目录”下的 `download-aria-skill/`（不是 Skill 目录）。
- 若内置二进制在你的环境不可用，可先在系统中安装 `aria2`，脚本会回退调用系统 `aria2c`。
