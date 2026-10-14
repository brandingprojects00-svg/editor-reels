# Editar: de clips sueltos + descripción a reel terminado

**Antes de tocar nada**, lee `~/editor-reels/marca/ESTILO.md` y `perfil.json`. Todo lo que
decidas (hook, ritmo, tarjetas, sonido, cierre) sale de ahí, de lo que pida el usuario y de
`guias/reglas.md`.

Lo que suele llegar: «aquí tienes 3 clips, es un tutorial de cómo hago X, quiero cerrar
pidiendo que comenten GUÍA». Si falta algo esencial (qué formato, si hay recurso detrás de
la palabra clave), pregúntalo en una sola tanda. Lo demás, decídelo tú con su ESTILO.md.

## 1. Proyecto

```bash
cp -R <skill>/template ~/editor-reels/proyectos/<nombre-corto>
cd ~/editor-reels/proyectos/<nombre-corto>
npm install --ignore-scripts          # una vez por proyecto (~1 min)
python scripts/aplica_perfil.py       # su marca en theme.ts y fonts.ts
mkdir -p input && cp <sus clips> input/
```

Nombres de clip sin espacios ni acentos y **que no se llamen `c1`** (`toma1.mp4`,
`intro.mov`…). Si usa efectos: `mkdir -p public/sfx && cp ~/editor-reels/marca/sfx/*.wav public/sfx/`
(Remotion solo sirve lo que está en `public/`).

## 2. Sondeo

```bash
python -c "import sys; sys.path.insert(0,'scripts'); import ff; [print(f, ff.sonda(f)) for f in sys.argv[1:]]" input/*
```

- **Vertical 1080x1920** (o 720x1280 etc.) → esta plantilla. Lo normal.
- **Horizontal** (charla, Zoom, pantalla) → `guias/avanzado/horizontal-16x9.md`.
- **Split de CapCut** (captura arriba, cara abajo) → `guias/avanzado/split-capcut.md`.
- **Datos sensibles en pantalla** (correos, nombres de clientes, tokens) → pregunta qué se
  tapa; `guias/avanzado/tapar-datos.md` (OCR solo en Mac; si no, que lo difumine antes).

## 3. Transcripción (local)

Un clip por llamada, con las marcas/nombres que salen en el vídeo en `--prompt`:

```bash
python scripts/transcribe.py input/toma1.mp4 work/toma1.json --prompt "Canva, Shopify"
python scripts/transcribe.py input/toma2.mp4 work/toma2.json --prompt "Canva, Shopify"
```

Comprueba que la duración del transcript cuadra con la del clip (lo imprime).

## 4. Montaje bruto — `montaje.py`

```bash
python scripts/montaje.py propone input/toma1.mp4 input/toma2.mp4 input/toma3.mp4
```

Imprime las frases de cada clip con su id (`toma1#3`) y marca ⚠ las sospechosas (tomas
repetidas, arranques en falso). Tu trabajo:

- **Lee las frases como un editor**: ¿dónde se equivoca y repite? ¿qué toma es la buena
  (normalmente la última)? ¿sobra algo que se va del tema? ¿el orden de los clips es el de la
  historia? Cuando un clip ya viene montado (CapCut), casi no habrá nada que quitar.
- Edita `work/montaje.json`: `orden`, `quitar` (ids de frase), `recortes` (trozos exactos).
- **Enséñale al usuario el guion resultante** (las frases que quedan, en orden) y lo que
  quitas y por qué. Espera su OK.

```bash
python scripts/montaje.py corta                 # → public/c1.mp4, work/c1.json, work/c1_spans.json
python scripts/words.py work/c1.json --convert  # → work/c1_words.json
```

`c1_spans.json` ya trae un zoom alterno (1.0 / 1.12) en cada salto dentro del mismo clip,
para que los jump cuts se sientan intencionales. Ajústalo al `ritmo` y `punch_ins` del
perfil: con `punch_ins: "nunca"` ponlos todos a 1.0; con ritmo frenético puedes subir a 1.18.

Un solo clip ya montado: igual, `propone` + `corta` (normaliza a 1080x1920/30 fps y deja el
transcript listo), o cópialo a `public/c1.mp4` y transcribe directamente `public/c1.mp4`.

## 5. Plan visual — `work/plan.md` (el usuario lo aprueba)

Antes de construir, escribe el plan como lo haría un editor para su cliente. Fuentes: lo que
pidió + su ESTILO.md (tono, formatos, evitar) + la receta del formato en `<skill>/formatos/`
+ la transcripción (`python scripts/words.py work/c1_words.json 0-60`).

```markdown
# Plan — <título>
Formato: <receta> · Duración: 38 s · Cierre: pregunta / comenta GUÍA

| Tiempo | Lo que dice | En pantalla | Sonido |
|---|---|---|---|
| 0.0–2.8 | «Si usas Canva…» | HOOK «3 trucos de *Canva*» (caja) | impact |
| 2.8–9.5 | primer truco | tarjeta `point`: «exporta en PNG, no JPG» · chip Canva | whoosh_in |
| … | | | |
| 33.0–38.0 | «¿Cuál usarías tú?» | pregunta grande (`grandes.pregunta`) | chime |

Correcciones del transcriptor: «can va» → Canva (12.3 s)
Dudas: ¿la palabra GUÍA tiene un recurso detrás?
```

Reglas para el plan (detalle en `guias/reglas.md` y `guias/componentes.md`):

- **Hook visible desde el primer fotograma** (salvo `hook.estilo: "ninguno"`), corto, en su tono.
- **Una tarjeta nunca repite lo que dice la voz**: contrasta, deduce o remata.
- **Un evento visual cada 3-6 s** con ritmo dinámico (tarjeta, diagrama, B-roll, chip,
  punch-in, sección). Si no hay material, dilo: mejor un plan honesto que relleno.
- **El acento de marca es para el CTA**; el resalte de subtítulos, `highlight`.
- **Nada de `notas.evitar`**. Revisa la lista antes de enseñar el plan.
- **B-roll**: si el usuario no lo dio, propón qué haría falta (capturas, fotos de producto)
  y pregunta si lo tiene. No metas imágenes de internet sin decirlo ni sin crédito.
- **Cifras, precios y nombres**: del audio o de una fuente que cites. Nunca a ojo.

Enséñalo y ajusta hasta que diga que sí.

## 6. Construcción

1. **`cortes.json`** — copia la estructura de `cortes.example.json` (comentado) y rellena
   con el plan: `hook`, `kicker`, `cards`, `flows`, `sections`, `topics`, `keyword` o
   `grandes.pregunta`, `sfx`, `hide`, `fix`. Los segundos de cada `at`/`start` salen de
   `words.py` (`--find palabra` o un rango), nunca a ojo.
2. **Logos** de las marcas que se NOMBRAN: `python scripts/logos_gen.py --add canva shopify`.
   Iconos nuevos: `python scripts/icons_fetch.py scissors palette`.
3. **Datos**: `python scripts/gen_data.py --work work --cuts c1 --config cortes.json`
   (avisa si un `fix` anclado no casa).
4. **Registro**: en `src/cuts.ts` cambia el id `Demo` por el nombre de la pieza
   (`{ id: "TrucosCanva", data: c1 }`). `Root.tsx` no se toca nunca.
5. **Geometría**: mide el espacio libre del plano y dónde está la cara
   (`guias/reglas.md` → «Cómo encontrar el espacio muerto»); ajusta `theme.ts` si hace falta.
6. **Stills de los momentos clave** (hook, cada tarjeta, el cierre) y **míralos**:
   ```bash
   npx remotion still src/index.ts TrucosCanva qa/f45.png --frame=45 --image-format=png
   ```
7. **Nada tapa la cara**:
   ```bash
   python scripts/caras.py && python scripts/verifica.py     # sale con error si algo pisa la cara
   ```
   Si choca: mueve la tarjeta a un tramo sin cara, bájala de tamaño, o usa
   `python scripts/subtitulos.py` / `python scripts/aparta.py --escribe`.

## 7. Render y export

```bash
HQ=1 python scripts/render.py TrucosCanva           # typecheck + render → out/  (2-6 min)
python scripts/export.py --video copy --only TrucosCanva   # −14 LUFS, bt709 → final/
python scripts/qa.py final/TrucosCanva.mp4          # fotogramas de control
```

- En Windows PowerShell `HQ=1 …` no funciona: `$env:HQ="1"; python scripts/render.py X`.
- `audio.micro = "cercano"` → `--pre "highpass=f=80"` en el export (el compresor aplasta un
  micro cercano). `"sala"` → el valor por defecto.
- Con efectos: `bash scripts/mide_sfx.sh TrucosCanva c1` comprueba que suenan a su nivel
  (`guias/audio.md`).

**Mira los fotogramas de `qa/`** y repasa: ¿se lee todo? ¿algo tapa la cara? ¿hay tramos
muertos? ¿se coló algo de `notas.evitar`? Arregla antes de entregar.

## 8. Entrega y ronda de ajustes

Dale la ruta de `final/<pieza>.mp4`, 3-4 fotogramas clave y un resumen corto de lo que
hiciste (y de lo que no pudiste: «no había B-roll para el truco 2, puse un diagrama»).

Cuando pida cambios: edita `cortes.json` → `gen_data.py` → still del tramo → render. Y si el
cambio es de **gusto** («los subtítulos más grandes», «no me pongas nunca X»), **ofrece
guardarlo** en `perfil.json` / `ESTILO.md` («Aprendido»). La próxima pieza saldrá así.

Para otra versión (otro hook, otro cierre): añade otro corte en `cortes.json` (`c1b` con
`"src": "c1.mp4"`), copia `work/c1_words.json` → `work/c1b_words.json` y
`work/c1_spans.json` → `work/c1b_spans.json`, genera con `--cuts c1 c1b` e importa `c1b` en
`cuts.ts` con su propia línea.
