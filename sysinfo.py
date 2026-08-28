#!/usr/bin/env python3
"""Cross-platform CLI for inspecting and exporting basic system metrics."""

from __future__ import annotations

import argparse
import json
import os
import platform
import socket
import time
from pathlib import Path
from typing import Any

import psutil

VERSION = "1.1.0"


def get_system_info() -> dict[str, Any]:
    return {
        "system": platform.system(),
        "node_name": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor() or "Unavailable",
    }


def get_cpu_info() -> dict[str, Any]:
    return {
        "physical_cores": psutil.cpu_count(logical=False),
        "total_cores": psutil.cpu_count(logical=True),
        "usage_per_core": psutil.cpu_percent(interval=0.1, percpu=True),
        "total_usage": psutil.cpu_percent(interval=None),
    }


def get_memory_info() -> dict[str, Any]:
    mem = psutil.virtual_memory()
    gib = 1024**3
    return {
        "total_gb": round(mem.total / gib, 2),
        "available_gb": round(mem.available / gib, 2),
        "used_gb": round(mem.used / gib, 2),
        "usage_percent": mem.percent,
    }


def get_disk_info() -> dict[str, Any]:
    disks: dict[str, Any] = {}
    gib = 1024**3
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except (PermissionError, OSError):
            continue
        key = part.device or part.mountpoint
        disks[key] = {
            "mountpoint": part.mountpoint,
            "filesystem": part.fstype or "Unknown",
            "total_gb": round(usage.total / gib, 2),
            "used_gb": round(usage.used / gib, 2),
            "free_gb": round(usage.free / gib, 2),
            "usage_percent": usage.percent,
        }
    return disks


def get_network_info() -> dict[str, str]:
    hostname = socket.gethostname()
    try:
        ip_address = socket.gethostbyname(hostname)
    except socket.error:
        ip_address = "Unavailable"
    return {"hostname": hostname, "ip_address": ip_address}


def collect_system_info() -> dict[str, Any]:
    return {
        "system": get_system_info(),
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "disk": get_disk_info(),
        "network": get_network_info(),
    }


def _print_mapping(data: dict[str, Any], indent: int = 0) -> None:
    prefix = " " * indent
    for key, value in data.items():
        if isinstance(value, dict):
            print(f"{prefix}{key}:")
            _print_mapping(value, indent + 2)
        else:
            print(f"{prefix}{key:<18}: {value}")


def display_all() -> None:
    for section, data in collect_system_info().items():
        print(f"\n=== {section.upper()} ===")
        _print_mapping(data)


def format_text(info: dict[str, Any]) -> str:
    lines: list[str] = []

    def append_mapping(mapping: dict[str, Any], indent: int = 0) -> None:
        prefix = " " * indent
        for key, value in mapping.items():
            if isinstance(value, dict):
                lines.append(f"{prefix}{key}:")
                append_mapping(value, indent + 2)
            else:
                lines.append(f"{prefix}{key}: {value}")

    for section, data in info.items():
        lines.append(f"=== {section.upper()} ===")
        append_mapping(data)
        lines.append("")
    return "\n".join(lines)


def export_to_file(path: str) -> None:
    output = Path(path)
    suffix = output.suffix.lower()
    if suffix not in {".json", ".txt"}:
        raise ValueError("Export file must end in .json or .txt")
    info = collect_system_info()
    if suffix == ".json":
        output.write_text(json.dumps(info, indent=2), encoding="utf-8")
    else:
        output.write_text(format_text(info), encoding="utf-8")
    print(f"Data exported to {output.resolve()}")


def live_monitor(interval: float = 2.0) -> None:
    if interval <= 0:
        raise ValueError("Interval must be greater than zero")
    try:
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            cpu = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory().percent
            print("=== LIVE MONITORING ===")
            print(f"CPU Usage    : {cpu}%")
            print(f"Memory Usage : {mem}%")
            print("Press Ctrl+C to stop.")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Display, export, or monitor basic system metrics.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("-d", "--display", action="store_true", help="Display system information")
    actions.add_argument("-e", "--export", metavar="FILE", help="Export to .json or .txt")
    actions.add_argument("-l", "--live", action="store_true", help="Monitor CPU and memory usage")
    parser.add_argument("-i", "--interval", type=float, default=2.0, help="Refresh interval in seconds")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.display:
            display_all()
        elif args.export:
            export_to_file(args.export)
        elif args.live:
            live_monitor(args.interval)
        else:
            parser.print_help()
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
