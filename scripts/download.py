import os
import sys
import subprocess
import platform
import argparse
import re
from typing import List, Optional

import shutil

DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# aria2c output pattern: [#2089b0 400.0KiB/30MiB(1%) CN:1 DL:115KiB ETA:4m23s]
PROGRESS_PATTERN = re.compile(
    r"\[#[0-9a-fA-F]+\s+([0-9.]+[KMGTP]?i?B)/([0-9.]+[KMGTP]?i?B)\((\d+)%\).*?DL:([0-9.]+[KMGTP]?i?B)(?:.*?ETA:([0-9a-z]+))?\]"
)

def print_progress(percent: str, downloaded: str, total: str, speed: str, eta: str = "未知"):
    """Prints a numeric progress line to stdout."""
    # Shorten labels to save space
    msg = f"进度:{percent}% 已下:{downloaded}/{total} 速:{speed} 剩:{eta}"

    # Get terminal width to prevent wrapping
    try:
        columns = shutil.get_terminal_size((80, 20)).columns
    except:
        columns = 80

    # Pad with spaces to clear previous line content
    # Truncate if too long to prevent wrapping
    if len(msg) > columns - 1:
        msg = msg[:columns-1]

    padding = " " * (columns - len(msg) - 1)

    # Use \r to return to start of line
    sys.stdout.write(f"\r{msg}{padding}")
    sys.stdout.flush()

def get_aria2_path():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == 'windows':
        return os.path.join(base_path, 'assets', 'bin', 'windows', 'aria2c.exe')
    elif system == 'linux':
        target = os.path.join(base_path, 'assets', 'bin', 'linux', 'aria2c')
        if os.path.exists(target):
            # Linux 下确保可执行位（在某些解压/拷贝场景下可能丢失）
            try:
                os.chmod(target, 0o755)
            except Exception:
                pass
            return target
    elif system == 'darwin':
        # macOS 根据 CPU 架构选择对应二进制
        # 常见取值：arm64 / aarch64 / x86_64 / amd64
        if machine in ('arm64', 'aarch64'):
            target = os.path.join(base_path, 'assets', 'bin', 'macos', 'arm64', 'aria2c')
        else:
            target = os.path.join(base_path, 'assets', 'bin', 'macos', 'x86_64', 'aria2c')
        if os.path.exists(target):
            try:
                os.chmod(target, 0o755)
            except Exception:
                pass
            return target
    return 'aria2c'

def build_aria2_command(
    aria2_path: str,
    url: str,
    output_dir: str,
    max_connection_per_server: int,
    split: int,
    min_split_size: str,
    proxy: Optional[str],
    out: Optional[str],
    user_agent: Optional[str],
    referer: Optional[str],
    header: List[str],
    continue_download: bool,
    file_allocation: str,
    allow_overwrite: bool,
    check_certificate: bool,
    extra_aria2_args: List[str],
) -> List[str]:
    cmd: List[str] = [
        aria2_path,
        "--dir",
        output_dir,
        f"--max-connection-per-server={max_connection_per_server}",
        f"--split={split}",
        f"--min-split-size={min_split_size}",
        f"--file-allocation={file_allocation}",
    ]

    if continue_download:
        cmd.append("--continue=true")
    else:
        cmd.append("--continue=false")

    if allow_overwrite:
        cmd.append("--allow-overwrite=true")
    else:
        cmd.append("--allow-overwrite=false")

    if check_certificate:
        cmd.append("--check-certificate=true")
    else:
        cmd.append("--check-certificate=false")

    if proxy:
        cmd.append(f"--all-proxy={proxy}")

    if out:
        cmd.append(f"--out={out}")

    if user_agent:
        cmd.append(f"--user-agent={user_agent}")
    else:
        cmd.append(f"--user-agent={DEFAULT_USER_AGENT}")

    if referer:
        cmd.append(f"--referer={referer}")

    for item in header:
        cmd.append(f"--header={item}")

    # 允许把未知/高级参数透传给 aria2c（使用 `--` 分隔）
    cmd.extend(extra_aria2_args)

    cmd.append(url)
    return cmd


def download(
    url: str,
    output_dir: str,
    max_connection_per_server: int,
    split: int,
    min_split_size: str,
    proxy: Optional[str],
    out: Optional[str],
    user_agent: Optional[str],
    referer: Optional[str],
    header: List[str],
    continue_download: bool,
    file_allocation: str,
    allow_overwrite: bool,
    check_certificate: bool,
    extra_aria2_args: List[str],
) -> None:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    aria2_path = get_aria2_path()
    cmd = build_aria2_command(
        aria2_path=aria2_path,
        url=url,
        output_dir=output_dir,
        max_connection_per_server=max_connection_per_server,
        split=split,
        min_split_size=min_split_size,
        proxy=proxy,
        out=out,
        user_agent=user_agent,
        referer=referer,
        header=header,
        continue_download=continue_download,
        file_allocation=file_allocation,
        allow_overwrite=allow_overwrite,
        check_certificate=check_certificate,
        extra_aria2_args=extra_aria2_args,
    )

    print(f"正在启动下载: {url}")
    print(f"输出目录: {os.path.abspath(output_dir)}")
    try:
        # Use Popen to capture output in real-time
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='utf-8',
            errors='replace',
            universal_newlines=True,
            bufsize=1
        )

        for line in process.stdout:
            line = line.strip()
            if not line:
                continue

            match = PROGRESS_PATTERN.search(line)
            if match:
                downloaded, total, percent, speed, eta = match.groups()
                if not eta:
                    eta = "未知"
                print_progress(percent, downloaded, total, speed, eta)
            else:
                # If not a progress line, only print if it's likely an error or important info
                # Clear line first
                if "ERROR" in line or "Exception" in line or "fail" in line.lower():
                     sys.stdout.write(f"\r\033[K{line}\n")
                     sys.stdout.flush()
                # Otherwise ignore to keep display clean during download

        process.wait()

        if process.returncode == 0:
            print("\n下载完成！")
        else:
            print(f"\n下载失败：aria2c 返回非 0 退出码（{process.returncode}）。")
            sys.exit(process.returncode)

    except FileNotFoundError:
        print("下载失败：未找到 aria2c 可执行文件（也未在系统 PATH 中找到）。")
        sys.exit(1)
    except Exception as e:
        print(f"下载失败：{e}")
        sys.exit(1)


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="download.py",
        description="使用内置 aria2c 进行多连接下载（支持代理与参数透传）。",
        add_help=True,
    )

    parser.add_argument("url", help="要下载的 URL")
    parser.add_argument(
        "-d",
        "--dir",
        dest="output_dir",
        default="download-aria-skill",
        help="输出目录（默认：download-aria-skill）",
    )
    parser.add_argument(
        "-o",
        "--out",
        default=None,
        help="输出文件名（可选，等价 aria2c 的 --out）",
    )
    parser.add_argument(
        "--proxy",
        default=None,
        help="代理地址（可选，等价 aria2c 的 --all-proxy），例如 http://127.0.0.1:7890 或 socks5://127.0.0.1:1080",
    )

    # 性能相关参数
    parser.add_argument(
        "-x",
        "--max-connection-per-server",
        type=int,
        default=16,
        help="单个服务器最大连接数（默认：16）",
    )
    parser.add_argument(
        "-s",
        "--split",
        type=int,
        default=16,
        help="分段数（默认：16）",
    )
    parser.add_argument(
        "-k",
        "--min-split-size",
        default="1M",
        help="最小分段大小（默认：1M）",
    )

    # 行为控制
    parser.add_argument(
        "-c",
        "--continue",
        dest="continue_download",
        action="store_true",
        default=True,
        help="启用断点续传（默认启用）",
    )
    parser.add_argument(
        "--no-continue",
        dest="continue_download",
        action="store_false",
        help="禁用断点续传",
    )
    parser.add_argument(
        "--allow-overwrite",
        action="store_true",
        default=False,
        help="允许覆盖同名文件（默认：否）",
    )
    parser.add_argument(
        "--check-certificate",
        action="store_true",
        default=True,
        help="启用 TLS 证书校验（默认启用）",
    )
    parser.add_argument(
        "--no-check-certificate",
        dest="check_certificate",
        action="store_false",
        help="禁用 TLS 证书校验（不建议，必要时再用）",
    )
    parser.add_argument(
        "--file-allocation",
        choices=["none", "prealloc", "trunc", "falloc"],
        default="none",
        help="文件预分配方式（默认：none）",
    )

    # 请求相关
    parser.add_argument("--user-agent", default=None, help="自定义 User-Agent")
    parser.add_argument("--referer", default=None, help="自定义 Referer")
    parser.add_argument(
        "-H",
        "--header",
        action="append",
        default=[],
        help="自定义请求头（可重复），例如 -H \"Authorization: Bearer xxx\"",
    )

    # `--` 之后的内容全部透传给 aria2c
    parser.add_argument(
        "extra_aria2_args",
        nargs=argparse.REMAINDER,
        help="额外透传给 aria2c 的参数（在命令行中使用 `--` 分隔）",
    )

    return parser.parse_args(argv)

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    # argparse.REMAINDER 会保留 `--` 本身；清理掉以免传给 aria2c 造成误解
    extra = list(args.extra_aria2_args)
    if extra and extra[0] == "--":
        extra = extra[1:]

    download(
        url=args.url,
        output_dir=args.output_dir,
        max_connection_per_server=args.max_connection_per_server,
        split=args.split,
        min_split_size=args.min_split_size,
        proxy=args.proxy,
        out=args.out,
        user_agent=args.user_agent,
        referer=args.referer,
        header=args.header,
        continue_download=args.continue_download,
        file_allocation=args.file_allocation,
        allow_overwrite=args.allow_overwrite,
        check_certificate=args.check_certificate,
        extra_aria2_args=extra,
    )
