# Receta: lista / top N

«3 herramientas que…», «5 errores de…». Funciona porque promete un número y el espectador
se queda a ver cuántos van.

**Duración típica**: 30-60 s · **Ritmo**: dinámico

## Estructura

| Beat | Qué se dice | En pantalla | Sonido |
|---|---|---|---|
| Hook (0-3 s) | «N cosas que…» | `hook` con la cifra en `*acento*` | `impact` |
| Teaser | el criterio del orden («de la más fácil a la más rentable») | `teaser`: números nítidos, etiquetas difuminadas; el marcador recorre las filas mientras lo dice | `riser` suave |
| Ítem N | «Número uno: …» | `sections` «01 · NOMBRE» en el raíl (mismas etiquetas que el teaser: lo que allí no se leía, aquí se lee) + lo que mejor lo cuente: `flows` si es un proceso, `stat` si es una cifra, `swap` si sustituye algo, B-roll si se puede enseñar | `tick` en cada sección, `whoosh_in` en tarjetas |
| Remate | la conclusión o el ítem extra | sección de remate («04 · EL VEREDICTO») si queda hueco antes del CTA | `sub_drop` |
| Cierre | según `cta.tipo` | | `chime` |

## Detalles que marcan la diferencia

- **La línea de secciones no se queda vacía**: si entre el último ítem y el CTA pasan
  muchos segundos, añade una sección de remate.
- **Un diagrama por paso narrado**: si enumera cuatro cosas en 4 s, son cuatro nodos con
  cuatro `at`, no un panel entero.
- Ejemplo completo en `template/cortes.example.json` (es justo este formato).
