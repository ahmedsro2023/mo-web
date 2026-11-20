/* OPSMO v7 — dynamic showcase: live pipeline, before/after, calculator, rollout, suite map */
(() => {
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const onView = (el, fn, th = .25) => { if (!el) return; const io = new IntersectionObserver(es => es.forEach(e => fn(e.isIntersecting)), { threshold: th }); io.observe(el); };
  const fmt = n => Math.round(n).toLocaleString('en-US');

  /* ---------- shared sector data + picker ---------- */
  const dataEl = $('.sector-data'); const SD = dataEl ? JSON.parse(dataEl.textContent) : {};
  let SECTOR = (($('#liveDemo') || $('#beforeAfter') || {}).dataset || {}).sector || 'real-estate';
  const setSector = k => { if (!SD[k]) return; SECTOR = k;
    $$('.sp__chip').forEach(b => { const on = b.dataset.sector === k; b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', on); });
    document.dispatchEvent(new CustomEvent('opsmo:sector', { detail: k })); };
  $$('.sp__chip').forEach(b => b.addEventListener('click', () => setSector(b.dataset.sector)));

  /* ---------- live pipeline ---------- */
  const lv = $('#liveDemo');
  if (lv && SD[SECTOR]) {
    const WHO = ['Sara', 'Omar', 'Lina', 'Yousef', 'Maya', 'Karim', 'Noor', 'Adam'];
    const feed = $('#lvFeed'), cols = $$('.lv__col', lv), k = { leads: $('#kLeads'), resp: $('#kResp'), tasks: $('#kTasks'), won: $('#kWon'), wonL: $('#kWonL') };
    let leads, won, tasks, resp, spark, timer = null, visible = false;
    const pick = a => a[Math.floor(Math.random() * a.length)];
    const count = () => cols.forEach(cl => $('[data-colcount]', cl).textContent = $$('.lv__card', cl).length);
    const card = (what, src, who) => { const d = document.createElement('div'); d.className = 'lv__card'; d.innerHTML = `<b>${what}</b><span>${src}</span><i>${who[0]}</i>`; return d; };
    const tick = () => {
      const S = SD[SECTOR], src = pick(S.sources), what = pick(S.items), who = pick(WHO), secs = 3 + Math.floor(Math.random() * 9);
      leads++; resp.push(secs); if (resp.length > 20) resp.shift();
      const li = document.createElement('li');
      li.innerHTML = `<span class="lv__src">${src}</span><b>${what}</b><span class="lv__ok">Assigned to ${who} · ${secs}s</span>`;
      feed.prepend(li); requestAnimationFrame(() => li.classList.add('is-in'));
      while (feed.children.length > 5) feed.lastElementChild.remove();
      const cd = card(what, src, who); $('.lv__cards', cols[0]).prepend(cd); requestAnimationFrame(() => cd.classList.add('is-in'));
      for (let i = cols.length - 2; i >= 0; i--) {
        const cs = $$('.lv__card', cols[i]);
        if (cs.length && Math.random() < (i === 0 ? .7 : .45)) {
          const m = cs[cs.length - 1]; m.classList.add('is-move');
          setTimeout(() => { if (!m.isConnected) return; m.classList.remove('is-move', 'is-in'); $('.lv__cards', cols[i + 1]).prepend(m); requestAnimationFrame(() => m.classList.add('is-in')); if (i + 1 === cols.length - 1) { won++; m.classList.add('is-won'); k.won.textContent = won; } count(); }, 450);
          tasks++; break;
        }
      }
      $$('.lv__cards', lv).forEach(c => { while (c.children.length > 4) c.lastElementChild.remove(); });
      count();
      k.leads.textContent = leads; k.won.textContent = won; k.tasks.textContent = Math.max(0, tasks - won);
      k.resp.textContent = Math.round(resp.reduce((a, b) => a + b, 0) / resp.length) + 's';
      spark.push(secs); if (spark.length > 24) spark.shift();
      $('#lvSpark').setAttribute('d', spark.map((v, i) => `${i ? 'L' : 'M'}${(i / 23) * 200} ${60 - v * 4.5}`).join(' '));
    };
    const reset = () => {
      const S = SD[SECTOR]; leads = 0; won = 0; tasks = 0; resp = []; spark = [];
      feed.innerHTML = ''; $$('.lv__cards', lv).forEach(c => c.innerHTML = '');
      cols.forEach((cl, i) => { const h = $('.lv__ch', cl); h.firstChild.textContent = S.stages[i]; });
      k.wonL.textContent = S.won; lv.classList.remove('is-swap'); void lv.offsetWidth; lv.classList.add('is-swap');
      for (let i = 0; i < 6; i++) tick();
    };
    reset();
    const play = () => { if (visible && !timer && !reduce) timer = setInterval(tick, 2300); };
    onView(lv, v => { visible = v; if (v) play(); else if (timer) { clearInterval(timer); timer = null; } });
    document.addEventListener('opsmo:sector', () => { clearInterval(timer); timer = null; reset(); play(); });
  }

  /* ---------- before / after ---------- */
  const ba = $('#beforeAfter');
  if (ba && SD[SECTOR]) {
    const clock = $('#baClock'), verdict = $('#baVerdict'), metric = $('#baMetric'), gain = $('#baGain'); let raf, auto = true, mode = 'before', timers = [];
    const fmtT = s => s >= 86400 ? `${Math.max(1, Math.round(s / 86400))} day${Math.round(s / 86400) > 1 ? 's' : ''}` : s >= 3600 ? `${Math.floor(s / 3600)}h ${Math.floor(s % 3600 / 60)}m` : s >= 60 ? `${Math.floor(s / 60)}m ${Math.floor(s % 60)}s` : `${Math.floor(s)}s`;
    const lanes = () => { const S = SD[SECTOR];
      ['before', 'after'].forEach(m => { $(`.ba__lane--${m}`, ba).innerHTML = S[m].steps.map(([t, h, p]) => `<li><span class="ba__t mono">${t}</span><div><b>${h}</b><p>${p}</p></div></li>`).join(''); });
      metric.textContent = S.metric; };
    const show = m => {
      mode = m; const S = SD[SECTOR]; ba.dataset.mode = m;
      $$('.ba__switch button', ba).forEach(b => b.setAttribute('aria-selected', b.dataset.mode === m));
      timers.forEach(clearTimeout); timers = [];
      $$('.ba__lane li', ba).forEach(li => li.classList.remove('is-on'));
      $$(`.ba__lane--${m} li`, ba).forEach((li, i) => timers.push(setTimeout(() => li.classList.add('is-on'), reduce ? 0 : 250 + i * 420)));
      cancelAnimationFrame(raf); verdict.classList.remove('is-on'); gain.classList.remove('is-on');
      const { total, label, verdict: v } = S[m], t0 = performance.now(), dur = reduce ? 0 : 2200;
      const step = now => { const p = dur ? Math.min(1, (now - t0) / dur) : 1;
        clock.textContent = p < 1 ? fmtT(total * (1 - Math.pow(1 - p, 3))) : label;
        if (p < 1) raf = requestAnimationFrame(step);
        else { verdict.textContent = v; verdict.classList.add('is-on');
          if (m === 'after') { const pct = Math.min(99, Math.round((1 - S.after.total / S.before.total) * 100)); gain.innerHTML = `<b>${pct}%</b> less waiting`; gain.classList.add('is-on'); } } };
      raf = requestAnimationFrame(step);
    };
    $$('.ba__switch button', ba).forEach(b => b.addEventListener('click', () => { auto = false; show(b.dataset.mode); }));
    let played = false;
    onView(ba, v => { if (v && !played) { played = true; lanes(); show('before'); timers.push(setTimeout(() => auto && show('after'), 4600)); } }, .4);
    document.addEventListener('opsmo:sector', () => { lanes(); auto = true; played = true; show('before'); timers.push(setTimeout(() => auto && show('after'), 4200)); });
  }

  /* ---------- calculator ---------- */
  const calc = $('#calc');
  if (calc) {
    const get = id => +$('#' + id).value; let shown = { h: 0, a: 0, f: 0 }, raf, sraf;
    const animate = (to) => { cancelAnimationFrame(raf); const from = { ...shown }, t0 = performance.now();
      const step = now => { const p = Math.min(1, (now - t0) / 600), e = 1 - Math.pow(1 - p, 3);
        shown = { h: from.h + (to.h - from.h) * e, a: from.a + (to.a - from.a) * e, f: from.f + (to.f - from.f) * e };
        $('#oHours').textContent = fmt(shown.h); $('#oAed').textContent = fmt(shown.a); $('#oFte').textContent = shown.f.toFixed(1);
        if (p < 1) raf = requestAnimationFrame(step); };
      raf = requestAnimationFrame(step); };
    const run = () => {
      $$('input[type=range]', calc).forEach(i => { $('#' + i.id + 'Out').textContent = (+i.value).toLocaleString('en-US') + i.dataset.unit; i.style.setProperty('--v', ((i.value - i.min) / (i.max - i.min) * 100) + '%'); });
      const h = get('cTeam') * get('cHours') * 46 * get('cCut') / 100;
      animate({ h, a: h * get('cRate'), f: h / 1800 });
      $('#oBar').style.width = Math.min(100, get('cCut')) + '%';
    };
    $$('input[type=range]', calc).forEach(i => i.addEventListener('input', run));
    const preset = key => { const P = SD[key] && SD[key].calc; if (!P) return; const ids = { cTeam: P.team, cHours: P.hours, cRate: P.rate, cCut: P.cut };
      const from = {}; Object.keys(ids).forEach(id => from[id] = get(id)); const t0 = performance.now(); cancelAnimationFrame(sraf);
      const step = now => { const p = Math.min(1, (now - t0) / 700), e = 1 - Math.pow(1 - p, 3);
        Object.keys(ids).forEach(id => { const el = $('#' + id), st = +el.step || 1; el.value = Math.round((from[id] + (ids[id] - from[id]) * e) / st) * st; });
        run(); if (p < 1) sraf = requestAnimationFrame(step); };
      sraf = requestAnimationFrame(step); };
    document.addEventListener('opsmo:sector', e => preset(e.detail));
    let first = true; onView(calc, v => { if (v && first) { first = false; run(); } });
  }

  /* ---------- impact board ---------- */
  const ib = $('#impactBoard');
  if (ib) onView(ib, v => { if (!v || ib.classList.contains('is-on')) return; ib.classList.add('is-on');
    const el = $('#lkMoney'), t0 = performance.now(), dur = reduce ? 0 : 1900;
    const step = now => { const p = dur ? Math.min(1, (now - t0) / dur) : 1; el.textContent = Math.round(500 * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step); }, .3);

  /* ---------- rollout (scroll-scrubbed) ---------- */
  const ro = $('#rollout');
  if (ro) {
    const now = $('#roNow'); let tk = false;
    const f = () => { tk = false; const r = ro.getBoundingClientRect(), vh = innerHeight;
      const p = Math.min(1, Math.max(0, (vh * .8 - r.top) / (r.height + vh * .2)));
      const wk = 1 + p * 12; ro.style.setProperty('--w', wk.toFixed(2)); now.textContent = wk >= 13 ? 'Ongoing' : 'Week ' + Math.floor(wk);
      $$('.ro__row', ro).forEach(row => { const s = +getComputedStyle(row).getPropertyValue('--s'), e = +getComputedStyle(row).getPropertyValue('--e');
        row.style.setProperty('--fill', Math.min(1, Math.max(0, (wk - s + 1) / (e - s + 1))).toFixed(3)); row.classList.toggle('is-done', wk >= e + 1); row.classList.toggle('is-on', wk >= s && wk < e + 1); }); };
    addEventListener('scroll', () => { if (!tk) { tk = true; requestAnimationFrame(f); } }, { passive: true }); f();
  }

  /* ---------- suite map ---------- */
  const sm = $('#suiteMap');
  if (sm) {
    let i = 0, timer = null;
    const go = n => { i = n;
      $$('.sm__tab', sm).forEach((t, j) => { t.classList.toggle('is-on', j === n); t.setAttribute('aria-selected', j === n); });
      $$('.sm__panel', sm).forEach((p, j) => p.classList.toggle('is-on', j === n));
      $$('.sm__node', sm).forEach((p, j) => p.classList.toggle('is-on', j === n));
      $$('.sm__lines line', sm).forEach((l, j) => l.classList.toggle('is-on', j === n)); };
    $$('.sm__tab', sm).forEach((t, j) => t.addEventListener('click', () => { clearInterval(timer); timer = null; go(j); }));
    $$('.sm__node', sm).forEach((t, j) => t.addEventListener('click', () => { clearInterval(timer); timer = null; go(j); }));
    go(0);
    onView(sm, v => { if (v && !timer && !reduce) timer = setInterval(() => go((i + 1) % 6), 3200); if (!v && timer) { clearInterval(timer); timer = null; } });
  }
})();
