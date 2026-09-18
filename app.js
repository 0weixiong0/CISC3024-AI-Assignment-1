const $ = (id) => document.getElementById(id);
const PAGE = 60;
const state = {
  path: null, offset: 0,
  manifest: null, session: null, device: "",
  fmLayer: 1, fmBlock: 0,
  cache: new Map(), // path -> {probs, pred, feats[4], dims[4], cam}
};

const imgUrl = (p) => "data/images/" + p.split("/").map(encodeURIComponent).join("/");
const gtOf = (p) => p.split("/")[0];

function badge(label, value) {
  const b = document.createElement("span");
  b.className = "badge";
  const t = document.createElement("span");
  t.textContent = `${label} `;
  const v = document.createElement("b");
  v.textContent = value;
  b.append(t, v);
  return b;
}

function currentList() {
  const split = state.manifest.splits[$("split").value];
  const cls = $("cls").value;
  if (cls === "all") return state.manifest.classes.flatMap((c) => split[c]);
  return split[cls];
}

async function loadModel() {
  const ortScript = document.querySelector('script[src$="ort.all.min.js"]');
  ort.env.wasm.wasmPaths = new URL(".", ortScript.src).href;
  ort.env.wasm.numThreads = 1;
  const buf = await (await fetch("model/model.onnx")).arrayBuffer();
  const eps = ["wasm"];
  try {
    if (navigator.gpu && await navigator.gpu.requestAdapter()) eps.unshift("webgpu");
  } catch (_) { /* navigator.gpu present but unusable */ }
  state.session = await ort.InferenceSession.create(buf, { executionProviders: eps });
  state.device = eps[0] === "webgpu" ? "webgpu" : "wasm (cpu)";
  $("summary").replaceChild(badge("runtime", state.device), $("runtime-badge"));
}

async function init() {
  try {
    state.manifest = await (await fetch("manifest.json")).json();
    const s = state.manifest.summary;
    $("summary").append(
      badge("model", s.model),
      badge("ckpt", `epoch ${s.checkpoint_epoch}, val ${(s.checkpoint_val_acc * 100).toFixed(2)}%`),
      badge("test top-1", `${(s.test_top1_acc * 100).toFixed(2)}%`),
      badge("macro-F1", `${(s.test_macro_f1 * 100).toFixed(2)}%`),
    );
    const rb = badge("runtime", "loading model…");
    rb.id = "runtime-badge";
    $("summary").append(rb);
    for (const c of state.manifest.classes) {
      const o = document.createElement("option");
      o.value = c;
      o.textContent = c;
      $("cls").appendChild(o);
    }
    $("split").addEventListener("change", () => loadGrid(true));
    $("cls").addEventListener("change", () => loadGrid(true));
    $("more").addEventListener("click", () => loadGrid(false));
    $("btn-cam").addEventListener("click", loadCam);
    $("btn-fm").addEventListener("click", loadFm);
    $("fm-layer").addEventListener("change", onFmLayerChange);
    $("fm-ch").addEventListener("change", onFmChChange);
    await loadGrid(true);
    await loadModel();
  } catch (e) {
    $("runtime-badge").querySelector("b").textContent = `failed: ${e.message}`;
  }
}

async function loadGrid(reset) {
  if (reset) {
    $("grid").textContent = "";
    state.offset = 0;
  }
  const items = currentList();
  $("count").textContent = `${items.length} images`;
  for (const p of items.slice(state.offset, state.offset + PAGE)) {
    const img = document.createElement("img");
    img.src = imgUrl(p);
    img.loading = "lazy";
    img.title = p;
    img.alt = p;
    img.dataset.path = p;
    img.addEventListener("click", () => select(p));
    $("grid").appendChild(img);
  }
  state.offset = Math.min(state.offset + PAGE, items.length);
  $("more").hidden = state.offset >= items.length;
}

async function select(p) {
  state.path = p;
  document.querySelectorAll("#grid img").forEach((el) =>
    el.classList.toggle("sel", el.dataset.path === p));
  $("placeholder").hidden = true;
  $("detail").hidden = false;
  $("cam-box").hidden = true;
  $("fm-box").hidden = true;
  $("gt-chip").textContent = `GT ${gtOf(p)}`;
  $("gt-chip").className = "chip ok";
  $("pred-chip").textContent = "running…";
  $("pred-chip").className = "chip";
  $("main-img").src = imgUrl(p);
  $("path").textContent = p;
  try {
    let entry = state.cache.get(p);
    if (!entry) {
      const img = new Image();
      img.src = imgUrl(p);
      await img.decode();
      if (state.path !== p) return;
      const x = preprocess(img);
      const zero = new ort.Tensor("float32", new Float32Array(10), [1, 10]);
      const r = await state.session.run({ image: x, target: zero });
      if (state.path !== p) return;
      entry = {
        probs: Array.from(r.probs.data),
        pred: -1,
        feats: [r.f0.data, r.f1.data, r.f2.data, r.f3.data],
        dims: [r.f0.dims, r.f1.dims, r.f2.dims, r.f3.dims],
        cam: null,
      };
      entry.pred = entry.probs.indexOf(Math.max(...entry.probs));
      cachePut(p, entry);
    }
    if (state.path !== p) return;
    renderPredict(p, entry);
  } catch (e) {
    if (state.path === p) $("pred-chip").textContent = `error: ${e.message}`;
  }
}

function cachePut(p, entry) {
  if (state.cache.size >= 40) {
    state.cache.delete(state.cache.keys().next().value);
  }
  state.cache.set(p, entry);
}

function preprocess(img) {
  const c = document.createElement("canvas");
  c.width = 224; c.height = 224;
  const ctx = c.getContext("2d", { willReadFrequently: true });
  ctx.imageSmoothingEnabled = true;
  ctx.drawImage(img, 0, 0, 224, 224);
  const d = ctx.getImageData(0, 0, 224, 224).data;
  const { mean, std } = state.manifest.summary.normalization;
  const plane = 224 * 224;
  const out = new Float32Array(3 * plane);
  for (let j = 0, i = 0; j < plane; j++, i += 4) {
    out[j] = (d[i] / 255 - mean[0]) / std[0];
    out[plane + j] = (d[i + 1] / 255 - mean[1]) / std[1];
    out[2 * plane + j] = (d[i + 2] / 255 - mean[2]) / std[2];
  }
  return new ort.Tensor("float32", out, [1, 3, 224, 224]);
}

function renderPredict(p, entry) {
  const gt = gtOf(p);
  const pred = state.manifest.classes[entry.pred];
  const correct = pred === gt;
  const el = $("pred-chip");
  el.textContent = `Pred ${pred} — ${correct ? "correct" : "wrong"}`;
  el.className = `chip ${correct ? "ok" : "bad"}`;
  const bars = $("probs");
  bars.textContent = "";
  state.manifest.classes
    .map((c, i) => ({ c, p: entry.probs[i] }))
    .sort((a, b) => b.p - a.p)
    .forEach(({ c, p: v }) => {
      const row = document.createElement("div");
      row.className = `bar-row${c === pred ? " top" : ""}`;
      const name = document.createElement("span");
      name.textContent = c;
      const track = document.createElement("div");
      track.className = "bar-track";
      const fill = document.createElement("div");
      fill.className = "bar-fill";
      fill.style.width = `${(v * 100).toFixed(1)}%`;
      const val = document.createElement("span");
      val.textContent = v.toFixed(4);
      track.appendChild(fill);
      row.append(name, track, val);
      bars.appendChild(row);
    });
}

async function runCam(entry, imgEl) {
  const t = new Float32Array(10);
  t[entry.pred] = 1;
  const r = await state.session.run({
    image: preprocess(imgEl),
    target: new ort.Tensor("float32", t, [1, 10]),
  });
  entry.cam = r.cam.data;
}

async function loadCam() {
  const p = state.path;
  if (!p || !state.session) return;
  const entry = state.cache.get(p);
  if (!entry) return;
  try {
    if (!entry.cam) {
      const img = new Image();
      img.src = imgUrl(p);
      await img.decode();
      if (state.path !== p) return;
      await runCam(entry, img);
    }
    renderCam(p, entry);
    $("cam-box").hidden = false;
  } catch (e) {
    alert(`Grad-CAM failed: ${e.message}`);
  }
}

function renderCam(p, entry) {
  const img = $("main-img");
  const c = $("cam-canvas");
  c.width = 224; c.height = 224;
  const ctx = c.getContext("2d", { willReadFrequently: true });
  ctx.imageSmoothingEnabled = true;
  ctx.drawImage(img, 0, 0, 224, 224);
  const base = ctx.getImageData(0, 0, 224, 224).data;
  const n = 224 * 224;
  const blended = new Float32Array(3 * n);
  let maxV = 0;
  for (let i = 0, j = 0; i < n; i++, j += 3) {
    const lut = JET_LUT[Math.max(0, Math.min(255, Math.round(entry.cam[i] * 255)))];
    blended[j] = 0.7 * (lut[0] / 255) + 0.3 * (base[i * 4] / 255);
    blended[j + 1] = 0.7 * (lut[1] / 255) + 0.3 * (base[i * 4 + 1] / 255);
    blended[j + 2] = 0.7 * (lut[2] / 255) + 0.3 * (base[i * 4 + 2] / 255);
    for (let k = 0; k < 3; k++) if (blended[j + k] > maxV) maxV = blended[j + k];
  }
  const out = ctx.createImageData(224, 224);
  for (let i = 0; i < n; i++) {
    out.data[i * 4] = blended[i * 3] / maxV * 255;
    out.data[i * 4 + 1] = blended[i * 3 + 1] / maxV * 255;
    out.data[i * 4 + 2] = blended[i * 3 + 2] / maxV * 255;
    out.data[i * 4 + 3] = 255;
  }
  ctx.putImageData(out, 0, 0);
}

function populateFmCh(entry) {
  const chSel = $("fm-ch");
  chSel.textContent = "";
  const C = entry.dims[state.fmLayer][1];
  const blocks = Math.ceil(C / 16);
  state.fmBlock = Math.min(state.fmBlock, blocks - 1);
  for (let b = 0; b < blocks; b++) {
    const start = b * 16;
    const o = document.createElement("option");
    o.value = String(b);
    o.textContent = `${start}\u2013${Math.min(start + 15, C - 1)}`;
    chSel.appendChild(o);
  }
  chSel.value = String(state.fmBlock);
}

function populateFmControls(entry) {
  const layerSel = $("fm-layer");
  layerSel.textContent = "";
  entry.dims.forEach((d, li) => {
    const o = document.createElement("option");
    o.value = String(li);
    o.textContent = `stages[${li}] (${d[1]}\u00d7${d[2]}\u00d7${d[3]})`;
    layerSel.appendChild(o);
  });
  layerSel.value = String(state.fmLayer);
  populateFmCh(entry);
}

function onFmLayerChange() {
  state.fmLayer = Number($("fm-layer").value);
  state.fmBlock = 0;
  const entry = state.cache.get(state.path);
  if (!entry) return;
  populateFmCh(entry);
  renderFm(entry);
}

function onFmChChange() {
  state.fmBlock = Number($("fm-ch").value);
  const entry = state.cache.get(state.path);
  if (!entry) return;
  renderFm(entry);
}

function loadFm() {
  const p = state.path;
  if (!p || !state.session) return;
  const entry = state.cache.get(p);
  if (!entry) return;
  populateFmControls(entry);
  renderFm(entry);
  $("fm-box").hidden = false;
}

function renderFm(entry) {
  const li = state.fmLayer;
  const dims = entry.dims[li];
  const C = dims[1], H = dims[2], W = dims[3];
  const start = state.fmBlock * 16;
  const k = Math.min(16, C - start);
  const feats = entry.feats[li];
  const cells = 4, cell = 160;
  const c = $("fm-canvas");
  c.width = cells * cell; c.height = cells * cell;
  const ctx = c.getContext("2d");
  ctx.imageSmoothingEnabled = false;
  const small = document.createElement("canvas");
  small.width = W; small.height = H;
  const sctx = small.getContext("2d");
  const plane = H * W;
  ctx.font = "12px monospace";
  ctx.textBaseline = "top";
  for (let ch = 0; ch < k; ch++) {
    const off = (start + ch) * plane;
    let mn = Infinity, mx = -Infinity;
    for (let i = 0; i < plane; i++) {
      const v = feats[off + i];
      if (v < mn) mn = v;
      if (v > mx) mx = v;
    }
    const id = sctx.createImageData(W, H);
    for (let i = 0; i < plane; i++) {
      const v = (feats[off + i] - mn) / (mx - mn + 1e-8);
      const lut = VIRIDIS_LUT[Math.max(0, Math.min(255, Math.round(v * 255)))];
      id.data[i * 4] = lut[0];
      id.data[i * 4 + 1] = lut[1];
      id.data[i * 4 + 2] = lut[2];
      id.data[i * 4 + 3] = 255;
    }
    sctx.putImageData(id, 0, 0);
    const px = (ch % cells) * cell, py = Math.floor(ch / cells) * cell;
    ctx.drawImage(small, px, py, cell, cell);
    ctx.fillStyle = "rgba(0,0,0,0.55)";
    ctx.fillRect(px + 4, py + 4, 42, 15);
    ctx.fillStyle = "#fff";
    ctx.fillText(`ch ${start + ch}`, px + 7, py + 5);
  }
  $("fm-title").textContent =
    `Intermediate feature maps — stages[${li}] (${C}\u00d7${H}\u00d7${W}), channels ${start}\u2013${start + k - 1} of ${C}`;
}

init();
