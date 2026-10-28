// Writes every library sound as a .catl6p, once per pickup setting:  node export_all.js [output folder]
//
// Output: <folder>/<pickups>/<category>/[<artist>/]<sound>.catl6p for the Catalyst 60,
// with the overall level "As designed". Default folder: Downloads/Catalyst Presets - all.
// Also rewrites the "All presets" list in README.md so it matches.
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
// Leaves a file alone when only its save date would change, so git shows only sounds that really changed.
const withoutDate = (text) => text.replace(/"modifieddate": \d+/, "");
const sameExceptDate = (file, text) => {
  try { return withoutDate(fs.readFileSync(file, "utf8")) === withoutDate(text); } catch { return false; }
};
let count = 0, written = 0;
for (const [folder, pickups] of Object.entries(PICKUPS)) {
  vm.runInContext(`state.device = "2424833"; state.level = 0; state.pickups = ${JSON.stringify(pickups)};`, ctx);
  for (const p of ctx.PRESET_LIBRARY) {
    const dir = path.join(OUT, folder, p.cat, ...(p.artist ? [safe(p.artist)] : []));
    fs.mkdirSync(dir, { recursive: true });
    const file = path.join(dir, safe(p.name) + ".catl6p"), text = JSON.stringify(ctx.buildPreset(p), null, 1);
    if (!sameExceptDate(file, text)) { fs.writeFileSync(file, text); written++; }
    count++;
  }
}
console.log(`${count} presets in ${OUT} (${written} new or changed)`);

// ---------- README preset list: one collapsible section per folder ----------
const START = "<!-- preset list: written by export_all.js -->", END = "<!-- end of preset list -->";
const cell = (s) => String(s || "").replace(/\|/g, "\\|");
const lib = ctx.PRESET_LIBRARY;
const table = (sounds, withSong) => [
  withSong ? "| Sound | Song | What it is |" : "| Sound | What it is |",
  withSong ? "|---|---|---|" : "|---|---|",
  ...sounds.map((p) => `| **${cell(p.name)}** |${withSong ? ` ${cell(p.song)} |` : ""} ${cell(p.desc)} |`),
].join("\n");
const details = (summary, body) => `<details>\n<summary><b>${summary}</b></summary>\n\n${body}\n\n</details>`;

const sections = [];
for (const cat of ["Clean", "Fingerstyle", "Blues", "Rock", "Metal", "Ambient"]) {
  const sounds = lib.filter((p) => p.cat === cat);
  if (sounds.length) sections.push(details(`${cat} (${sounds.length})`, table(sounds, false)));
}
const songs = lib.filter((p) => p.cat === "Songs");
const artists = [...new Set(songs.map((p) => p.artist))];
sections.push(details(`Songs (${songs.length})`, artists.map((a) => {
  const sounds = songs.filter((p) => p.artist === a);
  return details(`${a} (${sounds.length})`, table(sounds, true));
}).join("\n\n")));

const list = [
  `Every sound is in all three pickup folders, under \`<pickups>/<style>/\` (songs under \`<pickups>/Songs/<artist>/\`). Click a folder to see what's in it.`,
  "",
  ...sections.flatMap((s) => [s, ""]),
].join("\n");
const readmePath = path.join(HERE, "README.md");
const readme = fs.readFileSync(readmePath, "utf8");
const a = readme.indexOf(START), b = readme.indexOf(END);
if (a >= 0 && b > a) {
  fs.writeFileSync(readmePath, readme.slice(0, a + START.length) + "\n" + list + readme.slice(b));
  console.log(`Updated the preset list in README.md (${lib.length} sounds)`);
}
