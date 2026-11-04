"use strict";

const state = {
  data: null,
  brand: "all",
  polymer: "all",
  line: "all",
  search: "",
  onlySwatches: true,
  includeEstimates: false,
  onlyMulticolor: false,
  limit: 144,
  previousFocus: null
};

const byId = id => document.getElementById(id);
const el = (tag, className, value) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (value !== undefined) node.textContent = String(value);
  return node;
};
const hexValid = value =>
  typeof value === "string" && /^#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?$/.test(value);
const brandName = brandId => {
  const match = state.data.brands.find(brand => brand.id === brandId);
  return match ? match.name : brandId;
};
const norm = text => String(text || "").toLocaleLowerCase("ru-RU");
const allColors = () => state.data.lines.flatMap(line =>
  line.colors.map(color => ({ line, color })));
const sourceType = color => color.measured_sample || color.hex || (color.rgba_swatches || []).length ? "sample" : "missing";

function colorBackground(color) {
  if (hexValid(color.measured_sample?.hex)) return color.measured_sample.hex;
  const swatches = (color.rgba_swatches || []).filter(hexValid);
  if (color.color_mode === "gradient" && swatches.length > 1) {
    return "linear-gradient(112deg, " + swatches.join(", ") + ")";
  }
  if (color.color_mode === "multicolor" && swatches.length > 1) {
    const parts = swatches.map((hex, index) => {
      const start = Math.round(100 * index / swatches.length);
      const end = Math.round(100 * (index + 1) / swatches.length);
      return hex + " " + start + "% " + end + "%";
    });
    return "linear-gradient(112deg, " + parts.join(", ") + ")";
  }
  if (hexValid(color.hex)) return color.hex;
  if (swatches.length) return swatches[0];
  return null;
}


function renderHeroSamples() {
  const host = byId("heroSamples");
  const candidates = allColors().filter(({ color }) => {
    const ref = color.measured_sample?.hex || color.rgba_swatches?.[0] || color.hex;
    return hexValid(ref) && color.hex_source !== "estimated" && color.visual_data_status !== "estimated";
  });
  // Choose six different hues from source-backed data, not illustrative placeholder colors.
  const targets = [8, 45, 95, 155, 215, 285];
  const selected = [];
  const used = new Set();
  const hueDistance = (a, b) => Math.min(Math.abs(a - b), 360 - Math.abs(a - b));
  const info = color => {
    const hex = (color.measured_sample?.hex || color.rgba_swatches?.[0] || color.hex).slice(1, 7);
    const r = parseInt(hex.slice(0, 2), 16) / 255;
    const g = parseInt(hex.slice(2, 4), 16) / 255;
    const b = parseInt(hex.slice(4, 6), 16) / 255;
    const max = Math.max(r, g, b), min = Math.min(r, g, b), delta = max - min;
    let hue = 0;
    if (delta > 0) {
      if (max === r) hue = ((g - b) / delta) % 6;
      else if (max === g) hue = (b - r) / delta + 2;
      else hue = (r - g) / delta + 4;
      hue = (hue * 60 + 360) % 360;
    }
    return {hue, saturation: max === 0 ? 0 : delta / max};
  };
  for (const target of targets) {
    const remaining = candidates.filter(item => !used.has(item.color.id + ":" + item.line.id));
    if (!remaining.length) break;
    remaining.sort((a, b) => {
      const ia = info(a.color), ib = info(b.color);
      const da = hueDistance(ia.hue, target) + (1 - ia.saturation) * 75;
      const db = hueDistance(ib.hue, target) + (1 - ib.saturation) * 75;
      return da - db;
    });
    const choice = remaining[0];
    selected.push(choice);
    used.add(choice.color.id + ":" + choice.line.id);
  }
  host.replaceChildren();
  if (!selected.length) {
    host.appendChild(el("p", "preview-loading", "Нет подтверждённых образцов для предпросмотра"));
    return;
  }
  for (const {line, color} of selected) {
    const item = el("div", "hero-sample");
    const pigment = el("div", "hero-sample-pigment");
    pigment.style.background = colorBackground(color);
    item.appendChild(pigment);
    item.appendChild(el("span", "hero-sample-name", color.name));
    item.appendChild(el("span", "hero-sample-meta", brandName(line.brand) + " · " + line.polymer));
    host.appendChild(item);
  }
}

function swatchNode(color, detail = false) {
  const node = el("div", detail ? "detail-swatch checker" : "swatch checker");
  const background = colorBackground(color);
  if (background) {
    const pigment = el("div", "pigment");
    pigment.style.background = background;
    node.appendChild(pigment);
  } else {
    node.appendChild(el("div", "no-swatch", "Цвет пока не определён"));
  }
  if (!detail) {
    let status = "HEX";
    if (!background) status = "Нет образца";
    else if (color.measured_sample) status = "Измеренный";
    else if (color.visual_data_status === "estimated" || color.hex_source === "estimated") status = "Оценочный";
    else if (color.color_mode === "gradient") status = "Градиент";
    else if (color.color_mode === "multicolor") status = "Многоцветный";
    else if (color.rgba_swatches?.length === 1 && color.rgba_swatches[0].slice(-2).toUpperCase() !== "FF") status = "Полупрозрачный";
    node.appendChild(el("span", "chip", status));
  }
  return node;
}

function renderBrands() {
  const host = byId("brands");
  host.replaceChildren();
  byId("brandCount").textContent = String(state.data.brands.length);
  const counts = new Map();
  for (const line of state.data.lines) {
    if (state.polymer !== "all" && line.polymer !== state.polymer) continue;
    counts.set(line.brand, (counts.get(line.brand) || 0) + line.colors.length);
  }
  const entries = [{ id: "all", name: "Все бренды" }, ...state.data.brands];
  for (const brand of entries) {
    const button = el("button", "brand-option" + (state.brand === brand.id ? " active" : ""));
    button.type = "button";
    button.setAttribute("aria-pressed", String(state.brand === brand.id));
    button.appendChild(el("span", "letter", brand.id === "all" ? "–" : brand.name.slice(0, 1).toUpperCase()));
    button.appendChild(el("span", "", brand.name));
    const count = brand.id === "all"
      ? Array.from(counts.values()).reduce((a, b) => a + b, 0)
      : counts.get(brand.id) || 0;
    button.appendChild(el("span", "count", count));
    button.addEventListener("click", () => {
      state.brand = brand.id;
      state.line = "all";
      state.limit = 144;
      update();
    });
    host.appendChild(button);
  }
}

function renderLineFilter() {
  const select = byId("lineFilter");
  const available = state.data.lines.filter(line =>
    (state.brand === "all" || line.brand === state.brand) &&
    (state.polymer === "all" || line.polymer === state.polymer));
  if (state.line !== "all" && !available.some(line => line.id === state.line)) state.line = "all";
  select.replaceChildren(new Option("Все линейки", "all"));
  for (const line of available) {
    select.appendChild(new Option(
      (state.brand === "all" ? brandName(line.brand) + " · " : "") + line.name,
      line.id
    ));
  }
  select.value = state.line;
}

function filteredColors() {
  const query = norm(state.search.trim());
  return allColors().filter(({line, color}) => {
    if (state.brand !== "all" && line.brand !== state.brand) return false;
    if (state.polymer !== "all" && line.polymer !== state.polymer) return false;
    if (state.line !== "all" && state.line !== line.id) return false;
    if (state.onlySwatches && sourceType(color) === "missing") return false;
    if (!state.includeEstimates && color.hex_source === "estimated" && !color.measured_sample) return false;
    if (state.onlyMulticolor && !["multicolor", "gradient"].includes(color.color_mode)) return false;
    if (!query) return true;
    return norm([
      line.name, line.id, line.polymer, brandName(line.brand), color.name,
      color.id, color.manufacturer_color_code, color.hex, color.manufacturer_palette_code
    ].join(" ")).includes(query);
  });
}

function renderResults() {
  const matches = filteredColors();
  const host = byId("grid");
  const fragment = document.createDocumentFragment();
  host.replaceChildren();
  byId("resultsTitle").textContent = state.line !== "all"
    ? state.data.lines.find(line => line.id === state.line)?.name || "Каталог"
    : state.brand !== "all" ? brandName(state.brand) : "Все филаменты";
  byId("resultCount").textContent = matches.length + " вариантов";
  byId("empty").hidden = matches.length !== 0;

  for (const {line, color} of matches.slice(0, state.limit)) {
    const card = el("button", "swatch-card");
    card.type = "button";
    card.setAttribute("aria-label", brandName(line.brand) + ", " + line.name + ", " + color.name);
    card.appendChild(swatchNode(color));
    const body = el("div", "card-body");
    body.appendChild(el("div", "card-overline", brandName(line.brand) + " / " + line.name));
    body.appendChild(el("div", "card-name", color.name));
    const bottom = el("div", "card-bottom");
    bottom.appendChild(el("span", "", line.polymer + " · " + (line.finish || "standard")));
    bottom.appendChild(el("span", "code", color.manufacturer_color_code || color.hex || "—"));
    body.appendChild(bottom);
    card.appendChild(body);
    card.addEventListener("click", () => openDetails(line, color));
    fragment.appendChild(card);
  }
  if (matches.length > state.limit) {
    const more = el("button", "load-more", "Показать ещё " + Math.min(144, matches.length - state.limit) + " из " + (matches.length - state.limit));
    more.type = "button";
    more.addEventListener("click", () => {
      state.limit += 144;
      renderResults();
    });
    fragment.appendChild(more);
  }
  host.appendChild(fragment);
}

function addRow(container, label, value) {
  if (value === undefined || value === null || value === "") return;
  const row = el("div", "spec-row");
  row.appendChild(el("span", "", label));
  row.appendChild(el("strong", "", value));
  container.appendChild(row);
}

function openDetails(line, color) {
  const target = byId("detailContent");
  target.replaceChildren();
  state.previousFocus = document.activeElement;
  target.appendChild(el("h3", "", color.name));
  target.appendChild(el("p", "detail-sub", brandName(line.brand) + " / " + line.polymer + " / " + line.name));
  target.appendChild(swatchNode(color, true));
  const status = sourceType(color) === "missing"
    ? "Цвет не определён: есть название производителя, но нет достоверного HEX/RGB."
    : color.measured_sample
      ? "Есть измерение физического отпечатка из внешнего каталога. Условия печати, освещение и партия могут влиять на результат."
    : color.visual_data_status === "estimated" || color.hex_source === "estimated"
      ? "Оценочный оттенок по внешнему справочнику. Не является официальным HEX производителя или проверенным совпадением с печатью."
      : "Цветовой образец производителя. Не является результатом измерения готовой печати.";
  target.appendChild(el("div", "detail-status" + (sourceType(color) === "missing" ? " missing" : ""), status));
  const rows = el("div", "spec");
  addRow(rows, "Полимер", line.polymer);
  addRow(rows, "Линейка", line.name);
  addRow(rows, "Фактура", line.finish);
  addRow(rows, "HEX производителя / справочника", color.hex);
  addRow(rows, "Измеренный HEX отпечатка", color.measured_sample?.hex);
  addRow(rows, "CIELAB отпечатка", color.measured_sample?.lab?.join(" · "));
  addRow(rows, "Источник HEX", color.hex_source === "estimated" ? "Оценка третьей стороны" : color.hex_source === "manufacturer" ? "Производитель" : color.hex_source);
  addRow(rows, "RGBA-образцы", (color.rgba_swatches || []).join("  ·  "));
  addRow(rows, "Тип цвета", color.color_mode || "solid");
  addRow(rows, "Код производителя", color.manufacturer_color_code);
  addRow(rows, "Код палитры", color.manufacturer_palette_code);
  const preset = state.data.presets[line.appearance_preset] || {};
  addRow(rows, "Визуальный пресет", preset.name);
  addRow(rows, "Микрошероховатость", preset.appearance?.roughness);
  addRow(rows, "Точность пресета", preset.status === "uncalibrated" ? "Приближённый, не откалиброван" : preset.status);
  addRow(rows, "Проверено", color.verified_on);
  target.appendChild(rows);
  const url = color.source_url || line.source_url;
  if (url && /^https:\/\//.test(url)) {
    const link = el("a", "source-link", "Открыть первоисточник ↗");
    link.href = url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    target.appendChild(link);
  }
  if (color.measured_sample?.source_url && /^https:\/\//.test(color.measured_sample.source_url)) {
    const measuredLink = el("a", "source-link", "Измерение физического образца ↗");
    measuredLink.href = color.measured_sample.source_url;
    measuredLink.target = "_blank";
    measuredLink.rel = "noopener noreferrer";
    target.appendChild(measuredLink);
  }
  if (color.color_reference_url && /^https:\/\//.test(color.color_reference_url) && color.color_reference_url !== color.measured_sample?.source_url) {
    const refLink = el("a", "source-link", "Открыть источник приблизительного цвета ↗");
    refLink.href = color.color_reference_url;
    refLink.target = "_blank";
    refLink.rel = "noopener noreferrer";
    target.appendChild(refLink);
  }
  if (color.color_reference_note) target.appendChild(el("p", "caution", color.color_reference_note));
  if (color.visual_note) target.appendChild(el("p", "caution", color.visual_note));
  target.appendChild(el("p", "caution", "Это демонстрация данных каталога, а не физически корректный Fusion Render. Градиент на карточке показывает сочетание цветовых образцов, но не реальную ориентацию и высоту переходов в FDM-печати."));
  byId("overlay").hidden = false;
  byId("details").classList.add("open");
  byId("details").setAttribute("aria-hidden", "false");
  document.body.style.overflow = "hidden";
  byId("closeDetails").focus();
}

function closeDetails() {
  byId("details").classList.remove("open");
  byId("details").setAttribute("aria-hidden", "true");
  byId("overlay").hidden = true;
  document.body.style.overflow = "";
  if (state.previousFocus && document.contains(state.previousFocus)) state.previousFocus.focus();
}

function update() {
  document.querySelectorAll("[data-polymer]").forEach(button => {
    const active = state.polymer === button.dataset.polymer;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  });
  renderBrands();
  renderLineFilter();
  renderResults();
}

async function initialize() {
  byId("grid").appendChild(el("div", "empty", "Загрузка каталога…"));
  try {
    const response = await fetch("./data/catalog.json", {cache: "no-cache"});
    if (!response.ok) throw new Error("HTTP " + response.status);
    state.data = await response.json();
    const counts = state.data.meta.counts;
    byId("totalBrands").textContent = counts.brands;
    byId("totalLines").textContent = counts.lines;
    byId("totalColors").textContent = counts.colors;
    const date = new Date(state.data.meta.generated_at);
    byId("snapshotDate").textContent = "Сборка " + date.toLocaleDateString("ru-RU");
    byId("footerVersion").textContent = "Снимок каталога";
    renderHeroSamples();
    update();
  } catch (err) {
    byId("grid").replaceChildren();
    byId("resultCount").textContent = "Ошибка загрузки";
    byId("empty").hidden = false;
    byId("empty").querySelector("strong").textContent = "Каталог не загружен";
    byId("empty").querySelector("p").textContent = String(err);
  }
}

byId("search").addEventListener("input", event => {
  state.search = event.target.value;
  state.limit = 144;
  if (state.data) renderResults();
});
byId("polymerButtons").addEventListener("click", event => {
  const button = event.target.closest("[data-polymer]");
  if (!button || !state.data) return;
  state.polymer = button.dataset.polymer;
  state.line = "all";
  state.limit = 144;
  update();
});
byId("lineFilter").addEventListener("change", event => {
  state.line = event.target.value;
  state.limit = 144;
  if (state.data) renderResults();
});
byId("onlySwatches").addEventListener("change", event => {
  state.onlySwatches = event.target.checked;
  state.limit = 144;
  if (state.data) renderResults();
});
byId("includeEstimates").addEventListener("change", event => {
  state.includeEstimates = event.target.checked;
  state.limit = 144;
  if (state.data) renderResults();
});
byId("onlyMulticolor").addEventListener("change", event => {
  state.onlyMulticolor = event.target.checked;
  state.limit = 144;
  if (state.data) renderResults();
});
byId("reset").addEventListener("click", () => {
  Object.assign(state, {
    brand: "all", polymer: "all", line: "all", search: "",
    onlySwatches: true, includeEstimates: false, onlyMulticolor: false, limit: 144
  });
  byId("search").value = "";
  byId("onlySwatches").checked = true;
  byId("includeEstimates").checked = false;
  byId("onlyMulticolor").checked = false;
  if (state.data) update();
});
byId("toggleFilters").addEventListener("click", () => {
  const button = byId("toggleFilters");
  const expanded = button.getAttribute("aria-expanded") !== "true";
  button.setAttribute("aria-expanded", String(expanded));
  byId("filtersPanel").classList.toggle("is-open", expanded);
  byId("filterChevron").textContent = expanded ? "−" : "+";
});
byId("closeDetails").addEventListener("click", closeDetails);
byId("overlay").addEventListener("click", closeDetails);
window.addEventListener("keydown", event => {
  if (event.key === "Escape" && !byId("overlay").hidden) closeDetails();
  if (event.key === "Tab" && !byId("overlay").hidden) {
    const focusable = Array.from(byId("details").querySelectorAll("button, a[href], input, select")).filter(item => !item.disabled);
    if (focusable.length) {
      const first = focusable[0], last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
  }
});
initialize();
