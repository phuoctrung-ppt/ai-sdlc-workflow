(() => {
  const floor = document.getElementById("floor");
  const feed = document.getElementById("feed");
  const conn = document.getElementById("conn");
  const providerEl = document.getElementById("provider");
  const workRootEl = document.getElementById("workRoot");

  let agents = [];
  let agentState = {};
  let cursor = 0;

  function statusOf(id) {
    return (agentState[id] && agentState[id].status) || "idle";
  }

  function taskOf(id) {
    return (agentState[id] && agentState[id].task) || "—";
  }

  function renderFloor() {
    floor.innerHTML = "";
    for (const a of agents) {
      const st = statusOf(a.id);
      const el = document.createElement("article");
      el.className = "desk " + st;
      el.dataset.agent = a.id;
      el.innerHTML = `
        <div class="emoji">${a.emoji || "🤖"}</div>
        <div class="name">${a.id}</div>
        <div class="role">${a.role || "agent"}</div>
        <div class="task">${escapeHtml(taskOf(a.id))}</div>
        <div class="status-row">
          <span class="badge ${st}">${st}</span>
          <span>${a.desk || ""}</span>
        </div>`;
      floor.appendChild(el);
    }
  }

  function escapeHtml(s) {
    return String(s)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;");
  }

  function pushFeed(ev) {
    const li = document.createElement("li");
    const t = ev.ts ? new Date(ev.ts).toLocaleTimeString() : "";
    li.innerHTML = `
      <div class="when">${t} · ${escapeHtml(ev.phase || "—")}</div>
      <div><span class="who">${escapeHtml(ev.agent)}</span>
      <span class="badge ${ev.status}"> ${escapeHtml(ev.status)}</span></div>
      <div>${escapeHtml(ev.task || ev.detail || "")}</div>`;
    feed.prepend(li);
    while (feed.children.length > 80) feed.removeChild(feed.lastChild);
  }

  function applyEvents(events) {
    for (const ev of events) {
      if (!agentState[ev.agent]) agentState[ev.agent] = {};
      agentState[ev.agent] = {
        status: ev.status,
        task: ev.task || "",
        detail: ev.detail || "",
        phase: ev.phase || "",
        updated_at: ev.ts,
      };
      pushFeed(ev);
    }
    renderFloor();
  }

  async function loadSnapshot() {
    const res = await fetch("/api/snapshot");
    const data = await res.json();
    agents = data.agents || [];
    agentState = (data.state && data.state.agents) || {};
    providerEl.textContent = (data.config && data.config.provider) || "local";
    workRootEl.textContent = data.work_root || "";
    renderFloor();
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
          agentState = { ...agentState, ...data.state.agents };
        }
        if (data.events && data.events.length) applyEvents(data.events);
        else renderFloor();
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
