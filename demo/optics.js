/**
 * Filamentra visual haze approximation — shared 0..1 parameter.
 * Haze is distinct from transmitted-light fraction and from surface roughness.
 * Fusion's adapter uses the same mapping as a fallback, not as an exact feature.
 */
export function hazeEffectiveRoughness(haze, baseRoughness = 0) {
  if (!Number.isFinite(haze) || haze < 0 || haze > 1) {
    throw new RangeError("haze must be within [0,1]");
  }
  if (!Number.isFinite(baseRoughness) || baseRoughness < 0 || baseRoughness > 1) {
    throw new RangeError("roughness must be within [0,1]");
  }
  return Math.max(baseRoughness, 0.16 + 0.56 * haze);
}
