# nad-agent

Generador semanal de paquetes de publicación para **Notes After Dark (NAD)**, con enfoque jazz noir y salida en Markdown.

## Qué genera
Cada ejecución crea 3 archivos en `nad-agent/packages/` para:
- Martes
- Jueves
- Sábado

En la zona horaria `America/Chihuahua`, con:
- Frontmatter YAML (`date`, `weekday`, `series`, `keyword`, `duration_target`)
- Título final + 2 alternativos
- Descripción (micro-historia noir + SEO + bloque de marca NAD)
- 20–30 tags
- Plantilla de chapters
- Comentario fijado + 3 comentarios de engagement
- Prompt de miniatura en estilo NAD

## Series en rotación automática
La rotación semanal evita repetición:
1. After Hours
2. Case Files
3. Blue Alley Sessions

El orden se calcula con la semana ISO (determinístico).

## Requisitos
- Python 3.11+

## Uso local
Desde la raíz del repo:

```bash
python3 nad-agent/src/generate_packages.py
```

Opcionalmente puedes fijar una fecha base para reproducibilidad:

```bash
python3 nad-agent/src/generate_packages.py --base-date 2026-02-16
```

## Publicación sugerida (flujo)
1. Ejecuta el generador.
2. Revisa el archivo del día a publicar.
3. Ajusta chapters con timestamps reales del render final.
4. Copia título, descripción, tags y comentario fijado a YouTube Studio.
5. Usa el prompt de miniatura para crear una portada consistente con NAD.

## Cómo evitar problemas de "reused content"
Refuerza identidad de serie y autoría en cada publicación:
- Mantén intros/outros de marca con firma sonora NAD.
- Conserva continuidad narrativa (After Hours / Case Files / Blue Alley Sessions).
- Usa descripciones originales con micro-historias nuevas cada episodio.
- Personaliza miniaturas con un lenguaje visual propio (neón, lluvia, humo, noir).
- Publica comentarios fijados contextuales para demostrar curaduría activa.
- Evita reciclar exactamente la misma estructura textual entre videos; usa variantes.

## Estructura

```text
nad-agent/
  packages/            # Salida generada
  prompts/             # Guías de serie y plantilla
  src/
    generate_packages.py
  README.md
```
