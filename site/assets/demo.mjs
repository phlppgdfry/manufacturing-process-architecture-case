// Prototype of the Corvent Process House: catalogue, review, process council, improvements.
// Data: ../data/catalog.json (generated from catalog/catalog.json) and ../data/check-report.json (from scripts/check_models.py).
// The council decision and the release are simulated; state lives in localStorage and can be reset.
import { createTour } from "./tour.js";

const STORE = "corvent-demo-v1";
const STATUS = { "geen-model": "geen model", draft: "draft", "in-review": "in review", released: "released", retired: "retired" };
const STATUS_CHIP = { "geen-model": "risk", draft: "warn", "in-review": "info", released: "ok", retired: "muted" };
const MODEL_SVG = {
  "docs/04-reference-model/bpmn/otc-02-to-be.bpmn": "otc-02-to-be.svg",
  "docs/05-review/bpmn/otc-03-to-be.bpmn": "otc-03-to-be.svg",
  "docs/06-governance/bpmn/ste-04-proceswijziging.bpmn": "ste-04-proceswijziging.svg",
};
const DRAFT = "docs/05-review/bpmn/otc-03.draft.bpmn";
const REVISED = "docs/05-review/bpmn/otc-03-to-be.bpmn";
const OWNERS = { A: "Sales director", B: "Supply chain director" };
const INITIATIVES = [
  { id: "I-01", name: "Automatische kredietcheck onder de limiet", proc: "OTC-02", kpi: "% orders met manuele kredietcheck", from: "31%", to: "≤ 10%", owner: "Credit manager", prio: 1 },
  { id: "I-02", name: "Haalbare leverdatum voorstellen (capaciteitscheck)", proc: "OTC-03", kpi: "% orders bevestigd binnen 4 werkuren", from: "42%", to: "85%", owner: null, prio: 1, needs: "D-03" },
  { id: "I-03", name: "Productconfigurator in plaats van Excel", proc: "OTC-02", kpi: "% maatorders met overtypfout", from: "6%", to: "≤ 1%", owner: "Sales director", prio: 2 },
  { id: "I-04", name: "Eigenaars en released modellen voor ITR", proc: "ITR-01..03", kpi: "L2 met eigenaar in ITR", from: "0 / 3", to: "3 / 3", owner: "COO (D-05)", prio: 2 },
  { id: "I-05", name: "CAPA-opvolging uit Excel naar QMS", proc: "DTC-03", kpi: "CAPA's afgesloten binnen termijn", from: "55%", to: "85%", owner: "Quality director", prio: 3 },
];
const DECIDED = [
  { id: "D-01", text: "Governance-model en wijzigingsflow goedgekeurd", effect: "STE-04 released v1.0" },
  { id: "D-02", text: "Klachten alleen onder ITR-01; OTC-07 vervalt", effect: "OTC-07 retired" },
  { id: "D-05", text: "L1 issue-to-resolution krijgt een eigenaar vóór raad #3", effect: "actie COO" },
];

const $ = (sel) => document.querySelector(sel);
function h(tag, attrs = {}, ...children) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (v === false || v == null) continue;
    if (k === "class") el.className = v;
    else if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
    else el.setAttribute(k, v === true ? "" : v);
  }
  for (const c of children.flat()) if (c != null && c !== false) el.append(c instanceof Node ? c : String(c));
  return el;
}
const chip = (text, kind) => h("span", { class: `chip ${kind}` }, text);

// ---------- state ----------
const fresh = () => ({ decision: null, overrides: {}, log: [], selected: null, filters: { l1: "", status: "", system: "", noOwner: false, q: "" }, view: "catalogus", reviewModel: "draft" });
let state = load();
function load() {
  try { return { ...fresh(), ...JSON.parse(localStorage.getItem(STORE) || "{}") }; } catch { return fresh(); }
}
function save() {
  try { localStorage.setItem(STORE, JSON.stringify(state)); } catch { /* private mode: state stays in memory */ }
}
function log(text, kind = "info") {
  state.log.push({ t: new Date().toLocaleTimeString("nl-BE", { hour: "2-digit", minute: "2-digit", second: "2-digit" }), text, kind });
  save();
  renderLog();
}

let CAT, REPORT;
const proc = (id) => ({ ...CAT.processes.find((p) => p.id === id), ...(state.overrides[id] || {}) });
const processes = () => CAT.processes.map((p) => proc(p.id));
const l1Name = (id) => CAT.l1.find((x) => x.id === id);
const capName = (id) => CAT.capabilities.flatMap((g) => g.children).find((c) => c.id === id)?.name ?? id;
const sysName = (id) => CAT.systems.find((s) => s.id === id)?.name ?? id;

// ---------- catalogus ----------
function renderKpis() {
  const act = processes().filter((p) => p.status !== "retired");
  const owned = act.filter((p) => p.owner).length;
  const rel = act.filter((p) => p.status === "released").length;
  const rev = act.filter((p) => p.status === "in-review").length;
  const pct = (n) => Math.round((100 * n) / act.length);
  $("#kpis").replaceChildren(
    h("article", { class: "card kpi" }, h("p", {}, "Actieve L2-processen"), h("p", { class: "kpi-value" }, act.length), h("p", {}, `${CAT.l1.length} E2E-processen`)),
    h("article", { class: "card kpi", id: "kpi-owned" }, h("p", {}, "Met eigenaar"), h("p", { class: "kpi-value" }, `${owned}`), h("p", {}, `${pct(owned)}% · ${act.length - owned} zonder`)),
    h("article", { class: "card kpi", id: "kpi-released" }, h("p", {}, "Released"), h("p", { class: "kpi-value" }, `${rel}`), h("p", {}, `${pct(rel)}% · doel 12 mnd: 30`)),
    h("article", { class: "card kpi" }, h("p", {}, "In review"), h("p", { class: "kpi-value" }, rev), h("p", {}, "wacht op review of beslissing")),
  );
}

function filtered() {
  const f = state.filters;
  const q = f.q.trim().toLowerCase();
  return processes().filter((p) =>
    (!f.l1 || p.l1 === f.l1) && (!f.status || p.status === f.status) && (!f.system || p.systems.includes(f.system)) &&
    (f.status === "retired" || p.status !== "retired") &&
    (!f.noOwner || !p.owner) &&
    (!q || [p.id, p.name, ...(p.aliases || [])].some((s) => s.toLowerCase().includes(q))));
}

function renderList() {
  const rows = filtered();
  const groups = CAT.l0.map((l0) => {
    const l1s = CAT.l1.filter((x) => x.l0 === l0.id).map((x) => {
      const ps = rows.filter((p) => p.l1 === x.id);
      if (!ps.length) return null;
      return h("div", { class: "l1" },
        h("h4", {}, `${x.id} · ${x.name}`, " ", x.owner ? h("span", { class: "muted" }, `· ${x.owner}`) : chip("L1 zonder eigenaar", "risk")),
        h("ul", {}, ps.map((p) => h("li", {},
          h("button", { type: "button", class: `row${state.selected === p.id ? " active" : ""}`, "data-id": p.id, onclick: () => select(p.id) },
            h("span", { class: "pid" }, p.id), h("span", { class: "pname" }, p.name),
            p.owner ? h("span", { class: "powner" }, p.owner) : chip("geen eigenaar", "risk"),
            chip(STATUS[p.status], STATUS_CHIP[p.status]))))));
    }).filter(Boolean);
    return l1s.length ? h("section", { class: "l0" }, h("h3", {}, l0.name), l1s) : null;
  }).filter(Boolean);
  $("#list").replaceChildren(h("p", { class: "muted count" }, `${rows.length} proces(sen)`), ...groups);
}

function renderDetail() {
  const box = $("#detail");
  if (!state.selected) { box.replaceChildren(h("p", { class: "muted" }, "Kies een proces in de lijst.")); return; }
  const p = proc(state.selected);
  const l1 = l1Name(p.l1);
  const findings = CAT.warnings?.filter((w) => w.element === p.id) || [];
  const svg = p.model && MODEL_SVG[p.model];
  box.replaceChildren(
    h("p", { class: "eyebrow" }, `${l1.id} · ${l1.name}`),
    h("h3", {}, `${p.id} ${p.name}`),
    h("dl", { class: "facts" },
      h("dt", {}, "Eigenaar"), h("dd", {}, p.owner || chip("geen eigenaar", "risk")),
      h("dt", {}, "Status"), h("dd", {}, chip(STATUS[p.status], STATUS_CHIP[p.status]), p.version ? ` v${p.version}` : ""),
      h("dt", {}, "Review"), h("dd", {}, p.review || "—"),
      h("dt", {}, "Capability"), h("dd", {}, p.capabilities.map((c) => `${c} ${capName(c)}`).join(", ")),
      h("dt", {}, "Systemen"), h("dd", {}, p.systems.map(sysName).join(", ")),
      p.aliases ? [h("dt", {}, "Alias"), h("dd", {}, p.aliases.join(", "))] : null,
      h("dt", {}, "Model"), h("dd", {}, p.model ? (p.model.startsWith("docs/")
        ? h("a", { href: `https://github.com/phlppgdfry/manufacturing-process-architecture-case/blob/main/${p.model}` }, p.model.split("/").pop())
        : p.model) : "—")),
    p.issue ? h("p", { class: "issue" }, p.issue) : null,
    findings.length ? h("p", { class: "issue" }, findings.map((f) => f.message).join("; ")) : null,
    svg ? h("figure", { class: "thumb" }, h("img", { src: `../assets/models/${svg}`, alt: `Model ${p.id}`, loading: "lazy" })) : null,
  );
}

function select(id) {
  state.selected = id;
  save();
  renderList();
  renderDetail();
}

function initFilters() {
  const add = (sel, items) => items.forEach(([v, t]) => $(sel).append(h("option", { value: v }, t)));
  add("#f-l1", CAT.l1.map((x) => [x.id, `${x.id} · ${x.name}`]));
  add("#f-status", Object.entries(STATUS));
  add("#f-system", CAT.systems.map((s) => [s.id, s.name]));
  const f = state.filters;
  $("#f-l1").value = f.l1; $("#f-status").value = f.status; $("#f-system").value = f.system; $("#f-noowner").checked = f.noOwner; $("#f-q").value = f.q;
  const update = () => {
    state.filters = { l1: $("#f-l1").value, status: $("#f-status").value, system: $("#f-system").value, noOwner: $("#f-noowner").checked, q: $("#f-q").value };
    save();
    renderList();
  };
  ["#f-l1", "#f-status", "#f-system", "#f-noowner"].forEach((s) => $(s).addEventListener("change", update));
  $("#f-q").addEventListener("input", update);
}

function setFilter(patch) {
  state.filters = { ...fresh().filters, ...patch };
  $("#f-l1").value = state.filters.l1; $("#f-status").value = state.filters.status; $("#f-system").value = state.filters.system;
  $("#f-noowner").checked = state.filters.noOwner; $("#f-q").value = state.filters.q;
  save();
  renderList();
}

// ---------- review ----------
function renderReview() {
  const draft = state.reviewModel === "draft";
  const file = draft ? DRAFT : REVISED;
  const result = REPORT.models.find((m) => m.file === file);
  document.querySelectorAll("[data-model]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.model === state.reviewModel)));
  $("#review-img").src = `../assets/models/${draft ? "otc-03-draft" : "otc-03-to-be"}.svg`;
  $("#review-img").alt = draft ? "Draft-model OTC-03 van de analist" : "Herwerkt model OTC-03 v1.0";
  $("#review-caption").textContent = draft ? "Draft: lanes met een persoonsnaam, een inclusieve gateway en een losse draad." : "v1.0: lanes = rollen, drie vragen, uitzonderingspaden, overdrachten naar OTC-02 en OTC-04.";
  const rules = [...new Set(result.findings.map((f) => f.rule))];
  $("#findings").replaceChildren(
    h("h3", {}, "Automatisch rapport"),
    h("p", { class: "muted" }, h("code", {}, `check_models.py ${file.split("/").pop()}`)),
    result.findings.length
      ? h("p", {}, chip(`${result.findings.length} bevindingen op ${rules.length} regels`, "risk"))
      : h("p", {}, chip("0 bevindingen: alle 13 automatische regels groen", "ok")),
    result.findings.length ? h("div", { class: "table-wrap" }, h("table", {},
      h("thead", {}, h("tr", {}, h("th", {}, "Regel"), h("th", {}, "Element"), h("th", {}, "Bevinding"))),
      h("tbody", {}, result.findings.map((f) => h("tr", {}, h("td", {}, f.rule), h("td", {}, f.element || "—"), h("td", {}, f.message)))))) : null,
  );
  $("#feedback").classList.toggle("dim", !draft);
}

// ---------- procesraad ----------
function renderCouncil() {
  $("#decided").replaceChildren(...DECIDED.map((d) => h("article", { class: "card" }, chip("Beslist · raad #1", "ok"), h("h3", {}, d.id), h("p", {}, d.text), h("p", { class: "muted" }, d.effect))));
  const done = state.decision;
  $("#d03-chip").textContent = done ? "Beslist · procesraad #2" : "Voorstel · procesraad #2";
  $("#d03-chip").className = `chip ${done ? "ok" : "warn"}`;
  document.querySelectorAll('input[name="d03"]').forEach((r) => { r.disabled = Boolean(done); r.checked = r.value === done; });
  $("#btn-decide").disabled = Boolean(done);
  if (done) $("#d03-msg").textContent = `Beslist: optie ${done}, eigenaar ${OWNERS[done]}. OTC-03 is released.`;
}

function decide(option) {
  if (state.decision) return;
  const msg = $("#d03-msg");
  if (!option) { msg.textContent = "Kies eerst een optie."; return; }
  if (option === "C") {
    msg.textContent = "Niet toegepast: de catalogus vereist één eigenaar per proces (regel C04). Gedeeld eigenaarschap is geen eigenaar; dat is het probleem van vandaag.";
    log("Procesraad: optie C geweigerd door de catalogusregel 'één eigenaar per proces'", "warn");
    return;
  }
  const owner = OWNERS[option];
  state.decision = option;
  state.overrides["OTC-03"] = { owner, status: "released", version: "1.0", review: "2027-10-31" };
  log(`Procesraad #2: D-03 beslist, optie ${option} → eigenaar OTC-03 = ${owner}`, "ok");
  log(`Model OTC-03: attribuut eigenaar 'open' → '${owner}', status → released`);
  log("check_models.py: R09 eigenaar = catalogus ✓ · 0 bevindingen", "ok");
  log("Catalogus: OTC-03 in review → released v1.0, review 2027-10-31", "ok");
  if (option === "B") log("Verbeterportfolio: I-02 heeft nu een eigenaar en kan starten", "ok");
  save();
  renderAll();
}

// ---------- verbeteringen ----------
function renderInitiatives() {
  const rows = INITIATIVES.map((i) => {
    const blocked = i.needs && !state.decision;
    const owner = i.id === "I-02" ? (state.decision ? OWNERS[state.decision] : null) : i.owner;
    return h("tr", { id: `row-${i.id}` },
      h("td", {}, i.id), h("td", {}, i.name), h("td", {}, i.proc), h("td", {}, i.kpi), h("td", {}, i.from), h("td", {}, i.to),
      h("td", {}, owner || chip("wacht op D-03", "warn")), h("td", {}, i.prio),
      h("td", {}, blocked ? chip("geblokkeerd", "risk") : chip("kan starten", "ok")));
  });
  $("#initiatives").replaceChildren(
    h("thead", {}, h("tr", {}, ...["ID", "Initiatief", "Proces", "KPI", "Nu", "Doel", "Eigenaar", "Prio", "Status"].map((t) => h("th", {}, t)))),
    h("tbody", {}, rows));
}

// ---------- shell ----------
function show(view) {
  state.view = view;
  save();
  document.querySelectorAll("[data-view]").forEach((b) => b.setAttribute("aria-selected", String(b.dataset.view === view)));
  document.querySelectorAll(".view").forEach((v) => v.classList.toggle("hidden", v.id !== `view-${view}`));
  if (location.hash !== `#${view}`) history.replaceState(null, "", `${location.search}#${view}`);
}

function renderLog() {
  const items = state.log.length ? state.log : [{ t: "", text: "Nog niets gebeurd. Start de rondleiding of klik rond.", kind: "muted" }];
  $("#log").replaceChildren(...items.slice(-12).map((e) => h("li", { class: e.kind }, e.t ? h("time", {}, e.t) : null, e.text)));
}

function renderAll() {
  renderKpis();
  renderList();
  renderDetail();
  renderReview();
  renderCouncil();
  renderInitiatives();
  renderLog();
}

function reset() {
  state = fresh();
  save();
  setFilter({});
  show("catalogus");
  renderAll();
}

async function main() {
  [CAT, REPORT] = await Promise.all(["../data/catalog.json", "../data/check-report.json"].map((u) => fetch(u).then((r) => r.json())));
  CAT.warnings = REPORT.catalog.warnings;
  initFilters();
  document.querySelectorAll("[data-view]").forEach((b) => b.addEventListener("click", () => show(b.dataset.view)));
  document.querySelectorAll("[data-model]").forEach((b) => b.addEventListener("click", () => { state.reviewModel = b.dataset.model; save(); renderReview(); }));
  $("#btn-decide").addEventListener("click", () => decide(document.querySelector('input[name="d03"]:checked')?.value));
  $("#btn-reset").addEventListener("click", reset);
  const fromHash = location.hash.slice(1);
  show(["catalogus", "review", "procesraad", "verbeteringen"].includes(fromHash) ? fromHash : state.view);
  renderAll();

  const tour = createTour([
    { text: "Het proceshuis van Corvent: 41 actieve L2-processen onder 10 end-to-end processen. Elk proces heeft een ID, status, capability en systemen, allemaal uit één bron (catalog.json).",
      focus: "#kpis", before: () => { reset(); } },
    { text: "Filter 'zonder eigenaar': 8 processen, plus het hele L1-proces issue-to-resolution. Dit is geen falen maar de werklijst van de governance (regel C04).",
      focus: "#list", before: () => { show("catalogus"); setFilter({ noOwner: true }); } },
    { text: "OTC-03 Leverdatum bevestigen: in review, geen eigenaar, capability Leverbelofte. Hier zit het conflict: sales belooft, planning beslist.",
      focus: "#detail", before: () => { show("catalogus"); select("OTC-03"); } },
    { text: "De draft van de analist, door scripts/check_models.py gehaald: 9 bevindingen op 7 regels. Losse draad, inclusieve gateway, een persoon als lane, geen attributen.",
      focus: "#findings", before: () => { show("review"); state.reviewModel = "draft"; renderReview(); } },
    { text: "Mijn feedback: vijf punten over betekenis, elk als vraag. Naamgeving en labels lost de analist zelf op met de checklist.",
      focus: "#feedback", before: () => { show("review"); } },
    { text: "De herwerkte versie v1.0: lanes zijn rollen, drie duidelijke vragen, uitzonderingspaden en overdrachten. 0 bevindingen.",
      focus: "#review-figure", before: () => { show("review"); state.reviewModel = "tobe"; renderReview(); } },
    { text: "Wat geen model kan oplossen, gaat naar de procesraad: wie is eigenaar van de bevestigde leverdatum? Drie opties; het voorstel is B.",
      focus: "#d03", before: () => { show("procesraad"); const b = document.querySelector('input[name="d03"][value="B"]'); if (b && !b.disabled) b.checked = true; } },
    { text: "De raad beslist B. Achter de schermen: het modelattribuut wordt bijgewerkt, de check blijft groen, en OTC-03 wordt released.",
      focus: ".eventlog", before: () => { show("procesraad"); decide("B"); } },
    { text: "Terug in de catalogus: OTC-03 heeft een eigenaar en is released. De dekking stijgt naar 34 met eigenaar en 9 released.",
      focus: "#detail", before: () => { show("catalogus"); setFilter({}); select("OTC-03"); } },
    { text: "En het verbeterportfolio: I-02 (haalbare leverdatum, KPI van 42% naar 85% binnen 4 werkuren) heeft nu een eigenaar en kan starten. Dat is de keten: catalogus → review → beslissing → verbetering.",
      focus: "#row-I-02", before: () => { show("verbeteringen"); } },
  ], { label: "Rondleiding", labels: { step: "Stap", of: "van", back: "Terug", next: "Volgende", finish: "Klaar", close: "Sluiten" } });
  $("#btn-tour").addEventListener("click", () => tour.start());
}

main().catch((err) => {
  console.error(err);
  $("#list").replaceChildren(h("p", { class: "issue" }, "De data kon niet geladen worden. Open de demo via de live site (GitHub Pages) of een lokale server."));
});
