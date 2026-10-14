# editor-reels

**Edita tus reels con IA, con tu marca.** Una skill para Claude Code (y Codex) que primero te
entrevista —tu marca, tus colores, tu tipografía, los vídeos que te gustan, tus formatos, tus
efectos de sonido— y luego edita tus clips con ese estilo.

Tú grabas. Le pasas los clips y le cuentas qué quieres. Te devuelve el reel montado:

- sin silencios ni tomas repetidas
- subtítulos con resalte palabra a palabra, en tus colores y tu fuente
- hook de texto, tarjetas, diagramas animados, B-roll, logos de las marcas que nombras
- efectos de sonido (los tuyos o un kit libre de derechos) y CTA a tu manera
- exportado a 1080x1920, −14 LUFS y color correcto para Instagram, TikTok y Shorts

Todo corre en tu ordenador: la transcripción es local (Whisper), no se sube nada a ningún sitio.

## Cómo funciona

1. **La primera vez** te hace una entrevista de ~10 minutos y guarda tu estilo en
   `~/editor-reels/marca/` (un `perfil.json` y un `ESTILO.md` que puedes leer y editar).
   Termina con un vídeo de demo con tu estilo.
2. **Cada vídeo**: dejas tus clips en una carpeta y le dices, por ejemplo, *«es un tutorial
   de 3 trucos de Canva, cierra pidiendo que comenten GUÍA»*. Te propone el montaje y un
   plan visual; cuando das el OK, lo construye, lo revisa y lo exporta.
3. **Aprende**: cuando corriges algo («subtítulos más pequeños», «nunca pongas emojis»), te
   ofrece guardarlo para que el siguiente salga bien a la primera.

## Instalación

### Requisitos

- [Node.js](https://nodejs.org) 18 o más nuevo
- [Python](https://python.org) 3.10 o más nuevo
- ~3 GB libres (dependencias + modelo de transcripción)
- Recomendado: [ffmpeg](https://ffmpeg.org) (sin él funciona, con menos opciones de audio)

No hace falta instalarlo todo a mano: la skill revisa lo que falta, te da el comando de tu
sistema y te pide permiso antes de instalar nada.

### Claude Code

```bash
git clone https://github.com/brandingprojects00-svg/editor-reels ~/.claude/skills/editor-reels
```

Abre Claude Code en cualquier carpeta y escribe `/editor-reels` (o «quiero editar mis reels»).

### Codex

```bash
git clone https://github.com/brandingprojects00-svg/editor-reels ~/.codex/skills/editor-reels
```

Pídele «usa la skill editor-reels». Si tu versión de Codex no carga skills, clona el repo en
cualquier carpeta, abre Codex ahí y dile «lee AGENTS.md y empecemos».

### Otros agentes (Cursor, etc.)

Clona el repo y pídele al agente que lea `SKILL.md` y lo siga.

## Qué hay dentro

```
SKILL.md        las instrucciones que sigue el agente (empieza aquí si quieres entenderla)
guias/          instalación, entrevista, flujo de edición, reglas, componentes, audio, avanzado
template/       el proyecto Remotion que se copia para cada vídeo (+ scripts de Python)
formatos/       recetas de estructura: tutorial, lista, problema→solución, storytime…
presets/        paletas de partida si no tienes colores de marca
kit-ejemplo/    cómo se ve un perfil y una guía de estilo ya hechos
avanzado/       plantilla para vídeos horizontales (charlas, Zoom)
```

## Extras recomendados

- **Skills oficiales de Remotion** — ayudan al agente cuando le pides un efecto que la
  plantilla no trae: `npx skills add remotion-dev/skills`.
- Si prefieres animaciones sin cámara (explainers, motion graphics), mira
  [HyperFrames](https://github.com/heygen-com/hyperframes): es otro motor, no se mezcla con este.

## Preguntas frecuentes

**¿Cuánto tarda?** La primera vez, ~20 min entre instalación y entrevista. Después, un reel
de 40 s lleva unos 10-20 min de principio a fin (la mayoría es transcribir y renderizar en tu
ordenador).

**¿Funciona en Windows?** Sí (y en Mac y Linux). En Windows usa una ruta corta y fuera de
OneDrive; la skill te avisa.

**¿Puedo usar mis fuentes y mis efectos?** Sí: fuentes .ttf/.otf, tu logo y tus efectos de
sonido entran en la entrevista.

**¿Y si grabo en horizontal o con pantalla dividida de CapCut?** Hay guías para eso en
`guias/avanzado/`.

## Licencias

- El código propio de este repo: [MIT](LICENSE).
- **[Remotion](https://www.remotion.dev/license)** (el motor de vídeo) tiene su propia licencia:
  gratis para personas, organizaciones sin ánimo de lucro y empresas de hasta 3 personas;
  las empresas más grandes necesitan una licencia de empresa.
- Iconos de [Lucide](https://lucide.dev) (ISC). Logos de marca de [Simple Icons](https://simpleicons.org)
  (CC0; las marcas pertenecen a sus dueños: úsalas solo cuando hables de ellas).
- Efectos del kit de partida: [Freesound](https://freesound.org), solo CC0.
- Fuentes de [Google Fonts](https://fonts.google.com) (OFL). Transcripción con
  [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (MIT).
- Tus clips, tu marca, tus fuentes y tus efectos son tuyos y nunca salen de tu ordenador.
