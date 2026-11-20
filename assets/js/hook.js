/* OPSMO hook: a friendly message from Mohamed that appears once per visit */
(() => {
  const hook = document.getElementById('hook'), fab = document.getElementById('hookFab'); if (!hook || !fab) return;
  const path = location.pathname;
  if (/\/contact\/?$/.test(path)) { fab.style.display = 'none'; return; }      // already on the contact page
  const MSG = [
    [/real-estate/, "Hey 👋 I'm Mohamed. I spent years inside Property Finder.", "Losing portal leads? Book a <b>free 30-minute call</b> and I'll show you where they slip away."],
    [/platforms\/zoho|zoho/, "Hey 👋 I'm Mohamed, Zoho's first hire in Egypt.", "Thinking about Zoho One? Let's spend <b>30 free minutes</b> on which apps you really need."],
    [/approach|packages/, "Hey 👋 I'm Mohamed.", "Want a realistic price range? One <b>free call</b> is usually enough to give you one."],
    [/success-stories/, "Hey 👋 I'm Mohamed.", "Want results like these? Tell me how your team works today. <b>The first call is free.</b>"],
    [/solutions/, "Hey 👋 I'm Mohamed, ex-Zoho.", "Not sure which service fits? Book a <b>free 30-minute call</b> and I'll tell you honestly."],
    [/./, "Hey 👋 I'm Mohamed, ex-Zoho.", "Want a <b>free 30-minute call</b>? I'll tell you what to fix first, and what to leave alone."]];
  const [m1, m2] = MSG.find(([re]) => re.test(path)).slice(1);
  const KEY = 'opsmo-hook', store = { get() { try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { return {}; } }, set(v) { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) {} } };
  const st = store.get(), snoozed = st.until && Date.now() < st.until;
  let open = false, played = false, timer;
  const typing = hook.querySelector('.hook__typing'), e1 = document.getElementById('hookM1'), e2 = document.getElementById('hookM2');
  const play = () => { if (played) return; played = true; e1.innerHTML = m1; e2.innerHTML = m2;
    typing.classList.add('is-on');
    setTimeout(() => { typing.classList.remove('is-on'); e1.classList.add('is-on'); typing.classList.add('is-on', 'is-2'); }, 1100);
    setTimeout(() => { typing.classList.remove('is-on'); e2.classList.add('is-on'); hook.classList.add('is-cta'); }, 2500); };
  const show = () => { if (open) return; open = true; hook.classList.add('is-open'); hook.setAttribute('aria-hidden', 'false'); fab.setAttribute('aria-expanded', 'true'); fab.classList.add('is-read'); play(); };
  const hide = (snooze) => { open = false; hook.classList.remove('is-open'); hook.setAttribute('aria-hidden', 'true'); fab.setAttribute('aria-expanded', 'false');
    if (snooze) store.set({ until: Date.now() + 3 * 864e5 }); };
  fab.addEventListener('click', () => open ? hide(false) : show());
  hook.querySelector('.hook__x').addEventListener('click', () => hide(true));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && open) hide(true); });
  hook.querySelectorAll('[data-hook]').forEach(a => a.addEventListener('click', () => store.set({ until: Date.now() + 14 * 864e5 })));
  // show the launcher shortly after load
  setTimeout(() => fab.classList.add('is-in'), 1200);
  if (snoozed) return;
  // auto-open: after 18s, or after reading half the page, or when the mouse heads for the tab bar
  timer = setTimeout(show, 18000);
  const onScroll = () => { const p = scrollY / Math.max(1, document.documentElement.scrollHeight - innerHeight); if (p > .45) { show(); removeEventListener('scroll', onScroll); } };
  addEventListener('scroll', onScroll, { passive: true });
  document.addEventListener('mouseout', e => { if (!e.relatedTarget && e.clientY < 8) show(); });
})();
