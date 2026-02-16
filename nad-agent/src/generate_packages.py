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
TITLE_SUFFIX = "Dark Noir Jazz Mix (Late Night Bar Ambience)"

KEYWORD_POOL = [
    "noir jazz bar ambience",
    "late-night jazz bar",
    "smoky jazz bar ambience",
    "rainy night jazz bar ambience",
    "midnight jazz bar ambience",
    "quiet late-night jazz bar",
]

MELANCHOLIC_PHRASES = [
    "You Can Leave The Light On", "I Kept Your Seat Warm", "We Stayed Until The Rain", "You Said Nothing For Hours",
    "The Ice Melted Before Words", "I Heard You At Closing", "You Looked Past The Neon", "No One Asked Why Tonight",
    "I Poured Another Quiet One", "The Room Felt Smaller Tonight", "Your Coat Still Smelled Like Rain", "We Let The Song Finish",
    "You Smiled Then Looked Away", "I Never Cleared Your Glass", "The Door Chime Sounded Lonely", "We Talked In Half Sentences",
    "I Counted Empty Stools Again", "You Stayed Past Last Call", "The Rain Answered For You", "You Asked For Something Soft",
    "I Kept The Volume Low", "You Held The Warm Glass", "The Night Sat Between Us", "I Let The Silence Breathe",
    "You Said You Were Fine", "I Pretended To Believe You", "Your Voice Fell With The Rain", "No One Touched The Jukebox",
    "I Rinsed Glasses Very Slowly", "You Watched The Streetlights Fade", "The Bar Top Held Your Hands", "We Waited Out Another Storm",
    "You Whispered Not Tonight", "I Nodded And Poured", "The Neon Trembled On Glass", "We Shared A Quiet Cigarette",
    "I Heard Your Tired Laugh", "You Left Before The Chorus", "The Piano Stayed After Hours", "I Closed The Door Gently",
    "You Came In Soaking Wet", "I Knew You Needed Quiet", "The Ashtray Filled With Rain", "You Asked If It Gets Better",
    "I Said Stay A Minute", "The Clock Moved Like Smoke", "You Watched The Bourbon Spin", "I Wiped The Counter Twice",
    "You Looked Like Last Winter", "The Street Was All Reflections", "I Saved The Corner Booth", "You Traced Circles On Wood",
    "I Heard The Hurt In You", "The Window Caught Your Sigh", "You Asked For The Same Song", "I Let It Play Again",
    "The Room Forgot To Breathe", "You Talked To Your Shadow", "I Kept The Night Soft", "You Left A Ring On Oak",
    "I Remembered Your Last Goodbye", "You Stayed For One More", "The Rain Hid Your Face", "I Served The Silence Neat",
    "You Said Dont Ask Me", "I Did Not Ask", "The Neon Made Us Honest", "You Held Back Every Word",
    "I Heard The Street Cry", "You Looked Through Me Gently", "The Glassware Sang Quietly", "I Counted To Closing Again",
    "You Asked For No Questions", "I Dimmed The Back Light", "The Door Closed Like A Whisper", "You Sat Where She Sat",
    "I Knew Before You Spoke", "You Left Your Change Behind", "The Booth Stayed Warm", "I Saw Rain In Your Eyes",
    "You Said It Was Nothing", "I Poured Something Gentle", "The Night Needed Less Noise", "You Stayed For The Slow Song",
    "I Heard Your Chair Creak", "You Asked For Another Minute", "The Alley Stayed Blue", "I Could Not Fill The Quiet",
    "You Looked At The Empty Stool", "I Polished The Same Glass", "The Rain Kept Time Outside", "You Whispered Keep It Low",
    "I Let The Bassline Linger", "You Waited For Last Orders", "The Mirror Held Your Silence", "I Knew Youd Be Back",
    "You Said Dont Turn It Up", "I Left The Door Unlocked", "The Night Leaned On The Bar", "You Breathed In Wood Smoke",
    "I Heard The Chime Twice", "You Stayed Until Lights Dimmed", "The Counter Knew Your Hands", "I Let The Rain Play",
    "You Asked If Anyone Stays", "I Said Some Of Us Do", "The Glass Fogged Then Cleared", "You Looked At Nothing Long",
    "I Poured The Last Slow One", "You Left Before Sunrise", "The Stools Faced Empty Streets", "I Kept The Bar Quiet",
    "You Said Keep The Rain Outside", "I Left Your Water Near", "The Bar Clock Felt Heavy Tonight", "You Sat Through Closing Music",
    "I Heard Your Breath Go Quiet", "You Asked For Window Light", "The Night Stayed At My Shoulder", "I Saved The Last Clean Glass",
]

NARRATIVE_LINES = [
    "I stand behind the bar and keep the room soft enough for heavy thoughts.",
    "From behind the bar, I watch rain slide down neon like tired handwriting.",
    "I rinse the same glass twice while the piano settles into the wood.",
    "I keep my voice low because the night already sounds bruised.",
    "Behind the bar, I read shoulders before I read faces.",
    "I wipe the counter slowly and let the silence sit between chords.",
    "I line up empty tumblers like small confessions no one signed.",
    "I keep the amber light low so nobody has to explain themselves.",
    "Behind the bar, I can hear rain before the door even opens.",
    "I nod, pour, and let people borrow the dark for a while.",
    "I watch lonely stools hold more stories than crowded tables.",
    "Behind the bar, every pause sounds like a memory coming back.",
]

OVERHEARD_QUOTES = [
    "You okay?",
    "I'll stay a minute.",
    "Don't make it loud.",
    "Leave the door cracked.",
    "I just needed somewhere warm.",
    "Can you keep the lights low?",
    "Not tonight, just music.",
    "Pour the same as last time.",
    "I don't want to talk about it.",
    "Let the song finish first.",
    "You can stop asking now.",
    "I thought I'd feel better by now.",
    "Can I sit here a little longer?",
    "No rush, I know you're closing.",
]

SEO_CONTEXT = ["jazz for reading", "jazz for studying", "jazz for work"]

ABOUT_NAD_LINES = [
    "Notes After Dark (NAD) curates melancholic jazz-noir worlds for late hours.",
    "Rain, neon, smoke, and quiet conversation shape every release.",
    "Built for listeners who need focus, calm, and a little shelter after midnight.",
]

OPTIONAL_LATE_LINES = [
    "If you're still awake, this room is yours for a little while.",
    "For anyone working through the night, keep the volume low and stay with us.",
    "If the city feels too loud tonight, let this mix breathe beside you.",
    "For late-night listeners, this one is a gentle place to land.",
]

TAG_POOL = [
    "noir jazz", "dark noir jazz", "late-night bar ambience", "noir jazz bar ambience", "late-night jazz bar",
    "smoky jazz bar ambience", "midnight jazz ambience", "jazz bar atmosphere", "melancholic jazz mix", "rainy night jazz",
    "neon bar ambience", "faceless bartender vibe", "soft piano noir jazz", "saxophone night jazz", "quiet bar music",
    "jazz for reading", "jazz for studying", "jazz for work", "after hours jazz", "city rain jazz ambience",
    "cinematic jazz noir", "night writing music", "late-night focus music", "moody instrumental jazz", "urban night jazz",
    "empty stool ambience", "last call jazz", "cigarette glow ambience", "wood bar top ambience", "slow burn jazz",
    "notes after dark", "NAD jazz", "lonely bar soundtrack", "midnight lounge jazz", "soft neon jazz",
]

CHAPTERS_TEMPLATE = [
    "00:00 Door Chime In The Rain",
    "04:40 Glass Rinse And Neon Drip",
    "09:30 Empty Stool, Quiet Piano",
    "14:10 Cigarette Glow By The Window",
    "18:45 Quiet Confession At The Counter",
    "24:20 Last Call, Slow Footsteps",
    "29:50 Lights Dim Over Wet Wood",
]

THUMBNAIL_VARIANTS = [
    "Faceless bartender hands polishing a glass over a worn wood bar top, lonely empty stool in frame, soft neon reflections, light smoke haze, cinematic grain, melancholic mood, quiet rain outside, 16:9 YouTube thumbnail composition, no text, no visible face, no logos.",
    "Close detail of bar counter with whiskey glass, ring marks, and folded napkin, blurred faceless bartender in background, magenta-blue neon reflections, soft smoke haze, lonely late-night atmosphere, cinematic grain, 16:9 YouTube thumbnail composition, no text, no visible face, no logos.",
    "Faceless bartender silhouette behind bottles and glassware, empty stools, rainy window reflections, gentle neon glow, subtle smoke haze, melancholic late-night bar ambience, cinematic grain, 16:9 YouTube thumbnail composition, no text, no visible face, no logos.",
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
    parser.add_argument("--base-date", help="Base date in YYYY-MM-DD (simulates now in America/Chihuahua).")
    parser.add_argument("--output-dir", default="nad-agent/packages", help="Output directory for markdown files.")
    return parser.parse_args()


def get_base_date(raw: str | None) -> date:
    if raw:
        return date.fromisoformat(raw)
    return datetime.now(TZ).date()


def seed_from(*parts: str) -> int:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()
    return int(digest[:16], 16)


def pick_series_for_date(publish_date: date, slot_index: int) -> str:
    week_index = publish_date.isocalendar().week % len(SERIES)
    return SERIES[(week_index + slot_index) % len(SERIES)]


def next_publish_dates(now_date: date, count: int = 3) -> list[tuple[date, str]]:
    dates: list[tuple[date, str]] = []
    cursor = now_date + timedelta(days=1)
    while len(dates) < count:
        if cursor.weekday() in PUBLISH_WEEKDAYS:
            dates.append((cursor, PUBLISH_WEEKDAYS[cursor.weekday()]))
        cursor += timedelta(days=1)
    return dates


def build_contexts(base: date) -> list[PackageContext]:
    contexts: list[PackageContext] = []
    for idx, (publish_date, weekday_label) in enumerate(next_publish_dates(base, 3)):
        series = pick_series_for_date(publish_date, idx)
        rng = random.Random(seed_from("ctx", str(publish_date), series))
        contexts.append(
            PackageContext(
                publish_date=publish_date,
                weekday_label=weekday_label,
                series=series,
                keyword=rng.choice(KEYWORD_POOL),
                duration_target=rng.choice(DURATION_TARGETS),
            )
        )
    return contexts


def pick_week_phrases(contexts: list[PackageContext]) -> dict[str, list[str]]:
    week_key = "|".join(sorted(c.publish_date.isoformat() for c in contexts))
    rng = random.Random(seed_from("phrases", week_key))
    chosen = rng.sample(MELANCHOLIC_PHRASES, k=9)
    by_date: dict[str, list[str]] = {}
    for i, ctx in enumerate(contexts):
        by_date[ctx.publish_date.isoformat()] = chosen[i * 3 : i * 3 + 3]
    return by_date


def format_title(phrase: str) -> str:
    return f"{phrase} | {TITLE_SUFFIX}"


def build_micro_story(ctx: PackageContext) -> str:
    rng = random.Random(seed_from("story", str(ctx.publish_date), ctx.series))
    total_lines = rng.randint(8, 12)
    quote_count = rng.randint(4, min(6, total_lines - 3))
    narrative_count = total_lines - quote_count

    narrative = rng.sample(NARRATIVE_LINES, k=narrative_count)
    quotes = rng.sample(OVERHEARD_QUOTES, k=quote_count)

    lines: list[str] = []
    lines.append(narrative[0])
    ni = 1
    qi = 0
    while ni < len(narrative) or qi < len(quotes):
        if qi < len(quotes):
            lines.append(f'"{quotes[qi]}"')
            qi += 1
        if ni < len(narrative):
            lines.append(narrative[ni])
            ni += 1
    return "\n".join(lines[:total_lines])


def build_seo_paragraph(ctx: PackageContext) -> str:
    rng = random.Random(seed_from("seo", str(ctx.publish_date), ctx.series))
    context_term = rng.choice(SEO_CONTEXT)
    return (
        f"A mellow {ctx.keyword} set shaped by noir jazz textures and late-night bar ambience, "
        f"ideal as {context_term} when the city goes quiet."
    )


def build_about_nad(ctx: PackageContext) -> str:
    rng = random.Random(seed_from("about", str(ctx.publish_date), ctx.series))
    lines = rng.sample(ABOUT_NAD_LINES, k=2)
    if rng.random() < 0.35:
        lines.append(rng.choice([l for l in ABOUT_NAD_LINES if l not in lines]))
    return "\n".join(lines)


def pick_tags(ctx: PackageContext) -> str:
    rng = random.Random(seed_from("tags", str(ctx.publish_date), ctx.series))
    tags = TAG_POOL[:]
    rng.shuffle(tags)
    return ", ".join(tags[: rng.randint(22, 30)])


def build_markdown(ctx: PackageContext, phrases: list[str]) -> str:
    rng = random.Random(seed_from("optional", str(ctx.publish_date), ctx.series))
    titles = [format_title(p) for p in phrases]
    story = build_micro_story(ctx)
    seo = build_seo_paragraph(ctx)
    about_nad = build_about_nad(ctx)
    tags_line = pick_tags(ctx)
    thumbnail_variants = "\n".join(f"- Variant {i + 1}: {v}" for i, v in enumerate(THUMBNAIL_VARIANTS))
    chapters = "\n".join(f"- {c}" for c in CHAPTERS_TEMPLATE)

    return f"""---
date: {ctx.publish_date.isoformat()}
weekday: {ctx.weekday_label}
series: {ctx.series}
keyword: {ctx.keyword}
duration_target: {ctx.duration_target}
---

# Titles
- **Final title:** {titles[0]}
- **Alternate 1:** {titles[1]}
- **Alternate 2:** {titles[2]}

# Description (YouTube)
## Noir micro-story
{story}

## SEO paragraph
{seo}

## About NAD
{about_nad}

## Optional late-hours line
{rng.choice(OPTIONAL_LATE_LINES)}

# Tags (22–30)
{tags_line}

# Chapters (template)
> Replace timestamps after final mix export.

{chapters}

# Pinned comment
I kept the lights low for this one. Where are you listening from tonight? 🌧️🥃

# 3 engagement comments
1. Which detail hits you harder tonight: the rain, the glassware, or the silence?
2. Are you listening while reading, studying, or working late?
3. What bar moment should open the next mix: door chime, empty stool, or last call?

# Thumbnail prompts (NAD style)
{thumbnail_variants}
"""


def slugify_series(series: str) -> str:
    return series.lower().replace(" ", "-")


def write_packages(contexts: list[PackageContext], output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    for old in output_dir.glob("*.md"):
        old.unlink(missing_ok=True)

    phrase_map = pick_week_phrases(contexts)
    written: list[Path] = []
    for ctx in contexts:
        filename = f"{ctx.publish_date.isoformat()}_{ctx.weekday_label}_{slugify_series(ctx.series)}.md"
        target = output_dir / filename
        target.write_text(build_markdown(ctx, phrase_map[ctx.publish_date.isoformat()]), encoding="utf-8")
        written.append(target)
    return written


def main() -> None:
    args = parse_args()
    contexts = build_contexts(get_base_date(args.base_date))
    for p in write_packages(contexts, Path(args.output_dir)):
        print(p.as_posix())


if __name__ == "__main__":
    main()
