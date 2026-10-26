# PSP Forge — prototype 0.1

A starter toolkit for analysing a game project and scaffolding a native PSP port.
This is **not** a universal game converter. It inventories files, identifies common
game/project clues, writes a report, and includes a minimal PSPSDK homebrew target.

## Architecture

- `tools/forge.py`: Python CLI for project inventory, heuristics, JSON report.
- `runtime/psp/`: minimal C++ PSP app entry point and PSPSDK Makefile.
- `profiles/`: per-game/engine profiles. Add explicit, tested profiles instead
  of pretending every game has the same format.
- `docs/PORTING_PIPELINE.md`: realistic development plan.

## Requirements

- Python 3.10+ for the analyser.
- For building the PSP executable: PSPDEV/PSPSDK toolchain and GNU Make.
  Install guide: https://pspdev.github.io/

## Run the analyser

```bash
python tools/forge.py analyze /path/to/your/legally-obtained-game-files --out build/report.json
```

It scans filenames and sizes only; it does not modify source files or extract
protected content. It flags possible asset layouts and executables for manual
review. Heuristics are not proof of a game's origin or compatibility.

## Build the PSP smoke-test app

From `runtime/psp/` in a PSPDEV environment:

```bash
make
```

The PSPSDK `build.mak` generates an EBOOT.PBP target from the app. Build variables
and toolchain paths can differ by PSPDEV installation, so check the SDK samples if
your local environment uses a different layout.

## Safety / legal notes

Use game files you own or are authorised to modify. Do not distribute proprietary
game assets. Keep each port in a separate profile with its own source, asset,
licensing, memory, input, audio, and rendering notes.
