# aria2-download-skills

[English](./README.md)

面向 Agent skills 兼容工具的高性能并行下载 Skill：在弱网或需要加速下载大文件时，用 `aria2c`（多连接并发 + 断点续传 + 代理）替代 `curl`/`wget`。

## 这个 Skill 能做什么

- 默认 16 连接并发下载（`--split=16`、`--max-connection-per-server=16`）
- 内置跨平台 `aria2c` 可执行文件（Windows/Linux/macOS）
- 默认开启断点续传（`--continue=true`）
- 支持代理（通过 `--all-proxy`）
- 支持高级参数透传（在命令行中用 `--` 分隔，后续参数原样交给 `aria2c`）

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
### 使用 Skill（两种方式）
- 显式调用：在提示词中提到技能名（或用 `$` 选择）
- 隐式调用：任务与 skill 的 `description` 匹配时，Agent skills 兼容工具可能自动启用
## 常见问题

- 找不到 `aria2c`：检查 `assets/bin/**` 是否存在，或安装系统 `aria2` 并确保 `aria2c` 在 PATH 中
- Linux/macOS 权限问题：脚本会尝试 `chmod 755`，但某些文件系统/策略可能禁止
- TLS 证书报错：仅在你完全信任来源时再使用 `--no-check-certificate`
