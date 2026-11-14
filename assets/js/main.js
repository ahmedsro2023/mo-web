/* OPSMO — interactions (vanilla, no dependencies) */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const root = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isDesk = () => innerWidth > 980;

  /* ---------- theme (white / black) ---------- */
  const themeBtn = $('#themeBtn');
  const setTheme = t => {
    root.dataset.theme = t;
    try { localStorage.setItem('opsmo-theme', t); } catch (e) {}
    if (themeBtn) themeBtn.setAttribute('aria-label', t === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
    trailsAll.forEach(f => f.recolor && f.recolor());
  };
  const trailsAll = [];
  themeBtn && themeBtn.addEventListener('click', () => setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark'));
  if (themeBtn) themeBtn.setAttribute('aria-label', root.dataset.theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');

  /* ---------- light trails (Dubai interchange, abstracted) ---------- */
  function trails(canvas) {
    const host = canvas.parentElement, ctx = canvas.getContext('2d');
    const forceDark = canvas.dataset.dark === '1';
    let w, h, dpr, visible = false, lines = [], mouse = { x: -9999, y: -9999 }, dark;
    const count = forceDark ? 16 : 12;
    const recolor = () => { dark = forceDark || root.dataset.theme === 'dark'; };
    recolor();
    lines = Array.from({ length: count }, (_, i) => ({
      base: (i + .5) / count, amp: 18 + Math.random() * 60, freq: .0016 + Math.random() * .0022, phase: Math.random() * 6.28,
      speed: 110 + Math.random() * 220, len: 160 + Math.random() * 320, off: Math.random() * 3000, width: .8 + Math.random() * 1.8, hot: Math.random() < .55
    }));
    const size = () => { dpr = Math.min(devicePixelRatio || 1, 2); w = host.clientWidth; h = host.clientHeight; canvas.width = w * dpr; canvas.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); };
    const yAt = (L, x, t) => {
      let y = L.base * h + L.amp * Math.sin(x * L.freq + L.phase + t * .25);
      const dx = x - mouse.x, dy = y - mouse.y, d2 = dx * dx + dy * dy;
      if (d2 < 30000) y += (dy > 0 ? 1 : -1) * (30000 - d2) / 900;
      return y;
    };
    const draw = now => {
      const t = now / 1000; ctx.clearRect(0, 0, w, h);
      for (const L of lines) {
        const span = w + L.len * 2, head = ((L.off + t * L.speed) % span) - L.len, tail = head - L.len;
        const g = ctx.createLinearGradient(tail, 0, head, 0);
        const c = L.hot ? '255,100,20' : (dark ? '255,255,255' : '11,16,32');
        const a = L.hot ? (dark ? .85 : .5) : (dark ? .16 : .07);
        g.addColorStop(0, `rgba(${c},0)`); g.addColorStop(1, `rgba(${c},${a})`);
        ctx.strokeStyle = g; ctx.lineWidth = L.width; ctx.lineCap = 'round'; ctx.beginPath();
        for (let x = tail; x <= head; x += 10) { const y = yAt(L, x, t); x === tail ? ctx.moveTo(x, y) : ctx.lineTo(x, y); }
        ctx.stroke();
        if (L.hot) { const y = yAt(L, head, t); ctx.fillStyle = `rgba(255,170,90,${dark ? .9 : .65})`; ctx.beginPath(); ctx.arc(head, y, L.width + 1.2, 0, 6.28); ctx.fill(); }
      }
      if (visible && !reduce) requestAnimationFrame(draw);
    };
    size(); addEventListener('resize', size);
    host.addEventListener('pointermove', e => { const r = canvas.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; });
    host.addEventListener('pointerleave', () => { mouse.x = mouse.y = -9999; });
    new IntersectionObserver(([e]) => { const was = visible; visible = e.isIntersecting; if (visible && !was) requestAnimationFrame(draw); }).observe(host);
    if (reduce) draw(4000);
    trailsAll.push({ recolor: () => { recolor(); if (reduce) draw(4000); } });
  }
  $$('canvas.trails').forEach(trails);

  /* ---------- intro ---------- */
  $$('#heroH .ln').forEach((l, i) => l.firstElementChild.style.transitionDelay = (.1 + i * .09) + 's');
  requestAnimationFrame(() => setTimeout(() => root.classList.add('is-ready'), 80));

  /* ---------- reveal ---------- */
  const rObs = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-in'); rObs.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px', threshold: .06 });
  $$('.rv').forEach(n => {
    const sib = [...n.parentElement.children].filter(c => c.classList.contains('rv'));
    n.style.setProperty('--d', Math.min(sib.indexOf(n), 8) * .06 + 's');
    rObs.observe(n);
  });

  /* ---------- nav ---------- */
  const nav = $('#nav'), burger = $('#burger');
  $$('.dd').forEach(dd => {
    const b = $('.dd__btn', dd); let t;
    const open = v => { dd.classList.toggle('is-open', v); b.setAttribute('aria-expanded', v); };
    b.addEventListener('click', e => { e.stopPropagation(); const v = !dd.classList.contains('is-open'); $$('.dd').forEach(o => o !== dd && (o.classList.remove('is-open'), $('.dd__btn', o).setAttribute('aria-expanded', false))); open(v); });
    dd.addEventListener('mouseenter', () => { if (matchMedia('(hover:hover)').matches) { clearTimeout(t); $$('.dd').forEach(o => o !== dd && o.classList.remove('is-open')); open(true); } });
    dd.addEventListener('mouseleave', () => { if (matchMedia('(hover:hover)').matches) t = setTimeout(() => open(false), 160); });
    dd.addEventListener('keydown', e => { if (e.key === 'Escape') { open(false); b.focus(); } });
  });
  document.addEventListener('click', e => { if (!e.target.closest('.dd')) $$('.dd').forEach(o => { o.classList.remove('is-open'); $('.dd__btn', o).setAttribute('aria-expanded', false); }); });
  burger && burger.addEventListener('click', () => { const o = nav.classList.toggle('is-open'); burger.setAttribute('aria-expanded', o); });
  $$('#sheet a').forEach(a => a.addEventListener('click', () => { nav.classList.remove('is-open'); burger.setAttribute('aria-expanded', false); }));
  // mark current section in nav
  const here = location.pathname.replace(/index\.html$/, '');
  $$('.nav__a').forEach(a => { try { if (new URL(a.href).pathname === here) a.classList.add('is-on'); } catch (e) {} });

  /* ---------- counters ---------- */
  const countUp = (el, end, dur = 1400) => {
    if (reduce) { el.textContent = end; return; }
    const t0 = performance.now(), from = +el.textContent || 0;
    const step = now => { const k = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - k, 3); el.textContent = Math.round((from + (end - from) * e) * 2) / 2; if (k < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };

  /* ---------- hero stack parallax ---------- */
  const stack = $('#stack');
  let mx = 0, my = 0, sy = 0;
  const tiles = stack ? $$('.tile', stack) : [];
  const baseT = tiles.map(t => t.classList.contains('tile--photo') ? 'rotate(-6deg)' : '');
  const applyStack = () => tiles.forEach((t, i) => {
    const d = +t.dataset.depth || 1, fan = sy * (i === 0 ? -.04 : (i % 2 ? -.12 : .1));
    t.style.transform = `translate3d(${mx * d * 7}px, ${my * d * 7 + fan}px, 0) ${baseT[i]}`;
  });
  if (stack && !reduce) {
    setTimeout(() => tiles.forEach(t => t.style.transitionDelay = '0s'), 2600);
    addEventListener('pointermove', e => { if (!isDesk()) return; mx = (e.clientX / innerWidth - .5) * 2; my = (e.clientY / innerHeight - .5) * 2; requestAnimationFrame(applyStack); });
  }

  /* ---------- scroll engine ---------- */
  const bar = $('#progressBar'), reality = $('#reality'), track = $('#htrack'), hbar = $('#hbar');
  const msteps = $$('.method .mstep'), mimgs = $$('#mstack img'), mBadge = $('#mBadge'), mList = $('.method .msteps');
  const STG = ['Diagnose', 'Design', 'Implement', 'Integrate', 'Operate', 'Optimize'];
  let lastY = scrollY, ticking = false, curM = -1;
  function frame() {
    const y = scrollY, H = root.scrollHeight - innerHeight;
    if (bar) bar.style.transform = `scaleX(${H > 0 ? y / H : 0})`;
    if (!nav.classList.contains('is-open') && !$('.dd.is-open')) {
      if (y > 400 && y > lastY + 6) nav.classList.add('is-hidden');
      else if (y < lastY - 6 || y < 400) nav.classList.remove('is-hidden');
    }
    lastY = y;
    if (stack && !reduce) { sy = Math.min(y, 700); applyStack(); }
    if (reality && track && isDesk()) {
      const r = reality.getBoundingClientRect(), total = reality.offsetHeight - innerHeight;
      const p = Math.min(1, Math.max(0, -r.top / total));
      track.style.transform = `translate3d(${-(track.scrollWidth - innerWidth + 80) * p}px,0,0)`;
      if (hbar) hbar.style.transform = `scaleX(${p})`;
    }
    if (msteps.length) {
      const mid = innerHeight * .5; let active = 0;
      msteps.forEach((s, i) => { if (s.getBoundingClientRect().top < mid) active = i; });
      if (active !== curM) {
        curM = active;
        msteps.forEach((s, i) => s.classList.toggle('is-on', i === active));
        mimgs.forEach((im, i) => im.classList.toggle('is-on', i === active));
        if (mBadge) mBadge.textContent = `0${active + 1} / 06 · ${STG[active]}`;
      }
      const lr = mList.getBoundingClientRect();
      mList.style.setProperty('--fill', Math.min(100, Math.max(0, (mid - lr.top) / lr.height * 100)) + '%');
    }
    ticking = false;
  }
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }, { passive: true });
  addEventListener('resize', frame); frame();

  /* ---------- software-selection stages ---------- */
  $$('.stg').forEach(w => {
    const data = JSON.parse(w.dataset.stages), tabs = $$('.stg__tab', w), task = $('.stg__task', w), del = $('.stg__d', w);
    const show = i => {
      tabs.forEach((t, k) => { t.classList.toggle('is-on', k === i); t.setAttribute('aria-selected', k === i); });
      w.classList.add('is-swap');
      setTimeout(() => { task.textContent = data[i].t; del.textContent = data[i].d; w.classList.remove('is-swap'); }, reduce ? 0 : 220);
    };
    tabs.forEach((t, i) => t.addEventListener('click', () => show(i)));
    $('.stg__tabs', w).addEventListener('keydown', e => {
      const cur = tabs.findIndex(t => t.classList.contains('is-on'));
      if (['ArrowDown', 'ArrowRight'].includes(e.key)) { e.preventDefault(); const n = (cur + 1) % tabs.length; show(n); tabs[n].focus(); }
      if (['ArrowUp', 'ArrowLeft'].includes(e.key)) { e.preventDefault(); const n = (cur + tabs.length - 1) % tabs.length; show(n); tabs[n].focus(); }
    });
  });

  /* ---------- effort estimate ---------- */
  const est = $('#estimate');
  if (est) {
    const v = k => Math.max(0, parseFloat($(`[data-k=${k}]`, est).value) || 0);
    const calc = () => {
      const p = v('people'), demo = v('demos') * v('hpd') * p, rev = p * v('rev'), dec = v('dec') * p, oth = v('other');
      const tot = demo + rev + dec + oth, fmt = n => Math.round(n * 10) / 10;
      $('#estTotal').textContent = fmt(tot);
      $('#bDemo').textContent = fmt(demo); $('#bRev').textContent = fmt(rev); $('#bDec').textContent = fmt(dec); $('#bOth').textContent = fmt(oth);
      const mxv = Math.max(demo, rev, dec, oth, 1);
      [['demo', demo], ['rev', rev], ['dec', dec], ['oth', oth]].forEach(([k, n]) => $(`[data-b=${k}]`, est).style.width = (n / mxv * 100) + '%');
    };
    $$('input', est).forEach(i => i.addEventListener('input', calc));
    $$('[data-step]', est).forEach(b => b.addEventListener('click', () => {
      const i = $('input', b.parentElement); i.value = Math.max(0, (parseFloat(i.value) || 0) + (+b.dataset.step)); calc();
    }));
    calc();
  }

  /* ---------- fit guide ---------- */
  const fit = $('#fitGuide');
  if (fit) {
    const R = JSON.parse(fit.dataset.fit), res = $('.fit__res', fit);
    const upd = () => {
      const att = $('[name=att]:checked', fit).value, q = $('[name=fitq]:checked', fit).value;
      const r = (q === 'mostly') ? R.mostly : R[att];
      $('#fitT').textContent = r[0]; $('#fitP').textContent = r[1];
      const a = $('#fitA'); a.href = r[3]; a.firstChild.textContent = r[2] + ' ';
      res.classList.remove('is-swap'); void res.offsetWidth; res.classList.add('is-swap');
    };
    $$('input', fit).forEach(i => i.addEventListener('change', upd));
  }

  /* ---------- solutions explorer (home) ---------- */
  const ex = $('.explorer[data-sol]');
  if (ex) {
    const S = JSON.parse(ex.dataset.sol), book = ex.dataset.book, tabs = $$('.etab', ex), panel = $('#solPanel');
    const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    const arrow = '<svg class="i" aria-hidden="true"><use href="#i-arrow"/></svg>';
    const show = i => {
      const s = S[i];
      tabs.forEach((t, k) => { t.classList.toggle('is-on', k === i); t.setAttribute('aria-selected', k === i); });
      panel.innerHTML = `<div class="ep__img"><img src="${s.img}" alt=""><div><span class="mono">[SYSTEM: ${s.sys}]</span><h3>${esc(s.name)}</h3></div></div>
        <div class="ep__body"><div><p>${esc(s.desc)}</p><div class="btnrow"><a class="btn btn--fire btn--sm" href="${s.href}">Explore ${esc(s.short)} ${arrow}</a><a class="btn btn--line btn--sm" href="${book}">BOOK A CONSULTATION ${arrow}</a></div></div>
        <ul class="ticks">${s.bul.map(b => `<li>${esc(b)}</li>`).join('')}</ul></div>`;
    };
    tabs.forEach((t, i) => t.addEventListener('click', () => show(i)));
    $('.explorer__tabs', ex).addEventListener('keydown', e => {
      const cur = tabs.findIndex(t => t.classList.contains('is-on'));
      if (['ArrowDown', 'ArrowRight'].includes(e.key)) { e.preventDefault(); const n = (cur + 1) % tabs.length; show(n); tabs[n].focus(); }
      if (['ArrowUp', 'ArrowLeft'].includes(e.key)) { e.preventDefault(); const n = (cur + tabs.length - 1) % tabs.length; show(n); tabs[n].focus(); }
    });
    show(0);
  }

  /* ---------- FAQ: one open at a time ---------- */
  $$('.faq__list').forEach(l => { const q = $$('.qa', l); q.forEach(d => d.addEventListener('toggle', () => { if (d.open) q.forEach(o => o !== d && (o.open = false)); })); });

  /* ---------- forms ----------
     Set FORM_ENDPOINT (Formspree, Getform or your own API) to receive submissions. */
  const FORM_ENDPOINT = '';
  const validate = scope => {
    let ok = true;
    $$('[required]', scope).forEach(i => {
      const bad = !i.value.trim() || (i.type === 'email' && !/^\S+@\S+\.\S+$/.test(i.value));
      i.closest('.field').classList.toggle('is-err', bad); if (bad) ok = false;
    });
    return ok;
  };
  const send = async (form, okMsg) => {
    const msg = $('.form__msg', form);
    if (!FORM_ENDPOINT) { msg.className = 'form__msg err'; msg.textContent = "This form isn't connected yet — add a form endpoint in assets/js/main.js."; return; }
    msg.className = 'form__msg'; msg.textContent = 'Sending…';
    try {
      const fd = new FormData(form); fd.append('page', location.pathname);
      const r = await fetch(FORM_ENDPOINT, { method: 'POST', headers: { Accept: 'application/json' }, body: fd });
      if (!r.ok) throw 0;
      form.reset(); msg.className = 'form__msg ok'; msg.textContent = okMsg;
    } catch (e) { msg.className = 'form__msg err'; msg.textContent = "The request didn't go through. Check your connection and try again."; }
  };
  const wiz = $('#leadForm');
  if (wiz) {
    const steps = $$('.step', wiz); let at = 1;
    const go = n => { at = n; wiz.dataset.at = n; steps.forEach(s => s.classList.toggle('is-on', +s.dataset.step === n)); $('#stepLbl').textContent = n + '/3'; $('#stepFill').style.width = (n / 3 * 100) + '%'; };
    go(1);
    $('#wNext').addEventListener('click', () => { if (validate(steps[at - 1])) go(at + 1); else { const m = $('.form__msg', wiz); m.className = 'form__msg err'; m.textContent = 'Complete the required fields to continue.'; } });
    $('#wBack').addEventListener('click', () => go(Math.max(1, at - 1)));
    wiz.addEventListener('submit', e => { e.preventDefault(); if (!validate(steps[2])) { const m = $('.form__msg', wiz); m.className = 'form__msg err'; m.textContent = 'Choose a service and describe the main operational challenge.'; return; } send(wiz, "Request received. A person will review it within one business day."); });
  }
  const book = $('#bookForm');
  if (book) {
    const d = $('[name=date]', book); if (d) d.min = new Date().toISOString().slice(0, 10);
    book.addEventListener('submit', e => { e.preventDefault(); if (!validate(book)) { const m = $('.form__msg', book); m.className = 'form__msg err'; m.textContent = 'Fill in the required fields marked *.'; return; } send(book, "Call requested. OPSMO will confirm a time by email."); });
  }
})();
