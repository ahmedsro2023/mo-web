/* OPSMO v7 — dynamic showcase: live pipeline, before/after, calculator, rollout, suite map */
(() => {
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const onView = (el, fn, th = .25) => { if (!el) return; const io = new IntersectionObserver(es => es.forEach(e => fn(e.isIntersecting)), { threshold: th }); io.observe(el); };
  const fmt = n => Math.round(n).toLocaleString('en-US');

  /* ---------- live pipeline ---------- */
  const lv = $('#liveDemo');
  if (lv) {
    const SRC = ['Property Finder', 'Bayut', 'Website form', 'Meta ad', 'WhatsApp', 'Referral'];
    const WHAT = ['2BR · Dubai Marina', 'Villa · Al Furjan', '1BR · JVC', 'Office · Business Bay', 'Studio · Downtown', '3BR · Arabian Ranches', 'Townhouse · Damac Hills', '2BR · Creek Harbour'];
    const WHO = ['Sara', 'Omar', 'Lina', 'Yousef', 'Maya', 'Karim'];
    const feed = $('#lvFeed'), cols = $$('.lv__col', lv), k = { leads: $('#kLeads'), resp: $('#kResp'), tasks: $('#kTasks'), won: $('#kWon') };
    let leads = 0, won = 0, tasks = 0, resp = [], spark = [], timer = null, id = 0;
    const pick = a => a[Math.floor(Math.random() * a.length)];
    const count = () => cols.forEach(cl => $('[data-colcount]', cl).textContent = $$('.lv__card', cl).length);
    const card = (what, src, who) => { const d = document.createElement('div'); d.className = 'lv__card'; d.innerHTML = `<b>${what}</b><span>${src}</span><i>${who[0]}</i>`; return d; };
    const tick = () => {
      // 1) a new lead arrives
      const src = pick(SRC), what = pick(WHAT), who = pick(WHO), secs = 3 + Math.floor(Math.random() * 9);
      leads++; resp.push(secs); if (resp.length > 20) resp.shift();
      const li = document.createElement('li');
      li.innerHTML = `<span class="lv__src">${src}</span><b>${what}</b><span class="lv__ok">Assigned to ${who} · ${secs}s</span>`;
      feed.prepend(li); requestAnimationFrame(() => li.classList.add('is-in'));
      while (feed.children.length > 5) feed.lastElementChild.remove();
      const cd = card(what, src, who); $('.lv__cards', cols[0]).prepend(cd); requestAnimationFrame(() => cd.classList.add('is-in'));
      // 2) move one card forward somewhere in the pipeline
      for (let i = cols.length - 2; i >= 0; i--) {
        const cs = $$('.lv__card', cols[i]);
        if (cs.length && Math.random() < (i === 0 ? .7 : .45)) {
          const m = cs[cs.length - 1]; m.classList.add('is-move');
          setTimeout(() => { m.classList.remove('is-move', 'is-in'); $('.lv__cards', cols[i + 1]).prepend(m); requestAnimationFrame(() => m.classList.add('is-in')); if (i + 1 === cols.length - 1) { won++; m.classList.add('is-won'); } count(); }, 450);
          tasks++; break;
        }
      }
      $$('.lv__cards', lv).forEach(c => { while (c.children.length > 4) c.lastElementChild.remove(); });
      count();
      k.leads.textContent = leads; k.won.textContent = won; k.tasks.textContent = Math.max(0, tasks - won);
      k.resp.textContent = Math.round(resp.reduce((a, b) => a + b, 0) / resp.length) + 's';
      spark.push(secs); if (spark.length > 24) spark.shift();
      const d = spark.map((v, i) => `${i ? 'L' : 'M'}${(i / 23) * 200} ${60 - v * 4.5}`).join(' ');
      $('#lvSpark').setAttribute('d', d);
    };
    for (let i = 0; i < 6; i++) tick();
    onView(lv, v => { if (v && !timer && !reduce) timer = setInterval(tick, 2300); if (!v && timer) { clearInterval(timer); timer = null; } });
  }

  /* ---------- before / after ---------- */
  const ba = $('#beforeAfter');
  if (ba) {
    const clock = $('#baClock'), verdict = $('#baVerdict'); let raf, auto = true;
    const T = { before: [15600, '4h 20m', 'Lead lost'], after: [6, '6 seconds', 'Lead contacted'] };
    const show = mode => {
      ba.dataset.mode = mode;
      $$('.ba__switch button', ba).forEach(b => b.setAttribute('aria-selected', b.dataset.mode === mode));
      const lane = $(`.ba__lane--${mode}`, ba);
      $$('.ba__lane li', ba).forEach(li => li.classList.remove('is-on'));
      $$('li', lane).forEach((li, i) => setTimeout(() => li.classList.add('is-on'), reduce ? 0 : 250 + i * 420));
      cancelAnimationFrame(raf); verdict.classList.remove('is-on');
      const [secs, label, v] = T[mode], t0 = performance.now(), dur = reduce ? 0 : 2200;
      const step = now => { const p = dur ? Math.min(1, (now - t0) / dur) : 1, s = secs * (1 - Math.pow(1 - p, 3));
        clock.textContent = p < 1 ? (s >= 3600 ? `${Math.floor(s / 3600)}h ${Math.floor(s % 3600 / 60)}m` : s >= 60 ? `${Math.floor(s / 60)}m ${Math.floor(s % 60)}s` : `${Math.floor(s)}s`) : label;
        if (p < 1) raf = requestAnimationFrame(step); else { verdict.textContent = v; verdict.classList.add('is-on'); } };
      raf = requestAnimationFrame(step);
    };
    $$('.ba__switch button', ba).forEach(b => b.addEventListener('click', () => { auto = false; show(b.dataset.mode); }));
    let played = false;
    onView(ba, v => { if (v && !played) { played = true; show('before'); setTimeout(() => auto && show('after'), 4600); } }, .4);
  }

  /* ---------- calculator ---------- */
  const calc = $('#calc');
  if (calc) {
    const get = id => +$('#' + id).value, out = {}; let shown = { h: 0, a: 0, f: 0 }, raf;
    const animate = (to) => { cancelAnimationFrame(raf); const from = { ...shown }, t0 = performance.now();
      const step = now => { const p = Math.min(1, (now - t0) / 500), e = 1 - Math.pow(1 - p, 3);
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
    let first = true; onView(calc, v => { if (v && first) { first = false; run(); } });
  }

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
