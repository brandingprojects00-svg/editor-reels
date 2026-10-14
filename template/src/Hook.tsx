import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { COLORS, WIDTH, FEED_CROP, HOOK } from "./theme";
import { at, outAt, mix, SPR } from "./anim";
import { fontTitulos } from "./fonts";

/** Hook de texto, visible desde el frame 1. El estilo sale del perfil (HOOK en theme.ts):
 *  - "caja":   cada línea en su caja de color (HOOK.fondo) con letra HOOK.texto
 *  - "suelto": texto sin caja, con trazo y sombra para leerse sobre cualquier plano
 *
 *  `lines` son las líneas del título (cada una con su propia caja, apiladas). Una palabra
 *  entre asteriscos —`*gratis*`— toma el color de acento: «letras negras, color ocasional».
 *  No calla los subtítulos: el hook y la voz corren a la vez. */
export type HookData = {
  start: number; end: number;
  lines: string[];
  /** borde superior de la primera línea; por defecto justo dentro del recorte 4:5 del feed */
  top?: number;
  /** color de las palabras marcadas con *asteriscos*; por defecto COLORS.accent */
  color?: string;
  size?: number;
};

const PAD = "10px 28px";

const Linea: React.FC<{ text: string; color: string; size: number }> = ({ text, color, size }) => {
  const partes = text.split(/(\*[^*]+\*)/g).filter(Boolean);
  return (
    <div style={{
      ...(HOOK.estilo === "caja"
        ? { background: HOOK.fondo, borderRadius: HOOK.radio, padding: PAD, color: HOOK.texto }
        : { padding: "0 10px", color: COLORS.text,
            textShadow: "0 0 3px rgba(0,0,0,0.9), 0 4px 18px rgba(0,0,0,0.75)", WebkitTextStroke: "1.5px rgba(0,0,0,0.55)" }),
      fontFamily: fontTitulos, fontWeight: HOOK.peso, fontSize: size,
      lineHeight: 1.08, letterSpacing: 0, textTransform: HOOK.upper ? "uppercase" : "none", whiteSpace: "nowrap",
    }}>
      {partes.map((t, i) => t.startsWith("*")
        ? <span key={i} style={{ color }}>{t.slice(1, -1)}</span>
        : <span key={i}>{t}</span>)}
    </div>
  );
};

export const Hook: React.FC<{ hook: HookData }> = ({ hook }) => {
  const frame = useCurrentFrame(); const { fps } = useVideoConfig();
  const t = frame / fps;
  if (t < hook.start || t >= hook.end) return null;

  const size = hook.size ?? 64;
  const color = hook.color ?? COLORS.accent;
  const p = at(frame, fps, hook.start, SPR.snap);
  const out = outAt(t, hook.end, 0.3);
  // entra con un golpe de escala desde arriba; sale subiendo y desvaneciéndose (regla 5)
  return (
    <div style={{
      position: "absolute", left: 0, width: WIDTH,   // centrado en el cuadro, como los subtítulos
      top: hook.top ?? FEED_CROP.y0 + 15,
      display: "flex", flexDirection: "column", alignItems: "center", gap: 10,
      opacity: Math.min(1, p * 4) * out,
      transform: `translateY(${mix(p, -34, 0) + mix(out, -20, 0)}px) scale(${mix(p, 0.92, 1)})`,
      transformOrigin: "50% 0%",
    }}>
      {hook.lines.map((l, i) => <Linea key={i} text={l} color={color} size={size} />)}
    </div>
  );
};
