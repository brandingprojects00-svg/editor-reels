# La entrevista: conocer a la persona y personalizar la skill

Se hace **una vez** (y por partes cuando quiera cambiar algo). Produce dos archivos en
`~/editor-reels/marca/`:

- **`perfil.json`** — valores técnicos que la plantilla aplica sola (`aplica_perfil.py`).
  Esquema completo comentado: `<skill>/kit-ejemplo/perfil.example.json`.
- **`ESTILO.md`** — su guía de estilo en prosa: quién es, a quién le habla, cómo suena, qué
  le gusta y qué no, cómo son sus formatos. **Se lee antes de cada edición.** Plantilla:
  `<skill>/kit-ejemplo/ESTILO.example.md`.

## Cómo llevarla

- **7 bloques cortos.** Con herramienta de preguntas: hasta 4 preguntas por ronda con
  opciones (y `preview` cuando haya colores o estilos que enseñar). Sin ella: en el chat, en
  bloques numerados con las opciones escritas.
- **Lo que se sube se mira**: manual de marca, logo, capturas, referencias. Ábrelos (PDF e
  imágenes se leen directamente) y extrae tú los datos; luego confirma con la persona.
- **No preguntes lo que ya sabes**: si ya dijo su @ o te pasó su manual, úsalo.
- **Explica para qué es cada pregunta** en media frase la primera vez («para que los
  subtítulos sean de tu color»). Que sienta que la skill se está haciendo para ella.
- Todo es opcional salvo bloque 1 y bloque 2. Si algo no lo sabe, pon un valor razonable y
  anótalo en ESTILO.md como «por decidir: probar con un vídeo real».
- Al final de cada bloque escribe lo que ya tengas en `perfil.json`: si la sesión se corta,
  no se pierde.

## Bloque 1 — Quién eres

Pregunta en el chat (texto libre):

1. ¿Cómo te llamas y qué @ va en los vídeos? (vacío = sin firma) → `nombre`, `handle`
2. ¿A qué te dedicas y de qué hablan tus vídeos? (nicho, producto, servicio)
3. ¿A quién le hablas? (quién te ve, qué sabe, qué le preocupa)
4. ¿Para qué haces los vídeos? Vender · educar · crecer comunidad · marca personal

Con opciones:

5. ¿En qué idioma hablas? Español · Inglés · Portugués · Otro → `idioma`
6. ¿Dónde publicas? (varias) Instagram Reels · TikTok · YouTube Shorts · LinkedIn → `plataformas`

→ Sección «Quién soy» y «Mi audiencia» de ESTILO.md.

## Bloque 2 — Tu marca

1. **¿Tienes manual o guía de marca?** (PDF, imagen, link a Canva/Figma exportado). Si sí:
   léelo, extrae colores (hex), tipografías y reglas («el naranja solo para botones», «nunca
   el logo sobre fondo claro»). Enséñale lo que encontraste y confirma.
2. **Colores.** Si no hay manual: ¿tienes colores de marca (hex o una captura)? Si no,
   ofrece los presets de `<skill>/presets/` con `preview`:
   **Eléctrico** `#3DD6F5` · **Coral** `#FF5A36` + `#FFD23F` · **Lima** `#C6F432` ·
   **Violeta** `#A78BFA` + `#F0ABFC` · **Mono** blanco + `#FFE14D`.
   Con su propio color: ver «Construir la paleta» abajo.
3. **Tipografía.** ¿Usas alguna fuente? Opciones: Inter (neutra, técnica) · Montserrat
   (clásica de redes) · Poppins (redonda, cercana) · Plus Jakarta Sans (moderna) · otra
   Google Font · **un archivo propio** (.ttf/.otf → que lo deje en `marca/fuentes/` y se
   referencia con `archivo`). Puede haber una fuente para títulos y otra para subtítulos.
   La palabra clave gigante va en Anton salvo que diga otra (necesita una condensada).
4. **Logo.** ¿Tienes logo (PNG con fondo transparente o SVG)? → que lo deje en
   `marca/logos/` y anótalo en el perfil:
   `"logo_propio": {"id": "mimarca", "archivo": "logo.png", "nombre": "Mi Marca", "color": "#HEX"}`.
   `aplica_perfil.py` lo registra solo en cada proyecto (se pinta como pegatina redonda con
   anillo de su color; se usa con `"logo": "mimarca"` en tarjetas y chips).
5. ¿Hay marcas/herramientas que nombras a menudo? (Notion, Canva, Shopify…) →
   `marcas_frecuentes` (sus logos salen de Simple Icons al nombrarlas).

### Construir la paleta desde un color propio

`accent` = su color (CTA y detalles que mandan: se usa poco). `highlight` = el resalte de la
palabra que suena en el subtítulo: si su color es claro y saturado, el mismo; si es oscuro,
uno claro que combine (amarillo o una versión clara de su color). `ink` = un negro teñido de
su tono (luminosidad ~5 %). El resto de `presets/electrico.json`. **Si el color es muy oscuro
no se lee sobre vídeo**: díselo y propón una versión más clara para el resalte.

## Bloque 3 — Referencias (lo que más personaliza)

1. «¿Hay vídeos (tuyos o de otros) cuyo estilo de edición te encante?» Pide 1-3.
   - **Archivos**: que los deje en `marca/referencias/`.
   - **Links**: para analizarlos hay que descargarlos. Pide permiso para instalar `yt-dlp`
     en el entorno (`~/editor-reels/.venv/…/python -m pip install yt-dlp`) y bajarlos con
     `python -m yt_dlp -o "~/editor-reels/marca/referencias/%(id)s.%(ext)s" URL`. Solo para
     analizar en local: nunca se reutiliza ese material en sus vídeos.
2. Analiza (dentro de un proyecto, p. ej. el de demo):
   ```bash
   python scripts/analiza_referencia.py ~/editor-reels/marca/referencias/*.mp4
   ```
3. **Mira los fotogramas** que deja en `marca/referencias/analisis/<vídeo>/` y describe lo
   que ves: subtítulos (posición, mayúsculas, tamaño, caja o suelto, una palabra o frase,
   color del resalte), hook (texto arriba, caja, emoji), ritmo (cortes/min del resumen,
   punch-ins), B-roll, diagramas, ventanas flotantes, stickers, colores.
4. Propón cómo traducirlo a su perfil y **pregunta qué quiere copiar y qué no** («¿te gusta
   el subtítulo de una sola palabra o prefieres frases de 3-4?»).

→ Sección «Referencias» de ESTILO.md (qué se toma de cada una y qué no).

## Bloque 4 — Estilo de edición

1. **Ritmo**: Tranquilo (deja respirar, pocos cortes) · Dinámico (sin silencios, cortes
   cada pocos segundos) · Frenético (corte en cada frase, zooms constantes) → `ritmo`
   (`tranquilo` / `dinamico` / `frenetico`; decide el silencio máximo del montaje)
2. **Subtítulos** (con preview): MAYÚSCULAS sueltas con sombra · frase normal suelta con
   sombra · MAYÚSCULAS en píldora oscura · frase normal en píldora →
   `subtitulos.upper`, `subtitulos.band`. Tamaño: normal 80 · grande 92 · discreto 64 →
   `subtitulos.size`. Palabras por página: 1-2 (muy dinámico) · 3-4 (estándar) →
   `subtitulos.maxWords`.
3. **Color de la palabra que suena** cuando nombras una marca: siempre mi resalte · el color
   de esa marca → `subtitulos.byBrand`.
4. **Hook de texto** (el título de los primeros segundos): en caja de color (como un
   sticker) · texto suelto con sombra · sin hook escrito → `hook.estilo`
   (`caja` / `suelto` / `ninguno`), `hook.fondo`, `hook.upper`.
5. **Zooms** (punch-ins): sí, marcados · sutiles · nunca → `punch_ins`
6. **Emojis en pantalla**: sí · nunca → `emojis` (la plantilla no los pone salvo que se pidan)

## Bloque 5 — Formatos

1. **¿Cómo grabas casi siempre?** A cámara en vertical (móvil, cámara) → `camara` ·
   Pantalla dividida de CapCut (captura arriba, cara abajo) → `split` · Horizontal (Zoom,
   charla) → `horizontal` · Pantalla sin cara → `pantalla` → `plano.fuente_habitual`
2. **¿Dónde queda espacio libre en tu plano?** (para rótulos pequeños) A la izquierda de mi
   cara · a la derecha · arriba (estoy centrado) · no sé, mídelo → `plano.espacio_libre`
   (`izquierda` / `derecha` / `arriba`; «no sé» = `izquierda` + medir siempre). Si tiene un
   clip a mano, míralo tú (un fotograma basta) en vez de preguntar.
3. **¿Qué tipo de vídeos repites?** (varias) enseña las recetas de `<skill>/formatos/`:
   tutorial paso a paso · lista / top N · problema → solución · storytime · opinión ·
   antes y después · otro (que lo describa).
   - Para cada formato elegido, copia la receta a ESTILO.md («Mis formatos») y **ajústala
     con lo que diga**: cuánto dura, cómo abre, qué aparece en pantalla, cómo cierra.
   - Si describe uno propio, escríbelo con la misma estructura que las recetas (beats,
     grafismo de cada beat, sonido, cierre). Ejemplo: «voy contando un problema y la
     herramienta que lo soluciona; yo a la derecha, arriba a la izquierda la imagen del
     problema con 1-2 palabras, abajo el nombre de la herramienta, B-roll mientras explico».

## Bloque 6 — Sonido

1. **Efectos y música**: efectos sutiles sin música · efectos + música de fondo · solo
   música · nada, solo mi voz → `audio.efectos`, `audio.musica`
2. Si quiere efectos: **¿tienes efectos que ya uses y te gusten?** (un whoosh, un pop, un
   golpe). Que los deje en una carpeta; escucha qué es cada uno por el nombre o pregúntale,
   y asígnalos a huecos:
   ```bash
   python scripts/sfx_propios.py ruta/swoosh.mp3:whoosh_in ruta/boom.wav:impact ruta/pop.wav:pop
   python scripts/sfx_propios.py --lista      # huecos y qué falta
   ```
   Para los huecos vacíos: kit CC0 de Freesound (`guias/audio.md`, necesita una API key
   gratuita) o se dejan sin sonido. Avisa: **efectos con copyright pueden dar reclamaciones**.
3. Si quiere música: sus pistas (con licencia para redes) en `marca/musica/` con un
   `manifest.json` de autor y uso. Sin pistas, sin música (no la inventes ni la descargues
   de cualquier sitio).
4. **¿Qué micro usas?** De solapa o de mano cerca de la boca → `cercano` · el del móvil o la
   cámara → `sala` → `audio.micro` (decide la cadena de audio del export).

## Bloque 7 — Cierre y tono

1. **¿Cómo cierras normalmente?** Pregunta abierta para comentarios · «Comenta PALABRA» y
   mando un recurso por DM · «Sígueme para más» · sin CTA → `cta.tipo`
   (`pregunta` / `keyword` / `seguir` / `ninguno`), `cta.verbo`.
2. En el chat: **«¿Cómo es tu tono?»** («cercano y con humor», «sobrio, para empresas») →
   `notas.tono`. Decide cómo se redactan hooks, kickers y tarjetas.
3. En el chat: **«¿Hay algo que NUNCA quieras ver en tus vídeos?»** («emojis», «que me
   tapes la cara», «transiciones de destello», «palabras en inglés») → `notas.evitar`.

## Al terminar

1. Escribe `perfil.json` y `ESTILO.md` completos (ESTILO.md en segunda persona del
   singular, como notas de un editor que la conoce: concreto, con ejemplos, sin relleno).
2. Enséñale un **resumen en tabla**: colores (con hex), fuentes, subtítulos, hook, ritmo,
   formatos, sonido, cierre, cosas a evitar.
3. **Render de demo con su estilo** (dentro de `~/editor-reels/proyectos/demo`):
   ```bash
   python scripts/aplica_perfil.py
   python scripts/demo_words.py --video          # o --fondo ~/ruta/a/un/clip_suyo.mp4
   cp cortes.example.json cortes.json
   python scripts/gen_data.py --work work --cuts c1 --config cortes.json
   npx remotion still src/index.ts Demo qa/f45.png --frame=45 --image-format=png
   npx remotion still src/index.ts Demo qa/f760.png --frame=760 --image-format=png
   ```
   Mira los stills y enséñaselos (o `python scripts/render.py Demo` para el vídeo entero,
   ~2-5 min). Ajusta lo que no le guste **antes** de su primer vídeo real.
4. Explícale el uso a partir de ahora, en tres líneas:
   «Graba tus clips → déjalos en una carpeta → dime qué quieres hacer con ellos (de qué va,
   qué formato, si hay algo especial). Yo te propongo el montaje y un plan, tú apruebas, y
   te entrego el vídeo».
