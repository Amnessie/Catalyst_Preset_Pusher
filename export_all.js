// Writes every library sound as a .catl6p, once per pickup setting:  node export_all.js [output folder]
//
// Output: <folder>/<pickups>/<category>/[<artist>/]<sound>.catl6p for the Catalyst 60,
// with the overall level "As designed". Default folder: Downloads/Catalyst Presets - all.
const fs = require("fs");
const os = require("os");
const path = require("path");
const vm = require("vm");

const HERE = __dirname;
const OUT = process.argv[2] || path.join(os.homedir(), "Downloads", "Catalyst Presets - all");
const PICKUPS = { "Mixed (HSS)": "neutral", Humbucker: "humbucker", "Single coil": "single" };

// Run the page's own code in a bare-bones fake browser so presets are built exactly as the app builds them.
const el = () => ({ innerHTML: "", textContent: "", value: "", hidden: false, style: {}, dataset: {},
  addEventListener() {}, appendChild() {}, click() {}, remove() {} });
const els = {};
const ctx = {
  console, setTimeout, setInterval() {}, clearTimeout() {}, TextEncoder, Uint8Array, Uint32Array, DataView, ArrayBuffer,
  Date, Math, JSON, Number, String, Boolean, Object, Set,
  localStorage: { getItem: () => null, setItem() {} },
  location: { protocol: "file:" }, fetch: async () => { throw new Error("offline"); }, alert() {}, confirm: () => false,
  URL: { createObjectURL: () => "", revokeObjectURL() {} },
  Blob: class { constructor(parts) { this.parts = parts; } },
  document: { getElementById: (id) => (els[id] ||= el()), createElement: el, querySelector: () => null,
    addEventListener() {}, body: el() },
};
ctx.window = ctx;
vm.createContext(ctx);
const html = fs.readFileSync(path.join(HERE, "Catalyst Preset Picker.html"), "utf8");
vm.runInContext(fs.readFileSync(path.join(HERE, "models.js"), "utf8"), ctx);
vm.runInContext(fs.readFileSync(path.join(HERE, "presets.js"), "utf8"), ctx);
vm.runInContext(html.match(/<script>\s*"use strict";([\s\S]*?)<\/script>/)[1], ctx);

const safe = (s) => s.replace(/[\\/:*?"<>|]/g, "-").trim();
let count = 0;
for (const [folder, pickups] of Object.entries(PICKUPS)) {
  vm.runInContext(`state.device = "2424833"; state.level = 0; state.pickups = ${JSON.stringify(pickups)};`, ctx);
  for (const p of ctx.PRESET_LIBRARY) {
    const dir = path.join(OUT, folder, p.cat, ...(p.artist ? [safe(p.artist)] : []));
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, safe(p.name) + ".catl6p"), JSON.stringify(ctx.buildPreset(p), null, 1));
    count++;
  }
}
console.log(`Wrote ${count} presets to ${OUT}`);
