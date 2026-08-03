(() => {
  const chestField = document.getElementById("chestField");
  const camp = document.getElementById("camp");
  const mobsEl = document.getElementById("mobs");
  const world = document.getElementById("world");
  const board = document.getElementById("board");
  const benchmarksEl = document.getElementById("benchmarks");
  const skillList = document.getElementById("skillList");
  const conn = document.getElementById("conn");
  const providerEl = document.getElementById("provider");
  const workRootEl = document.getElementById("workRoot");
  const workflowPill = document.getElementById("workflowPill");
  const whPlanName = document.getElementById("whPlanName");
  const whGoal = document.getElementById("whGoal");

  const ins = {
    hint: document.getElementById("inspectHint"),
    body: document.getElementById("inspectBody"),
    sprite: document.getElementById("insSprite"),
    id: document.getElementById("insId"),
    role: document.getElementById("insRole"),
    status: document.getElementById("insStatus"),
    action: document.getElementById("insAction"),
    quote: document.getElementById("insQuote"),
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
  const chestAnchors = new Map(); // taskKey -> {x,y}
  const campAnchors = new Map();
  const mobPos = new Map();
  const skillEvents = []; // recent learning updates

  const QUOTES = {
    plan: [
      "Reading the treasure map…",
      "X marks the module boundary.",
      "Charting chests for the party.",
    ],
    brainstorm: [
      "Scouting the cave entrance…",
      "Many tunnels — pick the safest.",
    ],
    implement: [
      "Dig dig dig…",
      "Pickaxe to the API vein.",
      "Ore looks like clean code.",
    ],
    test: [
      "Tapping the wall for hollow spots.",
      "If it collapses, we failed the dig.",
    ],
    review: [
      "Weighing the gold… fair loot?",
      "Judge of the mine reporting.",
    ],
    fix: [
      "Cave-in! Shore up this shaft.",
      "Critical crack — patch it.",
    ],
    learning: [
      "New pattern for the skill chest.",
      "Storing a better dig technique.",
    ],
    error: [
      "Ouch — trap!",
      "Wrong tunnel. Back to storage.",
    ],
    done: [
      "Chest open. Loot secured.",
      "Gold counted. Next map?",
    ],
    idle: [
      "Waiting for the next chest…",
      "Sharpening the pickaxe.",
    ],
  };

  function escapeHtml(s) {
    return String(s ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;");
  }

  function st(id) {
    return (agentState[id] && agentState[id].status) || "idle";
  }
  function meta(id) {
    return agentState[id] || {};
  }
  function taskOf(id) {
    const t = meta(id).task;
    return t && String(t).strip?.() ? t : t && String(t).trim() ? t : "";
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

  function quoteFor(id) {
    const m = meta(id);
    const status = st(id);
    const phase = (m.phase || "").toLowerCase();
    const task = taskOf(id);
    // Prefer live task as speech when working
    if (status === "working" && task) {
      return task.length > 56 ? task.slice(0, 53) + "…" : task;
    }
    if (status === "error") return pick(QUOTES.error, id);
    if (status === "done") return task ? `Loot: ${task.slice(0, 40)}` : pick(QUOTES.done, id);
    if (status === "waiting") return "Holding the rope…";
    if (status === "idle") return pick(QUOTES.idle, id);
    if (/learn|skill/.test(id) || /learn/.test(phase)) return pick(QUOTES.learning, id);
    if (/fix/.test(phase)) return pick(QUOTES.fix, id);
    if (/test/.test(phase)) return pick(QUOTES.test, id);
    if (/review/.test(phase)) return pick(QUOTES.review, id);
    if (/plan|brainstorm|restore/.test(phase)) return pick(QUOTES.plan, id);
    if (/implement|scaffold|database|design|devops/.test(phase)) return pick(QUOTES.implement, id);
    return task || pick(QUOTES.implement, id);
  }

  function pick(arr, id) {
    const t = Math.floor(Date.now() / 4000);
    let h = t;
    for (let i = 0; i < id.length; i++) h += id.charCodeAt(i);
    return arr[h % arr.length];
  }

  /** Game action: where miner goes + what they do next */
  function actionFor(id) {
    const m = meta(id);
    const status = st(id);
    const phase = (m.phase || "").toLowerCase();
    const isLearner = /learning/.test(id);

    if (status === "error" || (status === "working" && /fix/.test(phase))) {
      return {
        label: isLearner ? "run to skill storage" : "cave-in → skill path",
        target: isLearner || status === "error" ? "skills" : "chest",
        walking: true,
        digging: /fix/.test(phase),
        next: "After error: patch shaft, then learning miner updates skill chest.",
      };
    }
    if (isLearner && (status === "working" || /review|learn/.test(phase))) {
      return {
        label: "stock skill storage",
        target: "skills",
        walking: true,
        digging: false,
        next: "Pattern logged into skill vault for future digs.",
      };
    }
    if (status === "idle") {
      return { label: "camp idle", target: "camp", walking: false, digging: false, next: "Wait for map / next chest." };
    }
    if (status === "waiting") {
      return { label: "hold path", target: "path", walking: false, digging: false, next: "Blocked on approval or upstream chest." };
    }
    if (status === "done") {
      return {
        label: "loot secured",
        target: "camp",
        walking: false,
        digging: false,
        next: "Return to camp; learning may scan for skill updates.",
      };
    }
    // working
    if (/plan|brainstorm|restore/.test(phase) || /architect/.test(id)) {
      return {
        label: "draw / read map",
        target: "map",
        walking: true,
        digging: false,
        next: "Map spawns chests on the dig site.",
      };
    }
    if (/review|judge/.test(phase) || /judge/.test(id)) {
      return {
        label: "weigh loot",
        target: "path",
        walking: true,
        digging: false,
        next: "Approve gold or send miners back to dig (fix).",
      };
    }
    return {
      label: "dig chest",
      target: "chest",
      walking: true,
      digging: true,
      next: "Open chest → done; traps → error/fix → skill storage.",
    };
  }

  function matchChestFor(id) {
    const tasks = plan.tasks || [];
    const byOwner = tasks.find((t) => t.owner && t.owner === id);
    if (byOwner) return byOwner;
    const task = taskOf(id);
    if (task) {
      const fuzzy = tasks.find((t) => (t.title || "").toLowerCase().includes(task.toLowerCase().slice(0, 12)));
      if (fuzzy) return fuzzy;
    }
    return null;
  }

  function taskKey(t, i) {
    return `t-${t.id || i}-${(t.title || "").slice(0, 24)}`;
  }

  function renderMap() {
    whPlanName.textContent = plan.name || plan.path || "No map yet";
    whGoal.textContent = plan.goal || "Planner writes the map · chests spawn below";
  }

  function renderSkillVault() {
    if (!skillEvents.length) {
      skillList.innerHTML = '<li class="empty">No skill updates yet</li>';
      return;
    }
    skillList.innerHTML = skillEvents
      .slice(-8)
      .reverse()
      .map(
        (s, i) =>
          `<li class="${i === 0 ? "pulse" : ""}">${escapeHtml(s)}</li>`
      )
      .join("");
  }

  function renderChests() {
    chestField.innerHTML = "";
    chestAnchors.clear();
    const tasks = plan.tasks || [];
    if (!tasks.length) {
      const empty = document.createElement("div");
      empty.className = "treasure-chest";
      empty.innerHTML = `<div class="lid"></div><div class="ctitle">Awaiting map…</div>`;
      chestField.appendChild(empty);
    } else {
      tasks.forEach((t, i) => {
        const key = taskKey(t, i);
        const el = document.createElement("button");
        el.type = "button";
        el.className = "treasure-chest";
        el.dataset.key = key;

        // status from owning agent
        let cstatus = t.status || "pending";
        let digging = false;
        for (const [aid, s] of Object.entries(agentState)) {
          if (s.status === "working" && t.owner && t.owner === aid) {
            cstatus = "digging";
            digging = true;
          } else if (s.status === "done" && t.owner && t.owner === aid) {
            cstatus = "looted";
          }
        }
        if (digging) el.classList.add("digging", "open");
        if (cstatus === "looted" || cstatus === "done") el.classList.add("looted", "open");

        el.innerHTML = `
          <div class="lid"></div>
          <span class="cstatus badge ${digging ? "working" : cstatus === "looted" ? "done" : "idle"}">${digging ? "DIG" : cstatus}</span>
          <div class="ctitle">${escapeHtml(t.title)}</div>
          ${t.owner ? `<div class="cowner">@${escapeHtml(t.owner)}</div>` : ""}`;

        el.addEventListener("click", () => {
          if (t.owner) selectAgent(t.owner);
        });
        chestField.appendChild(el);
      });
    }

    // camp pads
    camp.innerHTML = "";
    agents.forEach((a) => {
      const pad = document.createElement("div");
      pad.className = "camp-pad";
      pad.dataset.agent = a.id;
      pad.textContent = (a.role || a.id).slice(0, 12);
      camp.appendChild(pad);
    });

    requestAnimationFrame(() => {
      const wr = world.getBoundingClientRect();
      chestField.querySelectorAll(".treasure-chest").forEach((el) => {
        const r = el.getBoundingClientRect();
        if (el.dataset.key) {
          chestAnchors.set(el.dataset.key, {
            x: r.left - wr.left + r.width / 2 - 16,
            y: r.top - wr.top - 8,
          });
        }
      });
      camp.querySelectorAll(".camp-pad").forEach((el) => {
        const r = el.getBoundingClientRect();
        campAnchors.set(el.dataset.agent, {
          x: r.left - wr.left + r.width / 2 - 16,
          y: r.top - wr.top - 36,
        });
      });
      renderMobs();
    });
  }

  function ensureMob(a) {
    let el = mobNodes.get(a.id);
    if (!el) {
      el = document.createElement("div");
      el.dataset.agent = a.id;
      el.innerHTML = `
        <div class="speech"></div>
        <div class="mob-tag"></div>
        <div class="mob-inner">
          <div class="head"></div>
          <div class="arm-l"></div>
          <div class="arm-r"></div>
          <div class="body"></div>
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

  function targetPos(id, act, index) {
    if (act.target === "map") return { x: 48 + (index % 2) * 20, y: 70 + (index % 3) * 24 };
    if (act.target === "skills") return { x: 40 + (index % 2) * 24, y: 280 + (index % 4) * 20 };
    if (act.target === "path") return { x: 220, y: 90 + (index % 8) * 36 };
    if (act.target === "chest") {
      const chest = matchChestFor(id);
      if (chest) {
        const key = taskKey(chest, (plan.tasks || []).indexOf(chest));
        const p = chestAnchors.get(key);
        if (p) return p;
      }
      // first digging chest or field center
      const first = [...chestAnchors.values()][index % Math.max(chestAnchors.size, 1)];
      if (first) return first;
      return { x: 320 + (index % 4) * 40, y: 100 + Math.floor(index / 4) * 40 };
    }
    // camp
    return campAnchors.get(id) || { x: 300 + (index % 5) * 36, y: 400 };
  }

  function renderMobs() {
    agents.forEach((a, i) => {
      const el = ensureMob(a);
      const status = st(a.id);
      const act = actionFor(a.id);
      const pos = targetPos(a.id, act, i);
      const prev = mobPos.get(a.id) || pos;
      const faceLeft = pos.x < prev.x - 2 || act.target === "map" || act.target === "skills";
      mobPos.set(a.id, pos);

      el.className =
        `mob skin-${skinIndex(a.id)} ${status}` +
        (act.walking ? " walking" : "") +
        (act.digging ? " digging" : "") +
        (faceLeft ? " face-left" : "");

      el.querySelector(".mob-tag").textContent = (a.role || a.id.split("-")[0]).slice(0, 10);
      const speech = el.querySelector(".speech");
      const q = quoteFor(a.id);
      speech.textContent = q;
      speech.classList.toggle("hidden", !q || status === "idle");

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
      <span class="task-line">${escapeHtml(quoteFor(agentId))}</span>
      <span class="task-line" style="color:#9a9">${escapeHtml(act.label)} · Σ ${fmtTok(m.tokens_total)}</span>`;
  }

  function renderBoardAll() {
    for (const a of agents) upsertBoardRow(a.id);
  }

  function renderBenchmarks() {
    const wfs = benchmarks.workflows || {};
    const keys = Object.keys(wfs);
    if (!keys.length) {
      benchmarksEl.innerHTML = "<div class=\"hint\">Loot = tokens · pass --workflow on done</div>";
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
          <div class="row total"><span>TOTAL LOOT</span><span>${fmtTok(w.tokens_total)}</span></div></div>`;
      })
      .join("");
  }

  function noteSkillFromEvent(ev) {
    if (!ev) return;
    const isLearn = /learning/.test(ev.agent || "");
    const isErr = ev.status === "error";
    if (isLearn && (ev.status === "working" || ev.status === "done")) {
      skillEvents.push(ev.task || ev.detail || "Skill scan / pattern store");
      renderSkillVault();
    } else if (isErr) {
      skillEvents.push(`Trap flagged by ${ev.agent}: ${(ev.task || "error").slice(0, 40)}`);
      renderSkillVault();
    }
  }

  function selectAgent(id) {
    selectedId = id;
    const a = agents.find((x) => x.id === id) || { id, role: "miner" };
    const m = meta(id);
    const act = actionFor(id);
    const chest = matchChestFor(id);
    ins.hint.classList.add("hidden");
    ins.body.classList.remove("hidden");
    ins.sprite.className = "mob-preview skin-" + skinIndex(id);
    ins.sprite.innerHTML = `<div class="mob-inner"><div class="head"></div><div class="body"></div><div class="leg-l"></div><div class="leg-r"></div></div>`;
    ins.id.textContent = a.id;
    ins.role.textContent = a.role || "miner";
    ins.status.textContent = st(id);
    ins.status.className = "v badge " + st(id);
    ins.action.textContent = act.label;
    ins.quote.textContent = quoteFor(id);
    ins.planTask.textContent = chest ? chest.title : act.next;
    ins.tokens.textContent = fmtTok(m.tokens_total);
    ins.phase.textContent = m.phase || "—";
    renderChests();
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
    if (ev.workflow) workflowPill.textContent = "quest: " + ev.workflow;
    noteSkillFromEvent(ev);
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
      workflowPill.textContent = "quest: " + data.state.active_workflow;
    }
    renderMap();
    renderSkillVault();
    renderChests();
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
          renderMap();
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
        renderChests();
        if (selectedId) selectAgent(selectedId);
      } catch (_) {}
    };
  }

  // refresh quotes periodically so idle lines rotate
  setInterval(() => {
    renderMobs();
    if (selectedId) {
      ins.quote.textContent = quoteFor(selectedId);
    }
  }, 4000);

  loadSnapshot()
    .then(connectStream)
    .catch((e) => {
      conn.textContent = "error";
      console.error(e);
    });
})();
