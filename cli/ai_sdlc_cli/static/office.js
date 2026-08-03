(() => {
  const floor = document.getElementById("floor");
  const mobsEl = document.getElementById("mobs");
  const world = document.getElementById("world");
  const board = document.getElementById("board");
  const benchmarksEl = document.getElementById("benchmarks");
  const conn = document.getElementById("conn");
  const providerEl = document.getElementById("provider");
  const workRootEl = document.getElementById("workRoot");
  const workflowPill = document.getElementById("workflowPill");
  const whPlanName = document.getElementById("whPlanName");
  const whGoal = document.getElementById("whGoal");
  const whTasks = document.getElementById("whTasks");

  const ins = {
    hint: document.getElementById("inspectHint"),
    body: document.getElementById("inspectBody"),
    sprite: document.getElementById("insSprite"),
    id: document.getElementById("insId"),
    role: document.getElementById("insRole"),
    status: document.getElementById("insStatus"),
    action: document.getElementById("insAction"),
    task: document.getElementById("insTask"),
    planTask: document.getElementById("insPlanTask"),
    tokens: document.getElementById("insTokens"),
    phase: document.getElementById("insPhase"),
  };

  let agents = [];
  let agentState = {};
  let plan = { tasks: [] };
  let benchmarks = { workflows: {} };
  let selectedId = null;
  let cursor = 0;
  const boardRows = new Map();
  const mobNodes = new Map();
  const deskAnchors = new Map(); // agentId -> {x,y} relative to world

  // warehouse zone (left) target for "check plan" walks
  function warehouseTarget(i) {
    const rect = world.getBoundingClientRect();
    return { x: 40 + (i % 3) * 18, y: 120 + (i % 5) * 28 };
  }

  function escapeHtml(s) {
    return String(s ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;");
  }

  function st(id) {
    return (agentState[id] && agentState[id].status) || "idle";
  }
  function taskOf(id) {
    const t = agentState[id] && agentState[id].task;
    return t && String(t).trim() ? t : "—";
  }
  function meta(id) {
    return agentState[id] || {};
  }
  function fmtTok(n) {
    n = Number(n) || 0;
    if (n >= 1e6) return (n / 1e6).toFixed(2) + "M";
    if (n >= 1e3) return (n / 1e3).toFixed(1) + "k";
    return String(n);
  }

  function skinIndex(id) {
    let h = 0;
    for (let i = 0; i < id.length; i++) h = (h + id.charCodeAt(i) * (i + 1)) % 10;
    return h;
  }

  /** Map status/phase → action label + where mob walks */
  function actionFor(id) {
    const m = meta(id);
    const status = st(id);
    const phase = (m.phase || "").toLowerCase();
    if (status === "idle") return { label: "idle at desk", target: "desk", walking: false };
    if (status === "waiting") return { label: "waiting (path)", target: "path", walking: false };
    if (status === "error") return { label: "stuck", target: "desk", walking: false };
    if (status === "done") return { label: "report done", target: "desk", walking: false };
    // working
    if (/plan|brainstorm|restore|review/.test(phase) || /plan|brainstorm|architect/i.test(m.task || "")) {
      return { label: "→ vault: check plan", target: "warehouse", walking: true };
    }
    if (/implement|fix|database|design|test|devops|scaffold/.test(phase)) {
      return { label: "work at desk", target: "desk", walking: true };
    }
    return { label: "working", target: "desk", walking: true };
  }

  function planTaskFor(id) {
    const tasks = plan.tasks || [];
    const byOwner = tasks.find((t) => t.owner && t.owner === id);
    if (byOwner) return byOwner.title;
    // fuzzy: task text contains role keyword
    const role = (agents.find((a) => a.id === id) || {}).role || "";
    const fuzzy = tasks.find((t) =>
      (t.title || "").toLowerCase().includes(role.toLowerCase().slice(0, 4))
    );
    if (fuzzy) return fuzzy.title;
    const m = meta(id);
    if (m.task) return m.task;
    return tasks[0] ? tasks[0].title : "—";
  }

  function renderWarehouse() {
    whPlanName.textContent = plan.name || plan.path || "No active plan";
    whGoal.textContent = plan.goal || "Link docs/plans/.active-plan to bind vault";
    whTasks.innerHTML = "";
    const tasks = plan.tasks || [];
    if (!tasks.length) {
      const li = document.createElement("li");
      li.textContent = "No Task blocks parsed yet";
      whTasks.appendChild(li);
      return;
    }
    for (const t of tasks) {
      const li = document.createElement("li");
      const activeOwner = Object.entries(agentState).some(
        ([id, s]) => s.status === "working" && (s.task || "").includes((t.title || "").slice(0, 16))
      );
      if (activeOwner) li.classList.add("active");
      li.innerHTML = `${escapeHtml(t.title)}${
        t.owner ? `<span class="own">@${escapeHtml(t.owner)}</span>` : ""
      }`;
      whTasks.appendChild(li);
    }
  }

  function renderDesks() {
    floor.innerHTML = "";
    deskAnchors.clear();
    agents.forEach((a, i) => {
      const pad = document.createElement("div");
      pad.className = "desk-pad" + (selectedId === a.id ? " selected" : "");
      pad.dataset.agent = a.id;
      const status = st(a.id);
      pad.innerHTML = `
        <span class="dbadge badge ${status}">${status}</span>
        <div class="dname">${escapeHtml(a.id)}</div>
        <div class="drole">${escapeHtml(a.role || "agent")}</div>`;
      pad.addEventListener("click", () => selectAgent(a.id));
      floor.appendChild(pad);
    });
    // measure anchors after layout
    requestAnimationFrame(() => {
      const worldRect = world.getBoundingClientRect();
      floor.querySelectorAll(".desk-pad").forEach((pad) => {
        const r = pad.getBoundingClientRect();
        deskAnchors.set(pad.dataset.agent, {
          x: r.left - worldRect.left + r.width / 2 - 12,
          y: r.top - worldRect.top + 8,
        });
      });
      renderMobs();
    });
  }

  function ensureMob(a, index) {
    let el = mobNodes.get(a.id);
    if (!el) {
      el = document.createElement("div");
      el.className = "mob skin-" + skinIndex(a.id);
      el.dataset.agent = a.id;
      el.innerHTML = `
        <div class="mob-tag"></div>
        <div class="head"></div>
        <div class="body">
          <div class="leg-l"></div>
          <div class="leg-r"></div>
        </div>`;
      el.addEventListener("click", (e) => {
        e.stopPropagation();
        selectAgent(a.id);
      });
      mobsEl.appendChild(el);
      mobNodes.set(a.id, el);
    }
    return el;
  }

  function renderMobs() {
    agents.forEach((a, i) => {
      const el = ensureMob(a, i);
      const status = st(a.id);
      const act = actionFor(a.id);
      el.className = `mob skin-${skinIndex(a.id)} ${status}` + (act.walking ? " walking" : "");
      const tag = el.querySelector(".mob-tag");
      tag.textContent = a.role || a.id.split("-")[0];

      let pos;
      if (act.target === "warehouse") {
        pos = warehouseTarget(i);
      } else if (act.target === "path") {
        pos = { x: 210, y: 80 + (i % 8) * 36 };
      } else {
        pos = deskAnchors.get(a.id) || { x: 280 + (i % 4) * 40, y: 60 + Math.floor(i / 4) * 50 };
      }
      el.style.left = pos.x + "px";
      el.style.top = pos.y + "px";
    });
  }

  function upsertBoardRow(agentId) {
    const m = meta(agentId);
    const status = st(agentId);
    const act = actionFor(agentId);
    let li = boardRows.get(agentId);
    if (!li) {
      li = document.createElement("li");
      boardRows.set(agentId, li);
      board.appendChild(li);
    }
    li.innerHTML = `
      <span class="who">${escapeHtml(agentId)}</span>
      <span class="badge ${status}">${status}</span>
      <span class="task-line">${escapeHtml(taskOf(agentId))}</span>
      <span class="task-line" style="color:#9a9">${escapeHtml(act.label)} · Σ ${fmtTok(m.tokens_total)}</span>`;
  }

  function renderBoardAll() {
    for (const a of agents) upsertBoardRow(a.id);
  }

  function renderBenchmarks() {
    const wfs = benchmarks.workflows || {};
    const keys = Object.keys(wfs);
    if (!keys.length) {
      benchmarksEl.innerHTML = "<div class=\"hint\">Emit --tokens --workflow on done</div>";
      return;
    }
    benchmarksEl.innerHTML = keys
      .sort()
      .map((wf) => {
        const w = wfs[wf];
        const rows = Object.entries(w.agents || {})
          .sort((a, b) => (b[1].tokens_total || 0) - (a[1].tokens_total || 0))
          .map(
            ([id, v]) =>
              `<div class="row"><span>${escapeHtml(id)}</span><span>${fmtTok(v.tokens_total)}</span></div>`
          )
          .join("");
        return `<div class="wf"><div class="wf-title">${escapeHtml(wf)}</div>${rows}
          <div class="row total"><span>TOTAL</span><span>${fmtTok(w.tokens_total)}</span></div></div>`;
      })
      .join("");
  }

  function selectAgent(id) {
    selectedId = id;
    const a = agents.find((x) => x.id === id) || { id, role: "agent" };
    const m = meta(id);
    const act = actionFor(id);
    ins.hint.classList.add("hidden");
    ins.body.classList.remove("hidden");
    ins.sprite.className = "mob-preview skin-" + skinIndex(id);
    ins.sprite.innerHTML = `<div class="head"></div><div class="body"></div>`;
    ins.id.textContent = a.id;
    ins.role.textContent = a.role || "agent";
    ins.status.textContent = st(id);
    ins.status.className = "v badge " + st(id);
    ins.action.textContent = act.label;
    ins.task.textContent = taskOf(id);
    ins.planTask.textContent = planTaskFor(id);
    ins.tokens.textContent = fmtTok(m.tokens_total);
    ins.phase.textContent = m.phase || "—";
    renderDesks();
  }

  function applyEvent(ev) {
    if (!ev || !ev.agent) return;
    const prev = agentState[ev.agent] || {};
    const add = Number(ev.tokens) || 0;
    agentState[ev.agent] = {
      ...prev,
      status: ev.status || prev.status || "idle",
      task: ev.task !== undefined && ev.task !== "" ? ev.task : ev.status === "idle" ? "" : prev.task || "",
      phase: ev.phase || prev.phase || "",
      workflow: ev.workflow || prev.workflow || "",
      tokens_total: (Number(prev.tokens_total) || 0) + add,
      tokens_in_total: (Number(prev.tokens_in_total) || 0) + (Number(ev.tokens_in) || 0),
      tokens_out_total: (Number(prev.tokens_out_total) || 0) + (Number(ev.tokens_out) || 0),
      last_tokens: add,
      updated_at: ev.ts,
    };
    if (ev.workflow) workflowPill.textContent = "wf: " + ev.workflow;
    upsertBoardRow(ev.agent);
  }

  async function loadSnapshot() {
    const res = await fetch("/api/snapshot");
    const data = await res.json();
    agents = data.agents || [];
    agentState = (data.state && data.state.agents) || {};
    plan = data.plan || { tasks: [] };
    benchmarks = data.benchmarks || { workflows: {} };
    providerEl.textContent = (data.config && data.config.provider) || "local";
    workRootEl.textContent = data.work_root || "";
    if (data.state && data.state.active_workflow) {
      workflowPill.textContent = "wf: " + data.state.active_workflow;
    }
    renderWarehouse();
    renderDesks();
    renderBoardAll();
    renderBenchmarks();
  }

  function connectStream() {
    const es = new EventSource("/api/stream?after=" + cursor);
    es.onopen = () => {
      conn.textContent = "live";
      conn.classList.add("live");
      conn.classList.remove("muted");
    };
    es.onerror = () => {
      conn.textContent = "reconnecting…";
      conn.classList.remove("live");
      conn.classList.add("muted");
    };
    es.onmessage = (msg) => {
      try {
        const data = JSON.parse(msg.data);
        if (typeof data.cursor === "number") cursor = data.cursor;
        if (data.plan) {
          plan = data.plan;
          renderWarehouse();
        }
        if (data.benchmarks) {
          benchmarks = data.benchmarks;
          renderBenchmarks();
        }
        if (data.state && data.state.agents) {
          for (const [id, s] of Object.entries(data.state.agents)) {
            const prev = agentState[id] || {};
            agentState[id] = {
              ...prev,
              ...s,
              tokens_total: Math.max(Number(prev.tokens_total) || 0, Number(s.tokens_total) || 0),
            };
            upsertBoardRow(id);
          }
        }
        if (data.events && data.events.length) {
          for (const ev of data.events) applyEvent(ev);
        }
        renderDesks();
        if (selectedId) selectAgent(selectedId);
      } catch (_) {}
    };
  }

  // idle wander: occasionally walk idle agents a few pixels
  setInterval(() => {
    agents.forEach((a, i) => {
      if (st(a.id) !== "idle") return;
      const el = mobNodes.get(a.id);
      if (!el) return;
      const base = deskAnchors.get(a.id);
      if (!base) return;
      const jitter = Math.sin(Date.now() / 800 + i) * 6;
      el.style.left = base.x + jitter + "px";
      el.classList.add("walking");
      setTimeout(() => el.classList.remove("walking"), 400);
    });
  }, 2000);

  loadSnapshot()
    .then(connectStream)
    .catch((e) => {
      conn.textContent = "error";
      console.error(e);
    });
})();
