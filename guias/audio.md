# Audio: efectos, música y niveles

Si el perfil dice `audio.efectos: false`, `sfx: []` y listo.

## De dónde salen los efectos, por orden

1. **Los del usuario** (los que ya usa y le gustan): `python scripts/sfx_propios.py archivo:hueco …`
   (`--lista` enseña los huecos). Funciona con cualquier ffmpeg.
2. **Kit CC0 de Freesound** para los huecos vacíos (abajo). Necesita una API key gratuita y el
   ffmpeg del sistema.
3. Nada: mejor sin sonido que un sonido con copyright.

En cada proyecto: `mkdir -p public/sfx && cp ~/editor-reels/marca/sfx/*.wav public/sfx/`.
En `cortes.json`: `"sfx": [{ "s": "whoosh_in", "at": 3.1, "gain": -12 }]` (`s` = nombre del WAV en `public/sfx/`,
`at` en segundos, `gain` en dB).

En PowerShell, en vez de `set -a; . archivo`: `$env:FREESOUND_API_KEY="xxxx"`.

## Efectos de sonido — kit CC0 compartido

**El kit vive en la biblioteca del perfil** (`audio.biblioteca`, por defecto
`~/editor-reels/marca/sfx`), no en el proyecto: que el whoosh sea siempre el mismo es lo que hace que
suene tuyo. Fuente: **Freesound APIv2** con `license:"Creative Commons 0"` — sin atribución
ni reclamaciones. API key gratis en freesound.org → guárdala fuera de todo repo:

```bash
mkdir -p ~/editor-reels/marca && echo 'FREESOUND_API_KEY=xxxx' > ~/editor-reels/marca/freesound.env
set -a; . ~/editor-reels/marca/freesound.env; set +a
python scripts/sfx_search.py     # candidatos CC0 por hueco del kit (la elección es humana)
python scripts/sfx_fetch.py      # descarga y procesa (kit de partida, o <KIT>/picks.json si existe)
python scripts/sfx_deriva.py     # coin_1..5, cash, swell, air, reveal, tick_soft derivados del kit
```

`sfx_fetch.py` trae un **kit de partida neutro**; para uno propio, escucha los candidatos
de `sfx_search.py` y escribe `<KIT>/picks.json` (`{"slot": [id, "para qué"]}`). Cada sonido
se procesa igual: silencio de cabeza fuera, pico a −3 dBFS, WAV 48 kHz estéreo.

- **Consultas de una palabra**: CC0 es un pool estrecho (`"whoosh"` sí, `"reverse whoosh soft"` no).
- **Tira de un mismo pack**: mismo autor, coherencia gratis.
- **Deriva en vez de descargar**: `whoosh_out` = `whoosh_in` invertido con paso bajo.

| Momento | Sonido | Ganancia de partida |
|---|---|---|
| entra el título | `impact` | −8 |
| choque del «VS» | `hit` | −10 |
| entra un chip | `tick` | −19 |
| la tesis | `riser` + `sub_drop` | −13 / −9 |
| entra/sale una tarjeta | `whoosh_in` / `whoosh_out` | −12 / −15 |
| llegan avisos | `notify_a/b/c` escalonados | −12 |
| CTA | `chime` | −12 |
| cierre | `close` | −8 |

Si el perfil dice `audio.efectos: false`, `sfx: []` y listo.

### Verifica que suenan, y a qué nivel

Comparar `mean_volume` no sirve (un efecto 13 dB bajo aporta 0.2 dB). **Renderiza solo la
capa de sonido**:

```bash
bash scripts/mide_sfx.sh MiCorte c1     # REMOTION_MUTE_VIDEO=1 + tabla por cue (bash: Mac, Linux o Git Bash en Windows)
```

Objetivos con la voz picando en −10: **golpes −12/−16, ticks −18/−24, música −25/−30 dBFS**.
La tabla de ganancias es un punto de partida; **el nivel se mide**.

**El mezclador de Remotion NO es lineal** (reescala según cuántas pistas suenan a la vez:
doblar un cue puede dejarlo más bajo). Si las lecturas no responden, mezcla con ffmpeg:

```bash
python scripts/mezcla.py --cid c1 --objetivos              # gain de cada cue = objetivo − pico de su fichero
python scripts/mezcla.py --cid c1 --pega out/MiCorte.mp4    # vídeo copiado, audio nuevo
```

### Música

Solo si el perfil la pide (`audio.musica`). Tus pistas en `<biblioteca>/musica/` (CC0 o
con licencia para redes), con un `manifest.json` de autor y uso. La cama se declara en
`music.tramos` y la monta `scripts/musica.py` → `public/musica.wav`. **El suspenso corta EN
SECO justo antes de la revelación** y la resolución entra encima de la frase que la da.
Con micro cercano `gain: 0`; a −5 puede no oírse.
