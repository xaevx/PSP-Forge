# PSP Forge — prototype 0.2

PSP Forge is a toolkit scaffold for evaluating selected PC/PS2 game projects and building **title-specific native PSP ports**. It is not a universal ISO or executable converter.

## Current capabilities

- Read-only project inventory and extension counts.
- Preliminary feasibility classification based on file clues.
- JSON output suitable for later tooling.
- A profile template for recording engine, assets, target hardware, adapters and acceptance tests.
- Minimal C++ PSP homebrew smoke-test target using PSPSDK.
- Unit tests and GitHub Actions checks for the Python tooling.

Heuristic results are hints only. The analyser does not identify a game reliably, parse proprietary archives, reverse engineer executables, or convert assets yet.

## Architecture

- `tools/forge.py`: Python CLI for inventory and preliminary feasibility.
- `tests/`: analyser tests.
- `.github/workflows/python-tests.yml`: automated Python checks.
- `profiles/`: explicit per-game or per-engine port profiles.
- `runtime/psp/`: C++ PSP smoke test and PSPSDK Makefile.
- `docs/PORTING_PIPELINE.md`: development plan and acceptance gates.

## Requirements

- Python 3.10+ for host-side tools.
- PSPDEV/PSPSDK and GNU Make for building the PSP application.
- PPSSPP for early smoke tests; physical PSP hardware for final validation.

PSPDEV installation: https://pspdev.github.io/

## Run the analyser

```bash
python tools/forge.py analyze /path/to/your/game-project --out build/forge-report.json
```

The input must be a directory. The analyser scans filenames and sizes only and writes the report to the requested output path.

## Validate a profile

```bash
python tools/forge.py validate-profile profiles/example.json
```

This checks basic structure, not whether the profile is technically correct.

## Run Python tests

From the repository root:

```bash
python -m unittest discover -s tests -v
```

GitHub Actions runs these tests and validates the example profile on pushes and pull requests.

## Build the PSP smoke test

In a PSPDEV shell, from `runtime/psp/`:

```bash
make
```

The expected output includes `EBOOT.PBP`. If the SDK path is not configured, follow the installed PSPDEV environment's setup instructions. A successful build is not yet proof of emulator or hardware compatibility.

## Development gates

1. Validate the toolchain and run the smoke test in PPSSPP.
2. Test and harden the Python analyser.
3. Choose one legally usable, source-available PC game as the first port target.
4. Implement a minimal end-to-end slice: load a converted asset, render it, accept input and play a sound.
5. Investigate PS2 titles separately, one engine/title at a time.

## Legal and scope notes

Use source and assets you are authorised to modify. Do not commit proprietary game data. Native porting requires engine/game logic and PSP-specific renderer, audio, input, memory and filesystem work. An ISO alone cannot be converted directly into a PSP application.
