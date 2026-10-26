#!/usr/bin/env python3
"""PSP Forge: read-only project inventory and preliminary feasibility report."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

VERSION = "0.2"
MAX_FILES = 200_000

CLUE_GROUPS = {
    "pc_executables": [".exe", ".dll", ".pdb"],
    "console_disc_or_image": [".iso", ".bin", ".cue", ".elf", ".irx"],
    "common_asset_formats": [
        ".dff", ".txd", ".png", ".tga", ".bmp", ".wav", ".ogg",
        ".mp3", ".pak", ".wad", ".dat", ".ide", ".ipl", ".gxt",
        ".obj", ".mtl", ".fbx", ".gltf", ".glb"
    ],
}
KNOWN_GAME_FILES = {
    "gta_vc.dat", "default.ide", "american.gxt", "gta3.dir", "cuts.dir"
}


def inventory(root: Path) -> tuple[list[dict[str, Any]], Counter, list[str]]:
    entries: list[dict[str, Any]] = []
    extensions: Counter = Counter()
    names: list[str] = []
    scanned = 0

    for path in sorted(root.rglob("*")):
        if path.is_symlink() or not path.is_file():
            continue
        scanned += 1
        if scanned > MAX_FILES:
            raise RuntimeError(
                f"Safety limit exceeded ({MAX_FILES} files). Narrow the input directory."
            )
        try:
            size = path.stat().st_size
        except OSError:
            size = None
        ext = path.suffix.lower()
        extensions[ext or "[no extension]"] += 1
        names.append(path.name.lower())
        entries.append({
            "path": path.relative_to(root).as_posix(),
            "extension": ext,
            "size_bytes": size,
        })

    return entries, extensions, names


def analyze(root: Path) -> dict[str, Any]:
    root = root.resolve()
    entries, extensions, names = inventory(root)
    name_counts = Counter(names)
    clues: dict[str, list[dict[str, Any]]] = {}

    for group, tokens in CLUE_GROUPS.items():
        hits = []
        for token in tokens:
            if token.startswith("."):
                if extensions[token]:
                    hits.append({"clue": token, "count": extensions[token]})
            elif name_counts[token]:
                hits.append({"clue": token, "count": name_counts[token]})
        clues[group] = hits

    known_hits = [
        {"clue": name, "count": name_counts[name]}
        for name in sorted(KNOWN_GAME_FILES)
        if name_counts[name]
    ]
    clues["known_game_file_names"] = known_hits

    total_bytes = sum(entry["size_bytes"] or 0 for entry in entries)
    has_source = any(Path(entry["path"]).suffix.lower() in {".c", ".cc", ".cpp", ".h", ".hpp"} for entry in entries)
    has_disc_image = any(Path(entry["path"]).suffix.lower() in {".iso", ".bin", ".cue"} for entry in entries)
    has_pc_executable = any(Path(entry["path"]).suffix.lower() == ".exe" for entry in entries)

    if has_source:
        feasibility = {
            "category": "source_candidate",
            "summary": "Source files appear present; this does not prove the full game source or dependencies are available.",
            "next_step": "Identify the engine, license, build system, dependencies, and platform-specific code.",
        }
    elif has_disc_image:
        feasibility = {
            "category": "binary_or_disc_only",
            "summary": "A disc image was detected. It cannot be converted directly into a native PSP game.",
            "next_step": "Identify the title and engine, inspect permitted metadata, and investigate a title-specific port or reimplementation.",
        }
    elif has_pc_executable:
        feasibility = {
            "category": "binary_only",
            "summary": "A PC executable was detected, but its presence does not provide portable source code.",
            "next_step": "Identify the engine and source availability before estimating porting work.",
        }
    else:
        feasibility = {
            "category": "unknown",
            "summary": "The inventory does not contain enough evidence to classify this project.",
            "next_step": "Provide the title, source availability, engine, and intended PSP model.",
        }

    return {
        "tool": "PSP Forge",
        "prototype_version": VERSION,
        "input_root": str(root),
        "read_only": True,
        "summary": {
            "files": len(entries),
            "total_bytes": total_bytes,
            "total_mib": round(total_bytes / (1024 * 1024), 2),
            "extensions": dict(sorted(extensions.items())),
        },
        "clues": clues,
        "preliminary_feasibility": feasibility,
        "warnings": [
            "Filename and extension heuristics are clues, not proof of platform, title, ownership, or compatibility.",
            "No executable, disc image, or asset is converted by this analyser.",
            "Native ports require source/engine work and PSP-specific adaptations.",
            "The report is preliminary and must be reviewed by a developer.",
        ],
        "files": entries,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="PSP Forge project analyser (read-only prototype)"
    )
    sub = parser.add_subparsers(dest="command", required=True)
    analyse_parser = sub.add_parser("analyze", help="Inventory a game/project directory")
    analyse_parser.add_argument("root", type=Path)
    analyse_parser.add_argument("--out", type=Path, default=Path("build/forge-report.json"))

    profile_parser = sub.add_parser("validate-profile", help="Check a port profile's required fields")
    profile_parser.add_argument("profile", type=Path)

    args = parser.parse_args()
    if args.command == "analyze":
        if not args.root.exists() or not args.root.is_dir():
            parser.error(f"input must be an existing directory: {args.root}")
        try:
            report = analyze(args.root)
        except (OSError, RuntimeError) as exc:
            parser.error(str(exc))
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print("PSP Forge analysis complete")
        print(f"Files: {report['summary']['files']}")
        print(f"Total size: {report['summary']['total_mib']} MiB")
        print(f"Preliminary category: {report['preliminary_feasibility']['category']}")
        print(f"Report: {args.out}")
        print("Reminder: this is inventory and heuristics, not a converter.")
        return

    try:
        profile = json.loads(args.profile.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        parser.error(f"could not read profile JSON: {exc}")
    required = ["profile_name", "status", "source_platform", "source_engine", "psp_adaptations"]
    missing = [field for field in required if field not in profile]
    if missing:
        parser.error("profile is missing required fields: " + ", ".join(missing))
    if not isinstance(profile["psp_adaptations"], dict):
        parser.error("'psp_adaptations' must be a JSON object")
    print(f"Profile structure OK: {profile['profile_name']}")
    print("Note: structural validation does not establish technical compatibility.")


if __name__ == "__main__":
    main()
