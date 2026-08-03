(() => {
  const room = document.getElementById("room");
  const board = document.getElementById("board");
  const benchmarksEl = document.getElementById("benchmarks");
  const conn = document.getElementById("conn");
  const providerEl = document.getElementById("provider");
  const workRootEl = document.getElementById("workRoot");
  const workflowPill = document.getElementById("workflowPill");

  const ins = {
    hint: document.getElementById("inspectHint"),
    body: document.getElementById("inspectBody"),
    emoji: document.getElementById("insEmoji"),
    id: document.getElementById("insId"),
    role: document.getElementById("insRole"),
    status: document.getElementById("insStatus"),
    phase: document.getElementById("insPhase"),
    task: document.getElementById("insTask"),
    tokens: document.getElementById("insTokens"),
    tokensIO: document.getElementById("insTokensIO"),
    wf: document.getElementById("insWf"),
  };

  let agents = [];
  let agentState = {};
  let benchmarks = { workflows: {}, agents: {} };
  let selectedId = null;
  let cursor = 0;
  const boardRows = new Map(); // agentId -> <li>

  function escapeHtml(s) {
    return String(s ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;");
  }

  function st(id) {
    return (agentState[id] && agentState[id].status) || "idle";
  }
  function task(id) {
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

  function renderRoom() {
    room.innerHTML = "";
    for (const a of agents) {
      const status = st(a.id);
      const el = document.createElement("button");
      el.type = "button";
      el.className = "desk " + status + (selectedId === a.id ? " selected" : "");
      el.dataset.agent = a.id;
      el.innerHTML = `
        <span class="badge ${status}">${status}</span>
        <div class="sprite">${a.emoji || "🤖"}</div>
        <div class="name">${escapeHtml(a.id)}</div>
        <div class="role">${escapeHtml(a.role || "agent")}</div>
        <div class="mini-task">${escapeHtml(task(a.id))}</div>`;
      el.addEventListener("click", () => selectAgent(a.id));
      room.appendChild(el);
    }
  }

  function upsertBoardRow(agentId) {
    const m = meta(agentId);
    const status = st(agentId);
    let li = boardRows.get(agentId);
    if (!li) {
      li = document.createElement("li");
      li.dataset.agent = agentId;
      boardRows.set(agentId, li);
      board.appendChild(li);
    }
    li.className = status;
    li.innerHTML = `
      <span class="who">${escapeHtml(agentId)}</span>
      <span class="badge ${status}">${status}</span>
      <span class="task-line">${escapeHtml(task(agentId))}</span>
      <span class="tok">Σ ${fmtTok(m.tokens_total)} · last ${fmtTok(m.last_tokens)}</span>`;
    // keep order stable: working first
    const order = { working: 0, waiting: 1, error: 2, done: 3, idle: 4 };
    const items = [...board.querySelectorAll("li")];
    items.sort((a, b) => {
      const sa = order[st(a.dataset.agent)] ?? 9;
      const sb = order[st(b.dataset.agent)] ?? 9;
      return sa - sb || a.dataset.agent.localeCompare(b.dataset.agent);
    });
    items.forEach((node) => board.appendChild(node));
  }

  function renderBoardAll() {
    for (const a of agents) upsertBoardRow(a.id);
    // also any state keys not in roster
    for (const id of Object.keys(agentState)) {
      if (![...boardRows.keys()].includes(id)) upsertBoardRow(id);
    }
  }

  function renderBenchmarks() {
    const wfs = benchmarks.workflows || {};
    const keys = Object.keys(wfs);
    if (!keys.length) {
      benchmarksEl.innerHTML = "<div class=\"hint\">No token data yet. Pass --tokens / --workflow on done events.</div>";
      return;
    }
    benchmarksEl.innerHTML = keys
      .sort()
      .map((wf) => {
        const w = wfs[wf];
        const agentRows = Object.entries(w.agents || {})
          .sort((a, b) => (b[1].tokens_total || 0) - (a[1].tokens_total || 0))
          .map(
            ([id, v]) =>
              `<div class="row"><span>${escapeHtml(id)}</span><span>${fmtTok(v.tokens_total)} · ${v.tasks_done || 0} done</span></div>`
          )
          .join("");
        return `<div class="wf">
          <div class="wf-title">${escapeHtml(wf)}</div>
          ${agentRows || "<div class=\"row\"><span>—</span></div>"}
          <div class="row total"><span>TOTAL</span><span>${fmtTok(w.tokens_total)} (in ${fmtTok(w.tokens_in)} / out ${fmtTok(w.tokens_out)})</span></div>
        </div>`;
      })
      .join("");
  }

  function selectAgent(id) {
    selectedId = id;
    const a = agents.find((x) => x.id === id) || { id, role: "agent", emoji: "🤖" };
    const m = meta(id);
    ins.hint.classList.add("hidden");
    ins.body.classList.remove("hidden");
    ins.emoji.textContent = a.emoji || "🤖";
    ins.id.textContent = a.id;
    ins.role.textContent = a.role || "agent";
    ins.status.textContent = st(id);
    ins.status.className = "v badge " + st(id);
    ins.phase.textContent = m.phase || "—";
    ins.task.textContent = task(id);
    ins.tokens.textContent = fmtTok(m.tokens_total);
    ins.tokensIO.textContent = `${fmtTok(m.tokens_in_total)} / ${fmtTok(m.tokens_out_total)}`;
    ins.wf.textContent = m.workflow || benchmarks.active_workflow || "—";
    renderRoom();
  }

  function applyEvent(ev) {
    if (!ev || !ev.agent) return;
    const prev = agentState[ev.agent] || {};
    const add = Number(ev.tokens) || 0;
    const addIn = Number(ev.tokens_in) || 0;
    const addOut = Number(ev.tokens_out) || 0;
    agentState[ev.agent] = {
      status: ev.status || prev.status || "idle",
      task: ev.task !== undefined && ev.task !== "" ? ev.task : ev.status === "idle" ? "" : prev.task || "",
      detail: ev.detail || prev.detail || "",
      phase: ev.phase || prev.phase || "",
      workflow: ev.workflow || prev.workflow || "",
      updated_at: ev.ts || prev.updated_at,
      tokens_total: (Number(prev.tokens_total) || 0) + add,
      tokens_in_total: (Number(prev.tokens_in_total) || 0) + addIn,
      tokens_out_total: (Number(prev.tokens_out_total) || 0) + addOut,
      last_tokens: add,
    };
    if (ev.workflow) {
      workflowPill.textContent = "wf: " + ev.workflow;
    }
    upsertBoardRow(ev.agent);
    if (selectedId === ev.agent) selectAgent(ev.agent);
  }

  function applyEvents(events) {
    for (const ev of events) applyEvent(ev);
    renderRoom();
  }

  async function loadSnapshot() {
    const res = await fetch("/api/snapshot");
    const data = await res.json();
    agents = data.agents || [];
    agentState = (data.state && data.state.agents) || {};
    benchmarks = data.benchmarks || { workflows: {}, agents: {} };
    providerEl.textContent = (data.config && data.config.provider) || "local";
    workRootEl.textContent = data.work_root || "";
    if (data.state && data.state.active_workflow) {
      workflowPill.textContent = "wf: " + data.state.active_workflow;
    }
    renderRoom();
    renderBoardAll();
    renderBenchmarks();
  }

  async function refreshBenchmarks() {
    try {
      const res = await fetch("/api/benchmarks");
      if (res.ok) {
        benchmarks = await res.json();
        renderBenchmarks();
      }
    } catch (_) {}
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
        if (data.state && data.state.agents) {
          // merge server truth for status fields; keep local token sums if higher
          for (const [id, s] of Object.entries(data.state.agents)) {
            const prev = agentState[id] || {};
            agentState[id] = {
              ...prev,
              ...s,
              tokens_total: Math.max(Number(prev.tokens_total) || 0, Number(s.tokens_total) || 0),
              tokens_in_total: Math.max(Number(prev.tokens_in_total) || 0, Number(s.tokens_in_total) || 0),
              tokens_out_total: Math.max(Number(prev.tokens_out_total) || 0, Number(s.tokens_out_total) || 0),
            };
            upsertBoardRow(id);
          }
          if (data.state.active_workflow) {
            workflowPill.textContent = "wf: " + data.state.active_workflow;
          }
        }
        if (data.events && data.events.length) applyEvents(data.events);
        else renderRoom();
        if (selectedId) selectAgent(selectedId);
        refreshBenchmarks();
      } catch (_) {}
    };
  }

  loadSnapshot()
    .then(connectStream)
    .catch((e) => {
      conn.textContent = "error";
      console.error(e);
    });
})();
