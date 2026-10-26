#!/usr/bin/env python3
"""Read-only intake report for a local game disc image.

This tool hashes the supplied file and optionally asks 7z to list its contents.
It never extracts, edits, patches, uploads, or deletes the input image.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def list_with_7z(path: Path) -> dict[str, Any]:
    executable = shutil.which("7z") or shutil.which("7zz")
    if not executable:
        return {
            "available": False,
            "tool": None,
            "listed": False,
            "note": "Install p7zip/7zip to enable read-only archive listing. No files were extracted.",
        }

    try:
        result = subprocess.run(
            [executable, "l", "-slt", str(path)],
            check=False,
            capture_output=True,
            text=True,
            timeout=180,
        )
    except subprocess.TimeoutExpired:
        return {
            "available": True,
            "tool": Path(executable).name,
            "listed": False,
            "note": "Listing timed out after 180 seconds. No files were extracted.",
        }

    if result.returncode != 0:
        return {
            "available": True,
            "tool": Path(executable).name,
            "listed": False,
            "return_code": result.returncode,
            "stderr_tail": result.stderr[-2000:],
            "note": "The tool could not list this image format. No files were extracted.",
        }

    entries = []
    current: dict[str, str] = {}
    for line in result.stdout.splitlines():
        if not line.strip():
            if current.get("Path") and current.get("Path") != str(path):
                entries.append(current)
            current = {}
            continue
        if " = " in line:
            key, value = line.split(" = ", 1)
            if key in {"Path", "Size", "Folder", "Attributes", "Modified"}:
                current[key] = value
    if current.get("Path") and current.get("Path") != str(path):
        entries.append(current)

    sizes = []
    for item in entries:
        try:
            if item.get("Folder") != "+" and item.get("Size") is not None:
                sizes.append(int(item["Size"]))
        except ValueError:
            pass

    return {
        "available": True,
        "tool": Path(executable).name,
        "listed": True,
        "entry_count": len(entries),
        "file_count_with_size": len(sizes),
        "listed_file_bytes_total": sum(sizes),
        "largest_entries": sorted(
            [
                {"path": item.get("Path", ""), "size_bytes": int(item["Size"])}
                for item in entries
                if item.get("Folder") != "+" and item.get("Size", "").isdigit()
            ],
            key=lambda item: item["size_bytes"],
            reverse=True,
        )[:30],
        "note": "Listing is format/tool dependent and does not prove that every entry is a game asset.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a read-only metadata report for a local disc image."
    )
    parser.add_argument("image", type=Path, help="Path to a locally stored ISO/image")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("local-research/iso-intake.json"),
        help="Local JSON report path (default: local-research/iso-intake.json)",
    )
    parser.add_argument(
        "--list-contents",
        action="store_true",
        help="Attempt a read-only 7z listing; never extracts files",
    )
    args = parser.parse_args()

    image_path = args.image.expanduser()
    if not image_path.is_file():
        parser.error(f"image path is not an existing file: {image_path}")
    if image_path.is_symlink():
        parser.error("refusing to inspect a symbolic link; pass the real local file path")

    stat = image_path.stat()
    report: dict[str, Any] = {
        "tool": "PSP Forge ISO intake",
        "report_version": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "read_only": True,
        "input": {
            "file_name": image_path.name,
            "size_bytes": stat.st_size,
            "size_gib": round(stat.st_size / (1024 ** 3), 3),
            "sha256": sha256_file(image_path),
        },
        "content_listing": list_with_7z(image_path) if args.list_contents else {
            "requested": False,
            "note": "Rerun with --list-contents to attempt a read-only listing if 7z is installed.",
        },
        "warnings": [
            "This report does not identify the game or verify ownership.",
            "A disc image cannot be converted directly into a native PSP application.",
            "Do not commit the disc image, extracted proprietary assets, or this private report to Git.",
            "A successful archive listing does not establish that formats are understood or legally redistributable.",
        ],
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("PSP Forge ISO intake report created.")
    print(f"File: {image_path.name}")
    print(f"Size: {report['input']['size_bytes']} bytes ({report['input']['size_gib']} GiB)")
    print(f"SHA-256: {report['input']['sha256']}")
    print(f"Report: {args.out}")
    print("Input image was not modified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
