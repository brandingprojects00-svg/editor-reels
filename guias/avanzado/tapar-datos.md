# Tapar datos sensibles (avanzado · solo macOS)

> El OCR usa Vision de macOS. En Windows/Linux, difumina a mano en tu editor (CapCut, Premiere) antes de pasar el clip.

## Datos sensibles en la captura — `tapar.py`

Una captura real enseña nombres, correos, teléfonos, IPs, tokens. **No se decide solo qué
se tapa**: se busca, se enseña al usuario y él elige (a veces solo quiere tapar al cliente).

```bash
# work/tapar.json: src, out, alto, patron, rapidos, antes, bajo, manual (ejemplo: work/tapar.example.json)
python scripts/tapar.py ocr
python scripts/tapar.py busca --nombres Acme "Juan Pérez"   # -> PREGUNTAR
python scripts/tapar.py render       # -> public/c1.mp4
python scripts/tapar.py verifica     # LIMPIO o nada
```

OCR con Vision de macOS (`scripts/ocr/ocr.swift`, se compila solo). Lo que costó:

- **Por token, no por línea**, con margen vertical con techo de 6 px.
- El `patron` lleva **las lecturas torcidas del OCR** («Acrne», «Aeme»): `busca` las enseña.
- 30 fps + unión de ±4 muestras cubre un terminal. **No cubre un documento que se desplaza
  40-90 px entre muestras**: esos tramos van en `rapidos` — OCR de cada fotograma al doble
  de tamaño y vecinos unidos **compensados en movimiento**.
- `antes`, `bajo` y `manual` para los casos que el OCR no ve.
- Se difumina sobre los **planos YUV**: sin matriz de color que falle.
- `verifica` hace OCR del resultado en fotogramas que el primer pase no miró. Solo vale
  LIMPIO. Anota en `cortes.json` (`_src`) que el fuente es el vídeo tapado.

**Barre por tramos, no cada N segundos**: un panel claro de 3 s con una IP puede colarse
entre dos muestras.
