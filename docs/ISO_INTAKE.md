# Local ISO Intake Workflow

## Purpose

Use PSP Forge to record metadata about a legally obtained local PS2 disc image before any title-specific research. The reported Bully image is approximately 4.5 GB, but its exact size, release, and contents have not yet been independently verified.

A disc image is research input only. It is not a native PSP executable and cannot be converted directly into a PSP application.

## Safety rules

- Keep the original ISO unchanged and stored outside the Git repository.
- Do not upload an ISO or proprietary extracted assets to GitHub, issues, pull requests, or AI chat.
- Keep reports containing local file paths in an ignored local folder.
- Use read-only listing first. Do not extract or alter files until there is a specific, justified next step.
- Do not infer format or importance from file extensions alone.

## Recommended Windows/WSL layout

For example, store the image at:

`C:\PSPForge\source\Bully.iso`

From Ubuntu/WSL, that path appears as:

`/mnt/c/PSPForge/source/Bully.iso`

Check that the file is visible:

```bash
ls -lh /mnt/c/PSPForge/source/
```

## Create a metadata report

From the PSP Forge repository root, run:

```bash
python3 tools/iso_intake.py "/mnt/c/PSPForge/source/Bully.iso" --out local-research/bully-iso-intake.json
```

This records the exact byte size and SHA-256 hash. Hashing reads the entire file and may take a little while for a multi-gigabyte image. It does not modify the image.

## Optional read-only listing

Install a listing utility if needed, then run:

```bash
sudo apt-get update
sudo apt-get install -y p7zip-full
python3 tools/iso_intake.py "/mnt/c/PSPForge/source/Bully.iso" --list-contents --out local-research/bully-iso-intake.json
```

The listing uses `7z l`; it does not extract files. Some PS2 disc formats may not be listable by 7z. A listing failure is not proof that the ISO is corrupt.

## Next decisions

After the report exists locally:

1. Confirm the ISO size and hash.
2. Identify the regional release and disc serial using lawful, documented local inspection.
3. Review the listing, if supported, and group files by evidence-based categories.
4. Measure candidate asset groups before setting a size budget.
5. Keep proprietary content and local reports out of Git.

Do not promise a final package size until actual asset inventory and PSP runtime measurements exist.
