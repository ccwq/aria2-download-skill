# aria2-download（Agent Skills 兼容）

[English](./README.md)

面向 Agent skills 兼容工具的高性能并行下载 Skill：在弱网或需要加速下载大文件时，用 `aria2c`（多连接并发 + 断点续传 + 代理）替代 `curl`/`wget`。

## 这个 Skill 能做什么

- 默认 16 连接并发下载（`--split=16`、`--max-connection-per-server=16`）
- 内置跨平台 `aria2c` 可执行文件（Windows/Linux/macOS）
- 默认开启断点续传（`--continue=true`）
- 支持代理（通过 `--all-proxy`）
- 支持高级参数透传（在命令行中用 `--` 分隔，后续参数原样交给 `aria2c`）

## 前置要求

- 已安装 Agent skills 兼容工具（用于在工具中使用 Skill）
- Python 3.8+（用于运行 `scripts/download.py`）
- `aria2c`：
  - 优先使用本仓库内置的二进制（`assets/bin/**`）
  - 若内置不可用，会回退调用系统 PATH 中的 `aria2c`

## 安装

### 1）安装 Agent skills 兼容工具

前置：需要 Node.js + npm（建议 Node.js 18+）。

```bash
npm i -g @anthropic-ai/cli@latest
anthropic --version
```

首次运行并登录：

```bash
anthropic
```

### 2）安装/启用本 Skill

把本仓库放到以下任一目录下（任选其一即可）：

- 当前目录：`$CWD/.anthropic/skills/aria2-download/`
- 仓库根目录：`$REPO_ROOT/.anthropic/skills/aria2-download/`
- 用户全局：`$ANTHROPIC_HOME/skills/aria2-download/`（默认 `~/.anthropic/skills`）

完成后重启你的 Agent skills 兼容工具，在交互界面输入 `/skills` 确认已出现。

### 3）（可选）使用 `skill-installer` 安装

如果你在 Agent skills 兼容工具中已启用系统自带的 `skill-installer`，也可以直接让它从 GitHub 仓库路径安装本 Skill。安装完成后需要重启工具才会加载新技能。

## 在 Agent skills 兼容工具中使用

在 Agent skills 兼容工具的交互界面：

- 查看可用 skills：`/skills`
- 显式调用：在提示词中直接提到 `aria2-download`（或输入 `$` 选择该 skill）

示例提示词：

- "使用 `aria2-download` 下载 https://example.com/bigfile.zip"
- "使用 `aria2-download` 下载 URL 到 `my-downloads/`，并使用代理 `http://127.0.0.1:7890`"

## 直接运行脚本（不通过 Agent skills 兼容工具）

基础下载：

```bash
python scripts/download.py https://example.com/bigfile.zip
```

指定目录 / 代理：

```bash
python scripts/download.py https://example.com/bigfile.zip -d download-aria-skill --proxy http://127.0.0.1:7890
```

高级参数透传（`--` 后面的内容原样传给 `aria2c`）：

```bash
python scripts/download.py https://example.com/bigfile.zip -- --max-tries=0 --retry-wait=3
```

## 主流工具安装与使用

### 安装 Git

- https://git-scm.com/downloads

### 安装 Python

- Windows：到 https://www.python.org/downloads/ 下载（或使用 Microsoft Store）
- macOS：`brew install python`
- Linux（Ubuntu/Debian）：`sudo apt-get update && sudo apt-get install -y python3 python3-pip`

### 安装 aria2（可选：用于系统回退）

- Windows（Chocolatey）：`choco install aria2`
- Windows（Scoop）：`scoop install aria2`
- macOS（Homebrew）：`brew install aria2`
- Linux（Ubuntu/Debian）：`sudo apt-get install -y aria2`
- Arch：`sudo pacman -S aria2`

常见 `aria2c` 用法：

```bash
aria2c -x 16 -s 16 -c https://example.com/bigfile.zip
```

### 手动安装 / 自建 Skill（目录 + `SKILL.md`）

1. 选择存放位置（任一即可）：`$CWD/.anthropic/skills`、`$REPO_ROOT/.anthropic/skills`、`$ANTHROPIC_HOME/skills`
2. 创建目录：`.../.anthropic/skills/my-skill/`
3. 创建文件：`.../.anthropic/skills/my-skill/SKILL.md`，包含至少 `name` 与 `description` 的 YAML 头
4. 重启 Agent skills 兼容工具，输入 `/skills` 验证已加载

### 使用 Skill（两种方式）

- 显式调用：在提示词中提到技能名（或用 `$` 选择）
- 隐式调用：任务与 skill 的 `description` 匹配时，Agent skills 兼容工具可能自动启用

## 目录结构

- `SKILL.md`：Skill 元信息与使用说明
- `scripts/download.py`：下载脚本入口
- `assets/bin/**`：各平台内置 `aria2c` 二进制

## 支持的工具

### Claude Code

**安装此 Skill**：
1. 克隆或下载本仓库
2. 将整个 `aria2-download` 文件夹复制到：
   - 项目目录：`$CWD/.anthropic/skills/`
   - 全局目录：`~/.anthropic/skills/`
3. 重启 Claude Code
4. 验证安装：输入 `/skills` 查看 `aria2-download` 是否出现

**使用方法**：
- 查看技能：`/skills`
- 显式调用：在提示词中提到 "aria2-download"
- 示例："使用 aria2-download 下载 https://example.com/bigfile.zip"

### iFlow (阿里心流)

**安装此 Skill**：

**方式一：CLI（推荐）**
```bash
iflow agent add aria2-download --scope project
# 或全局安装：
iflow agent add aria2-download --scope global
```

**方式二：手动安装**
1. 克隆或下载本仓库
2. 将整个 `aria2-download` 文件夹复制到：
   - 项目目录：`$CWD/.iflow/skills/`
   - 全局目录：`~/.iflow/skills/`
3. 重启 iFlow
4. 验证安装：输入 `/skills` 查看 `aria2-download` 是否出现

**使用方法**：
- 查看技能：`/skills`
- 显式调用：在提示词中提到 "aria2-download"
- 示例："使用 aria2-download 下载 https://example.com/bigfile.zip"

### Gemini CLI

**安装此 Skill**：
1. 克隆或下载本仓库
2. 将整个 `aria2-download` 文件夹复制到你的 skill 目录（如 `~/.gemini/skills/` 或 `$CWD/.gemini/skills/`）
3. **重要**：配置 `gemini-extension.json`（通常位于 `~/.gemini/extensions/skillz/`），将你的 skill 目录的绝对路径添加到 `args` 中：
   ```json
   "args": ["skillz@latest", "/absolute/path/to/.gemini/skills", "--verbose"]
   ```
4. 重启 Gemini CLI
5. 验证安装：输入 `/skills` 查看 `aria2-download` 是否出现

**使用方法**：
- 查看技能：`/skills`
- 显式调用：在提示词中提到 "aria2-download"
- 示例："使用 aria2-download 下载 https://example.com/bigfile.zip"

## 常见问题

- 找不到 `aria2c`：检查 `assets/bin/**` 是否存在，或安装系统 `aria2` 并确保 `aria2c` 在 PATH 中
- Linux/macOS 权限问题：脚本会尝试 `chmod 755`，但某些文件系统/策略可能禁止
- TLS 证书报错：仅在你完全信任来源时再使用 `--no-check-certificate`
