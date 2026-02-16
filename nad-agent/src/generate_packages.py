#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import random
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Chihuahua")
SERIES = ["After Hours", "Case Files", "Blue Alley Sessions"]
PUBLISH_WEEKDAYS = {1: "TUE", 3: "THU", 5: "SAT"}  # Monday=0
DURATION_TARGETS = ["34:00", "42:00", "58:00", "1:06:00", "1:18:00"]

SERIES_KEYWORDS = {
    "After Hours": [
        "late night jazz ambience",
        "rainy noir jazz",
        "night bar sax",
        "jazz for deep focus",
        "smoky midnight jazz",
        "after hours jazz mix",
    ],
    "Case Files": [
        "detective jazz playlist",
        "film noir jazz soundtrack",
        "mystery lounge jazz",
        "dark academia jazz",
        "cinematic night jazz",
        "lofi noir detective",
    ],
    "Blue Alley Sessions": [
        "smoky jazz bar",
        "blue alley jazz",
        "sax and smoke ambience",
        "vintage noir jazz",
        "jazz for reading",
        "midnight club jazz",
    ],
}

TITLE_PATTERNS = {
    "After Hours": [
        "After Hours: Neon Rain and Empty Glasses",
        "Midnight Drizzle | Noir Jazz for Quiet Streets",
        "After Hours Noir — Sax, Smoke, and Sleepless Lights",
    ],
    "Case Files": [
        "Case Files: The Blue Corner Dossier",
        "Night Dossier | Detective Jazz in the City",
        "Case Files Noir — Clues in Smoke and Basslines",
    ],
    "Blue Alley Sessions": [
        "Blue Alley Sessions: Beneath the Alley Light",
        "Blue Alley Sessions | Rainy Neon Jazz Noir",
        "Blue Alley Sessions — Stories from the Midnight Bar",
    ],
}

MICRO_STORY_LINES = [
    "The bar breathed slowly, like it knew every secret on the block.",
    "A dripping trench coat dropped a coin on the piano and asked for silence.",
    "The sax fell like warm rain across old wooden tables.",
    "Outside, a red neon sign blinked three times—someone was lying.",
    "No one traded names here; only glasses and bass notes spoke.",
    "When the brushes came in, even the shadows started dancing guilty.",
    "The night opened another file and sealed it with blue smoke.",
    "The last train passed by, but the melody stayed at the station.",
]

SEO_TEMPLATES = [
    "This {keyword} set is made for deep focus, study sessions, writing sprints, and rainy film-noir nights.",
    "If you were looking for {keyword}, moody night jazz, and cinematic atmosphere, this mix is built for late work and reading hours.",
    "This episode blends {keyword}, vintage bar ambience, and lo-fi textures for fans of noir aesthetics, dark jazz, and concentration playlists.",
]

ABOUT_NAD = (
    "Notes After Dark (NAD) is a jazz-noir channel: rain, neon, smoke, and midnight storytelling turned into music for focus, creation, and long nights."
)

LATE_HOURS_LINE = "If you're studying or working late, let this set hold the room while you keep going."

TAG_POOL = [
    "jazz noir",
    "noir jazz",
    "dark jazz",
    "night jazz",
    "jazz for studying",
    "jazz for work",
    "jazz for reading",
    "rainy night ambience",
    "saxophone jazz",
    "smooth noir jazz",
    "city night jazz",
    "instrumental jazz",
    "focus music",
    "film noir music",
    "detective jazz",
    "lofi jazz noir",
    "midnight jazz",
    "late night coffee jazz",
    "rain ambience jazz",
    "cinematic jazz",
    "smoky jazz bar",
    "late night playlist",
    "relaxing jazz",
    "study music",
    "writing music",
    "vintage jazz vibes",
    "urban noir soundtrack",
    "notes after dark",
    "NAD jazz",
    "blue alley sessions",
    "after hours jazz",
    "case files jazz",
]

THUMBNAIL_VARIANTS = [
    "Faceless bartender in close-up, wet wooden bar top, magenta/blue neon reflections on glass, soft smoke, cinematic grain, high contrast, jazz-noir mood, no text.",
    "Rainy neon street with blurred signs, distant silhouette holding a saxophone, cyan/red reflections in puddles, mysterious atmosphere, vertical thumbnail composition, no visible face, no text.",
    "Saxophone on a table beside a whiskey glass, curling smoke, deep blue side lighting, dark club background, floating particles, 35mm analog look, elegant noir style, no text.",
]


@dataclass
class PackageContext:
    publish_date: date
    weekday_label: str
    series: str
    keyword: str
    duration_target: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate weekly publishing packages for Notes After Dark")
    parser.add_argument(
        "--base-date",
        help="Base date in YYYY-MM-DD (simulates current date in America/Chihuahua).",
    )
    parser.add_argument(
        "--output-dir",
        default="nad-agent/packages",
        help="Output directory for markdown files.",
    )
    return parser.parse_args()


def get_base_date(raw: str | None) -> date:
    if raw:
        return date.fromisoformat(raw)
    return datetime.now(TZ).date()


def seed_from(*parts: str) -> int:
    joined = "|".join(parts)
    digest = hashlib.sha256(joined.encode("utf-8")).hexdigest()
    return int(digest[:16], 16)


def pick_series_for_date(publish_date: date, slot_index: int) -> str:
    week_index = publish_date.isocalendar().week % len(SERIES)
    return SERIES[(week_index + slot_index) % len(SERIES)]


def next_publish_dates(now_date: date, count: int = 3) -> list[tuple[date, str]]:
    dates: list[tuple[date, str]] = []
    cursor = now_date + timedelta(days=1)

    while len(dates) < count:
        weekday = cursor.weekday()
        if weekday in PUBLISH_WEEKDAYS:
            dates.append((cursor, PUBLISH_WEEKDAYS[weekday]))
        cursor += timedelta(days=1)

    return dates


def build_contexts(base: date) -> list[PackageContext]:
    contexts: list[PackageContext] = []
    upcoming = next_publish_dates(base, count=3)

    for idx, (publish_date, weekday_label) in enumerate(upcoming):
        series = pick_series_for_date(publish_date, idx)
        rng = random.Random(seed_from(str(publish_date), series))
        keyword = rng.choice(SERIES_KEYWORDS[series])
        duration_target = rng.choice(DURATION_TARGETS)
        contexts.append(
            PackageContext(
                publish_date=publish_date,
                weekday_label=weekday_label,
                series=series,
                keyword=keyword,
                duration_target=duration_target,
            )
        )

    return contexts


def pick_titles(ctx: PackageContext) -> tuple[str, list[str]]:
    rng = random.Random(seed_from("titles", str(ctx.publish_date), ctx.series))
    candidates = TITLE_PATTERNS[ctx.series][:]
    rng.shuffle(candidates)
    return candidates[0], candidates[1:3]


def build_micro_story(ctx: PackageContext) -> str:
    rng = random.Random(seed_from("story", str(ctx.publish_date), ctx.series))
    line_count = rng.randint(3, 6)
    lines = rng.sample(MICRO_STORY_LINES, k=line_count)
    return "\n".join(lines)


def pick_tags(ctx: PackageContext) -> str:
    rng = random.Random(seed_from("tags", str(ctx.publish_date), ctx.series))
    tags = TAG_POOL[:]
    rng.shuffle(tags)
    count = rng.randint(22, 26)
    return ", ".join(tags[:count])


def build_markdown(ctx: PackageContext) -> str:
    title_final, alternates = pick_titles(ctx)
    story = build_micro_story(ctx)
    rng = random.Random(seed_from("seo", str(ctx.publish_date), ctx.series))
    seo = rng.choice(SEO_TEMPLATES).format(keyword=ctx.keyword)
    tags_line = pick_tags(ctx)

    thumbnail_variants = "\n".join(
        f"- Variant {i + 1}: {variant}" for i, variant in enumerate(THUMBNAIL_VARIANTS)
    )

    return f"""---
date: {ctx.publish_date.isoformat()}
weekday: {ctx.weekday_label}
series: {ctx.series}
keyword: {ctx.keyword}
duration_target: {ctx.duration_target}
---

# Titles
- **Final title:** {title_final}
- **Alternate 1:** {alternates[0]}
- **Alternate 2:** {alternates[1]}

# Description (YouTube)
## Noir micro-story
{story}

## SEO paragraph
{seo}

## About NAD
{ABOUT_NAD}

## Optional late-hours line
{LATE_HOURS_LINE}

# Tags (20–30)
{tags_line}

# Chapters (template)
> Replace timestamps with final edit timings before publishing.

- 00:00 Opening — Rain and neon
- 04:40 First turn — Sax in the alley
- 09:30 Interlude — Conversation at the bar
- 14:10 Open file — Bassline and suspicion
- 18:45 Slow chase — Brush drums
- 24:20 Last call — Midnight piano
- 29:50 Closing — Night credits

# Pinned comment
Built for long nights. What city are you listening from, and what time is it there? 🌃🎷

# 3 engagement comments
1. Do you use this vibe for reading, studying, or driving at night?
2. If this set were a noir movie scene, what would be happening?
3. What should lead the next episode: more rain, more sax, or more piano?

# Thumbnail prompt (NAD style)
{thumbnail_variants}
"""


def slugify_series(series: str) -> str:
    return series.lower().replace(" ", "-")


def write_packages(contexts: list[PackageContext], output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for ctx in contexts:
        filename = f"{ctx.publish_date.isoformat()}_{ctx.weekday_label}_{slugify_series(ctx.series)}.md"
        target = output_dir / filename
        target.write_text(build_markdown(ctx), encoding="utf-8")
        written.append(target)
    return written


def main() -> None:
    args = parse_args()
    base = get_base_date(args.base_date)
    contexts = build_contexts(base)
    written = write_packages(contexts, Path(args.output_dir))
    for path in written:
        print(path.as_posix())


if __name__ == "__main__":
    main()
