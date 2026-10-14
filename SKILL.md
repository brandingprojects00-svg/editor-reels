---
name: editor-reels
description: Edita reels, TikToks y Shorts verticales (1080x1920) a partir de clips grabados a cámara, con el estilo de marca de cada persona. La primera vez entrevista al usuario (marca, colores, tipografía, logo, vídeos de referencia, formatos, efectos de sonido, tono) y guarda su perfil; después basta con soltar los clips y una descripción para que monte el vídeo con Remotion: quita silencios y tomas repetidas, subtítulos palabra a palabra, hook, tarjetas, diagramas, B-roll, logos, efectos, CTA y export listo para redes. Úsala cuando el usuario quiera "editar mi reel", "montar este vídeo", "ponerle subtítulos a mis clips", "configurar mi estilo de edición", "cambiar mi marca" o retocar un reel ya montado.
---

# editor-reels

Editor de reels con IA que se adapta a la marca de cada persona. Tres modos; decide cuál
según el estado y lo que pida el usuario.

## Antes de nada: dónde vive cada cosa

- **Esta carpeta (la skill)**: instrucciones (`guias/`), plantilla Remotion (`template/`),
  presets de color (`presets/`) y recetas de formato (`formatos/`). No se escribe aquí.
- **La casa del usuario**: `~/editor-reels/` (o `$EDITOR_REELS_HOME`). Ahí van:
  - `marca/perfil.json` (datos técnicos) y `marca/ESTILO.md` (su guía de estilo en prosa),
    `marca/fuentes/`, `marca/logos/`, `marca/sfx/`, `marca/musica/`, `marca/referencias/`
  - `proyectos/<nombre>/` — un proyecto Remotion por vídeo, con `input/` para sus clips
  - `.venv/` y `models/` — el entorno de Python y Whisper

`<skill>` en las guías es la ruta de esta carpeta. Todos los comandos se corren **dentro del
proyecto** (`~/editor-reels/proyectos/<nombre>/`) con `python scripts/…`. En Windows usa
`python`; en Mac/Linux, si `python` no existe, `python3`.

```bash
ls ~/editor-reels/marca/perfil.json 2>/dev/null && echo "CON PERFIL" || echo "SIN PERFIL"
```

## Modo 1 — Primera vez (sin perfil)

1. **Instalación**: lee `guias/instalacion.md`. Corre el doctor, explica lo que falte y
   **pide permiso antes de instalar cualquier cosa**.
2. **Entrevista**: lee `guias/entrevista.md` y síguela. Termina con `marca/perfil.json`,
   `marca/ESTILO.md` y un **render de demo con su estilo**.
3. Dile cómo se usa a partir de ahora: «suelta tus clips en una carpeta y cuéntame qué
   quieres hacer con ellos».

Si tiene prisa: ofrece arrancar con un preset de `presets/` y hacer la entrevista
completa después. Nunca edites su primer vídeo sin al menos colores, tipografía y @.

## Modo 2 — Editar (con perfil + clips)

Lee **siempre** antes de empezar: `marca/ESTILO.md` y `marca/perfil.json` del usuario.
Son tan obligatorios como las reglas de la skill: `notas.evitar` son prohibiciones.

Después sigue `guias/editar.md`. Resumen:

1. Proyecto nuevo desde `template/` + perfil aplicado.
2. Sondea y transcribe los clips.
3. **Montaje bruto** (`montaje.py`): propone cortes (silencios, tomas repetidas) → el
   usuario confirma → une todo.
4. **Plan visual** (`work/plan.md`) a partir de su descripción, su ESTILO.md y la receta del
   formato → **el usuario lo aprueba** antes de construir nada.
5. Construye `cortes.json`, revisa stills, comprueba que nada tape la cara.
6. Render + export → `proyectos/<nombre>/final/`. Enseña fotogramas y pide feedback.

Guías de consulta mientras construyes: `guias/reglas.md` (las reglas que no se negocian,
geometría, QA), `guias/componentes.md` (hook, tarjetas, diagramas, B-roll, logos, CTA),
`guias/audio.md` (efectos y música). Casos especiales en `guias/avanzado/`.

## Modo 3 — Ajustar el estilo

«Cambia mis colores», «quiero otra fuente», «añade un formato», «tengo efectos nuevos»,
«ya no quiero emojis» → repite **solo** las preguntas afectadas de `guias/entrevista.md`,
actualiza `perfil.json` **y** `ESTILO.md`, y vuelve a correr `python scripts/aplica_perfil.py`
en los proyectos abiertos.

## La skill aprende

Cada vez que el usuario corrija algo de estilo durante una edición («subtítulos más
pequeños», «nunca pongas X», «me gusta más así»), **ofrécele guardarlo**: en `perfil.json` si
es un valor técnico, en `ESTILO.md` (sección «Aprendido») si es criterio. Así la siguiente
pieza sale bien a la primera. Es lo que hace que esta skill sea *suya*.

## Cómo preguntar

Si tienes una herramienta de preguntas con opciones (p. ej. `AskUserQuestion` en Claude
Code), úsala: rondas de hasta 4 preguntas con opciones y vista previa. Si no la tienes
(Codex u otros), pregunta en el chat en bloques cortos y numerados, con las opciones
escritas, y espera la respuesta antes de seguir.

## Principios

- **Pide permiso** antes de instalar algo, descargar de internet o borrar archivos del usuario.
- **No inventes datos**: cifras, precios, nombres y logos salen del audio, de la pantalla o
  de una fuente consultada. Si no hay, se pregunta o se omite.
- **El subtítulo sigue al audio**: corrige errores del transcriptor, nunca al hablante.
- **Mira lo que haces**: un render no está terminado hasta que has visto sus fotogramas
  (`scripts/qa.py`). Cuéntale al usuario lo que viste, también lo que no quedó bien.
- **Para crear un efecto que la plantilla no trae**, si está instalada la skill oficial
  `remotion-best-practices`, consúltala antes de escribir el componente.
