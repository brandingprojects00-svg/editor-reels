# Componentes: qué grafismo hay y cuándo usarlo

Todo se declara en `cortes.json` (formato completo y comentado en `template/cortes.example.json`). Las claves que empiezan por `_` son notas: el script las ignora.

## Hook, kicker y cierre — lo que más pesa

### Hook (`hook`)

```json
"hook": { "start": 0, "end": 3.2, "lines": ["3 trucos de", "*Canva* que no usas"] }
```

- **Visible desde el primer fotograma** (`start: 0`). Es lo que decide si se quedan.
- Estilo del perfil (`HOOK` en `theme.ts`): `caja` (cada línea en su caja, como sticker) o
  `suelto` (texto con trazo y sombra). Con `hook.estilo: "ninguno"` no se escribe hook.
- `*palabra*` = esa palabra en el color de acento. Una por hook, como mucho dos.
- 2 líneas de 14-22 caracteres. Más largo no se lee en 3 s.
- Complementa a la voz, no la transcribe: si dice «hay tres trucos de Canva que nadie usa»,
  el hook puede ser «3 trucos de *Canva*» (resume) o «nadie usa *esto*» (intriga).
- `top`, `size`, `color` opcionales. Por defecto va dentro del recorte 4:5 del feed.

### Kicker (`kicker`)

Rótulo pequeño en el raíl (la zona libre del plano) que dice de qué va la pieza
(«lo que ya no hago a mano»). Entra al salir el hook y lo relevan las secciones si las hay.
Vacío (`""`) si no aporta.

### Cierre según `cta.tipo` del perfil

| `cta.tipo` | Qué se pone | Cuándo |
|---|---|---|
| `keyword` | `"keyword": { "verb": "comenta", "word": "GUÍA", "start": 36.1 }` | **solo si el audio lo dice y hay un recurso que entregar**. Si no lo sabes, pregunta |
| `pregunta` | `"grandes": { "pregunta": { "start": 41.5, "pre": "¿y tú qué le", "word": "DELEGARÍAS?", "icon": "message-circle-question" } }` y `keyword: null` | la pregunta casi siempre ya está en el audio: búscala en la transcripción |
| `seguir` | un chip corto al final (tarjeta `point` o `keyword` con verbo «sígueme») | |
| `ninguno` | nada | |

`firma` (opcional en `keyword`): una línea bajo el chip («y yo soy Ana»). Si ya lo dice en
voz alta, no la escribas.

## Reels de lista numerada: teaser, índice y diagramas

Tres capas; ejemplo en `cortes.example.json`.

**`Teaser.tsx` — la lista DIFUMINADA del hook.** Cuando se dice «tres tareas», entra un
panel con los temas: números nítidos en color de acento, etiquetas a 40 px con
`blur(7px)` (nunca nítidas). Se ve que hay tres cosas y no se lee cuáles: esa es la
promesa. Un marcador recorre las filas (`sweepFrom`/`sweepTo`) mientras dice «de la más
fácil a la más rentable». Los subtítulos NO callan (es el hook).

**`Sections.tsx` — el índice que paga el teaser.** «01 · CORREOS» en el sitio del kicker
(raíl, y 300, dentro del 4:5), que cambia en cada «Número N». Las etiquetas son las MISMAS
que las del teaser: lo que allí no se leía, aquí se lee. El kicker se apaga al entrar la
primera sección; la última acaba antes del chip de CTA, que vive en la misma banda. **La
línea no puede quedarse vacía**: si entre la última sección y el CTA quedan muchos
segundos, añade una sección de remate («04 · EL VEREDICTO»).

**`Flow.tsx` — diagramas de proceso.** Sustituyen al B-roll en un plano fijo: el proceso
se ve mientras se cuenta. Nodos con icono que entran con rebote cuando se nombra el paso
(`at` de `scripts/words.py`) y flechas SVG que se dibujan entre ellos:

```
chain   a → b → c → d          secuencia; `badge` etiqueta una flecha («tú revisas»)
fanin   [a b c] → hub → out    varias fuentes convergen
fanout  in → hub → [a b c]     una fuente se reparte (1 vídeo → guion + subtítulos + post)
rows    a → b  /  c → d        pares apilados
```

`icon` es un id de Lucide (`scripts/icons_fetch.py clock database bell` los baja y
regenera `src/Icons.ts`) o un `LogoId`. Marcas de Simple Icons, conceptos de Lucide (ISC).
Medidas: **etiquetas a 22 px mínimo**, **6 nodos como mucho en un `chain`** (750 px
interiores), líneas de tarjeta a 50 px **hasta 27 caracteres**.

Un diagrama por paso narrado, no por sección: si se enumeran cuatro cosas en 4 s, son
cuatro nodos con cuatro `at`, no un panel que aparece entero.

## Tarjetas

| tipo | para qué |
|---|---|
| `point` | 1-3 líneas: la deducción o el remate |
| `contrast` | dos columnas con logo: A vs B |
| `logos` | fila de marcas + una línea |
| `stat` | una cifra grande y qué significa |
| `swap` | lo que usas → la alternativa de pago → su precio. `fromIcon`/`toIcon` (Lucide) si no hay marca |
| `specs` | ficha técnica: icono · concepto · valor |
| `bill`  | concepto ⋯ precio con línea de puntos, y un total grande que sube |
| `palabra` | el concepto central en UNA palabra grande (Anton, mayúsculas, itálica), sin panel; `sub` opcional |

```json
{ "t": "swap", "start": 24.9, "end": 30.2, "kicker": "lo que sustituye",
  "rows": [{ "from": "github", "fromLabel": "Git propio", "to": "github", "toLabel": "GitHub Team", "price": "$4", "at": 25.6 }],
  "total": { "label": "al mes", "prefix": "$", "num": 54, "suffix": "" } }
```

- **`at` por fila** (`swap`, `specs`, `bill`): la fila entra en el segundo en que se NOMBRA
  esa cosa. Sin `at` desfilan escalonadas y se lee como una lista que va sola.
- **El total sube** (`cuenta()` en `anim.ts`): uno que aparece hecho es un dato; uno que
  sube mientras caen las filas es el argumento. Y se oye: `coin_1..5` + `cash`.
- **`from` es opcional.** Si se dice «el gestor de contraseñas» sin la marca, va sin logo.
  Antes eso que inventarse el icono.
- **Cuatro filas es el techo** con la altura de `CARD_BAND`.
- **Verifica cada precio y deja fecha y plan en `_precios`.** Mensual y anual no se suman.

**Un chip de marca puede llevar dato**: `Topic` acepta `spec`. Pasa de decir *de quién*
se habla a decir *qué*.

## B-roll de verdad y grafismo GRANDE — `Broll.tsx` · `Grandes.tsx`

### `broll`: cortes a pantalla completa

```json
{ "kind": "video", "full": true, "src": "broll/producto.mp4", "start": 0.55, "end": 1.18, "from": 0.4,
  "tag": "Nombre", "sub": "dato que la voz no dice", "logo": "github", "zoom": [1.12, 1.04] }
{ "kind": "image", "full": true, "src": "broll/foto.png", "start": 23.45, "end": 24.5,
  "tag": "Producto", "sub": "$1,349 · chip X", "credit": "Fabricante", "plain": true, "bg": "#000000", "zoom": [1.28, 1.36] }
```

- **`full`** sustituye al plano mientras la voz sigue: entra y sale en SECO (es un corte)
  con un empujón de escala. Vídeo en `cover`; imagen en `contain` sobre sí misma
  desenfocada, o sobre fondo liso con `plain`. Sin `full` es una ventana (`cy`, `w`, `h`).
- **`tag`/`sub`** abajo a la izquierda, **`credit`** arriba a la derecha: abajo choca con
  los subtítulos. Material ajeno: el crédito va siempre.
- **El rótulo da un dato que la voz NO dice** (regla 1). Y **nada que caduque** («salió
  ayer»): se publica días después.
- **Patrón pantalla → foto**: si la captura enseña la lista, primero la etiqueta anclada en
  la pantalla (la prueba) y cuando se NOMBRA el producto, corte a la foto.
- **Capas**: el B-roll va por DEBAJO de las escenas y de `grandes`.

De dónde sale el material, por orden:

1. **Su propio archivo**: vídeos anteriores, desde el clip limpio del proyecto (nunca
   desde un export con subtítulos quemados). Tira de contacto a `fps=1/2` para elegir,
   luego a `fps=4` para el segundo exacto; corta con `-an -crf 12`.
2. **Web**: un agente aparte con la lista de productos. Webs oficiales, notas de prensa,
   `yt-dlp` solo para vídeo del fabricante. Que MIRE cada imagen y descarte lo dudoso
   (fotos «de producto» generadas con IA existen). Fuente y fecha en `_broll_…`.
3. Recorta marcas de agua con `crop` antes de meterlo en `public/broll/`.

**No etiquetes nada como colaboración o patrocinio sin preguntar.**

### `grandes`: iconos grandes que se dibujan

```json
"grandes": {
  "pasos": [{ "start": 29.1, "end": 41.3, "top": 190, "mode": "live", "kicker": "lo que hace solo",
              "nodes": [{ "icon": "search", "label": "investiga", "color": "#4CC4F4", "at": 31.48 }],
              "badge": { "text": "tú envías", "icon": "user-round", "after": 3, "at": 36.24 } }],
  "pregunta": { "start": 41.46, "top": 205, "icon": "message-circle-question", "pre": "¿y tú qué le", "word": "DELEGARÍAS?" }
}
```

- **`Pasos` `live`** sustituye a un `Flow` chain cuando hay ~300 px libres sobre la cabeza:
  baldosa grande para el paso que se NOMBRA, check en las hechas, punteadas las pendientes;
  el icono se dibuja trazo a trazo, rebote, onda y chispas. Cinco nodos caben en 830 px.
- **`Pasos` `teaser`**: el gancho — todas en cascada, etiquetas difuminadas.
- **`Pregunta`**: el cierre de `cta.tipo = "pregunta"` en grande. Sustituye al chip.
- **`DrawIcon`** inyecta `pathLength="1"` en cada trazo de Lucide y anima
  `strokeDashoffset` 1→0. Vale para cualquier icono.

## Logos de marca

```bash
python scripts/logos_gen.py --add notion figma              # Simple Icons: baja, aclara si es oscuro, regenera
python scripts/logos_gen.py --imagen mimarca logo.png "Mi Marca" "#FF5A36"   # fuera de Simple Icons: pegatina
```

`src/Logos.tsx` se genera desde `public/logos/marcas.json`; no se edita a mano.
**Nunca inventes un logo** y **no metas marcas que no se nombran** — si no dice «Docker»,
no hay logo de Docker. El color oficial se aclara cuando es negro o casi negro (queda
anotado); el trazo no se toca nunca. Las marcas del perfil (`marcas_frecuentes`) añádelas
en cada proyecto nuevo.
