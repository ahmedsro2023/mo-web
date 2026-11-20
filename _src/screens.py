# Light, animated "app screens" for each solution (illustrations, sample data). CSS drives the motion.
def _bar(title):
    return f'<div class="scr__bar"><span class="scr__dots"><i></i><i></i><i></i></span><span class="scr__t">{title}</span><span class="scr__live">Live</span></div>'

def _sel():
    rows = [("Zoho One", 92, "Best fit"), ("Salesforce", 74, ""), ("HubSpot", 68, ""), ("Odoo", 61, "")]
    r = "".join(f'<div class="ss__r{" is-win" if w else ""}" style="--i:{i};--v:{v}%"><b>{n}</b><span class="ss__bar"><i></i></span><em>{v}</em>{f"<s>{w}</s>" if w else ""}</div>' for i, (n, v, w) in enumerate(rows))
    crit = "".join(f'<span style="--i:{i}">{x}</span>' for i, x in enumerate(["Fit to process", "Total cost", "Integrations", "Ease of use", "Arabic support"]))
    return _bar("Vendor scorecard") + f'<div class="scr__body"><div class="ss__crit">{crit}</div>{r}<p class="scr__foot">Example scorecard · real scores depend on your needs</p></div>'

def _crm():
    cols = [("Lead", ["Al Noor Trading", "Gulf Tech"]), ("Qualified", ["Desert Rose"]), ("Proposal", ["Marina Group"]), ("Won", [])]
    c = "".join(f'<div class="pp__c"><p>{n}<b>{len(x)}</b></p>' + "".join(f'<span class="pp__k">{y}</span>' for y in x) + '</div>' for n, x in cols)
    return _bar("Sales pipeline") + f'<div class="scr__body"><div class="pp">{c}<span class="pp__fly">Marina Group<em>AED 240K</em></span></div><div class="scr__kpi"><span>Pipeline <b>AED 1.8M</b></span><span>Win rate <b>34%</b></span></div></div>'

def _mig():
    rows = [("Contacts", "12,480"), ("Companies", "3,210"), ("Deals", "1,946"), ("Activities", "48,300"), ("Files", "6,120")]
    r = "".join(f'<div class="mg__r" style="--i:{i}"><b>{n}</b><span class="mg__bar"><i></i></span><em>{v}</em><s>✓</s></div>' for i, (n, v) in enumerate(rows))
    return _bar("Data migration") + f'<div class="scr__body"><div class="mg__h"><span class="mg__old">Old CRM</span><span class="mg__arrow"></span><span class="mg__new">Zoho CRM</span></div>{r}<p class="scr__foot">Every record checked against the old system</p></div>'

def _auto():
    nodes = [("New lead", "trigger"), ("Duplicate?", "check"), ("Assign agent", "action"), ("Notify on mobile", "action"), ("Follow-up in 24h", "task")]
    n = "".join(f'<div class="af__n af__n--{t}" style="--i:{i}"><span>{x}</span></div>' for i, (x, t) in enumerate(nodes))
    return _bar("Workflow · Lead routing") + f'<div class="scr__body"><div class="af">{n}<i class="af__dot"></i></div><div class="scr__kpi"><span>Runs today <b>1,284</b></span><span>Errors <b class="ok">0</b></span></div></div>'

def _int():
    sat = ["Website", "Zoho Books", "WhatsApp", "ERP", "Payments", "Portals"]
    s = "".join(f'<span class="ig__s" style="--i:{i}">{x}</span>' for i, x in enumerate(sat))
    return _bar("Integration map") + f'<div class="scr__body scr__body--center"><div class="ig"><span class="ig__hub">CRM</span>{s}<svg class="ig__l" viewBox="-100 -100 200 200">' + "".join(f'<line x1="0" y1="0" x2="{x}" y2="{y}" style="--i:{i}"/>' for i, (x, y) in enumerate([(0, -78), (68, -39), (68, 39), (0, 78), (-68, 39), (-68, -39)])) + '</svg></div><p class="scr__foot">6 connections · all syncing · last error 0</p></div>'

def _rev():
    st = [("Leads", 100, "2,400"), ("Qualified", 62, "1,488"), ("Proposal", 38, "912"), ("Won", 18, "432")]
    f = "".join(f'<div class="fn__r" style="--i:{i};--w:{w}%"><span class="fn__b"><b>{n}</b><em>{v}</em></span></div>' for i, (n, w, v) in enumerate(st))
    return _bar("Revenue funnel · this quarter") + f'<div class="scr__body"><div class="fn">{f}</div><div class="scr__kpi"><span>Forecast <b>AED 4.2M</b></span><span>Accuracy <b class="ok">94%</b></span></div></div>'

def _bi():
    bars = [42, 55, 48, 66, 72, 61, 80, 88]
    b = "".join(f'<i style="--j:{i};--h:{h}%"></i>' for i, h in enumerate(bars))
    return _bar("Leadership dashboard") + f'<div class="scr__body"><div class="bi__k"><span>Revenue <b>AED 3.1M</b><em class="up">+18%</em></span><span>Margin <b>27%</b><em class="up">+3pt</em></span><span>Cash <b>AED 940K</b><em>on target</em></span></div><div class="bi__c">{b}<svg viewBox="0 0 100 40" preserveAspectRatio="none"><path d="M0 30 L14 26 L28 28 L42 18 L57 15 L71 19 L85 9 L100 5"/></svg></div></div>'

def _dt():
    ph = [("Phase 1 · CRM & sales", 1, 4), ("Phase 2 · Finance & ops", 4, 8), ("Phase 3 · Reporting & BI", 8, 11), ("Phase 4 · Optimise", 11, 13)]
    p = "".join(f'<div class="rm__r" style="--i:{i};--s:{a};--e:{b}"><b>{n}</b><span class="rm__t"><i></i></span></div>' for i, (n, a, b) in enumerate(ph))
    q = "".join(f"<span>{x}</span>" for x in ["Q1", "Q2", "Q3", "Q4"])
    return _bar("Transformation roadmap") + f'<div class="scr__body"><div class="rm__q">{q}</div>{p}<p class="scr__foot">4 departments · 7 apps · 1 plan</p></div>'

def _ops():
    t = [("Add 3 new users", "Done"), ("Fix quote approval rule", "Done"), ("New dashboard for sales", "In progress"), ("Sync error: Books", "Resolved")]
    r = "".join(f'<div class="tk__r" style="--i:{i}"><b>{x}</b><span class="tk__s" data-s="{s}">{s}</span></div>' for i, (x, s) in enumerate(t))
    return _bar("Monthly support") + f'<div class="scr__body">{r}<div class="scr__kpi"><span>Avg. response <b>1h 12m</b></span><span>System health <b class="ok">98%</b></span></div></div>'

def _desk():
    t = [("Order not delivered", "High", "Sara", "0:45"), ("Change booking date", "Normal", "Omar", "3:10"), ("Invoice copy", "Low", "Lina", "7:30"), ("Refund request", "High", "Karim", "1:05")]
    r = "".join(f'<div class="dk__r" style="--i:{i}"><b>{x}</b><span class="dk__p dk__p--{p.lower()}">{p}</span><span class="dk__a">{a[0]}</span><em>{s}</em></div>' for i, (x, p, a, s) in enumerate(t))
    return _bar("Support inbox · Zoho Desk") + f'<div class="scr__body"><div class="dk__h"><span>Ticket</span><span>Priority</span><span>Owner</span><span>Reply due</span></div>{r}<div class="scr__kpi"><span>On time <b class="ok">96%</b></span><span>Open <b>14</b></span></div></div>'

SCREENS = {"software-selection": _sel, "crm-implementation": _crm, "crm-migration": _mig, "business-process-automation": _auto,
           "api-systems-integration": _int, "commercial-revenue-operations": _rev, "business-intelligence-reporting": _bi,
           "digital-transformation": _dt, "managed-crm-operations": _ops, "zoho-desk-implementation": _desk}
def screen(slug):
    return f'<div class="scr scr--{slug}" aria-hidden="true">{SCREENS[slug]()}</div>'
