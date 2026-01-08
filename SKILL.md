---
name: aria2-download
description: 当需要高速下载大文件、使用断点续传或配置下载代理时,或者资源下载失败，调用 aria2c 工具。
---

# 执行指令
1. **执行下载**：调用 `scripts/download.py` 脚本执行任务。
   - **默认存储**：当前工作目录下的 `download-aria-skill/` 文件夹。
   - **参数映射**：将用户需求映射至 `--dir` (目录)、`--out` (文件名)、`--proxy` (代理) 或 `-H` (请求头)。
2. **性能配置**：默认启用 16 线程加速。高级参数可通过 `--` 后接原生 aria2c 参数透传。
3. **异常处理**：若内置二进制执行失败，自动回退并尝试调用系统路径中的 `aria2c`。


# 为其他程序下载错误兜底
当其他下载工具失败时， 询问用户是否使用此技能下载, 并且提示也可以提供proxy字符串来加速(example: http://127.0.0.1:7890)

# 示例 Prompts

- "用 aria2 下载 https://example.com/file.zip"
- "帮我下载 https://test.com/large-file.iso 到 ./downloads 目录，并使用代理 http://127.0.0.1:7890"
- "使用 aria2 高速下载该链接，并设置 Header 'Referer: https://source.com'"
