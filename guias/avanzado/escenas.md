# Escenas de suspenso y drama (avanzado)

## Escenas: suspenso, drama e interactividad — `Escenas.tsx`

Para demos de pantalla donde solo subtítulos se queda corto. Todo en `cortes.json → escenas`.

| escena | qué hace | cuándo |
|---|---|---|
| `sellos` | tampón que cae con rebote y hace temblar el cuadro | hook («CONFIDENCIAL»), remate («LISTO» en verde) |
| `tuberias` | fila de pasos con logos: `blur: true` en el hook, `blur: false` + `checkFrom` en el cierre | la promesa y su pago en una línea |
| `pins` | punto que late sobre algo de la PANTALLA + guía + chip | «esto es mi panel» — x,y del OCR |
| `marcas` | recuadro que sigue una línea del terminal a saltos (`keys`) | la línea que importa en un terminal lleno |
| `crono` | cronómetro que COPIA los segundos de la pantalla | un agente trabajando: la espera es el suspenso |
| `expedientes` | campos que «se encuentran» (caracteres barajando) y se tachan | «busca la empresa» |
| `censuras` | barras que barren la captura + sello «CLASIFICADO» | «vamos a borrar los datos privados» |
| `entregas` | casillas 0/N → N/N al nombrarlas | el resumen de lo que hizo |
| `firmas` | cursor que pulsa el botón REAL de la captura, firma y ✓ | lo que hará el cliente |
| `glitches` | franjas de color desplazadas 0.2-0.4 s | cambios bruscos, corte de música |
| `consolas` | terminal que se escribe AL RITMO DE LA VOZ, `tone` red/green | el dolor antes de la solución |
| `memoria` | medidor que copia lecturas del panel (OCR) y cronometra la carga | «cargó en 2,8 s» |

`tone`: `"red"`, `"green"`, `"accent"` o un hex. Los segundos del crono salen de
`scripts/crono_ocr.py`; el botón de la firma, del OCR. **Nunca un número a ojo.**

Capas: escenas encima de tarjetas y diagramas (un sello puede rematar un panel), debajo
de los subtítulos; el crono arriba del todo. `verifica.py` las juzga contra la cara.

Sonido típico: `braam` con el sello del hook, `clock` bajo el expediente, `heart` bajo la
censura con `riser` hasta la revelación, la música de suspenso cortando en seco y la
resolución entrando con un impacto, `coin_1..5` + `cash` en cada casilla.
