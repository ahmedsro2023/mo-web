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

  /* ---------- the race: spreadsheet + WhatsApp vs OPSMO system ---------- */
  const race = $('#race');
  if (race && SD[SECTOR]) {
    const NAMES = ['Ahmed Khalil', 'Sara Haddad', 'Omar Nasser', 'Lina Farouk', 'Yousef Ali', 'Maya Saeed', 'Karim Adel', 'Noor Hamdan', 'Adam Rashid', 'Hala Mansour', 'Rami Aziz', 'Dana Yasin', 'Tariq Fahd', 'Reem Kamal'];
    const OWN = ['Sara', 'Omar', 'Lina', 'Yousef', 'Maya'];
    const E = id => document.getElementById(id);
    let T = [], raf = [], running = false, played = false;
    const later = (ms, fn) => T.push(setTimeout(fn, reduce ? 0 : ms));
    const stop = () => { T.forEach(clearTimeout); T = []; raf.forEach(cancelAnimationFrame); raf = []; running = false; };
    const fmtT = s => s >= 86400 ? `${Math.floor(s / 86400)}d ${Math.floor(s % 86400 / 3600)}h` : s >= 3600 ? `${Math.floor(s / 3600)}h ${String(Math.floor(s % 3600 / 60)).padStart(2, '0')}m` : `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`;
    const clock = (el, total, ms, done) => { const t0 = performance.now();
      const mir = E(el.id === 'rcClockL' ? 'dualL' : 'dualR');
      const st = now => { const p = reduce ? 1 : Math.min(1, (now - t0) / ms); el.textContent = fmtT(total * p); if (mir) mir.textContent = el.textContent; if (p < 1) raf.push(requestAnimationFrame(st)); else done && done(); };
      raf.push(requestAnimationFrame(st)); };
    const type = (el, txt, speed, cb) => { let i = 0; el.classList.add('is-typing'); const go = () => { el.textContent = txt.slice(0, ++i); E('xlFx').textContent = el.textContent;
      if (i < txt.length) later(speed + Math.random() * speed, go); else { el.classList.remove('is-typing'); cb && cb(); } }; go(); };
    const wa = (txt, who, me) => { const d = document.createElement('p'); d.className = 'wa2__m' + (me ? ' wa2__m--me' : '');
      d.innerHTML = `${me ? '' : `<b>${who}</b>`}${txt}<em>${new Date().toTimeString().slice(0, 5)}</em>`; E('waBody').appendChild(d);
      requestAnimationFrame(() => d.classList.add('is-in')); const b = E('waBody'); while (b.children.length > 4) b.firstElementChild.remove(); };
    const reset = () => {
      stop(); const S = SD[SECTOR];
      ['xlA', 'xlB', 'xlC', 'xlD', 'xlE', 'xlFx'].forEach(id => E(id).textContent = '');
      E('waBody').innerHTML = ''; E('logOld').innerHTML = ''; E('crmFeed').innerHTML = ''; E('crmCount').textContent = '0';
      E('rcClockL').textContent = '0:00'; E('rcClockR').textContent = '0:00'; E('dualL').textContent = '0:00'; E('dualR').textContent = '0:00';
      E('rcMetricL').textContent = S.metric; E('rcMetricR').textContent = S.metric;
      E('stampOld').textContent = S.before.verdict; E('stampNew').textContent = S.after.verdict;
      E('crmSteps').innerHTML = S.after.steps.map(([t, h]) => `<li><i></i><span class="mono">${t}</span><b>${h}</b></li>`).join('');
      E('endOld').textContent = S.before.label; E('endNew').textContent = S.after.label;
      E('barNew').style.setProperty('--r', Math.max(.03, S.after.total / S.before.total).toFixed(3));
      E('raceGain').textContent = Math.min(99, Math.round((1 - S.after.total / S.before.total) * 100)) + '%';
      race.className = 'race is-reset'; void race.offsetWidth; race.classList.remove('is-reset');
      E('xlSave').textContent = 'Not saved';
    };
    const run = () => {
      reset(); running = true; const S = SD[SECTOR];
      const item = S.items[0], src = S.sources[0], name = NAMES[0];
      race.classList.add('is-run');
      /* ---- LEFT: slow, manual ---- */
      clock(E('rcClockL'), S.before.total, 11000);
      later(300, () => wa(`New enquiry 👀 ${item} from ${src}`, 'Reception'));
      later(900, () => type(E('xlA'), name, 140, () => type(E('xlB'), src, 120, () => later(900, () => type(E('xlC'), '#N/A', 160)))));
      later(2600, () => wa('Who is free to take this?', 'Manager'));
      later(4400, () => wa('With a client, will check later', 'Omar'));
      later(5600, () => { race.classList.add('is-dup'); E('xlSave').textContent = 'Someone else is editing'; });
      later(6800, () => wa(`Did anyone reply to ${name.split(' ')[0]}?`, 'Manager'));
      later(8600, () => { type(E('xlD'), 'Call back?', 150); wa('Sorry, just saw this 🙏', 'Lina', true); });
      S.before.steps.forEach(([t, h], i) => later(400 + i * 2400, () => { const li = document.createElement('li'); li.innerHTML = `<span class="mono">${t}</span>${h}`; E('logOld').appendChild(li); requestAnimationFrame(() => li.classList.add('is-in')); }));
      later(11200, () => race.classList.add('is-lost'));
      /* ---- RIGHT: instant, automatic ---- */
      E('crmSrc').textContent = src; E('crmName').textContent = name; E('crmWhat').textContent = item; E('crmSt').textContent = 'New';
      E('crmOwner').innerHTML = '<i>…</i>Assigning'; E('crmNext').textContent = '—'; E('crmPushT').textContent = `${name} · tap to call`;
      clock(E('rcClockR'), S.after.total, 2400, () => race.classList.add('is-won'));
      later(200, () => race.classList.add('s1'));
      const steps = $$('#crmSteps li'); steps.forEach((li, i) => later(300 + i * 520, () => li.classList.add('is-on')));
      later(800, () => { E('crmOwner').innerHTML = `<i>${OWN[0][0]}</i>${OWN[0]}`; race.classList.add('s2'); });
      later(1300, () => race.classList.add('s3'));
      later(2100, () => { E('crmSt').textContent = S.stages[1]; E('crmNext').textContent = 'Follow-up booked'; race.classList.add('s4'); });
      // after the first one, the system keeps clearing requests while the left side is still stuck
      let n = 0; const more = () => { n++; E('crmCount').textContent = n;
        const r = document.createElement('div'); const o = OWN[n % OWN.length];
        r.innerHTML = `<i>${o[0]}</i><b>${NAMES[n % NAMES.length]}</b><span>${S.items[n % S.items.length]}</span><em>✓ ${3 + (n * 7) % 9}s</em>`;
        E('crmFeed').prepend(r); requestAnimationFrame(() => r.classList.add('is-in')); const f = E('crmFeed'); while (f.children.length > 4) f.lastElementChild.remove();
        if (n < 14) later(560, more); };
      later(2600, more);
      later(11800, () => { race.classList.add('is-end'); running = false; });
    };
    E('raceReplay').addEventListener('click', run);
    onView(race, v => { if (v && !played) { played = true; run(); } }, .35);
    document.addEventListener('opsmo:sector', () => { played = true; run(); });
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
