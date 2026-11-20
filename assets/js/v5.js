/* OPSMO v5 — boot seams, hero split, Zoho chapter, stories, explorer, videos, conversion helpers */
(() => {
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const desk = () => matchMedia('(hover:hover) and (min-width:981px)').matches;

  /* hero word split */
  $$('[data-split]').forEach(h => {
    let i = 0;
    const walk = n => [...n.childNodes].forEach(ch => {
      if (ch.nodeType === 3) {
        const frag = document.createDocumentFragment();
        ch.textContent.split(/(\s+)/).forEach(w => {
          if (!w) return;
          if (/^\s+$/.test(w)) { frag.appendChild(document.createTextNode(w)); return; }
          const s = document.createElement('span'); s.className = 'w'; s.textContent = w;
          s.style.transitionDelay = (i++ * 0.045) + 's'; frag.appendChild(s);
        });
        ch.replaceWith(frag);
      } else walk(ch);
    });
    walk(h);
  });

  /* section seams + boot reveal (the new transition) */
  const secs = $$('main > section').slice(1);
  secs.forEach(s => { const d = document.createElement('div'); d.className = 'seam'; d.setAttribute('aria-hidden', 'true'); d.innerHTML = '<i></i><b></b>'; s.prepend(d); });
  const boots = $$('.storybox, .bento, .vids, .port, .leaks, .explorer, .paths, .zcards, .ws, .grid, .cards, .tiers');
  boots.forEach(b => b.classList.add('boot'));
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    e.target.classList.add(e.target.classList.contains('seam') ? 'is-on' : 'is-in');
    io.unobserve(e.target);
  }), { rootMargin: '0px 0px -12% 0px', threshold: .05 });
  $$('.seam').forEach(s => io.observe(s)); boots.forEach(b => io.observe(b));

  /* numbers: every figure counts up when it scrolls in (prefix/suffix kept, ranges and decimals too) */
  const NUM_SEL = '.leak b, .sty__rev, .sectors b, .zchap__facts b, .bt__stats b, .port__list li>b, .port__n, .bt--stat>b, .num-big, .tier__price, .price, .stat b';
  const fmt = (v, dec, comma) => { const s = v.toFixed(dec); return comma ? (+s).toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec }) : s; };
  const prep = el => {
    if (el.dataset.numed) return; el.dataset.numed = 1;
    $$('[data-count]', el).forEach(n => n.removeAttribute('data-count'));
    const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), nodes = [];
    while (tw.nextNode()) nodes.push(tw.currentNode);
    nodes.forEach(t => {
      if (!/\d/.test(t.textContent)) return;
      const frag = document.createDocumentFragment();
      t.textContent.split(/(\d[\d,]*(?:\.\d+)?)/).forEach(part => {
        if (!/^\d/.test(part)) { if (part) frag.appendChild(document.createTextNode(part)); return; }
        const comma = part.includes(','), raw = part.replace(/,/g, ''), dec = (raw.split('.')[1] || '').length, to = parseFloat(raw);
        const sp = document.createElement('span'); sp.className = 'cnt'; sp.textContent = part;
        const yr = to >= 1900 && to <= 2100 && !dec && !comma;
        sp.dataset.to = to; sp.dataset.dec = dec; sp.dataset.comma = (comma || (to >= 10000 && !yr)) ? 1 : '';
        sp.dataset.from = (to >= 1900 && to <= 2100 && !dec) ? to - 17 : 0;   // years tick up, not from zero
        frag.appendChild(sp);
      });
      t.replaceWith(frag);
    });
  };
  const run = el => {
    el.classList.add('num-in');
    $$('.cnt', el).forEach((sp, k) => {
      const to = +sp.dataset.to, from = +sp.dataset.from, dec = +sp.dataset.dec, comma = !!sp.dataset.comma;
      if (reduce) { sp.textContent = fmt(to, dec, comma); return; }
      const dur = 1400 + Math.min(900, Math.log10(to + 1) * 220), t0 = performance.now() + k * 120;
      sp.textContent = fmt(from, dec, comma);
      const step = now => { const p = Math.min(1, Math.max(0, (now - t0) / dur)), e = 1 - Math.pow(1 - p, 4);
        sp.textContent = fmt(from + (to - from) * e, p < 1 ? (to < 10 && dec === 0 ? 0 : dec) : dec, comma);
        if (p < 1) requestAnimationFrame(step); else { sp.textContent = fmt(to, dec, comma); el.classList.add('num-done'); } };
      requestAnimationFrame(step);
    });
  };
  const nio = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { nio.unobserve(e.target); run(e.target); } }), { threshold: .5 });
  const lock = el => $$('.cnt', el).forEach(sp => { sp.style.minWidth = sp.getBoundingClientRect().width + 'px'; });
  $$(NUM_SEL).forEach(el => { prep(el); if ($('.cnt', el)) { el.classList.add('num'); lock(el); nio.observe(el); } });
  $$('[data-count]').forEach(n => { const p = n.parentElement; prep(p); p.classList.add('num'); lock(p); nio.observe(p); });

  /* cursor glow + bento spotlight + portrait tilt */
  const glow = $('#glow'), portrait = $('#portrait');
  addEventListener('pointermove', e => {
    if (!desk()) return;
    if (glow) glow.style.transform = `translate(${e.clientX - 260}px, ${e.clientY - 260}px)`;
    if (portrait && !reduce) {
      const r = portrait.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      if (Math.abs(x) < 1.4 && Math.abs(y) < 1.4) portrait.style.transform = `perspective(1200px) rotateY(${-6 + x * 8}deg) rotateX(${2 - y * 6}deg)`;
    }
  }, { passive: true });
  $$('.bt').forEach(b => b.addEventListener('pointermove', e => { const r = b.getBoundingClientRect(); b.style.setProperty('--mx', (e.clientX - r.left) + 'px'); b.style.setProperty('--my', (e.clientY - r.top) + 'px'); }));

  /* scroll-linked: Zoho chapter, steps line, horizon, CTA helpers */
  const z = $('#zoho'), zr = $('#zRail'), facts = z ? $$('.zchap__facts li', z) : [];
  const s4 = $('#steps4'), s4l = $('#s4line'), hor = $('.horizon'), fab = $('.wa-fab'), mbar = $('.mbar');
  let ticking = false;
  const frame = () => {
    ticking = false;
    const vh = innerHeight;
    if (z && matchMedia('(min-width:981px)').matches) {
      const r = z.getBoundingClientRect(), p = Math.min(1, Math.max(0, -r.top / (r.height - vh)));
      z.style.setProperty('--zp', Math.min(1, p * 3)); z.style.setProperty('--zs', 1.25 - p * .2); z.style.setProperty('--zo', .22 + p * .3);
      z.classList.toggle('is-lit', p > .12);
      facts.forEach((f, i) => f.classList.toggle('is-on', p > .25 + i * .14));
      if (zr) zr.style.transform = `scaleX(${p})`;
    } else if (z) { z.classList.add('is-lit'); }
    if (s4 && s4l) {
      const r = s4.getBoundingClientRect(), p = Math.min(1, Math.max(0, (vh * .85 - r.top) / (r.height + vh * .4)));
      s4l.style.transform = `scaleX(${p})`;
      $$('li', s4).forEach((li, i) => li.classList.toggle('is-on', p > (i + .5) / 4));
    }
    if (hor) { const r = hor.parentElement.getBoundingClientRect(); hor.parentElement.style.setProperty('--hp', Math.min(1, Math.max(0, 1 - r.top / vh))); }
    const y = scrollY > vh * .7;
    mbar && mbar.classList.toggle('is-on', y);
  };
  const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(frame); } };
  addEventListener('scroll', onScroll, { passive: true }); addEventListener('resize', onScroll); frame();

  /* tabs helper (stories + explorer) */
  const tabs = (list, tabSel, panelOf) => {
    const ts = $$(tabSel, list);
    const go = i => ts.forEach((t, j) => {
      const on = i === j, p = panelOf(t);
      t.classList.toggle('is-on', on); t.setAttribute('aria-selected', on); t.tabIndex = on ? 0 : -1;
      if (p) { p.hidden = !on; p.classList.toggle('is-on', on); }
    });
    ts.forEach((t, i) => t.addEventListener('click', () => go(i)));
    list.addEventListener('keydown', e => {
      const i = ts.indexOf(document.activeElement); if (i < 0) return;
      const k = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key]; if (!k) return;
      e.preventDefault(); const n = (i + k + ts.length) % ts.length; go(n); ts[n].focus();
    });
    go(0);
  };
  $$('.storybox__tabs').forEach(l => tabs(l, '.stab', t => document.getElementById(t.getAttribute('aria-controls'))));
  $$('.explorer:not([data-sol]) .explorer__tabs').forEach(l => tabs(l, '.etab', t => document.getElementById(t.getAttribute('aria-controls'))));

  /* native video cards: muted preview on hover, click plays with sound */
  $$('.vid__frame').forEach(fr => {
    const v = $('video', fr), btn = $('.vid__play', fr), snd = $('.vid__sound', fr); if (!v) return;
    let started = false;
    const start = () => { started = true; fr.classList.add('is-playing'); v.muted = false; v.controls = true; v.currentTime = fr.classList.contains('is-preview') ? 0 : v.currentTime; fr.classList.remove('is-preview'); v.play(); $$('.vid__v').forEach(o => { if (o !== v) o.pause(); }); };
    btn.addEventListener('click', start);
    if (desk() && !reduce) {
      fr.addEventListener('mouseenter', () => { if (started) return; v.muted = true; fr.classList.add('is-preview'); v.play().catch(() => {}); });
      fr.addEventListener('mouseleave', () => { if (started) return; v.pause(); fr.classList.remove('is-preview'); });
    }
    v.addEventListener('ended', () => { started = false; fr.classList.remove('is-playing'); v.controls = false; v.load(); });
  });
  /* (legacy) LinkedIn embeds */
  $$('.vid__play').forEach(b => b.addEventListener('click', () => {
    const f = document.createElement('iframe');
    f.src = b.dataset.embed; f.title = b.getAttribute('aria-label').replace('Play video: ', '');
    f.allow = 'autoplay; encrypted-media; picture-in-picture'; f.allowFullscreen = true; f.loading = 'lazy';
    b.replaceWith(f);
  }));
})();
