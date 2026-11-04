"use strict";

const state = {
  data: null,
  brand: "all",
  polymer: "all",
  line: "all",
  search: "",
  onlySwatches: false,
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
const sourceType = color => color.hex || (color.rgba_swatches || []).length ? "sample" : "missing";

function colorBackground(color) {
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
    if (!background) status = "NAME ONLY";
    else if (color.color_mode === "gradient") status = "GRADIENT";
    else if (color.color_mode === "multicolor") status = "MULTICOLOR";
    else if (color.rgba_swatches?.length === 1 && color.rgba_swatches[0].slice(-2).toUpperCase() !== "FF") status = "ALPHA";
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
    button.appendChild(el("span", "letter", brand.id === "all" ? "✦" : brand.name.slice(0, 1).toUpperCase()));
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
    const more = el("button", "swatch-card", "Показать ещё 144 из " + (matches.length - state.limit));
    more.style.minHeight = "100px";
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
    : "Цветовой образец производителя. Не является результатом измерения готовой печати.";
  target.appendChild(el("div", "detail-status" + (sourceType(color) === "missing" ? " missing" : ""), status));
  const rows = el("div", "spec");
  addRow(rows, "Полимер", line.polymer);
  addRow(rows, "Линейка", line.name);
  addRow(rows, "Фактура", line.finish);
  addRow(rows, "HEX", color.hex);
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
    byId("footerVersion").textContent = "MANUAL SNAPSHOT";
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
byId("onlyMulticolor").addEventListener("change", event => {
  state.onlyMulticolor = event.target.checked;
  state.limit = 144;
  if (state.data) renderResults();
});
byId("reset").addEventListener("click", () => {
  Object.assign(state, {
    brand: "all", polymer: "all", line: "all", search: "",
    onlySwatches: false, onlyMulticolor: false, limit: 144
  });
  byId("search").value = "";
  byId("onlySwatches").checked = false;
  byId("onlyMulticolor").checked = false;
  if (state.data) update();
});
byId("closeDetails").addEventListener("click", closeDetails);
byId("overlay").addEventListener("click", closeDetails);
window.addEventListener("keydown", event => {
  if (event.key === "Escape" && !byId("overlay").hidden) closeDetails();
});
initialize();
