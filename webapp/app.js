const $ = (id) => document.getElementById(id);
const state = { path: null, camPath: null, fmKey: null, offset: 0, fmLayer: 1, fmBlock: 0 };

async function api(route, params = {}) {
  const qs = new URLSearchParams(params).toString();
  const r = await fetch(qs ? `${route}?${qs}` : route);
  const body = await r.json();
  if (!r.ok) throw new Error(body.error || `HTTP ${r.status}`);
  return body;
}

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

async function init() {
  try {
    const data = await api("/api/classes");
    const s = data.summary;
    $("summary").append(
      badge("model", s.model),
      badge("ckpt", `epoch ${s.checkpoint_epoch}, val ${(s.checkpoint_val_acc * 100).toFixed(2)}%`),
      badge("test top-1", `${(s.test_top1_acc * 100).toFixed(2)}%`),
      badge("macro-F1", `${(s.test_macro_f1 * 100).toFixed(2)}%`),
      badge("device", s.device),
    );
    for (const c of data.classes) {
      const o = document.createElement("option");
      o.value = c.name;
      o.textContent = c.name;
      $("cls").appendChild(o);
    }
  } catch (e) {
    $("summary").textContent = `API error: ${e.message}`;
  }
  $("split").addEventListener("change", () => loadGrid(true));
  $("cls").addEventListener("change", () => loadGrid(true));
  $("more").addEventListener("click", () => loadGrid(false));
  $("btn-cam").addEventListener("click", loadCam);
  $("btn-fm").addEventListener("click", loadFm);
  $("fm-layer").addEventListener("change", onFmLayerChange);
  $("fm-ch").addEventListener("change", onFmChChange);
  await loadGrid(true);
}

async function loadGrid(reset) {
  if (reset) {
    $("grid").textContent = "";
    state.offset = 0;
  }
  const data = await api("/api/samples", {
    split: $("split").value,
    cls: $("cls").value,
    offset: state.offset,
    limit: 60,
  });
  $("count").textContent = `${data.total} images`;
  for (const p of data.items) {
    const img = document.createElement("img");
    img.src = `/api/image?path=${encodeURIComponent(p)}`;
    img.loading = "lazy";
    img.title = p;
    img.alt = p;
    img.dataset.path = p;
    img.addEventListener("click", () => select(p));
    $("grid").appendChild(img);
  }
  state.offset += data.items.length;
  $("more").hidden = state.offset >= data.total;
}

async function select(p) {
  state.path = p;
  document.querySelectorAll("#grid img").forEach((el) =>
    el.classList.toggle("sel", el.dataset.path === p));
  $("placeholder").hidden = true;
  $("detail").hidden = false;
  $("cam-box").hidden = true;
  $("fm-box").hidden = true;
  state.camPath = null;
  state.fmKey = null;
  $("gt-chip").textContent = "GT …";
  $("pred-chip").textContent = "…";
  $("main-img").src = `/api/image?path=${encodeURIComponent(p)}`;
  $("path").textContent = p;
  try {
    const d = await api("/api/predict", { path: p });
    if (state.path !== p) return;
    renderPredict(d);
  } catch (e) {
    $("pred-chip").textContent = `error: ${e.message}`;
  }
}

function chip(el, text, ok) {
  el.textContent = text;
  el.className = `chip ${ok ? "ok" : "bad"}`;
}

function renderPredict(d) {
  chip($("gt-chip"), `GT ${d.gt}`, true);
  chip($("pred-chip"), `Pred ${d.pred} — ${d.correct ? "correct" : "wrong"}`, d.correct);
  const bars = $("probs");
  bars.textContent = "";
  for (const { c, p } of d.probs) {
    const row = document.createElement("div");
    row.className = `bar-row${c === d.pred ? " top" : ""}`;
    const name = document.createElement("span");
    name.textContent = c;
    const track = document.createElement("div");
    track.className = "bar-track";
    const fill = document.createElement("div");
    fill.className = "bar-fill";
    fill.style.width = `${(p * 100).toFixed(1)}%`;
    const val = document.createElement("span");
    val.textContent = p.toFixed(4);
    track.appendChild(fill);
    row.append(name, track, val);
    bars.appendChild(row);
  }
}

async function loadCam() {
  const p = state.path;
  if (!p) return;
  if (state.camPath !== p) {
    try {
      const d = await api("/api/gradcam", { path: p });
      if (state.path !== p) return;
      $("cam-img").src = `data:image/png;base64,${d.png}`;
      state.camPath = p;
    } catch (e) {
      alert(`Grad-CAM failed: ${e.message}`);
      return;
    }
  }
  $("cam-box").hidden = false;
}

function updateFmCh(C) {
  const chSel = $("fm-ch");
  chSel.textContent = "";
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

async function loadFm() {
  const p = state.path;
  if (!p) return;
  const key = `${p}|${state.fmLayer}|${state.fmBlock}`;
  if (state.fmKey !== key) {
    try {
      const d = await api("/api/featuremaps", {
        path: p, layer: state.fmLayer, start: state.fmBlock * 16,
      });
      if (state.path !== p) return;
      if ($("fm-layer").options.length === 0) {
        for (let li = 0; li < d.stages; li++) {
          const o = document.createElement("option");
          o.value = String(li);
          o.textContent = `stages[${li}]`;
          $("fm-layer").appendChild(o);
        }
        $("fm-layer").value = String(state.fmLayer);
      }
      const end = d.start + Math.min(16, d.channels - d.start) - 1;
      $("fm-img").src = `data:image/png;base64,${d.png}`;
      $("fm-title").textContent =
        `Intermediate feature maps — stages[${d.layer}] (${d.channels}\u00d7${d.hw[0]}\u00d7${d.hw[1]}), channels ${d.start}\u2013${end} of ${d.channels}`;
      updateFmCh(d.channels);
      state.fmKey = key;
    } catch (e) {
      alert(`Feature maps failed: ${e.message}`);
      return;
    }
  }
  $("fm-box").hidden = false;
}

function onFmLayerChange() {
  state.fmLayer = Number($("fm-layer").value);
  state.fmBlock = 0;
  loadFm();
}

function onFmChChange() {
  state.fmBlock = Number($("fm-ch").value);
  loadFm();
}

init();
