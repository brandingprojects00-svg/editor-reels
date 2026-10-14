# Versión en otro idioma (avanzado)

## Versión en otro idioma

```bash
python scripts/traduce.py --de c1 --a c1en --texto work/traduccion_en.json
```

**Se traduce por FRASES, no por palabras**: se conserva la ventana de cada segmento y las
palabras nuevas se reparten en proporción a su longitud. Es **otro corte** en
`cortes.json` (`c1en`) con `"src": "c1.mp4"` y `fix` vacío. **Traduce también el
grafismo**, y cuida la persona (en su propio vídeo es *I*, no *he*).
