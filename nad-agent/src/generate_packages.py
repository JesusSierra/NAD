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
DAY_SLOTS = [(1, "TUE"), (3, "THU"), (5, "SAT")]  # Monday=0
DURATION_TARGETS = ["34:00", "42:00", "58:00", "1:06:00", "1:18:00"]

SERIES_KEYWORDS = {
    "After Hours": [
        "jazz noir para estudiar",
        "night jazz ambience",
        "lluvia y saxofón",
        "música para escribir de noche",
        "smooth noir jazz",
        "late night coffee jazz",
    ],
    "Case Files": [
        "detective jazz playlist",
        "misterio urbano con jazz",
        "dark academia jazz",
        "film noir soundtrack vibes",
        "jazz cinematográfico",
        "lofi noir detective",
    ],
    "Blue Alley Sessions": [
        "smoky bar jazz",
        "club de jazz nocturno",
        "sax and smoke ambience",
        "jazz para leer",
        "vintage noir jazz",
        "chill jazz de madrugada",
    ],
}

TITLE_PATTERNS = {
    "After Hours": [
        "After Hours: Lluvia sobre neón y vasos vacíos",
        "Después de Medianoche | Jazz Noir para Calles Mojadas",
        "After Hours Noir — Sax, Humo y Ciudad Despierta",
    ],
    "Case Files": [
        "Case Files: El expediente de la esquina azul",
        "Archivo Nocturno | Detective Jazz en la Ciudad",
        "Case Files Noir — Pistas en humo y contrabajo",
    ],
    "Blue Alley Sessions": [
        "Blue Alley Sessions: Bajo la luz del callejón",
        "Sesión en Callejón Azul | Rainy Jazz Noir",
        "Blue Alley Sessions — Midnight Bar Stories",
    ],
}

MICRO_STORY_LINES = [
    "La barra respiraba despacio, como si conociera cada secreto del barrio.",
    "Una gabardina goteando dejó una moneda sobre el piano y pidió silencio.",
    "El sax cayó como lluvia tibia sobre las mesas de madera vieja.",
    "Afuera, el neón rojo titiló tres veces: señal de que alguien mentía.",
    "Nadie preguntó nombres; aquí solo hablan los vasos y el contrabajo.",
    "Cuando la batería entró, hasta las sombras parecieron bailar con culpa.",
    "La noche abrió otro expediente y lo selló con humo azul.",
    "El último tren pasó de largo, pero la melodía se quedó en la estación.",
]

SEO_TEMPLATES = [
    "Disfruta este set de {keyword} ideal para concentrarte, estudiar, escribir o ambientar noches lluviosas con estética film noir.",
    "Si buscabas {keyword}, jazz nocturno y atmósfera cinematográfica, este mix te acompaña en sesiones de trabajo, lectura y madrugada.",
    "Este episodio combina {keyword}, ambiente de bar vintage y texturas lo-fi para fans de la estética noir, dark jazz y playlists de enfoque.",
]

ABOUT_NAD = (
    "Notes After Dark (NAD) es un canal de jazz noir: historias nocturnas, lluvia, "
    "neón y humo convertidos en música para pensar, crear y perderse un rato en la ciudad."
)

TAG_POOL = [
    "jazz noir",
    "noir jazz",
    "dark jazz",
    "night jazz",
    "jazz para estudiar",
    "jazz para trabajar",
    "jazz para leer",
    "rainy night ambience",
    "saxophone jazz",
    "smooth jazz noir",
    "city night jazz",
    "música instrumental",
    "música para concentración",
    "film noir music",
    "detective jazz",
    "lofi jazz noir",
    "midnight jazz",
    "café nocturno",
    "ambiente lluvioso",
    "jazz cinematográfico",
    "smoky jazz bar",
    "playlist de madrugada",
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
    "Cantinero sin rostro en primer plano, barra de madera mojada, neón magenta/azul reflejado en cristales, humo suave, grano fílmico, contraste alto, estética jazz noir cinematográfica, sin texto.",
    "Calle lluviosa con neones desenfocados, silueta con paraguas y saxofón al fondo, charcos con reflejos cian/rojo, atmósfera de misterio, composición vertical para miniatura, sin rostro visible, sin texto.",
    "Saxofón sobre mesa con vaso de whisky y humo en espiral, luz lateral azul profundo, fondo de club oscuro, partículas en el aire, look analógico 35mm, estilo noir elegante, sin texto.",
]


@dataclass
class PackageContext:
    publish_date: date
    weekday_label: str
    series: str
    keyword: str
    duration_target: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera paquetes semanales para Notes After Dark")
    parser.add_argument(
        "--base-date",
        help="Fecha base en formato YYYY-MM-DD (zona America/Chihuahua).",
    )
    parser.add_argument(
        "--output-dir",
        default="nad-agent/packages",
        help="Directorio de salida para archivos markdown.",
    )
    return parser.parse_args()


def get_base_date(raw: str | None) -> date:
    if raw:
        return date.fromisoformat(raw)
    return datetime.now(TZ).date()


def monday_anchor(d: date) -> date:
    return d - timedelta(days=d.weekday())


def seed_from(*parts: str) -> int:
    joined = "|".join(parts)
    digest = hashlib.sha256(joined.encode("utf-8")).hexdigest()
    return int(digest[:16], 16)


def pick_week_series(week_monday: date) -> list[str]:
    rotation_index = week_monday.isocalendar().week % len(SERIES)
    return [SERIES[(rotation_index + i) % len(SERIES)] for i in range(3)]


def build_contexts(base: date) -> list[PackageContext]:
    week_monday = monday_anchor(base)
    weekly_series = pick_week_series(week_monday)
    contexts: list[PackageContext] = []

    for idx, (weekday_num, weekday_label) in enumerate(DAY_SLOTS):
        publish_date = week_monday + timedelta(days=weekday_num)
        series = weekly_series[idx]
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
    lines = rng.sample(MICRO_STORY_LINES, k=4)
    return "\n".join(lines)


def pick_tags(ctx: PackageContext) -> str:
    rng = random.Random(seed_from("tags", str(ctx.publish_date), ctx.series))
    tags = TAG_POOL[:]
    rng.shuffle(tags)
    count = rng.randint(22, 26)
    selected = tags[:count]
    return ", ".join(selected)


def build_markdown(ctx: PackageContext) -> str:
    title_final, alternates = pick_titles(ctx)
    story = build_micro_story(ctx)
    rng = random.Random(seed_from("seo", str(ctx.publish_date), ctx.series))
    seo = rng.choice(SEO_TEMPLATES).format(keyword=ctx.keyword)
    tags_line = pick_tags(ctx)

    thumbnail_variants = "\n".join(
        f"- Variante {i + 1}: {variant}" for i, variant in enumerate(THUMBNAIL_VARIANTS)
    )

    return f"""---
date: {ctx.publish_date.isoformat()}
weekday: {ctx.weekday_label}
series: {ctx.series}
keyword: {ctx.keyword}
duration_target: {ctx.duration_target}
---

# Títulos
- **Título final:** {title_final}
- **Alternativa 1:** {alternates[0]}
- **Alternativa 2:** {alternates[1]}

# Descripción (YouTube)
## Micro-historia noir
{story}

## Párrafo SEO
{seo}

## Sobre NAD
{ABOUT_NAD}

# Tags (20–30)
{tags_line}

# Chapters (plantilla)
> Reemplaza los timestamps según el corte final del video antes de publicar.

- 00:00 Apertura — Lluvia y neón
- 04:40 Primer giro — Sax en el callejón
- 09:30 Interludio — Conversación en la barra
- 14:10 Archivo abierto — Contrabajo y sospechas
- 18:45 Persecución lenta — Batería en escobillas
- 24:20 Última llamada — Piano de madrugada
- 29:50 Cierre — Créditos de la noche

# Comentario fijado
Esta sesión nació para las noches largas. ¿En qué ciudad y a qué hora la estás escuchando? 🌃🎷

# 3 comentarios de engagement
1. ¿Prefieres esta vibra para leer, estudiar o conducir de noche?
2. Si esta sesión fuera una escena de película noir, ¿qué estaría pasando?
3. ¿Qué elemento quieres para el próximo episodio: más lluvia, más sax o más piano?

# Prompt de miniatura (estilo NAD)
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
