# Kit de marca (ejemplo)

Esta carpeta enseña qué guarda la skill sobre ti. **La tuya se crea sola** en
`<casa>/marca/` (la casa es la carpeta de trabajo que abriste en Claude Code) durante la entrevista; no copies esta.

```
<tu carpeta de trabajo>/marca/
├── perfil.json      valores técnicos: colores, fuentes, subtítulos, hook, audio, cierre
│                    (ejemplo comentado: perfil.example.json)
├── ESTILO.md        tu guía de estilo en prosa: quién eres, tono, formatos, qué evitar,
│                    y lo que la skill va aprendiendo de tus correcciones (ESTILO.example.md)
├── fuentes/         tus tipografías si no son de Google Fonts (.ttf / .otf)
├── logos/           tu logo (PNG transparente o SVG)
├── sfx/             tus efectos de sonido, ya procesados (los mete sfx_propios.py)
├── musica/          tus pistas con licencia para redes + manifest.json (autor, licencia)
└── referencias/     vídeos que te gustan, para analizar su estilo (solo en local)
```

Puedes editar `perfil.json` y `ESTILO.md` a mano cuando quieras, o pedirle al agente
«cambia mi estilo». Si usas la skill en otro ordenador, copia esta carpeta y listo.
