/* OPSMO — interactions (vanilla, no dependencies) */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isDesk = () => innerWidth > 900;

  /* ---------- light-trail canvases (the Dubai interchange, abstracted) ---------- */
  function trails(canvas, { dark = false, count = 14 } = {}) {
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let w, h, dpr, lines = [], visible = false, mouse = { x: -9999, y: -9999 };
    const host = canvas.parentElement;
    const seed = () => {
      lines = Array.from({ length: count }, (_, i) => ({
        base: (i + .5) / count,
        amp: 18 + Math.random() * 60,
        freq: .0016 + Math.random() * .0022,
        phase: Math.random() * 6.28,
        speed: 110 + Math.random() * 220,
        len: 160 + Math.random() * 320,
        off: Math.random() * 3000,
        width: .8 + Math.random() * 1.8,
        hot: Math.random() < .55
      }));
    };
    const size = () => {
      dpr = Math.min(devicePixelRatio || 1, 2);
      w = host.clientWidth; h = host.clientHeight;
      canvas.width = w * dpr; canvas.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    const yAt = (L, x, t) => {
      let y = L.base * h + L.amp * Math.sin(x * L.freq + L.phase + t * .25);
      const dx = x - mouse.x, dy = y - mouse.y, d2 = dx * dx + dy * dy;
      if (d2 < 30000) y += (dy > 0 ? 1 : -1) * (30000 - d2) / 900;
      return y;
    };
    const draw = (now) => {
      const t = now / 1000;
      ctx.clearRect(0, 0, w, h);
      for (const L of lines) {
        const span = w + L.len * 2;
        const head = ((L.off + t * L.speed) % span) - L.len;
        const tail = head - L.len;
        const g = ctx.createLinearGradient(tail, 0, head, 0);
        const c = L.hot ? '255,100,20' : (dark ? '255,255,255' : '11,16,32');
        const a = L.hot ? (dark ? .85 : .55) : (dark ? .18 : .08);
        g.addColorStop(0, `rgba(${c},0)`);
        g.addColorStop(1, `rgba(${c},${a})`);
        ctx.strokeStyle = g; ctx.lineWidth = L.width; ctx.lineCap = 'round';
        ctx.beginPath();
        for (let x = tail; x <= head; x += 10) {
          const y = yAt(L, x, t);
          x === tail ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }
        ctx.stroke();
        if (L.hot) { // glowing head
          const y = yAt(L, head, t);
          ctx.fillStyle = `rgba(255,170,90,${dark ? .9 : .7})`;
          ctx.beginPath(); ctx.arc(head, y, L.width + 1.2, 0, 6.28); ctx.fill();
        }
      }
      if (visible && !reduce) requestAnimationFrame(draw);
    };
    seed(); size();
    addEventListener('resize', size);
    host.addEventListener('pointermove', e => { const r = canvas.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; });
    host.addEventListener('pointerleave', () => { mouse.x = mouse.y = -9999; });
    new IntersectionObserver(([e]) => {
      const was = visible; visible = e.isIntersecting;
      if (visible && !was) requestAnimationFrame(draw);
    }).observe(host);
    if (reduce) draw(4000);
  }
  trails($('#heroTrails'), { dark: false, count: 12 });
  trails($('#darkTrails'), { dark: true, count: 18 });
  trails($('#caseTrails'), { dark: true, count: 14 });

  /* ---------- intro ---------- */
  $$('#heroH .ln').forEach((l, i) => l.firstElementChild.style.transitionDelay = (.1 + i * .09) + 's');
  requestAnimationFrame(() => setTimeout(() => document.documentElement.classList.add('is-ready'), 80));

  // pipeline numbers count up after intro
  const countUp = (el, end, dur = 1600) => {
    if (reduce) { el.textContent = end.toLocaleString('en-US'); return; }
    const t0 = performance.now();
    const step = now => {
      const k = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - k, 3);
      el.textContent = Math.round(end * e).toLocaleString('en-US');
      if (k < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  setTimeout(() => $$('.pipe b').forEach(b => countUp(b, +b.dataset.n, 1800)), 900);

  // live feed rotates new events in
  const events = [
    ['ok', 'Bayut enquiry assigned to agent', 'now'],
    ['ok', 'Contract signed — onboarding started', 'now'],
    ['ok', 'Payment matched to invoice in Books', 'now'],
    ['warn', 'Follow-up overdue — manager notified', 'now'],
    ['ok', 'WhatsApp lead merged with existing contact', 'now'],
    ['ok', 'Weekly pipeline report sent to leadership', 'now']
  ];
  const feed = $('#feed'); let ei = 0;
  if (!reduce) setInterval(() => {
    const [k, txt, ts] = events[ei++ % events.length];
    const li = document.createElement('li');
    li.innerHTML = `<i class="${k}"></i>${txt}<span>${ts}</span>`;
    feed.prepend(li);
    $$('li', feed).forEach((n, i) => { if (i > 0) n.lastElementChild.textContent = ['now', '8s', '21s', '40s'][i] || '1m'; });
    if (feed.children.length > 3) feed.lastElementChild.remove();
  }, 3200);

  /* ---------- hero stack: mouse parallax + scroll fan-out ---------- */
  const stack = $('#stack'), tiles = $$('.tile', stack);
  const base = ['rotate(-7deg)', 'rotate(-3deg)', 'rotate(2deg)'];
  let mx = 0, my = 0, sy = 0;
  const applyStack = () => {
    tiles.forEach((t, i) => {
      const d = +t.dataset.depth;
      const fan = sy * (i === 0 ? -.04 : i === 1 ? -.16 : .12);
      t.style.transform = `translate3d(${mx * d * 8}px, ${my * d * 8 + fan}px, 0) ${base[i]}`;
    });
  };
  if (!reduce) {
    addEventListener('pointermove', e => {
      if (!isDesk()) return;
      mx = (e.clientX / innerWidth - .5) * 2; my = (e.clientY / innerHeight - .5) * 2;
      requestAnimationFrame(applyStack);
    });
  }

  /* ---------- counters on reveal ---------- */
  const cObs = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    countUp(e.target, +e.target.dataset.count, 1800);
    cObs.unobserve(e.target);
  }), { threshold: .6 });
  $$('[data-count]').forEach(n => cObs.observe(n));

  /* ---------- reveal ---------- */
  const rObs = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    e.target.classList.add('is-in'); rObs.unobserve(e.target);
  }), { rootMargin: '0px 0px -8% 0px', threshold: .06 });
  $$('.rv').forEach(n => {
    const sib = [...n.parentElement.children].filter(c => c.classList.contains('rv'));
    n.style.setProperty('--d', Math.min(sib.indexOf(n), 8) * .06 + 's');
    rObs.observe(n);
  });

  /* ---------- reality: symptom / fix toggle ---------- */
  const tog = $('.toggle'), pill = $('.toggle__pill'), track = $('#htrack');
  const place = b => { pill.style.width = b.offsetWidth + 'px'; pill.style.transform = `translateX(${b.offsetLeft - 5}px)`; };
  $$('button', tog).forEach(b => b.addEventListener('click', () => {
    $$('button', tog).forEach(x => { x.classList.toggle('is-on', x === b); x.setAttribute('aria-selected', x === b); });
    track.dataset.view = b.dataset.view; place(b);
  }));
  const placeOn = () => place($('button.is-on', tog));
  (document.fonts ? document.fonts.ready : Promise.resolve()).then(placeOn); placeOn();
  addEventListener('resize', placeOn);

  /* ---------- scroll engine ---------- */
  const nav = $('#nav'), bar = $('#progressBar'), reality = $('#reality'), hbar = $('#hbar');
  const msteps = $$('.mstep'), mimgs = $$('#mstack img'), mBadge = $('#mBadge'), mList = $('#msteps');
  const STAGES = ['Diagnose', 'Design', 'Implement', 'Integrate', 'Operate', 'Optimize'];
  let lastY = scrollY, ticking = false, curM = -1;
  function frame() {
    const y = scrollY, H = document.documentElement.scrollHeight - innerHeight;
    bar.style.transform = `scaleX(${H > 0 ? y / H : 0})`;
    if (!nav.classList.contains('is-open')) {
      if (y > 400 && y > lastY + 6) nav.classList.add('is-hidden');
      else if (y < lastY - 6 || y < 400) nav.classList.remove('is-hidden');
    }
    lastY = y;
    // hero fan-out
    sy = Math.min(y, 700); if (!reduce) applyStack();
    // horizontal reality track
    if (isDesk()) {
      const r = reality.getBoundingClientRect(), total = reality.offsetHeight - innerHeight;
      const p = Math.min(1, Math.max(0, -r.top / total));
      const dist = track.scrollWidth - innerWidth + 80;
      track.style.transform = `translate3d(${-dist * p}px,0,0)`;
      hbar.style.transform = `scaleX(${p})`;
    }
    // method steps
    const mid = innerHeight * .5; let active = 0;
    msteps.forEach((s, i) => { if (s.getBoundingClientRect().top < mid) active = i; });
    if (active !== curM) {
      curM = active;
      msteps.forEach((s, i) => s.classList.toggle('is-on', i === active));
      mimgs.forEach((im, i) => im.classList.toggle('is-on', i === active));
      mBadge.textContent = `0${active + 1} / 06 · ${STAGES[active]}`;
    }
    const lr = mList.getBoundingClientRect();
    mList.style.setProperty('--fill', Math.min(100, Math.max(0, (mid - lr.top) / lr.height * 100)) + '%');
    ticking = false;
  }
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }, { passive: true });
  addEventListener('resize', frame);
  frame();

  /* active nav link */
  const links = $$('.nav__links a');
  const sObs = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) links.forEach(a => a.classList.toggle('is-on', a.getAttribute('href') === '#' + e.target.id));
  }), { rootMargin: '-45% 0px -50% 0px' });
  ['reality', 'solutions', 'method', 'founder', 'faq'].forEach(id => sObs.observe(document.getElementById(id)));

  /* ---------- disciplines: cursor-follow image ---------- */
  const cImg = $('#cursorImg'), cIm = $('img', cImg);
  let cx = 0, cy = 0, tx = 0, ty = 0, cRun = false;
  const follow = () => {
    cx += (tx - cx) * .16; cy += (ty - cy) * .16;
    cImg.style.left = cx + 'px'; cImg.style.top = cy + 'px';
    if (cRun) requestAnimationFrame(follow);
  };
  $$('.disc__row').forEach(row => {
    row.addEventListener('pointerenter', e => {
      if (!isDesk()) return;
      cIm.src = row.dataset.img; cImg.classList.add('is-on');
      tx = cx = e.clientX + 180; ty = cy = e.clientY;
      if (!cRun) { cRun = true; requestAnimationFrame(follow); }
    });
    row.addEventListener('pointermove', e => { tx = e.clientX + 180; ty = e.clientY; });
    row.addEventListener('pointerleave', () => { cImg.classList.remove('is-on'); cRun = false; });
  });

  /* ---------- solutions explorer ---------- */
  const SOL = [
    { t: 'CRM Implementation', img: 'office', p: 'You need a CRM your team will actually use — set up around your sales process, not the vendor\'s default.', d: ['Pipeline and stage design with exit criteria', 'Data model, fields, layouts and permissions', 'Lead assignment and response-time rules', 'Training and an adoption plan'], pl: ['Zoho CRM', 'Salesforce', 'Odoo CRM'], m: 'Typically starts with a 2-week Diagnose & Design stage.' },
    { t: 'CRM Migration', img: 'servers', p: 'You\'ve outgrown your current CRM, or two systems need to become one after a merger or acquisition.', d: ['Field-by-field data mapping', 'Clean-up and de-duplication before the move', 'Migration scripts with test runs', 'Parallel run and cut-over plan'], pl: ['Salesforce → Zoho One', 'HubSpot → Zoho', 'Spreadsheets → CRM'], m: 'Our founder led PropSpace\'s move from Salesforce to Zoho One.' },
    { t: 'Process Automation', img: 'workshop', p: 'Approvals, reminders and handoffs depend on people remembering to do them.', d: ['Routing and assignment rules', 'Approval chains with audit trail', 'SLA alerts and escalation paths', 'Automated follow-up sequences'], pl: ['Zoho Flow', 'n8n', 'Salesforce Flow'], m: 'Every automation ships with logging and an error path.' },
    { t: 'Systems Integration', img: 'servers', p: 'Your CRM, ERP, website, portals and messaging tools each hold a different version of the customer.', d: ['Integration map of every system', 'Two-way sync between CRM and finance', 'Portal and WhatsApp lead capture', 'Monitoring and failure alerts'], pl: ['REST APIs', 'Webhooks', 'n8n', 'Property Finder', 'Bayut'], m: 'Data is entered once and flows to everything that needs it.' },
    { t: 'Revenue Operations', img: 'team', p: 'Leadership can\'t see the pipeline clearly, and every team defines "qualified" differently.', d: ['Sales process and stage governance', 'Customer lifecycle design', 'Forecast cadence and pipeline reviews', 'Ownership and handoff rules'], pl: ['Zoho CRM', 'Salesforce', 'Power BI'], m: 'Built from more than ten years in UAE commercial teams.' },
    { t: 'Analytics & Reporting', img: 'analytics', p: 'Reports take days to build and never match what finance sees.', d: ['Agreed KPI definitions, written down', 'Governed data model', 'Executive and team dashboards', 'Scheduled reports with data-quality checks'], pl: ['Power BI', 'Zoho Analytics'], m: 'One number per question — and everyone sees the same one.' },
    { t: 'Digital Transformation', img: 'sme', p: 'Several departments need to change how they work at the same time, without stopping the business.', d: ['Current-state operating map', 'Target operating model', 'Phased roadmap with governance', 'Executive steering reports'], pl: ['Zoho One', 'Odoo', 'Custom'], m: 'Delivered in stages, each with its own sign-off.' },
    { t: 'Managed Operations', img: 'monitor', p: 'The system went live, but no one owns keeping it healthy as the business changes.', d: ['Administration and user support', 'Monthly system health review', 'Improvement backlog and releases', 'Quarterly roadmap with leadership'], pl: ['Any platform we build'], m: 'A monthly retainer with a clear support process.' }
  ];
  const tabs = $('#solTabs'), panel = $('#solPanel');
  SOL.forEach((s, i) => {
    const b = document.createElement('button');
    b.className = 'etab'; b.setAttribute('role', 'tab'); b.id = 'tab' + i;
    b.innerHTML = `<span>0${i + 1}</span>${s.t}`;
    b.addEventListener('click', () => showSol(i));
    tabs.appendChild(b);
  });
  function showSol(i) {
    const s = SOL[i];
    $$('.etab', tabs).forEach((b, k) => { b.classList.toggle('is-on', k === i); b.setAttribute('aria-selected', k === i); });
    panel.setAttribute('aria-labelledby', 'tab' + i);
    panel.innerHTML = `
      <div class="ep__img"><img src="assets/img/${s.img}.webp" alt=""><h3>${s.t}</h3></div>
      <div class="ep__body">
        <div><h4>The situation</h4><p>${s.p}</p><h4>What we deliver</h4><ul class="ep__list">${s.d.map(x => `<li>${x}</li>`).join('')}</ul></div>
        <div><h4>Platforms</h4><div class="ep__plats">${s.pl.map(x => `<span>${x}</span>`).join('')}</div>
        <p class="ep__meta"><b>Good to know:</b> ${s.m}</p>
        <a href="#contact" class="btn btn--fire btn--sm" style="margin-top:20px">Discuss ${s.t.toLowerCase()}</a></div>
      </div>`;
  }
  showSol(0);
  tabs.addEventListener('keydown', e => {
    const cur = $$('.etab', tabs).findIndex(b => b.classList.contains('is-on'));
    if (e.key === 'ArrowDown' || e.key === 'ArrowRight') { e.preventDefault(); showSol((cur + 1) % 8); $$('.etab', tabs)[(cur + 1) % 8].focus(); }
    if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') { e.preventDefault(); showSol((cur + 7) % 8); $$('.etab', tabs)[(cur + 7) % 8].focus(); }
  });

  /* ---------- self-assessment gauge ---------- */
  const form = $('#assessForm'), gVal = $('#gVal'), gNum = $('#gNum'), gTitle = $('#gTitle'), gText = $('#gText'), gCta = $('#gCta');
  const LEN = gVal.getTotalLength(); gVal.style.strokeDasharray = LEN;
  let shown = 100;
  function score() {
    const lost = $$('input:checked', form).reduce((a, c) => a + +c.value, 0);
    const n = $$('input:checked', form).length;
    const s = Math.max(0, 100 - lost);
    gVal.style.strokeDashoffset = LEN * (1 - s / 100);
    const from = shown, t0 = performance.now();
    const step = now => { const k = Math.min(1, (now - t0) / 700); gNum.textContent = Math.round(from + (s - from) * k); if (k < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step); shown = s;
    if (n === 0) { gTitle.textContent = 'Looking healthy'; gText.textContent = 'Tick what applies on the left to see where friction is building up.'; gCta.textContent = 'Book a discovery call'; }
    else if (s >= 70) { gTitle.textContent = 'Early friction'; gText.textContent = 'A focused Implementation Project usually fixes this — one system, one scope, done properly.'; gCta.textContent = 'Scope a project'; }
    else if (s >= 40) { gTitle.textContent = 'Friction is costing you'; gText.textContent = 'Fix the core, then keep it healthy. Most teams here pair a project with Managed Operations.'; gCta.textContent = 'Talk about a retainer'; }
    else { gTitle.textContent = 'Time for a rebuild'; gText.textContent = 'Several teams and systems are affected. An End-to-End Transformation, delivered in stages, is the safer route.'; gCta.textContent = 'Plan a programme'; }
  }
  form.addEventListener('change', score);

  /* ---------- mobile nav ---------- */
  const burger = $('#burger');
  burger.addEventListener('click', () => { const o = nav.classList.toggle('is-open'); burger.setAttribute('aria-expanded', o); });
  $$('#sheet a').forEach(a => a.addEventListener('click', () => { nav.classList.remove('is-open'); burger.setAttribute('aria-expanded', false); }));

  /* ---------- FAQ: one open at a time ---------- */
  const qas = $$('.qa');
  qas.forEach(d => d.addEventListener('toggle', () => { if (d.open) qas.forEach(o => o !== d && (o.open = false)); }));

  /* ---------- lead form ----------
     Set FORM_ENDPOINT (Formspree, Getform or your own API) to receive requests. */
  const FORM_ENDPOINT = '';
  const lf = $('#leadForm'), msg = $('#formMsg');
  lf.addEventListener('submit', async e => {
    e.preventDefault();
    let ok = true;
    $$('[required]', lf).forEach(i => {
      const bad = !i.value.trim() || (i.type === 'email' && !/^\S+@\S+\.\S+$/.test(i.value));
      i.parentElement.classList.toggle('is-err', bad); if (bad) ok = false;
    });
    if (!ok) { msg.className = 'form__msg err'; msg.textContent = 'Add your name, company and a valid work email to continue.'; return; }
    if (!FORM_ENDPOINT) { msg.className = 'form__msg err'; msg.textContent = 'This form isn\'t connected yet — add a form endpoint in assets/js/main.js.'; return; }
    msg.className = 'form__msg'; msg.textContent = 'Sending…';
    try {
      const r = await fetch(FORM_ENDPOINT, { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(lf) });
      if (!r.ok) throw 0;
      lf.reset(); msg.className = 'form__msg ok'; msg.textContent = 'Request sent. We\'ll reply by email to book your call.';
    } catch { msg.className = 'form__msg err'; msg.textContent = 'The request didn\'t go through. Check your connection and try again.'; }
  });
})();
