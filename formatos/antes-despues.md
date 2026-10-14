# Receta: antes y después

Enseñas una transformación: un diseño, un espacio, un proceso, una cifra. El «después» es el
premio; todo el vídeo lo hace esperar lo justo.

**Duración típica**: 20-45 s · **Ritmo**: dinámico, con una pausa antes de la revelación

## Estructura

| Beat | Qué se dice | En pantalla | Sonido |
|---|---|---|---|
| Hook (0-2 s) | un adelanto del después, o el antes en su peor momento | B-roll del resultado a pantalla completa 1 s + `hook` | `impact` |
| Antes | cómo estaba / cómo lo hacías | B-roll o captura del antes con rótulo «ANTES» (`tag`), tarjeta `stat` con la cifra de partida | — |
| Proceso | qué cambiaste | `flows` chain o `grandes.pasos` con los pasos entrando al nombrarlos; cortes rápidos del proceso | `tick` por paso, `riser` al final |
| Revelación | «y así quedó» | corte seco al después a pantalla completa (`broll` `full`), rótulo «DESPUÉS»; si hay cifra, tarjeta `swap` o `bill` con el total que sube | `sub_drop` + `close` |
| Cierre | pregunta o CTA | según `cta.tipo` | `chime` |

## Detalles

- Mismo encuadre en antes y después si se puede: la comparación se ve sola.
- La revelación entra **en el segundo exacto** en que lo dice (`words.py --find`).
- Si solo hay fotos, `broll` `kind: image` con `zoom` lento ([1.0, 1.08]) para que no se vean estáticas.
