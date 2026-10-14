#!/usr/bin/env python3
"""Montaje bruto: varios clips sueltos → un solo public/c1.mp4 sin silencios ni tomas falsas,
con su transcript ya re-cronometrado (no hay que volver a transcribir).

PASOS
  1. Transcribe cada clip (un fichero por llamada):
       python scripts/transcribe.py input/clip1.mp4 work/clip1.json
  2. Propón el montaje:
       python scripts/montaje.py propone input/clip1.mp4 input/clip2.mp4 [--ritmo dinamico]
     → work/montaje.json con las FRASES de cada clip (id, segundos, texto) y las
       sospechas: tomas repetidas (se sugiere quedarse con la última) y frases sueltas.
     El agente lee las frases, decide qué se quita y en qué orden, y lo ENSEÑA al
     usuario antes de cortar. En el JSON:
       "orden":  ["clip2", "clip1"]          orden de los clips (por defecto, el de entrada)
       "quitar": ["clip1#3", "clip2#0"]       frases fuera (tomas falsas, repeticiones)
       "recortes": [{"clip": "clip1", "de": 12.4, "a": 13.1}]   trozos exactos fuera
  3. Corta:
       python scripts/montaje.py corta [--cid c1]
     → public/c1.mp4 (1080x1920, 30 fps, AAC 48 kHz), work/c1.json (transcript en el
       formato de whisper: sigue con `words.py work/c1.json --convert`), work/c1_spans.json
       (zoom alterno 1.0 / 1.12 en cada salto dentro del mismo clip, para que el jump cut
       se sienta intencional) y work/c1_montaje_mapa.json (qué segundo sale de qué clip).

RITMO (silencio máximo que se deja entre frases): tranquilo 0.8 s · dinamico 0.45 s ·
frenetico 0.25 s. Por defecto el del perfil (`ritmo`).

Funciona con el ffmpeg que trae Remotion (no necesita el del sistema): corta cada tramo
re-codificando (preciso al fotograma) y los une con una última pasada de alta calidad.
"""
import argparse, difflib, json, pathlib, re, shutil, sys, unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import ff  # noqa: E402
from perfil import carga  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent
WORK = RAIZ / "work"
RITMOS = {"tranquilo": 0.8, "dinamico": 0.45, "dinámico": 0.45, "frenetico": 0.25, "frenético": 0.25}
PAD_IN, PAD_OUT = 0.10, 0.16      # aire antes y después de cada frase: sin esto se comen consonantes
FPS = 30
W, H = 1080, 1920


def norm(t):
    t = unicodedata.normalize("NFKD", t.lower())
    return re.sub(r"[^a-z0-9ñ ]", "", "".join(c for c in t if not unicodedata.combining(c))).split()


def palabras(transcript):
    d = json.loads(pathlib.Path(transcript).read_text(encoding="utf-8"))
    return [{"w": w["word"].strip(), "s": float(w["start"]), "e": float(w["end"])}
            for s in d["segments"] for w in s.get("words", []) if w["word"].strip()]


def frases(ws, silencio):
    """Agrupa palabras en frases separadas por silencios más largos que `silencio`."""
    out, cur = [], []
    for w in ws:
        if cur and w["s"] - cur[-1]["e"] > silencio:
            out.append(cur); cur = []
        cur.append(w)
    if cur:
        out.append(cur)
    return [{"de": f[0]["s"], "a": f[-1]["e"], "texto": " ".join(x["w"] for x in f)} for f in out]


def sospechas(fr):
    """Marca la frase i si la i+1 o la i+2 empiezan casi igual: es una toma repetida."""
    for i, f in enumerate(fr):
        a = norm(f["texto"])[:6]
        for j in (i + 1, i + 2):
            if j >= len(fr) or len(a) < 2:
                continue
            b = norm(fr[j]["texto"])[:6]
            r = difflib.SequenceMatcher(None, a, b).ratio()
            if r >= 0.6:
                f["sospecha"] = f"toma repetida: se repite en #{j} ({r:.0%}); sugerido quitar esta y quedarse con la última"
                break
        if "sospecha" not in f and len(norm(f["texto"])) <= 2 and (f["a"] - f["de"]) < 1.2:
            f["sospecha"] = "frase suelta muy corta (¿muletilla o arranque en falso?)"


def propone(a):
    perfil = carga()
    silencio = a.silencio or RITMOS.get(a.ritmo or perfil.get("ritmo", "dinamico"), 0.45)
    WORK.mkdir(exist_ok=True)
    clips, quitar = [], []
    for src in a.clips:
        p = pathlib.Path(src)
        cid = p.stem
        tr = WORK / f"{cid}.json"
        if not tr.exists():
            sys.exit(f"Falta el transcript {tr}. Corre antes: python scripts/transcribe.py {src} {tr.relative_to(RAIZ)}")
        info = ff.sonda(p)
        fr = frases(palabras(tr), silencio)
        sospechas(fr)
        for i, f in enumerate(fr):
            f["id"] = f"{cid}#{i}"
            if f.get("sospecha", "").startswith("toma repetida"):
                quitar.append(f["id"])
        clips.append({"clip": cid, "src": str(p.resolve().relative_to(RAIZ)) if p.resolve().is_relative_to(RAIZ) else str(p.resolve()),
                      "dur": round(info["dur"], 3), "w": info.get("w"), "h": info.get("h"), "frases": fr})
        print(f"\n== {cid}  ({info.get('w')}x{info.get('h')}, {info['dur']:.1f}s, {len(fr)} frases)")
        for i, f in enumerate(fr):
            marca = "  ⚠ " + f["sospecha"] if "sospecha" in f else ""
            print(f"  #{i:<3} {f['de']:7.2f}-{f['a']:7.2f}  {f['texto']}{marca}")
    plan = {"_como": "edita orden/quitar/recortes y corre: python scripts/montaje.py corta",
            "silencio": silencio, "orden": [c["clip"] for c in clips], "quitar": quitar,
            "recortes": [], "clips": clips}
    (WORK / "montaje.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n→ work/montaje.json   (sugerido quitar: {', '.join(quitar) or 'nada'})")


def tramos(plan):
    """Lista final de (clip, de, a) en orden, con aire y sin pisar a la frase vecina."""
    por_id = {c["clip"]: c for c in plan["clips"]}
    quitar = set(plan.get("quitar", []))
    rec = plan.get("recortes", [])
    out = []
    for cid in plan["orden"]:
        c = por_id[cid]
        fr = c["frases"]
        for i, f in enumerate(fr):
            if f["id"] in quitar:
                continue
            lo = max(0.0, f["de"] - PAD_IN)
            hi = min(c["dur"], f["a"] + PAD_OUT)
            if i > 0:
                lo = max(lo, (fr[i - 1]["a"] + f["de"]) / 2)
            if i + 1 < len(fr):
                hi = min(hi, (f["a"] + fr[i + 1]["de"]) / 2)
            piezas = [(lo, hi)]
            for r in (r for r in rec if r["clip"] == cid):
                nuevo = []
                for x, y in piezas:
                    if r["a"] <= x or r["de"] >= y:
                        nuevo.append((x, y)); continue
                    if r["de"] > x: nuevo.append((x, r["de"]))
                    if r["a"] < y:  nuevo.append((r["a"], y))
                piezas = nuevo
            out += [(cid, x, y) for x, y in piezas if y - x >= 0.2]
    # tramos contiguos del mismo clip se funden (si no se quitó nada entre medias, no hay corte)
    fundidos = []
    for t in out:
        if fundidos and fundidos[-1][0] == t[0] and abs(fundidos[-1][2] - t[1]) < 0.02:
            fundidos[-1] = (t[0], fundidos[-1][1], t[2])
        else:
            fundidos.append(t)
    return fundidos


def vf_vertical(w, h):
    """Escala para LLENAR 1080x1920 recortando lo que sobra (centrado). Sin barras."""
    if w and h and abs(w / h - W / H) > 0.01:
        if w / h > W / H:   # más ancho: recorta los lados
            return f"scale=-2:{H},crop={W}:{H}"
        return f"scale={W}:-2,crop={W}:{H}"
    return f"scale={W}:{H}"


def corta(a):
    plan = json.loads((WORK / "montaje.json").read_text(encoding="utf-8"))
    por_id = {c["clip"]: c for c in plan["clips"]}
    if a.cid in por_id:
        sys.exit(f"Un clip se llama «{a.cid}» y su transcript se pisaría: renómbralo (p. ej. toma1) o usa --cid otro.")
    ts = tramos(plan)
    if not ts:
        sys.exit("El montaje se quedó vacío: revisa «quitar».")
    tmp = WORK / "montaje_tmp"
    shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir(parents=True)
    horizontales = [c for c in plan["clips"] if c.get("w") and c.get("h") and c["w"] > c["h"]]
    if horizontales:
        print(f"  aviso: {', '.join(c['clip'] for c in horizontales)} es horizontal: se recorta al centro para llenar el vertical."
              " Si es una charla o pantalla, mejor la plantilla 16:9 (guias/avanzado).")

    lista, mapa, segs, spans = [], [], [], []
    t_out, prev_clip, zoom = 0.0, None, 1.0
    for n, (cid, x, y) in enumerate(ts):
        c = por_id[cid]
        dur = round(round((y - x) * FPS) / FPS, 4)
        seg = tmp / f"s{n:03d}.mov"
        src = c["src"] if pathlib.Path(c["src"]).is_absolute() else str(RAIZ / c["src"])
        r = ff.run(["-v", "error", "-y", "-ss", f"{x:.3f}", "-i", src, "-t", f"{dur:.4f}",
                    "-vf", vf_vertical(c.get("w"), c.get("h")), "-r", str(FPS),
                    "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p",
                    "-af", "aresample=48000,apad", "-ac", "2", "-c:a", "pcm_s16le", "-shortest", str(seg)])
        if r.returncode != 0:
            sys.exit(f"ffmpeg falló cortando {cid} {x:.2f}-{y:.2f}:\n{r.stderr[-800:]}")
        real = ff.duracion(seg)
        lista.append(f"file '{seg.name}'")
        # palabras del tramo, movidas a su sitio en la salida
        for w in palabras(WORK / f"{cid}.json"):
            if w["s"] >= x - 0.02 and w["e"] <= y + 0.05:
                s = max(0.0, w["s"] - x) + t_out
                e = min(real, w["e"] - x) + t_out
                segs.append({"word": " " + w["w"], "start": round(s, 3), "end": round(max(e, s + 0.04), 3)})
        # zoom alterno en los saltos dentro del mismo clip (jump cut); al cambiar de clip, plano normal
        zoom = (1.12 if zoom == 1.0 else 1.0) if cid == prev_clip else 1.0
        spans.append({"start": round(t_out, 3), "end": round(t_out + real, 3), "scale": zoom})
        mapa.append({"salida": [round(t_out, 3), round(t_out + real, 3)], "clip": cid, "de": round(x, 3), "a": round(y, 3)})
        t_out += real; prev_clip = cid

    (tmp / "lista.txt").write_text("\n".join(lista) + "\n", encoding="utf-8")
    (RAIZ / "public").mkdir(exist_ok=True)
    salida = RAIZ / "public" / f"{a.cid}.mp4"
    # se une RE-CODIFICANDO: con «-c copy» quedan marcas de tiempo partidas en cada costura y
    # Remotion falla con «No frame found at position…». Calidad alta: la imagen se comprime otra vez al render.
    r = ff.run(["-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(tmp / "lista.txt"),
                "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", "-r", str(FPS),
                "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", str(salida)])
    if r.returncode != 0:
        sys.exit(f"ffmpeg falló uniendo:\n{r.stderr[-800:]}")
    total = ff.duracion(salida)
    spans[-1]["end"] = round(total + 1, 3)   # el último tramo cubre hasta el final
    whisper = {"language": carga().get("idioma", "es"), "duration": round(total, 3),
               "segments": [{"start": segs[0]["start"] if segs else 0, "end": segs[-1]["end"] if segs else 0,
                             "text": "".join(s["word"] for s in segs), "words": segs}]}
    (WORK / f"{a.cid}.json").write_text(json.dumps(whisper, ensure_ascii=False, indent=1), encoding="utf-8")
    (WORK / f"{a.cid}_spans.json").write_text(json.dumps(spans, indent=1), encoding="utf-8")
    (WORK / f"{a.cid}_montaje_mapa.json").write_text(json.dumps(mapa, ensure_ascii=False, indent=1), encoding="utf-8")
    shutil.rmtree(tmp, ignore_errors=True)
    bruto = sum(c["dur"] for c in plan["clips"])
    print(f"{len(ts)} tramos · {bruto:.1f}s de material → {total:.1f}s · {len(segs)} palabras")
    print(f"→ public/{a.cid}.mp4 · work/{a.cid}.json · work/{a.cid}_spans.json")
    print(f"siguiente: python scripts/words.py work/{a.cid}.json --convert")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("propone"); p.add_argument("clips", nargs="+")
    p.add_argument("--ritmo"); p.add_argument("--silencio", type=float)
    c = sub.add_parser("corta"); c.add_argument("--cid", default="c1")
    a = ap.parse_args()
    propone(a) if a.cmd == "propone" else corta(a)


if __name__ == "__main__":
    main()
