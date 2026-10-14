# Demo grabada con el móvil (avanzado)

## Demo grabada con el MÓVIL apuntando a la pantalla

Sin cara, cámara en mano:

- **La línea de tiempo sale del OCR, no del ojo.** OCR a 5 fps en toda la pieza y a 30 fps
  ±0.5 s alrededor de cada clic. Un clic = el último fotograma con el texto del botón; el
  cambio = el primero con el texto nuevo. Sellos, sonidos y punches caen ahí.
- **Seguir un botón con `rastrea.py` funciona** aunque la cámara vaya en mano:
  compruébalo contra el OCR, no solo mirando.
- Subtítulos abajo del todo (`cy 1465`, 56 px) si el panel ocupa el centro.
- `verifica.py` / `caras.py` no aplican.
