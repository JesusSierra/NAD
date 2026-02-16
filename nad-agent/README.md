# nad-agent

Weekly package generator for **Notes After Dark (NAD)** in a melancholic, late-night bar noir style.

## What it generates
Each run creates **exactly 3 markdown files** for the next **future** publish dates in `America/Chihuahua`:
- Tuesday
- Thursday
- Saturday

Each package includes:
- YAML frontmatter (`date`, `weekday`, `series`, `keyword`, `duration_target`)
- English-only titles in this exact format:
  - `<Melancholic Phrase> | Dark Noir Jazz Mix (Late Night Bar Ambience)`
- English description with bartender POV micro-story (8–12 lines + 4–6 overheard quotes)
- SEO paragraph with required keywords (`noir jazz`, `late-night bar ambience`, and reading/studying/work context)
- Short NAD brand block + optional soft late-night line
- 22–30 English tags focused on bar/noir/late-night ambience
- Chapters template with 10–12 bar-moment lines for ~60–75 minutes
- Suno Tracklist section with Mood Arc + 12–18 song-title lines
- Pinned comment + engagement comments
- 3 thumbnail prompt variants in NAD visual style

## Rotation and determinism
- Series rotation remains: `After Hours`, `Bar Conversations`, `Midnight Service`.
- Output remains deterministic (seeded by date/series context).

## Requirements
- Python 3.11+

## Local usage
```bash
python3 nad-agent/src/generate_packages.py
```

Optional base date for reproducible testing:
```bash
python3 nad-agent/src/generate_packages.py --base-date 2026-02-16
```

## Package versioning policy
- `nad-agent/packages/*.md` is git-ignored.
- `nad-agent/packages/.gitkeep` is tracked to preserve directory structure.
- CI clears old package markdowns and uploads only newly generated files as an artifact.

## Structure
```text
nad-agent/
  packages/            # Generated output (untracked, except .gitkeep)
  prompts/             # Editorial template and series guide
  src/
    generate_packages.py
  README.md
```
