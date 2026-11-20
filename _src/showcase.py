# v7 dynamic showcase modules (rendered server-side, animated by assets/js/showcase.js)
from build import E, ARROW, EXT, btn, chip, sec, head, em_last, a_attrs
import json
from sectors import SECTORS, ORDER

def sector_data():
    return '<script type="application/json" class="sector-data">' + json.dumps(SECTORS, ensure_ascii=False).replace("</", "<\\/") + '</script>'
def picker(cur, label="Pick your sector"):
    chips = "".join(f'<button type="button" class="sp__chip{" is-on" if k==cur else ""}" data-sector="{k}" aria-pressed="{"true" if k==cur else "false"}">{E(SECTORS[k]["label"])}</button>' for k in ORDER)
    return f'<div class="sp" role="group" aria-label="{E(label)}"><span class="mono dim">{E(label)}</span>{chips}</div>'

def live_demo(c, sector="real-estate", pick=True):
    cols = SECTORS[sector]["stages"]
    colhtml = "".join(f'<div class="lv__col" data-col="{i}"><p class="lv__ch">{n}<b data-colcount>0</b></p><div class="lv__cards"></div></div>' for i, n in enumerate(cols))
    return sec(f'''<div class="head head--split"><div>{chip("See it working")}<h2 class="h2 rv">Every lead caught. <em>Every lead followed up.</em></h2></div>
<p class="lead rv">This is what a well-built system does all day, without anyone chasing it: leads arrive, get assigned in seconds, and move through the pipeline while managers watch the numbers live.</p></div>
{picker(sector) if pick else ""}<div class="lv rv" id="liveDemo" data-sector="{sector}" aria-label="Animated illustration of a CRM pipeline with sample data">{sector_data()}
<div class="lv__top"><span class="lv__dots"><i></i><i></i><i></i></span><span class="mono">Sales pipeline · live</span><span class="lv__badge mono"><i class="dot"></i>Sample data</span></div>
<div class="lv__grid">
<aside class="lv__feed"><p class="mono dim">Incoming leads</p><ul id="lvFeed"></ul></aside>
<div class="lv__board">{colhtml}</div>
<aside class="lv__kpis"><div><span class="mono dim">Leads today</span><b id="kLeads">0</b></div><div><span class="mono dim">Avg. first response</span><b id="kResp">—</b></div><div><span class="mono dim">Follow-ups due</span><b id="kTasks">0</b></div><div><span class="mono dim" id="kWonL">{E(SECTORS[sector]["won"])}</span><b id="kWon">0</b></div>
<div class="lv__spark"><svg viewBox="0 0 200 60" preserveAspectRatio="none"><path id="lvSpark" d="M0 60"/></svg></div></aside>
</div></div>
<p class="fine rv">Illustration with sample data. Real setups use your sources, stages and team.</p>''', "", "live")

def before_after(c, sector="real-estate", pick=True):
    d = SECTORS[sector]
    rows = [("Ahmed K.", "Website", "050 •••", "Called?", "—"), ("Sara M.", "Referral", "055 •••", "?", "Omar"),
            ("Ahmed K.", "Website", "050 •••", "DUPLICATE", "—"), ("J. Smith", "Portal", "#N/A", "Follow up", "?"), ("Fatima A.", "WhatsApp", "052 •••", "", "")]
    grid = "".join(f'<tr class="xl__r{" xl__r--dup" if r[3]=="DUPLICATE" else ""}"><td>{i+2}</td>' + "".join(f"<td>{E(x)}</td>" for x in r) + "</tr>" for i, r in enumerate(rows))
    after = "".join(f'<li><i></i><span class="mono">{E(t)}</span><b>{E(h)}</b></li>' for t, h, p in d["after"]["steps"])
    return sec(f'''<div class="head head--center">{chip("Before and after")}<h2 class="h2 rv">One request. Two teams. <em>Watch the race.</em></h2>
<p class="lead rv">The same request arrives at two companies at the same moment. One runs on spreadsheets and WhatsApp. The other runs on a system we built.</p></div>
{picker(sector) if pick else ""}
<div class="race rv" id="race" data-sector="{sector}">{sector_data()}
<div class="race__dual" aria-hidden="true"><span class="race__dl">Today <b id="dualL">0:00</b></span><span class="race__dr">OPSMO <b id="dualR">0:00</b></span></div>
<div class="race__side race__side--old">
<div class="race__top"><span class="race__tag">Today</span><span class="mono">Excel + WhatsApp</span><span class="race__clock"><small id="rcMetricL">{E(d["metric"])}</small><b id="rcClockL">0:00</b></span></div>
<div class="xl"><div class="xl__bar"><span class="xl__ic">X</span><span>leads_FINAL_v3 (2).xlsx</span><em id="xlSave">Not saved</em></div>
<div class="xl__fx"><span>fx</span><span id="xlFx"></span></div>
<table><thead><tr><th></th><th>A · Name</th><th>B · Source</th><th>C · Phone</th><th>D · Status</th><th>E · Owner</th></tr></thead><tbody id="xlBody">{grid}<tr class="xl__r xl__r--new" id="xlNew"><td>7</td><td id="xlA"></td><td id="xlB"></td><td id="xlC"></td><td id="xlD"></td><td id="xlE"></td></tr></tbody></table></div>
<div class="wa2" id="waChat"><div class="wa2__h"><b>Sales Team 🏢</b><span>12 participants</span></div><div class="wa2__body" id="waBody"></div></div>
<ol class="race__log" id="logOld"></ol>
<div class="race__stamp" id="stampOld">{E(d["before"]["verdict"])}</div>
</div>
<div class="race__vs" aria-hidden="true"><span>VS</span></div>
<div class="race__side race__side--new">
<div class="race__top"><span class="race__tag race__tag--new">With OPSMO</span><span class="mono">Zoho CRM</span><span class="race__clock race__clock--new"><small id="rcMetricR">{E(d["metric"])}</small><b id="rcClockR">0:00</b></span></div>
<div class="crm"><div class="crm__card" id="crmCard"><div class="crm__h"><span class="crm__src" id="crmSrc">Property Finder</span><span class="crm__st" id="crmSt">New</span></div>
<b class="crm__name" id="crmName">Ahmed Khalil</b><p class="crm__what" id="crmWhat">2BR · Dubai Marina</p>
<div class="crm__f"><span>Owner</span><b id="crmOwner"><i>S</i>Sara</b></div><div class="crm__f"><span>Next step</span><b id="crmNext">Call within 5 min</b></div></div>
<div class="crm__push" id="crmPush"><b>New lead assigned</b><span id="crmPushT">Ahmed Khalil · tap to call</span></div>
<ul class="crm__steps" id="crmSteps">{after}</ul>
<div class="crm__q"><span class="mono">Handled during this demo</span><b id="crmCount">0</b><div class="crm__feed" id="crmFeed"></div></div></div>
<div class="race__stamp race__stamp--ok" id="stampNew">{E(d["after"]["verdict"])}</div>
</div>
<div class="race__end" id="raceEnd"><div class="race__bars"><div><span>Today</span><i class="race__b race__b--old" id="barOld"></i><b id="endOld">{E(d["before"]["label"])}</b></div>
<div><span>OPSMO</span><i class="race__b race__b--new" id="barNew"></i><b id="endNew">{E(d["after"]["label"])}</b></div></div>
<div class="race__gain"><b id="raceGain">99%</b><span>less waiting</span></div><button type="button" class="btn btn--line btn--sm" id="raceReplay">↻ Run it again</button></div>
</div>
<p class="fine rv center">Illustrative simulation, sped up. Your timings will differ.</p>''', "", "before-after")

def savings_calc(c, sector="real-estate", pick=True):
    cv = SECTORS[sector]["calc"]
    def rng(id_, label, mn, mx, step, val, unit):
        return f'<label class="calc__row" for="{id_}"><span>{label}</span><output id="{id_}Out">{val}{unit}</output><input type="range" id="{id_}" min="{mn}" max="{mx}" step="{step}" value="{val}" data-unit="{unit}"></label>'
    return sec(f'''<div class="calc rv" id="calc">
<div class="calc__in">{chip("Time & cost calculator")}<h2 class="h2">How much time is <em>manual work costing you?</em></h2>
<p class="lead">Move the sliders to match your team. In the businesses we audit, manual work takes 25–40% of team time.</p>
{picker(sector, "Start from a typical") if pick else ""}{sector_data() if pick else ""}
{rng("cTeam","People on the team",2,200,1,cv["team"],"")}
{rng("cHours","Hours each spends on manual work, per week",1,25,1,cv["hours"]," h")}
{rng("cRate","Average cost per hour (AED)",20,300,5,cv["rate"]," AED")}
{rng("cCut","Share of that work a good system removes",10,80,5,cv["cut"],"%")}</div>
<div class="calc__out" aria-live="polite"><p class="mono dim">Every year you could get back</p>
<div class="calc__big"><b id="oHours">0</b><span>hours</span></div>
<div class="calc__row2"><div><b id="oAed">0</b><span>AED in team time</span></div><div><b id="oFte">0</b><span>full-time people freed up</span></div></div>
<div class="calc__bar"><i id="oBar"></i></div><p class="fine">An estimate to start a conversation, not a quote. Based on 46 working weeks and 1,800 working hours per person a year.</p>
<div class="btnrow">{btn(c,"Check my numbers on a call","/book")}</div></div></div>''', "", "calculator")

ROLL = [(1,2,"Diagnose","We map how your team works today and size the gaps."),
        (3,4,"Design","Pipeline, fields, permissions and reports agreed on paper."),
        (5,9,"Build & connect","Zoho set up, data moved, portals and apps connected."),
        (10,11,"Test & train","Real cases tested. Every team trained in Arabic or English."),
        (12,12,"Go live","Switch on, with us beside the team for the first weeks."),
        (13,13,"Improve","Monthly reviews keep the system getting better.")]
def rollout(c):
    bars = "".join(f'<div class="ro__row" style="--s:{a};--e:{b}"><div class="ro__lbl"><b>{E(n)}</b><span>{E(d)}</span></div><div class="ro__track"><i class="ro__bar"><span class="mono">{"Ongoing" if a==13 else ("Week "+str(a) if a==b else f"Weeks {a}–{b}")}</span></i></div></div>' for a, b, n, d in ROLL)
    weeks = "".join(f'<span>{w}</span>' for w in range(1, 14))
    return sec(f'''<div class="head head--split"><div>{chip("A typical rollout")}<h2 class="h2 rv">Live in about <em>12 weeks.</em></h2></div>
<p class="lead rv">Scroll to watch a standard Zoho rollout unfold. Smaller setups go faster; multi-company projects run in phases.</p></div>
<div class="ro rv" id="rollout"><div class="ro__head"><span class="mono dim">Week</span><div class="ro__weeks">{weeks}</div></div>{bars}
<div class="ro__now" aria-hidden="true"><span class="mono" id="roNow">Week 1</span></div></div>''', "", "timeline")

DEPTS = [("Sales", ["Zoho CRM","SalesIQ","Bookings","Forms","Sign"], "Leads, deals, quotes and follow-ups in one pipeline."),
         ("Marketing", ["Campaigns","Marketing Automation","Social","Survey","Sites"], "Campaigns that feed leads straight into the CRM."),
         ("Service", ["Zoho Desk","Assist","Lens"], "Every customer request with an owner and a deadline."),
         ("Finance", ["Books","Invoice","Expense","Billing","Checkout"], "Quotes become invoices, and payments match automatically."),
         ("HR", ["People","Recruit","Payroll","Workerly"], "Hiring, attendance and payroll for the same team that sells."),
         ("Operations", ["Projects","Inventory","Creator","Flow","Analytics"], "Delivery, stock, custom apps and dashboards on the same data.")]
def suite_map(c):
    tabs = "".join(f'<button role="tab" class="sm__tab{" is-on" if i==0 else ""}" data-i="{i}" aria-selected="{"true" if i==0 else "false"}">{E(n)}</button>' for i, (n, _, _) in enumerate(DEPTS))
    panels = "".join(f'<div class="sm__panel{" is-on" if i==0 else ""}" data-i="{i}"><p>{E(d)}</p><div class="sm__apps">' + "".join(f'<span style="--k:{j}">{E(a)}</span>' for j, a in enumerate(apps)) + '</div></div>' for i, (n, apps, d) in enumerate(DEPTS))
    import math
    nodes = "".join(f'<span class="sm__node" style="left:{50+40*math.cos(math.radians(i*60-90)):.1f}%;top:{50+40*math.sin(math.radians(i*60-90)):.1f}%" data-i="{i}">{E(n)}</span>' for i, (n, _, _) in enumerate(DEPTS))
    return sec(f'''<div class="head head--split"><div>{chip("One suite, every department")}<h2 class="h2 rv">One customer record, <em>shared by every team.</em></h2></div>
<p class="lead rv">Zoho One has 45+ apps. Pick a department to see what it uses. We connect them so sales, service and finance all see the same customer.</p></div>
<div class="sm rv" id="suiteMap"><div class="sm__orbit" aria-hidden="true"><svg class="sm__lines" viewBox="-200 -200 400 400">{"".join(f'<line x1="0" y1="0" x2="{160*__import__("math").cos(__import__("math").radians(i*60-90)):.1f}" y2="{160*__import__("math").sin(__import__("math").radians(i*60-90)):.1f}" data-i="{i}"/>' for i in range(6))}</svg>
<div class="sm__core"><b>1</b><span>customer record</span></div>{nodes}</div>
<div class="sm__side"><div class="sm__tabs" role="tablist" aria-label="Departments">{tabs}</div>{panels}
<p class="fine">App names as listed by Zoho for Zoho One. We switch on only what you need.</p></div></div>''', "", "suite")
