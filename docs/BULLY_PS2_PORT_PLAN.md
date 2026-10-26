# Bully (PS2) to PSP: Port Plan

## Objective

Investigate whether the original PlayStation 2 release of **Bully** can be adapted into a native PSP application, using PSP Forge to manage the title-specific research, build pipeline, and validation.

This is a feasibility plan, not a claim that a playable port already exists. An ISO is not a native PSP executable, and PSP Forge does not currently convert PS2 games automatically.

## Size-reduction strategy

The reported ~4.5 GB figure is the size of the PS2 disc image, not a requirement that a native PSP port must occupy the same amount of storage or RAM. Disc images can contain padding and data laid out for the original disc. Compressing the image for archival storage does not make its executable compatible with PSP.

Plan for a selective, measured port rather than a one-to-one disc copy:

1. **Inventory before modifying:** identify the exact release, inspect file sizes and archive structure, and distinguish padding from meaningful data only when evidence supports it.
2. **Set an asset budget:** record size and format for textures, models, animation, audio, cutscenes, scripts, and level data. Do not set a final package-size target until the inventory is measured.
3. **Textures:** reduce resolution where acceptable and convert to a PSP-supported compressed format. Validate visual quality and runtime memory cost.
4. **Models and animation:** simplify geometry, remove unused data, and reduce animation data where safe.
5. **Audio and video:** use lower-bitrate/reduced-resolution media where appropriate; omit optional languages or cutscenes only if the chosen scope permits it.
6. **World streaming:** load nearby areas and required mission assets on demand. This reduces peak RAM pressure, but does not by itself reduce total installed size.
7. **Content scope:** first prototype a small, clearly defined slice (one environment, player movement, camera, and one interaction). Add missions and locations only after performance and asset-loading gates pass.

Never delete files or rebuild a disc image based on file extensions alone. Keep the original legally obtained dump unchanged and make experiments on a separate working copy. Do not upload the disc image or proprietary extracted assets to GitHub.

## Constraints and ground rules

- Target the original PS2 release, not Scholarship Edition (PC/Xbox 360/Wii).
- Record the exact regional release and disc serial/version before analysing executable details.
- Keep game ISOs, executables, extracted assets, and proprietary code out of this repository.
- Use media and tools you are legally entitled to use. Share only metadata, original tooling, and permitted research notes.
- Treat all engine and file-format identification as provisional until verified against the exact release.
- Test on PPSSPP first, then physical PSP hardware when available.

## Work stages

### B0 — Confirm the environment

- [ ] Confirm the developer host OS and available disk space.
- [ ] Install or verify PSPDEV/PSPSDK.
- [ ] Build the existing PSP Forge smoke test.
- [ ] Confirm its generated EBOOT.PBP boots in PPSSPP.
- [ ] Record toolchain versions and build output.

**Exit gate:** a known-good native PSP homebrew build exists before game-specific work begins.

### B1 — Identify the exact game release

- [ ] Identify region, disc serial, and revision from a legally obtained copy.
- [ ] Keep the disc image local; do not upload it to GitHub or chat.
- [ ] Record hashes and non-sensitive metadata locally if useful.
- [ ] Locate the main executable through documented, local inspection tools.
- [ ] Record findings without copying proprietary code or asset data into this repository.

**Exit gate:** exact target version and executable entry point are documented.

### B2 — Inventory and feasibility

- [ ] Run PSP Forge's read-only inventory against a local working directory.
- [ ] Separate executable, archive, texture, model, animation, audio, and script-format hypotheses.
- [ ] Mark each hypothesis as confirmed, likely, or unknown, with evidence.
- [ ] Establish whether useful public documentation or reusable, legally available tooling exists.
- [ ] Estimate CPU, RAM, GPU, storage, and streaming requirements.
- [ ] Establish an evidence-based installed-size budget after the asset inventory; do not promise a compressed final size in advance.
- [ ] Separate archival image compression from runtime asset optimization in all reports.

**Exit gate:** produce a title-specific feasibility report with explicit unknowns and blockers.

### B3 — Native PSP foundation

- [ ] Establish a minimal PSP application with input, frame timing, logging, and file access.
- [ ] Implement a simple 3D test scene at 480x272.
- [ ] Measure memory use and frame time on the target PSP profile.
- [ ] Add a small test asset pipeline using original or openly licensed assets.
- [ ] Add regression checks for loading, rendering, input, and failure handling.

**Exit gate:** a stable, measurable PSP runtime exists independently of proprietary Bully assets.

### B4 — Title-specific technical prototype

Proceed only if B2 provides a credible route forward.

- [ ] Validate one format at a time using authorised local data.
- [ ] Prototype one static model or environment element, if technically and legally appropriate.
- [ ] Measure source and converted asset sizes and document visual/performance trade-offs.
- [ ] Investigate animation, collision, scripting, audio, and world streaming separately.
- [ ] Compare results against reference behaviour without distributing copyrighted material.
- [ ] Reassess performance and memory after each subsystem.

**Exit gate:** a repeatable proof of concept demonstrates at least one meaningful game-specific subsystem on PSP.

### B5 — Scope decision

Choose one evidence-based path:
1. Continue a native title-specific port.
2. Build a clean-room reimplementation of selected systems.
3. Stop or narrow scope if technical blockers make the target infeasible.

A complete game port must not be promised until core gameplay, world loading, animation, input, audio, saving, stability, and performance have all been demonstrated.

## Initial risks

| Risk | Why it matters | Mitigation |
|---|---|---|
| No verified original source | Binary analysis and reimplementation can be extensive | Investigate source availability and tooling before implementation |
| PS2/PSP architecture differences | Executable code and hardware APIs are not directly interchangeable | Use a native PSP runtime and explicit subsystem adapters |
| Memory and performance limits | Open-world assets and streaming can exceed PSP budgets | Profile early; use reduced assets, streaming, and measured budgets |
| Unknown proprietary formats | Asset extraction/conversion may be a major project itself | Validate formats incrementally; do not assume extensions prove format |
| Legal and repository hygiene | Game code and assets should not be redistributed | Keep game material local; commit original tools and permitted metadata only |

## Current status

**Research / feasibility.** No Bully game files have been inspected by PSP Forge yet. The next useful evidence is the exact PS2 release metadata and a successful native PSP smoke test.
