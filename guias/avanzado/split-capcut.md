# Pantalla dividida de CapCut y fuentes mixtas (avanzado)

## Fuente SPLIT SCREEN de CapCut (captura arriba, cámara abajo)

`template/` sirve, pero **la geometría de `theme.ts` se recalibra entera**: no hay
pared muerta ni torso libre. **Mide el borde**: luminancia media por fila sobre un
fotograma con la captura clara. Ejemplo:

```
captura        y    0 → 841    intocable: es lo que se ha venido a ver
COSTURA        y  841 → 1030   fondo oscuro del set
cara           y 1040 → 1360
torso          y 1400 → 1520
               y 1560 → 1920   ya es zona de UI
```

- **Los SUBTÍTULOS van en la costura** (`size 60`, `maxWords 3`, `cy 945`). Bajo la
  barbilla, las páginas de dos líneas se comen la cara.
- **El grafismo pequeño baja al torso** (`KICKER_Y = 1400`).
- **El logo va DENTRO de la línea** (`TOPIC_ALIGN = "inline"`): en esa banda no caben dos
  cosas y un chip suelto acaba sobre la barbilla.
- **`punches: []` y `spans` a escala 1**: un punch-in amplía LAS DOS mitades.
- **Sin scrim arriba** (oscurecería la captura); una junta tenue en la costura.
- **Sin handle** si no hay banda libre (`handle: ""`).
- **Tarjetas ENCIMA de la captura solo cuando lo que enseña no se lee** (un terminal
  esperando, comandos desfilando): ahí es tu B-roll (`CARD_BAND = { cy: 546, h: 330 }`).
  Si la captura es la protagonista, no la tapes. Decide tramo a tramo.
- **Cámara del split muy cerca** (cara hasta y 1540): `TOPIC_ALIGN = "off"`, sin kicker.

### Fuente MIXTA: split y cámara completa alternando — `layout.py`

A cámara completa, los subtítulos de la costura caen en la boca. Hay que saber dónde
cambia, al fotograma:

```bash
python scripts/layout.py --src public/c1.mp4
#   costura en y ≈ 838 · 0.000 → 3.300 SPLIT · 3.300 → 6.017 cámara completa · …
```

Deja `work/c1_layout.json` con `split` (el scrim cambia en el tiempo) y `cap_zones`
sugeridas que no parten una palabra.
