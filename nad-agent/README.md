# nad-agent

Weekly publishing package generator for **Notes After Dark (NAD)** with a jazz-noir editorial tone and Markdown output.

## What it generates
Each run creates **exactly 3 files** in `nad-agent/packages/` for the **next future** publish dates in `America/Chihuahua`:
- Tuesday
- Thursday
- Saturday

Each package includes:
- YAML frontmatter (`date`, `weekday`, `series`, `keyword`, `duration_target`)
- Final title + 2 alternates
- English description (noir micro-story + SEO + NAD brand paragraph + optional late-hours line)
- 20–30 English tags
- Chapters template
- Pinned comment + 3 engagement comments
- Thumbnail prompt in NAD style

## Automatic series rotation
The weekly rotation avoids repetition:
1. After Hours
2. Case Files
3. Blue Alley Sessions

Output is deterministic by date/series (seeded randomness).

## Requirements
- Python 3.11+

## Local usage
From repo root:

```bash
python3 nad-agent/src/generate_packages.py
```

Optional base date (simulate "now" for testing):

```bash
python3 nad-agent/src/generate_packages.py --base-date 2026-02-16
```

## Package versioning note
- `nad-agent/packages/*.md` is git-ignored.
- `nad-agent/packages/.gitkeep` keeps the folder in the repo.
- `.md` outputs are generated per run (local/CI) and consumed as workflow artifacts.

## Suggested publishing flow
1. Run the generator.
2. Open the package for the next publish day.
3. Replace chapter timestamps with final render timings.
4. Copy title, description, tags, and pinned comment into YouTube Studio.
5. Use the thumbnail prompt to keep NAD visual consistency.

## How to reduce “reused content” risk
Strengthen series identity and authorship on every release:
- Keep branded intros/outros with a recognizable NAD sonic signature.
- Preserve narrative continuity across series (After Hours / Case Files / Blue Alley Sessions).
- Use original episode descriptions and fresh micro-stories.
- Maintain a distinct visual language in thumbnails (neon, rain, smoke, noir).
- Post contextual pinned comments that show active channel curation.
- Avoid reusing identical text blocks across episodes.

## Structure

```text
nad-agent/
  packages/            # Generated output (untracked, except .gitkeep)
  prompts/             # Series and template guides
  src/
    generate_packages.py
  README.md
```
