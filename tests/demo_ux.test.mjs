import test from "node:test";
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {createContext, runInContext} from "node:vm";

const source = readFileSync(new URL("../demo/app.js", import.meta.url), "utf8")
  .replace(/initialize\(\);\s*$/, "");

function harness() {
  const elements = new Map();
  const createNode = (tagName = "div") => ({
    tagName, children: [], attributes: {}, style: {}, dataset: {}, textContent: "",
    className: "", hidden: false, disabled: false, value: "",
    classList: {toggle() {}, add() {}, remove() {}},
    appendChild(...items) {
      for (const item of items) this.children.push(...(item.tagName === "fragment" ? item.children : [item]));
      return items.at(-1);
    },
    append(...items) { this.appendChild(...items); },
    replaceChildren(...items) { this.children = []; this.appendChild(...items); },
    setAttribute(name, value) { this.attributes[name] = String(value); },
    getAttribute(name) { return this.attributes[name]; },
    addEventListener() {},
    querySelectorAll() { return []; },
    focus() {}
  });
  const document = {
    createElement: createNode,
    createDocumentFragment: () => createNode("fragment"),
    getElementById(id) {
      if (!elements.has(id)) elements.set(id, createNode(id));
      return elements.get(id);
    },
    querySelectorAll() { return []; },
    body: {style: {}}, activeElement: null
  };
  const window = {
    location: {
      href: "https://example.test/Filamentra-DataSource/",
      get search() { return new URL(this.href).search; }
    },
    addEventListener() {}
  };
  const history = {replaceState(_state, _title, url) { window.location.href = String(url); }};
  const Option = (label, value) => ({label, value});
  const context = createContext({document, window, history, Option, URL, URLSearchParams, Intl});
  runInContext(source, context, {filename: "demo/app.js"});
  const state = runInContext("state", context);
  state.data = {
    brands: [{id: "a", name: "Maker A"}, {id: "b", name: "Maker B"}],
    presets: {},
    lines: [
      {id: "a-pla", brand: "a", name: "PLA Matte", polymer: "PLA", finish: "matte",
        colors: [
          {id: "red", name: "Red", hex: "#FF0000", hex_source: "manufacturer"},
          {id: "blue", name: "Blue", hex: "#0000FF", hex_source: "estimated"},
          {id: "none", name: "Unknown"}
        ]},
      {id: "b-petg", brand: "b", name: "PETG Clear", polymer: "PETG", finish: "transparent",
        colors: [{id: "gradient", name: "Rainbow", color_mode: "gradient",
          rgba_swatches: ["#FF0000", "#0000FF"]}]}
    ]
  };
  const run = expression => runInContext(expression, context);
  return {state, document, window, elements, run};
}

test("curated colors remain the default; estimates and name-only records are opt-in", () => {
  const {state, run} = harness();
  const colors = () => Array.from(run("filteredColors()"), item => item.color.id);
  assert.deepEqual(colors(), ["red", "gradient"]);
  state.includeEstimates = true;
  assert.deepEqual(colors(), ["red", "blue", "gradient"]);
  state.onlySwatches = false;
  assert.deepEqual(colors(), ["red", "blue", "none", "gradient"]);
  state.onlyMulticolor = true;
  assert.deepEqual(colors(), ["gradient"]);
  state.onlyMulticolor = false;
  state.search = "rainbow";
  assert.deepEqual(colors(), ["gradient"]);
});

test("faceted brand counts reflect the currently eligible colors", () => {
  const {state, run, elements} = harness();
  run("renderBrands()");
  assert.deepEqual(elements.get("brands").children.map(b => b.children.at(-1).textContent), ["2", "1", "1"]);
  state.polymer = "PLA";
  run("renderBrands()");
  assert.deepEqual(elements.get("brands").children.map(b => b.children.at(-1).textContent), ["1", "1", "0"]);
});

test("grid and grouped views render the same eligible records", () => {
  const {state, run, elements} = harness();
  run("renderResults()");
  assert.equal(elements.get("grid").children.length, 2);
  state.view = "grouped";
  run("renderResults()");
  assert.deepEqual(elements.get("grid").children.map(section =>
    section.children[0].children[0].children[0].textContent),
    ["Maker A · PLA Matte", "Maker B · PETG Clear"]);
});

test("comparison keeps at most four unique records", () => {
  const {state, run, elements} = harness();
  for (const [line, color] of state.data.lines.flatMap(line => line.colors.map(color => [line, color]))) {
    run("toggleCompare(state.data.lines[" + state.data.lines.indexOf(line) + "], state.data.lines[" +
      state.data.lines.indexOf(line) + "].colors[" + line.colors.indexOf(color) + "])");
  }
  assert.equal(state.comparison.length, 4);
  assert.equal(elements.get("compareCount").textContent, "4 из 4");
  run("toggleCompare(state.data.lines[0], state.data.lines[0].colors[0])");
  assert.equal(state.comparison.length, 3);
});

test("filter permalinks retain the chosen material ID", () => {
  const {state, run, window} = harness();
  window.location.href += "?item=a-pla%7Cred";
  state.search = "Red";
  state.polymer = "PLA";
  run("persistFilters()");
  const url = new URL(window.location.href);
  assert.equal(url.searchParams.get("item"), "a-pla|red");
  assert.equal(url.searchParams.get("q"), "Red");
  assert.equal(url.searchParams.get("polymer"), "PLA");
});
