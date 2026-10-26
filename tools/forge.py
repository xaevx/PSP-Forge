#!/usr/bin/env python3
"""PSP Forge: read-only game project inventory and port-readiness report."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from collections import Counter

CLUE_GROUPS = {
    "vice_city_like_assets": [
        "gta_vc.dat", "default.ide", "american.gxt", "gta3.dir", "cuts.dir"
    ],
    "pc_executables": [".exe", ".dll", ".pdb"],
    "ps2_disc_or_image": [".iso", ".bin", ".cue", ".elf", ".irx"],
    "common_asset_formats": [
        ".dff", ".txd", ".png", ".tga", ".bmp", ".wav", ".ogg",
        ".mp3", ".pak", ".wad", ".dat", ".ide", ".ipl", ".gxt"
    ],
}
MAX_FILES = 200_000

def inventory(root: Path):
    entries = []
    extensions = Counter()
    names_lower = []
    scanned = 0
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        scanned += 1
        if scanned > MAX_FILES:
            raise RuntimeError(f"Safety limit exceeded ({MAX_FILES} files). Narrow the input directory.")
        try:
            size = p.stat().st_size
        except OSError:
            size = None
        rel = str(p.relative_to(root))
        ext = p.suffix.lower()
        extensions[ext or "[no extension]"] += 1
        names_lower.append(p.name.lower())
        entries.append({"path": rel, "extension": ext, "size_bytes": size})
    return entries, extensions, names_lower

def analyze(root: Path):
    entries, extensions, names = inventory(root)
    name_set = set(names)
    clues = {}
    for group, tokens in CLUE_GROUPS.items():
        hits = []
        for token in tokens:
            if token.startswith("."):
                if extensions[token]:
                    hits.append({"clue": token, "count": extensions[token]})
            elif token in name_set:
                hits.append({"clue": token, "count": sum(1 for n in names if n == token)})
        clues[group] = hits

    total_bytes = sum(e["size_bytes"] or 0 for e in entries)
    return {
        "tool": "PSP Forge",
        "prototype_version": "0.1",
        "input_root": str(root.resolve()),
        "read_only": True,
        "summary": {
            "files": len(entries),
            "total_bytes": total_bytes,
            "total_mib": round(total_bytes / (1024 * 1024), 2),
            "extensions": dict(extensions.most_common()),
        },
        "clues": clues,
        "warnings": [
            "Filename heuristics do not prove platform, game version, ownership, or port compatibility.",
            "An ISO/ELF is not converted to a PSP executable by this tool.",
            "Native ports require engine/source work and PSP-specific replacements."
        ],
        "files": entries,
    }

def main():
    parser = argparse.ArgumentParser(description="PSP Forge project analyser (read-only prototype)")
    sub = parser.add_subparsers(dest="command", required=True)
    a = sub.add_parser("analyze", help="Inventory a game/project directory")
    a.add_argument("root", type=Path)
    a.add_argument("--out", type=Path, default=Path("build/forge-report.json"))
    args = parser.parse_args()

    if not args.root.exists() or not args.root.is_dir():
        parser.error(f"input must be an existing directory: {args.root}")

    report = analyze(args.root)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"PSP Forge analysis complete")
    print(f"Files: {report['summary']['files']}")
    print(f"Total size: {report['summary']['total_mib']} MiB")
    print(f"Report: {args.out}")
    print("Reminder: this is inventory/heuristics, not a converter.")

if __name__ == "__main__":
    main()
