// GENERADO por scripts/aplica_perfil.py — cambia las fuentes en tu perfil, no aquí.
// (Valores neutros hasta que corras aplica_perfil.py: Inter + Anton.)
import { loadFont as load_principal } from "@remotion/google-fonts/Inter";
import { loadFont as load_keywords } from "@remotion/google-fonts/Anton";
import { loadFont as loadMono } from "@remotion/google-fonts/JetBrainsMono";

export const { fontFamily } = load_principal("normal", {
  weights: ["600", "700", "800"], subsets: ["latin", "latin-ext"], ignoreTooManyRequestsWarning: true,
});
export const fontTitulos = fontFamily;
export const fontSubs = fontFamily;
export const { fontFamily: fontKeywords } = load_keywords("normal", {
  weights: ["400"], subsets: ["latin", "latin-ext"], ignoreTooManyRequestsWarning: true,
});
export const { fontFamily: mono } = loadMono("normal", {
  weights: ["500", "700"], subsets: ["latin"], ignoreTooManyRequestsWarning: true,
});
