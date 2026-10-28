// Builds the shareable zip:  node build_share.js
//
// Output: dist/Catalyst Preset Picker.zip containing
//   Catalyst Preset Picker.html   one self-contained file (models + sounds inlined)
//   Ready-made presets/<amp>/<category>/<sound>.catl6p
//   HOW TO USE.txt
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const HERE = __dirname;
const DIST = path.join(HERE, "dist");
const ROOT = "Catalyst Preset Picker";
const DEVICES = { "Catalyst 60": "2424833", "Catalyst 100": "2424834", "Catalyst 200": "2424835" };

const read = (f) => fs.readFileSync(path.join(HERE, f), "utf8");
const inline = (html, file) => {
  const tag = `<script src="${file}"></script>`;
  if (!html.includes(tag)) throw new Error(`${tag} not found in the page`);
  return html.replace(tag, () => `<script>\n${read(file)}</script>`);
};
const page = inline(inline(read("Catalyst Preset Picker.html"), "models.js"), "presets.js");

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
for (const m of page.matchAll(/<script>([\s\S]*?)<\/script>/g)) vm.runInContext(m[1], ctx);

const safe = (s) => s.replace(/[\\/:*?"<>|]/g, "-").trim();
const files = [{ name: `${ROOT}/Catalyst Preset Picker.html`, text: page }];
for (const [amp, id] of Object.entries(DEVICES)) {
  vm.runInContext(`state.device = ${JSON.stringify(id)};`, ctx);
  for (const p of ctx.PRESET_LIBRARY) {
    files.push({
      name: `${ROOT}/Ready-made presets/${amp}/${p.cat}/${p.artist ? safe(p.artist) + "/" : ""}${safe(p.name)}.catl6p`,
      text: JSON.stringify(ctx.buildPreset(p), null, 1),
    });
  }
}
files.push({
  name: `${ROOT}/HOW TO USE.txt`,
  text: `Catalyst Preset Picker
======================
${ctx.PRESET_LIBRARY.length} ready-to-play sounds for the Line 6 Catalyst 60 / 100 / 200.
Not made by or affiliated with Line 6.

You need Catalyst Edit (free from line6.com) and your amp connected by USB.

EASIEST: use a ready-made preset
  1. Open Catalyst Edit.
  2. Click the guitar menu (top left) > Load Preset... (or press Ctrl+O).
  3. Go to "Ready-made presets", then the folder for your amp model, and pick a sound.
     Famous songs are in the "Songs" folder, sorted by artist.
  4. To keep it on the amp: guitar menu > Save Current Preset to Catalyst (Ctrl+D).

TWEAK SOUNDS FIRST: use the picker
  1. Double-click "Catalyst Preset Picker.html". It opens in your web browser.
     Nothing is installed and it works offline.
  2. Choose your amp model at the top. Browse, search (try a song or guitarist),
     click "Songs" to pick by artist, star your favorites (☆),
     and tweak any sound with the sliders.
  3. Click "Download .catl6p", then load it in Catalyst Edit with Ctrl+O as above.
  4. "Save as my sound" keeps your own versions. "Export my sounds" zips them up
     to share. To add a friend's sounds, drag their zip or .catl6p files onto the
     picker (or click "Import presets"). No need to unzip first.

Too loud? Use "Overall level" at the top of the picker to turn every sound down.
`.replace(/\n/g, "\r\n"),
});

const zip = ctx.makeZip(files);
const buf = Buffer.concat(zip.parts.map((x) => Buffer.from(x.buffer, x.byteOffset || 0, x.byteLength)));
fs.mkdirSync(DIST, { recursive: true });
const out = path.join(DIST, `${ROOT}.zip`);
fs.writeFileSync(out, buf);
console.log(`Wrote ${out} (${files.length} files, ${(buf.length / 1024).toFixed(0)} KB)`);
