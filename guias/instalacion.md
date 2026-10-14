# Instalación

Objetivo: que el usuario pueda transcribir y renderizar en su máquina. **No instales nada
sin permiso explícito**: antes de cada paso di qué es, de dónde viene, cuánto ocupa y para
qué sirve. Si dice que no, explica qué deja de funcionar y sigue con lo que se pueda.

## 1. Preparar la casa y un proyecto de prueba

```bash
mkdir -p ~/editor-reels/marca/{fuentes,logos,sfx,musica,referencias} ~/editor-reels/proyectos
cp -R <skill>/template ~/editor-reels/proyectos/demo
cd ~/editor-reels/proyectos/demo
python scripts/doctor.py
```

> **Windows**: la ruta del proyecto tiene que ser corta (el navegador de Remotion falla con
> rutas de más de 260 caracteres). `~/editor-reels` suele valer. Si su usuario de Windows es
> muy largo o está en OneDrive, usa `EDITOR_REELS_HOME=C:/reels` (y díselo para que lo
> recuerde). Evita carpetas sincronizadas con OneDrive/iCloud: `node_modules` las colapsa.

El doctor no instala nada: dice OK/FALTA y da el comando de cada sistema.

## 2. Lo esencial

| Qué | Para qué | Cómo (con permiso) |
|---|---|---|
| **Node.js 18+** | Remotion (el motor que dibuja y renderiza el vídeo) | Windows `winget install OpenJS.NodeJS.LTS` · Mac `brew install node` · Linux nodejs.org |
| **Python 3.10+** | los scripts de la skill | Windows `winget install Python.Python.3.12` · Mac `brew install python@3.12` |
| **Dependencias del proyecto** | Remotion y sus fuentes | `npm install --ignore-scripts` dentro del proyecto (~250 paquetes, ~400 MB). Luego `npm audit` |
| **Entorno de Python** | Whisper (transcripción local, sin nube) + OpenCV (detectar la cara para no taparla) | `python scripts/setup_entorno.py` — crea `~/editor-reels/.venv`, instala `faster-whisper`, `numpy`, `opencv-python-headless` de PyPI y baja el modelo `small` (~0,5 GB) de Hugging Face |

`npm install` siempre con `--ignore-scripts` (no ejecuta scripts de terceros al instalar).

## 3. Recomendado

| Qué | Para qué | Sin él |
|---|---|---|
| **ffmpeg del sistema** | compresor de voz en el export, efectos derivados, hojas de contacto | Se usa el ffmpeg que trae Remotion (recortado): monta, transcribe, renderiza y exporta a −14 LUFS, pero sin compresor de voz ni `sfx_deriva.py`/`musica.py`/`mezcla.py`. Windows `winget install Gyan.FFmpeg` · Mac `brew install ffmpeg` · Linux `sudo apt install ffmpeg` |
| **Skills oficiales de Remotion** | que el agente escriba mejor código si el usuario pide un efecto nuevo | Todo lo de la plantilla funciona igual. `npx skills add remotion-dev/skills` |

## 4. Modelo de Whisper

| Modelo | Tamaño | Cuándo |
|---|---|---|
| `small` (por defecto) | ~0,5 GB | cualquier portátil; acierta bien el habla, falla nombres propios (se arreglan con `fix`) |
| `medium` | ~1,5 GB | si los subtítulos salen con muchos errores o habla rápido / con acento marcado |
| `large-v3-turbo` | ~1,6 GB | solo con GPU NVIDIA |

Se elige con `python scripts/setup_entorno.py --modelo medium` y se guarda en el perfil
(`transcripcion_modelo`). Pasa las marcas que salen en el vídeo con `--prompt` al transcribir:
mejora mucho los nombres.

## 5. Comprobar

```bash
python scripts/doctor.py          # todo OK
npx remotion --version
```

Luego la entrevista (`guias/entrevista.md`). El render de demo del final de la entrevista
es la prueba de que todo funciona.

## Problemas típicos

- **`python` no se encuentra (Mac/Linux)** → usa `python3` en todos los comandos.
- **El navegador de Remotion no arranca / errores de ruta en Windows** → ruta más corta (ver arriba).
- **El render falla con «No frame found at position…»** → `render.py` ya reintenta solo con un
  hilo; si quieres forzarlo: `CONCURRENCY=1 python scripts/render.py X` (en PowerShell
  `$env:CONCURRENCY="1"`).
- **Fuentes que no cargan en el render** → sin conexión a internet las Google Fonts no bajan;
  la primera vez hace falta red.
- **`faster-whisper` falla al instalar** → Python demasiado nuevo para sus binarios: instala
  Python 3.12 y repite `setup_entorno.py` con ese Python.
- **Mac con Apple Silicon** → `faster-whisper` va en CPU y es suficiente. (Más rápido:
  `mlx-whisper`; produce el mismo JSON que lee `words.py`.)
