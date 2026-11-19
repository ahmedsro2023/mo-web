/* OPSMO v4 — motion */
(() => {
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const root = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const desk = () => innerWidth > 980;

  /* hero: split words */
  const h = $('[data-split]');
  if (h) {
    let i = 0;
    const wrap = node => {
      [...node.childNodes].forEach(n => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(p => {
            if (!p) return;
            if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(p)); return; }
            const s = document.createElement('span'); s.className = 'w'; s.textContent = p;
            s.style.transitionDelay = (0.12 + i++ * 0.045) + 's'; frag.appendChild(s);
          });
          n.replaceWith(frag);
        } else wrap(n);
      });
    };
    wrap(h);
  }
  requestAnimationFrame(() => setTimeout(() => root.classList.add('is-ready'), 60));

  /* ribbon renderer */
  const PAL = {
    fire: ['#FF3D17', '#FF6A10', '#FFA126', '#FFE2B8'],
    zoho: ['#E42527', '#089949', '#226DB4', '#F9B21D']
  };
  let scrollPhase = 0;
  function ribbon(cv) {
    const ctx = cv.getContext('2d'), pal = PAL[cv.dataset.ribbon] || PAL.fire;
    let w, hh, dpr, vis = false, t0 = performance.now();
    const N = innerWidth < 700 ? 34 : 56;
    const size = () => { dpr = Math.min(devicePixelRatio || 1, 2); w = cv.clientWidth; hh = cv.clientHeight; cv.width = w * dpr; cv.height = hh * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); };
    const draw = now => {
      const t = (now - t0) / 1000 * 0.6 + scrollPhase;
      ctx.clearRect(0, 0, w, hh);
      ctx.globalCompositeOperation = 'lighter';
      for (let i = 0; i < N; i++) {
        const s = (i / (N - 1)) * 2 - 1;            // -1..1 across the ribbon
        const edge = Math.abs(s);
        const col = edge > .78 ? 'rgba(200,200,210,' : null;
        const pi = Math.min(pal.length - 1, Math.floor(((s + 1) / 2) * pal.length));
        const g = ctx.createLinearGradient(0, 0, w, 0);
        const a = (edge > .78 ? .10 : .16) * (1 - edge * .35);
        const c = col || hexA(pal[pi], 1);
        const cc = col ? col + a + ')' : hexA(pal[pi], a);
        g.addColorStop(0, col ? col + '0)' : hexA(pal[pi], 0));
        g.addColorStop(.25, cc); g.addColorStop(.55, col ? col + (a * 1.6) + ')' : hexA(pal[(pi + 1) % pal.length], a * 1.5));
        g.addColorStop(.85, cc); g.addColorStop(1, col ? col + '0)' : hexA(pal[pi], 0));
        ctx.strokeStyle = g; ctx.lineWidth = edge > .95 ? 1.2 : 1;
        ctx.beginPath();
        for (let x = -20; x <= w + 20; x += 10) {
          const c0 = hh / 2 + hh * .16 * Math.sin(x * .0042 + t * .5) + hh * .07 * Math.sin(x * .011 - t * .8);
          const wd = hh * .24 * Math.sin(x * .0031 + t * .35 + 1.2) * (.6 + .4 * Math.sin(x * .0017 - t * .2));
          const y = c0 + wd * s;
          x === -20 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }
        ctx.stroke();
      }
      ctx.globalCompositeOperation = 'source-over';
      if (vis && !reduce) requestAnimationFrame(draw);
    };
    size(); addEventListener('resize', size);
    new IntersectionObserver(([e]) => { const was = vis; vis = e.isIntersecting; if (vis && !was) requestAnimationFrame(draw); }, { rootMargin: '100px' }).observe(cv);
    if (reduce) draw(performance.now());
  }
  function hexA(hx, a) { const n = parseInt(hx.slice(1), 16); return `rgba(${n >> 16 & 255},${n >> 8 & 255},${n & 255},${a})`; }
  $$('canvas[data-ribbon]').forEach(ribbon);

  /* reveal */
  const targets = ['.head', '.tile', '.pains li', '.leak', '.ctab', '.port__big', '.port__list', '.sectors div', '.steps li', '.ws', '.quote', '.fcopy>p', '.fcopy__cta', '.press', '.fphoto', '.zc', '.cta__card', '.note', '.callout'];
  $$(targets.join(',')).forEach(el => {
    el.classList.add('rv');
    const sib = [...el.parentElement.children].filter(c => c.matches(targets.join(',')));
    el.style.setProperty('--d', Math.min(sib.indexOf(el), 6) * .07 + 's');
  });
  const ro = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-in'); ro.unobserve(e.target); } }), { rootMargin: '0px 0px -10% 0px', threshold: .05 });
  $$('.rv').forEach(el => ro.observe(el));

  /* counters */
  const count = el => {
    const end = +el.dataset.count;
    if (reduce) { el.textContent = end.toLocaleString('en-US'); return; }
    const t0 = performance.now(), d = 1600;
    const step = n => { const k = Math.min(1, (n - t0) / d), e = 1 - Math.pow(1 - k, 4); el.textContent = Math.round(end * e).toLocaleString('en-US'); if (k < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  const co = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { count(e.target); co.unobserve(e.target); } }), { threshold: .6 });
  $$('[data-count]').forEach(el => co.observe(el));

  /* tile spotlight + cursor glow */
  const glow = $('#glow');
  addEventListener('pointermove', e => {
    if (glow) glow.style.transform = `translate(${e.clientX - 260}px,${e.clientY - 260}px)`;
  }, { passive: true });
  $$('.tile').forEach(t => t.addEventListener('pointermove', e => {
    const r = t.getBoundingClientRect(); t.style.setProperty('--mx', (e.clientX - r.left) + 'px'); t.style.setProperty('--my', (e.clientY - r.top) + 'px');
  }));

  /* portrait tilt */
  const pt = $('#portrait');
  if (pt && !reduce) {
    pt.addEventListener('pointermove', e => {
      const r = pt.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      pt.style.transform = `perspective(1200px) rotateY(${x * 10 - 4}deg) rotateX(${-y * 8}deg)`;
    });
    pt.addEventListener('pointerleave', () => pt.style.transform = '');
  }

  /* scroll engine */
  const nav = $('#nav'), bar = $('#bar'), zoho = $('#zoho'), zRail = $('#zohoRail'), facts = $$('.zoho__facts li');
  const impact = $('.impact'), steps = $$('#steps li'), sLine = $('#stepsLine');
  const links = $$('.nav__pill a[href^="#"]');
  let lastY = scrollY, tick = false;
  function frame() {
    const y = scrollY, H = root.scrollHeight - innerHeight;
    bar.style.transform = `scaleX(${H > 0 ? y / H : 0})`;
    scrollPhase = y * .0016;
    if (!nav.classList.contains('is-open')) {
      if (y > 300 && y > lastY + 6) nav.classList.add('is-hidden');
      else if (y < lastY - 6 || y < 300) nav.classList.remove('is-hidden');
    }
    lastY = y;
    if (zoho && desk()) {
      const r = zoho.getBoundingClientRect(), tot = zoho.offsetHeight - innerHeight;
      const p = Math.min(1, Math.max(0, -r.top / tot));
      zoho.style.setProperty('--zp', Math.min(1, p * 3).toFixed(3));
      zoho.style.setProperty('--zs', (1.25 - p * .2).toFixed(3));
      zoho.style.setProperty('--zo', (.28 + p * .32).toFixed(3));
      zoho.classList.toggle('is-lit', p > .08);
      facts.forEach((f, i) => f.classList.toggle('is-on', p > .18 + i * .17));
      zRail.style.transform = `scaleX(${p})`;
    } else if (zoho) { zoho.classList.add('is-lit'); facts.forEach(f => f.classList.add('is-on')); }
    if (impact) {
      const r = impact.getBoundingClientRect();
      impact.style.setProperty('--hp', Math.min(1, Math.max(0, 1 - r.top / innerHeight)).toFixed(3));
    }
    if (steps.length) {
      const r = $('#steps').getBoundingClientRect();
      const p = Math.min(1, Math.max(0, (innerHeight * .75 - r.top) / (r.height + innerHeight * .3)));
      sLine.style.transform = `scaleX(${p})`;
      steps.forEach((s, i) => s.classList.toggle('is-on', p > i / steps.length + .05));
    }
    tick = false;
  }
  addEventListener('scroll', () => { if (!tick) { tick = true; requestAnimationFrame(frame); } }, { passive: true });
  addEventListener('resize', frame); frame();

  /* active nav */
  const so = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) links.forEach(a => a.classList.toggle('is-on', a.getAttribute('href') === '#' + e.target.id));
  }), { rootMargin: '-45% 0px -50% 0px' });
  ['zoho', 'career', 'stories', 'method', 'founder'].forEach(id => { const s = document.getElementById(id); if (s) so.observe(s); });

  /* mobile nav */
  const burger = $('#burger');
  burger.addEventListener('click', () => { const o = nav.classList.toggle('is-open'); burger.setAttribute('aria-expanded', o); });
  $$('#sheet a').forEach(a => a.addEventListener('click', () => { nav.classList.remove('is-open'); burger.setAttribute('aria-expanded', false); }));

  /* success stories */
  const CASES = [
    { logo: 'assets/img/logos/propspace-w.png', k: 'Reduced complexity. Increased visibility. Scaled revenue.', rev: '650K+ USD', sub: 'Annual revenue',
      from: ['Salesforce', 'Tableau', 'NetSuite', 'Zendesk', 'Workplace', 'Slack', 'Zapier', 'DocuSign'],
      ch: 'This setup was impractical for scaling and growth due to the high costs and complexities associated with multiple subscriptions and the need for extensive customizations across different systems.',
      so: 'Built a Unified Revenue Operating System.',
      goal: 'Streamline the entire business sales, online subscription, support, and finance enabling seamless online client communication and integrating all offline channels into a single CRM system.',
      take: ['PropSpace was able to reduce costs, simplify workflows, and improve overall business performance, achieving their goal of a unified, efficient, and scalable operating system.'] },
    { logo: 'assets/img/logos/elnaggar-w.png', k: 'Transforming Elnaggar & Partners with Zoho One', rev: '500K+ USD', sub: 'Annual revenue generated',
      from: ['Excel', 'Paper files', 'WhatsApp'],
      ch: 'Relied on Excel, paper files, and WhatsApp to manage client onboarding, due diligence, and proposal approvals — resulting in inefficiencies, poor tracking, and frequent follow-ups.',
      so: 'Deployed Zoho One with a fully automated deal lifecycle: Qualification → KYC → Due Diligence → Proposal → Engagement Letter → Proforma → Payment → Close. All actions are tracked, approved, and streamlined through custom workflows.',
      goal: 'Digitize and automate the entire client engagement process — from KYC and compliance to proposal, engagement letter, and payment — ensuring accuracy, traceability, and faster deal closures.',
      take: ['Centralized client lifecycle in one CRM', 'Cut manual errors and delays', 'Improved compliance and documentation flow', 'Accelerated time-to-close and client experience'] },
    { logo: 'assets/img/logos/r1-w.png', k: 'From Excel & WhatsApp to', rev: '4M+ AED', sub: 'Annual revenue',
      from: ['Excel', 'WhatsApp'],
      ch: 'Relied on Excel and WhatsApp to manage operations — causing delays, errors, and zero scalability. Disconnected tools created chaos and high operational costs.',
      so: 'Implemented Zoho One with a custom blueprint covering the full service cycle — diagnosis, estimates, payments, parts, repairs, QC, and delivery — all under one platform.',
      goal: 'Centralize all business functions into one streamlined system to enable control, efficiency, and scale.',
      take: ['Cut costs & manual work', 'Full operational visibility', 'Scalable, digital-first operations', '4M+ AED Annual Recurring Revenue'] },
    { logo: 'assets/img/logos/fawry.png', k: 'From fragmented operations to one scalable lending platform', rev: '2.7M+ USD', sub: 'Annual revenue',
      from: ['3CX', 'Outlook', 'Excel', 'WhatsApp', 'SurveyMonkey'],
      ch: 'Fragmented loan processing, poor data management.',
      so: 'The transition has resulted in a more cohesive, secure, and efficient operation for Fawry Microfinance, enabling them to scale and grow effectively.',
      goal: 'Streamline operations by centralizing data and processes on a single platform, ensuring ease of access and improved efficiency.',
      take: ['The unified platform has transformed their workflows, improved decision-making, and increased their ability to serve clients better.'] }
  ];
  const panel = $('#casePanel'), tabs = $$('.ctab');
  const esc = s => s.replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
  const show = i => {
    const c = CASES[i];
    tabs.forEach((t, k) => { t.classList.toggle('is-on', k === i); t.setAttribute('aria-selected', k === i); });
    panel.classList.remove('is-swap'); void panel.offsetWidth;
    panel.innerHTML = `<div class="case__top"><div><p class="mono case__k">${esc(c.k)}</p><p class="case__rev fire">${esc(c.rev)}<small>${esc(c.sub)}</small></p></div><img class="case__logo" src="${c.logo}" alt=""></div>
      <div class="flowx"><div><p class="mono" style="color:var(--ink3);margin-bottom:10px">Previous systems</p><div class="flowx__from">${c.from.map(f => `<span>${esc(f)}</span>`).join('')}</div></div><i class="flowx__arrow"></i><div class="flowx__to"><img src="assets/img/logos/zohoone-w.png" alt="Zoho One"></div></div>
      <div class="case__grid"><div><h4>Challenge</h4><p>${esc(c.ch)}</p></div><div><h4>Solution</h4><p>${esc(c.so)}</p></div><div><h4>Goal</h4><p>${esc(c.goal)}</p></div><div><h4>${i === 2 ? 'The results' : 'Key takeaways'}</h4><ul>${c.take.map(x => `<li>${esc(x)}</li>`).join('')}</ul></div></div>`;
    panel.classList.add('is-swap');
  };
  tabs.forEach((t, i) => t.addEventListener('click', () => show(i)));
  $('.cases__tabs').addEventListener('keydown', e => {
    const cur = tabs.findIndex(t => t.classList.contains('is-on'));
    if (['ArrowDown', 'ArrowRight'].includes(e.key)) { e.preventDefault(); const n = (cur + 1) % 4; show(n); tabs[n].focus(); }
    if (['ArrowUp', 'ArrowLeft'].includes(e.key)) { e.preventDefault(); const n = (cur + 3) % 4; show(n); tabs[n].focus(); }
  });
  show(0);
})();
