#!/usr/bin/env python3
"""Aplica tu perfil (el del cuestionario) a ESTE proyecto.

  python scripts/aplica_perfil.py              # perfil de ~/editor-reels/marca/perfil.json
  python scripts/aplica_perfil.py --perfil otro.json

Qué toca, y nada más:
  - src/theme.ts  → el bloque entre «PERFIL» y «FIN PERFIL» (colores, subtítulos, raíl, hook)
  - src/fonts.ts  → las tipografías por rol (Google Fonts o archivo local en public/fonts/)
  - perfil.json   → copia en el proyecto, para que el proyecto se renderice igual
                    aunque cambies tu perfil más adelante

La geometría fina (bandas, CAPTION_CY, SPLIT_Y…) NO sale del perfil: depende de cada
grabación y se mide (SKILL.md → «Cómo encontrar el espacio muerto»).

Tipografías: `fuente` admite cuatro roles — principal (paneles y tarjetas), titulos (hook),
subtitulos y keywords. Cada uno es «Inter» o {familia, peso, archivo?}. Con `archivo` la
fuente es LOCAL: se busca bajo `fuente.carpeta_marca` (por defecto ~/editor-reels/marca/fuentes)
y se copia a public/fonts/. Sin rol `keywords`, la palabra clave grande va en Anton.
"""
import argparse, json, os, pathlib, re, shutil, subprocess, sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))

DEF_COLORES = {
    "text": "#FFFFFF", "soft": "#D6DCE5", "accent": "#3DD6F5", "highlight": "#3DD6F5",
    "ok": "#4ADE80", "alert": "#FB7185", "ink": "#0B0F14", "line": "#7C8794",
}
NOTAS = {
    "text": "texto principal de paneles y rótulos", "soft": "texto secundario",
    "accent": "el color del CTA y de los detalles que mandan: úsalo poco",
    "highlight": "resalte de la palabra activa del subtítulo",
    "ok": "checks, «hecho», sellos en verde", "alert": "tachados, errores, sellos en rojo",
    "ink": "fondo de paneles y lienzo", "line": "líneas finas, handle, etiquetas apagadas",
}
DEF_SUBS = {"upper": True, "size": 80, "maxWords": 4, "band": False, "byBrand": True,
            "peso": 800, "interletrado": "-0.02em"}
DEF_HOOK = {"estilo": "caja", "fondo": "#FFFFFF", "texto": None, "upper": False, "radio": 28, "peso": 800}
RAILES = {   # dónde queda la zona libre del plano → columna del kicker, secciones y chips
    "izquierda": {"x": 70, "w": 430},
    "derecha":   {"x": 470, "w": 430},
    "arriba":    {"x": 70, "w": 830},
}
FUENTE_VAR = {"principal": "fontFamily", "titulos": "fontTitulos",
              "subtitulos": "fontSubs", "keywords": "fontKeywords"}

FONTS_CABECERA = '''// GENERADO por scripts/aplica_perfil.py — cambia las fuentes en tu perfil, no aquí.
import { continueRender, delayRender, staticFile } from "remotion";
'''
FONTS_LOCAL = '''
/** Fuente local de public/fonts/: Remotion espera a que cargue antes de pintar. */
const cargaLocal = (familia: string, archivo: string): string => {
  const h = delayRender(`fuente ${familia}`);
  new FontFace(familia, `url(${staticFile(`fonts/${archivo}`)})`).load()
    .then((f) => { (document.fonts as unknown as { add(f: FontFace): void }).add(f); continueRender(h); })
    .catch((e) => { console.error(`fuente ${familia}`, e); continueRender(h); });
  return `"${familia}", sans-serif`;
};
'''


def modulo(nombre):
    """«Plus Jakarta Sans» -> «PlusJakartaSans» (nombre del módulo de @remotion/google-fonts)."""
    return re.sub(r"[^A-Za-z0-9]", "", nombre.title() if nombre.islower() else nombre)


def pesos(mod, quiero):
    """Pesos disponibles de la fuente; si no hay node_modules, se confía en la lista."""
    nm = RAIZ / "node_modules" / "@remotion" / "google-fonts"
    if not nm.exists():
        return quiero
    js = f"const f=require('@remotion/google-fonts/{mod}');console.log(JSON.stringify(Object.keys(f.getInfo().fonts.normal||{{}})))"
    r = subprocess.run(["node", "-e", js], cwd=RAIZ, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"«{mod}» no está en Google Fonts (o el nombre no casa). Mira https://fonts.google.com")
    hay = json.loads(r.stdout)
    ok = [w for w in quiero if w in hay]
    if len(ok) < len(quiero):
        print(f"  aviso: {mod} no tiene los pesos {sorted(set(quiero) - set(ok))}; el navegador los simulará")
    return ok or hay[-1:]


def ts(v):
    return json.dumps(v, ensure_ascii=False) if not isinstance(v, bool) else ("true" if v else "false")


def rol(fuente, nombre):
    """Un rol de tipografía como dict {familia, peso?, archivo?}; cae al rol principal
    (salvo keywords, que cae a Anton: una palabra gigante necesita una fuente condensada)."""
    v = fuente.get(nombre) or ("Anton" if nombre == "keywords" else fuente.get("principal", "Inter"))
    return v if isinstance(v, dict) else {"familia": v}


def escribe_fuentes(fuente):
    from perfil import MARCA
    carpeta = fuente.get("carpeta_marca") or str(MARCA / "fuentes")
    destino = RAIZ / "public" / "fonts"
    imports, cuerpo, resumen, hay_local = [], [], [], False
    for nombre in FUENTE_VAR:
        r = rol(fuente, nombre)
        fam, var = r["familia"], FUENTE_VAR[nombre]
        if r.get("archivo"):
            hay_local = True
            hits = list(pathlib.Path(os.path.expanduser(carpeta)).rglob(r["archivo"])) if carpeta else []
            if not hits and not (destino / r["archivo"]).exists():
                sys.exit(f"No encuentro {r['archivo']} (fuente.carpeta_marca={carpeta!r})")
            destino.mkdir(parents=True, exist_ok=True)
            if hits:
                shutil.copyfile(hits[0], destino / r["archivo"])
            cuerpo.append(f'export const {var} = cargaLocal({json.dumps(fam)}, {json.dumps(r["archivo"])});')
        else:
            mod = modulo(fam)
            quiero = ["400"] if nombre == "keywords" else (["600", "700", "800"] if nombre == "principal"
                                                          else [str(r.get("peso", 800))])
            ws = pesos(mod, quiero)
            imports.append(f'import {{ loadFont as load_{nombre} }} from "@remotion/google-fonts/{mod}";')
            cuerpo.append(f'export const {{ fontFamily: {var} }} = load_{nombre}("normal", {{\n'
                          f'  weights: {json.dumps(ws)}, subsets: ["latin", "latin-ext"], ignoreTooManyRequestsWarning: true,\n'
                          f'}});')
        resumen.append(f"{nombre}={fam}")
    mono = modulo(fuente.get("mono", "JetBrains Mono"))
    wm = pesos(mono, ["500", "700"])
    out = FONTS_CABECERA + "\n".join(imports) + "\n"
    out += f'import {{ loadFont as loadMono }} from "@remotion/google-fonts/{mono}";\n'
    out += (FONTS_LOCAL if hay_local else "") + "\n" + "\n".join(cuerpo) + "\n"
    out += (f'export const {{ fontFamily: mono }} = loadMono("normal", {{\n'
            f'  weights: {json.dumps(wm)}, subsets: ["latin"], ignoreTooManyRequestsWarning: true,\n}});\n')
    (RAIZ / "src" / "fonts.ts").write_text(out, encoding="utf-8")
    return ", ".join(resumen)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--perfil")
    a = ap.parse_args()
    if a.perfil:
        perfil = json.loads(pathlib.Path(a.perfil).read_text(encoding="utf-8"))
    else:
        from perfil import carga
        perfil = carga()
    if not perfil:
        print("sin perfil: se quedan los valores neutros (corre el cuestionario de la skill)")

    col = {**DEF_COLORES, **perfil.get("colores", {})}
    subs = {**DEF_SUBS, **perfil.get("subtitulos", {})}
    subs.setdefault("color", col["soft"])      # color de la palabra que aún no suena
    plano = perfil.get("plano", {})
    rail = RAILES.get(plano.get("espacio_libre", "izquierda"), RAILES["izquierda"])
    align = "inline" if plano.get("fuente_habitual") == "split" else "chip"

    w = max(len(k) for k in col) + 2
    bloque = "// ── PERFIL (generado por aplica_perfil.py) ──\nexport const COLORS = {\n"
    bloque += "".join(f'  {(k + ":").ljust(w)} "{v}",   // {NOTAS.get(k, "")}\n' for k, v in col.items())
    bloque += "} as const;\nexport const CAPTIONS = {\n"
    bloque += "".join(f"  {k}: {ts(v)},\n" for k, v in subs.items())
    bloque += "} as const;\n"
    bloque += f'export const RAIL = {{ x: {rail["x"]}, w: {rail["w"]} }} as const;   // columna libre del plano\n'
    bloque += f'export const TOPIC_ALIGN_DEFAULT: "chip" | "inline" | "off" = "{align}";\n'
    hk = {**DEF_HOOK, **{k: v for k, v in perfil.get("hook", {}).items() if k in DEF_HOOK}}
    if hk["estilo"] not in ("caja", "suelto"):
        hk["estilo"] = "caja"    # "ninguno" = no se escribe hook en cortes.json; el tipo sigue siendo válido
    hk["texto"] = hk["texto"] or col["ink"]
    bloque += (f'export const HOOK = {{ estilo: "{hk["estilo"]}" as "caja" | "suelto", fondo: "{hk["fondo"]}", '
               f'texto: "{hk["texto"]}", upper: {ts(bool(hk["upper"]))}, radio: {int(hk["radio"])}, peso: {int(hk["peso"])} }} as const;\n')
    bloque += "// ── FIN PERFIL ──\n"

    th = RAIZ / "src" / "theme.ts"
    s = th.read_text(encoding="utf-8")
    s2, n = re.subn(r"// ── PERFIL.*?// ── FIN PERFIL ──\n", lambda _: bloque, s, flags=re.S)
    if not n:
        sys.exit("theme.ts no tiene el bloque PERFIL")
    th.write_text(s2, encoding="utf-8")

    fuentes = escribe_fuentes(perfil.get("fuente", {}))
    # logo propio (fuera de Simple Icons): se registra en este proyecto como pegatina
    lp = perfil.get("logo_propio")
    if lp and lp.get("archivo"):
        from perfil import MARCA
        ruta = pathlib.Path(os.path.expanduser(lp["archivo"]))
        ruta = ruta if ruta.is_absolute() else MARCA / "logos" / ruta
        if ruta.exists():
            subprocess.run([sys.executable, str(RAIZ / "scripts" / "logos_gen.py"), "--imagen", lp.get("id", "mimarca"),
                            str(ruta), lp.get("nombre", perfil.get("nombre", "Mi marca")), lp.get("color", col["accent"])],
                           check=True, capture_output=True)
            print(f"  logo propio registrado: {lp.get('id', 'mimarca')}")
        else:
            print(f"  aviso: no encuentro el logo {ruta}")
    if perfil:
        (RAIZ / "perfil.json").write_text(json.dumps(perfil, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"perfil aplicado: fuentes {fuentes} · acento {col['accent']} · resalte {col['highlight']} · "
          f"subtítulos {'MAYÚS' if subs['upper'] else 'normal'} {subs['size']}px · raíl {plano.get('espacio_libre', 'izquierda')} · hook {hk['estilo']}")


if __name__ == "__main__":
    main()
