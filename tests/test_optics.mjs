import test from "node:test";
import assert from "node:assert/strict";
import { hazeEffectiveRoughness } from "../demo/optics.js";

test("haze raises effective transmission blur without changing source roughness", () => {
  const base = 0.2;
  const pla = hazeEffectiveRoughness(0.8, base);
  const petg = hazeEffectiveRoughness(0.55, base);
  const clear = hazeEffectiveRoughness(0.35, base);
  assert.ok(pla > petg && petg > clear);
  assert.equal(base, 0.2);
  assert.equal(hazeEffectiveRoughness(0, 0.7), 0.7);
});

test("haze bounded 0..1 and never removes existing roughness", () => {
  assert.throws(() => hazeEffectiveRoughness(-0.1, 0.2), RangeError);
  assert.throws(() => hazeEffectiveRoughness(1.1, 0.2), RangeError);
  assert.throws(() => hazeEffectiveRoughness(NaN, 0.2), RangeError);
  for (const haze of [0, 0.1, 0.4, 0.8, 1]) {
    assert.ok(hazeEffectiveRoughness(haze, 0.7) >= 0.7);
  }
});
