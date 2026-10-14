# Etiquetas que siguen a un objeto (avanzado)

## Etiquetas con SEGUIMIENTO — `Track.tsx`

En un recorrido por un espacio o equipo, un panel tapa lo que se ha venido a ver. Una
etiqueta anclada al objeto, no.

```bash
python scripts/rastrea.py --id obj1 --desde 11.40 --hasta 18.80 --x 470 --y 1020
```
```json
{ "id": "obj1", "start": 11.40, "end": 18.80, "n": 1, "label": "Servidor", "sub": "24 contenedores", "side": "above" }
```

Movimiento global de cámara (Lucas-Kanade + `estimateAffinePartial2D` con RANSAC), no
seguimiento de objeto: aguanta aunque una mano cruce por delante.

- **Un tramo NUNCA cruza un corte de plano** (`select='gt(scene,0.15)'`).
- **Comprueba el punto dibujándolo sobre el vídeo**, no por los números. Si se despega,
  acorta el tramo y re-siembra.
- **`bounds`** limita dónde cae el chip cuando hay cara.

Un track no calla a los subtítulos, salvo que su etiqueta caiga en su banda.
