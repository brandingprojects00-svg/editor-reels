# Reglas de oro, geometría y QA

Léelo antes de construir el `cortes.json` de cualquier pieza. Son las decisiones que separan un reel que se ve profesional de uno que se ve hecho con plantilla.

## Zonas protegidas — los números correctos

Medido contra las plataformas en orgánico:

```
TikTok   top ~140 · bottom ~334 (450 en ads) · left ~60 · right 140-180
Reels    top ~180 · bottom ~320-420          · left ~60 · right ~120
Shorts   top ~150 · bottom ~350              · left ~50 · right ~120

UNIÓN →  top 180 · bottom 420 · left 70 · right 180
         zona segura: x 70 → 900 · y 180 → 1500
```

- **`right` es el que más se falla**: la columna de acciones de TikTok llega a 180 px.
  Nada de contenido pasa de **x = 900**.
- Un `bottom` de 500 es demasiado prudente: regala 80 px por nada.

### El recorte 4:5 del feed de Instagram — lo que más cuesta recordar

En el **feed principal** el reel se ve a **4:5 recortado desde el centro**: se oculta todo
lo que quede fuera de **y 285 → 1635**. **El CTA va dentro de esa franja o desaparece
justo donde caen la mayoría de las impresiones.** Por eso `KICKER_Y = 300`.

## Cómo encontrar el espacio muerto de una grabación

No lo estimes a ojo: mídelo. Luminancia media por columna y por fila sobre una docena de
fotogramas revela dónde no pasa nada en toda la pieza.

```bash
ffmpeg -v error -i FUENTE -vf "fps=1/6,scale=108:192,format=gray" -f rawvideo -pix_fmt gray - > lum.raw
# promediar por columna y por fila (108x192 bytes por fotograma)
```

Un resultado típico de alguien encuadrado a la derecha:

```
cara            x 480→900 · y 240→700
pared muerta    x  70→480 · todo el alto (por debajo del 55 % del pico)
franja oscura   y   0→240
```

**Las gráficas pequeñas — kicker, CTA, chips de marca — van sobre la pared muerta, no
apiladas abajo.** Es lo que hace que el cuadro deje de parecer vacío sin tocar el plano.
El perfil da un punto de partida (`plano.espacio_libre` → `RAIL` en `theme.ts`); cada
grabación se comprueba.

Para la **silueta** (barba, pelo oscuro) mide el **máximo por columna**, no la media: lo
oscuro tira la media hacia abajo y la barbilla acaba más abajo de lo que dice.

## Geometría de `template/`

```
RAIL         x 70, ancho 430   columna libre (izquierda por defecto; la fija el perfil)
KICKER_Y     300               kicker y CTA; dentro del recorte 4:5
TOPIC_Y      596               chip de marca
TITLE_BAND   cy 940, h 360     760 → 1120
CARD_BAND    cy 965, h 350     790 → 1140, ancho x 70 → 900
CAPTION_CY   1290              2 líneas a 80px caben entre 1188 y 1392
HANDLE_Y     1445
```

**Sin barra de progreso**: come espacio y no dice nada.

`theme.ts` tiene dos partes: el bloque **PERFIL** (colores, `CAPTIONS`, `RAIL`), que
escribe `scripts/aplica_perfil.py`, y la **geometría**, que se recalibra por fuente. Más
constantes para fuentes de CapCut: `SPLIT_Y` (borde inferior de la captura en un split;
lo mide `layout.py`) y `TOPIC_ALIGN` — `"chip"` (plano lleno), `"inline"` (el logo va
dentro de la línea del kicker y de las secciones) u `"off"` (solo da el color del
resalte). `verifica.py` lee todas de `theme.ts`: recalibrar ahí basta.

## Las reglas que no se negocian

**1. Una tarjeta NUNCA repite lo que dice la voz.**
Contrasta, deduce o remata. Si dice «esta herramienta trabaja contigo y la otra trabaja
por ti», la tarjeta da la consecuencia — *vive mientras la ventana está abierta* vs *sigue
cuando la cierras* — no la frase.

**2. El subtítulo sigue al AUDIO, no a lo que debió decir.**
Se corrigen errores del transcriptor (marcas y palabras técnicas: `Cloud`→`Claude`,
`Chrome Jobs`→`cron jobs`). No se corrige al hablante: si dijo «en 40 segundos» y el reel
dura 76, se queda.

**3. Cada corrección se verifica por CONTEXTO, no por parecido sonoro.**
Documenta cada arreglo con la frase donde vive, en las claves `_fix_...` y `_no_se_toca`
de `cortes.json` (las que empiezan por `_` el script las ignora a cualquier profundidad).

**4. Una sola cosa que leer a la vez.**
Cuando una tarjeta de TEXTO está en pantalla, los subtítulos callan (`hide`). Los chips
pequeños sí conviven: están en otra banda y se leen de un vistazo. Un **diagrama de
iconos** (`Flow.tsx`) tampoco calla a los subtítulos: es visual. Si en tu geometría la
banda de tarjetas pisa la de subtítulos, `FLOW_CAPTION_CY` (theme.ts) los mueve mientras
dura el diagrama; si no la pisa, vale `CAPTION_CY` y no se mueven.

**5. Entrada y salida no son el mismo movimiento invertido.**
El panel entra con barrido lateral y sale desvaneciéndose hacia abajo con desenfoque. El
título entra desde los lados y sale hacia arriba. El chip entra deslizando desde fuera.

**6. El cierre sigue el perfil (`cta.tipo`), y la keyword solo si hay algo que entregar.**
- `keyword`: el chip «comenta PALABRA» existe para disparar un envío por DM. **Solo si el
  audio lo dice y hay un recurso detrás**; sin recurso es un CTA pegado que no lleva a
  ningún sitio. Si no hay, pregunta antes de ponerlo.
- `pregunta`: el remate es una pregunta abierta, humilde y de barrera baja, y casi
  siempre ya está dicha en el propio vídeo — búscala en la transcripción. Va en grande con
  `grandes.pregunta` y `keyword: null`. La misma pregunta sirve para el caption y el
  comentario fijado.
- `seguir` / `ninguno`: un chip corto al final o nada.

**7. El color de acento es para el CTA.**
El resalte del subtítulo usa `COLORS.highlight` o el color de la marca de la que se habla
(`CAPTIONS.byBrand`; `topics` da el color). Si el acento hace seis trabajos a la vez, no
hay jerarquía.

**8. Ningún velo a pantalla completa cuando entra un panel.**
El panel lleva su propio fondo al 0.88 con blur: se lee solo. Un negro sobre TODO el plano
con diez paneles deja a la persona a oscuras media pieza.

**9. Nada tapa la cara.** Se mide y se verifica (`verifica.py`), no se promete. Ver abajo.

**10. Nunca un dato a ojo.** Cifras, precios, segundos y nombres salen de la pantalla, del
audio o de una web consultada, y se anotan en `cortes.json` (`_precios`, `_broll_…`).

## Subtítulos: por qué la palabra NO entra sola

Animar la opacidad de cada palabra con un muelle de ~0.30 s parece bonito y es un error.
Medido sobre un transcript real:

```
páginas 85 · mediana 0.86 s · 55 de 85 por debajo de 1 s
palabras: mediana 0.18 s · 149 de 342 duran menos de 0.15 s
→ el 46 % del tiempo el subtítulo estaba a medio aparecer
```

Por eso:

- **La opacidad de la palabra no se anima nunca.** El movimiento lo lleva un
  desplazamiento en Y escalonado por palabra.
- **La banda no se funde en cada página.** Las páginas son contiguas; lo único que la
  apaga es una tarjeta.
- Lo único que sigue a la voz es el **resalte**. Así se puede leer por delante, que es lo
  que retiene.

`CAPTIONS` en el perfil: `upper`, `size` (80 por defecto), `maxWords` (4), `band` (píldora
o texto suelto con trazo y sombra), `byBrand`. `MERGE_LIMIT = 5` para una banda de 720 px:
con 7 palabras a 84 px se van a tres líneas y chocan con el handle.

Muelles: `damping 200` con `stiffness 260` está **sobre**amortiguado (ζ ≈ 9.8) y entra
lentísimo. Para asentar en ~0.12 s hace falta ζ ≈ 1: `{ damping: 20, mass: 0.4, stiffness: 250 }`.

Whisper llega a meter 6 palabras en 0.18 s; esas páginas se **fusionan** con la vecina
(`MIN_PAGE_MS 950`) y tienen techo (`MAX_PAGE_MS 2200`).

El resalte escala la palabra activa a 1.09 desde su centro, así que invade a la vecina:
el margen entre palabras se calcula **una vez por página** a partir de la palabra más
larga (≈0.58em por carácter a peso 800). Con margen fijo «CON DESARROLLO» se leía
«CONDESARROLLO». Si cambias a una fuente muy ancha, revisa un still con palabras largas.

## Correcciones ancladas en tiempo

```json
"fix": { "cloud@16.70": "Nextcloud", "next@16.50": "", "24@86.48": "24/7" }
```

`"token@12.34"` solo corrige la ocurrencia que empieza en ese segundo (±0.06 s), para
palabras comunes que una corrección global pisaría. `""` borra el token. `gen_data.py`
**avisa si un ancla no casa**.

## Cruces, transiciones y ritmo

- **La rampa va POR DENTRO**: cuando una tarjeta releva a los subtítulos, la rampa de los
  subtítulos va dentro del tramo `hide`. Los dos se cruzan en vez de dejar un hueco.
- **Transiciones en un plano continuo: con movimiento, no con destellos de color.** Golpe
  de escala (+5 %), desenfoque corto (2.6 px) y +10 % de brillo, 0.06 s de subida y 0.28 de
  caída (`impulse()` en `Plate.tsx`). Un lavado de color a pantalla completa se lee como
  fallo de render.
- **Los punch-ins tienen que verse**: ×1.09 no se percibe. ×1.16–×1.22 con muelle, origen
  `50% 42%` para crecer alrededor de la cara.
- **Jump cuts de CapCut** (mismo encuadre): `gt(scene,0.2)` no los ve; salen con **0.05**,
  mezclados con gestos, y se separan porque coinciden con marcas del guion. Sobre un jump
  cut: **alterna la escala en `spans`** (1.0 / 1.13). `punches: []` — un golpe encima de un
  corte real se lee doble.
- **Scrim mínimo**: 0.30 arriba, 0.42 abajo, centro limpio. Más enterraba el decorado.

## Nada tapa la cara — y se comprueba

```bash
python scripts/caras.py       # pista de caras + ventanas sin cara
python scripts/subtitulos.py  # cap_zones bajo la barbilla
python scripts/aparta.py --escribe
python scripts/verifica.py    # el juez
```

- **`caras.py`** (YuNet) devuelve las **ventanas SIN cara**. Fuera de ahí, un panel fijo a
  ancho completo no cabe. Dos cajas: **casco** (con pelo/barba: lo que un panel no invade)
  y **cara** (frente → barbilla: lo que NADA tapa). **Calibra la caja contra un still.**
- **`verifica.py` manda**: fotograma a fotograma, sale con código 1 si algo pisa la cara.
  Encadénalo antes del render.
- **`subtitulos.py`** coloca los subtítulos bajo la barbilla (2 líneas a 72 px) o al lado
  libre (`x0`/`x1`). Si no hay salida, lo dice y los oculta en ese tramo.
- **`aparta.py`**: cuando la cara sube a la banda del raíl, kicker y chips **se desvanecen
  y vuelven solos** (rampa de 0.3 s: más corta parece un parpadeo de error).

## QA antes de renderizar entero

Un render completo son minutos; un `still`, segundos.

```bash
npx remotion still src/index.ts MiCorte qa/f660.png --frame=660 --image-format=png   # un fotograma antes de renderizar
python scripts/qa.py out/MiCorte.mp4                        # ritmo: un fotograma cada 3 s
python scripts/qa.py out/MiCorte.mp4 --desde 20.95 --n 6    # una animación paso a paso
```

**Mira las imágenes** (no basta con que el script termine): el agente las abre y las revisa.

En la tira de contacto se ve la monotonía: si 22 de 24 fotogramas son el mismo plano con
la misma caja abajo, faltan eventos visuales. **Se arregla con B-roll de verdad, no con más
tarjetas**; si no hay material, dilo en vez de rellenar. Excepción: en una demo de
pantalla ilegible en el móvil, las `escenas` SON el B-roll.

Antes de entregar, repasa el perfil: ¿algo de `notas.evitar` se coló?

## Trampas conocidas (ya resueltas en la plantilla; no las reintroduzcas)

- **Las notas `_` de `fix`** se filtran ANTES de normalizar; si no, `"_nota"` se volvía
  `"nota"` y pisaba una corrección real.
- **Las claves `_` dentro de tarjetas** se quitan a cualquier profundidad (`sin_notas()`);
  si no, rompen el typecheck.
- **`spring()` con `Infinity` revienta el render**: un evento que no llega va a un instante
  lejano y finito.
- **Remotion no sirve symlinks desde `public/`**: 404. Copia o enlace duro.
- **`remotion still` exige que la extensión case con `--image-format`.**
- **Windows y macOS no distinguen mayúsculas**: nombres de QA en minúsculas (`qa/f675.png`).
- **whisper con varios ficheros a la vez escribe todos en el mismo JSON.** Un fichero por
  llamada, y comprueba que la duración del transcript cuadra con la del audio.
- **Whisper alucina en los silencios largos**: si el audio tiene mucho aire, recórtalo
  antes de transcribir.
- **El typecheck no se corta con `tail`**: Remotion renderiza aunque `tsc` falle.
  `render.py` corre `tsc` entero y para si hay errores.
