# Fuente horizontal: charla, Zoom, Meet (avanzado)

Usa la plantilla `avanzado/template-16x9/` (cópiala igual que `template/`). El 16:9 va en una ventana con fondo desenfocado detrás.

## Fuente de videollamada (Zoom, Meet) — `avanzado/template-16x9/`

1. **El rótulo del nombre va quemado**: se recorta en `spans` (`crop`). El recorte deja un
   formato menos ancho que 16:9 y la ventana crece — mejora el encuadre.
2. **La imagen va por detrás del audio** (~1 s en hablante activo). **Una tarjeta cubre ese
   retraso** y suelta justo en la primera palabra del remate.
3. **Sin punch-ins**: a 640x360 la ventana ya va a ×2.25.
4. El AGC deja el audio aplastado: `PRE="highpass=f=80"` sin compresor.
5. Si el clip llega densificado (sin silencios, acelerado), `src` configurable y `seams`
   desde `work/<cid>_costuras.json`: la ventana alterna escala 1 / 1.05 en cada costura
   notoria. **Transcribe el clip YA densificado**, nunca el original.
