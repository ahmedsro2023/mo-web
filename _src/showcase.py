# v7 dynamic showcase modules (rendered server-side, animated by assets/js/showcase.js)
from build import E, ARROW, EXT, btn, chip, sec, head, em_last, a_attrs

def live_demo(c):
    cols = ["New", "Contacted", "Viewing", "Offer", "Won"]
    colhtml = "".join(f'<div class="lv__col" data-col="{i}"><p class="lv__ch">{n}<b data-colcount>0</b></p><div class="lv__cards"></div></div>' for i, n in enumerate(cols))
    return sec(f'''<div class="head head--split"><div>{chip("See it working")}<h2 class="h2 rv">Every lead caught. <em>Every lead followed up.</em></h2></div>
<p class="lead rv">This is what a well-built system does all day, without anyone chasing it: leads arrive, get assigned in seconds, and move through the pipeline while managers watch the numbers live.</p></div>
<div class="lv rv" id="liveDemo" aria-label="Animated illustration of a CRM pipeline with sample data">
<div class="lv__top"><span class="lv__dots"><i></i><i></i><i></i></span><span class="mono">Sales pipeline · live</span><span class="lv__badge mono"><i class="dot"></i>Sample data</span></div>
<div class="lv__grid">
<aside class="lv__feed"><p class="mono dim">Incoming leads</p><ul id="lvFeed"></ul></aside>
<div class="lv__board">{colhtml}</div>
<aside class="lv__kpis"><div><span class="mono dim">Leads today</span><b id="kLeads">0</b></div><div><span class="mono dim">Avg. first response</span><b id="kResp">—</b></div><div><span class="mono dim">Follow-ups due</span><b id="kTasks">0</b></div><div><span class="mono dim">Won this week</span><b id="kWon">0</b></div>
<div class="lv__spark"><svg viewBox="0 0 200 60" preserveAspectRatio="none"><path id="lvSpark" d="M0 60"/></svg></div></aside>
</div></div>
<p class="fine rv">Illustration with sample data. Real setups use your sources, stages and team.</p>''', "", "live")

BEFORE = [("0:00","A lead comes in on Property Finder","The email sits in a shared inbox."),
          ("0:45","Someone forwards it to a WhatsApp group","Three agents see it. Nobody owns it."),
          ("2:10","An agent copies it into Excel","The source and listing are lost."),
          ("4:20","First call back","The buyer already spoke to another agency."),
          ("Day 3","No follow-up reminder","The lead goes cold. Nobody notices.")]
AFTER = [("0:00","The lead lands in Zoho CRM","Source, listing and campaign attached."),
         ("0:05","Assigned automatically","By area, language and agent availability."),
         ("0:06","Agent notified on mobile","With one-tap call and WhatsApp."),
         ("4:00","Call logged, next step set","A follow-up task is created for tomorrow."),
         ("Live","Manager dashboard updates","Source, speed and conversion, in real time.")]
def before_after(c):
    def lane(items, cls):
        return f'<ol class="ba__lane {cls}">' + "".join(f'<li><span class="ba__t mono">{E(t)}</span><div><b>{E(h)}</b><p>{E(p)}</p></div></li>' for t, h, p in items) + "</ol>"
    return sec(f'''<div class="head head--center">{chip("Before and after")}<h2 class="h2 rv">The same lead. <em>Two very different days.</em></h2>
<p class="lead rv">Switch between a typical setup and one we build, and watch the clock.</p></div>
<div class="ba rv" id="beforeAfter" data-mode="before">
<div class="ba__switch" role="tablist" aria-label="Compare"><button role="tab" aria-selected="true" data-mode="before">Today: WhatsApp &amp; Excel</button><button role="tab" aria-selected="false" data-mode="after">With an OPSMO system</button><i class="ba__pill" aria-hidden="true"></i></div>
<div class="ba__stage"><div class="ba__clock"><span class="mono dim">Time to first call</span><b id="baClock">4h 20m</b><span class="ba__verdict" id="baVerdict">Lead lost</span></div>
<div class="ba__lanes">{lane(BEFORE, "ba__lane--before")}{lane(AFTER, "ba__lane--after")}</div></div></div>
<p class="fine rv center">Typical example from real-estate teams. Your timings will differ.</p>''', "", "before-after")

def savings_calc(c):
    def rng(id_, label, mn, mx, step, val, unit):
        return f'<label class="calc__row" for="{id_}"><span>{label}</span><output id="{id_}Out">{val}{unit}</output><input type="range" id="{id_}" min="{mn}" max="{mx}" step="{step}" value="{val}" data-unit="{unit}"></label>'
    return sec(f'''<div class="calc rv" id="calc">
<div class="calc__in">{chip("Time & cost calculator")}<h2 class="h2">How much time is <em>manual work costing you?</em></h2>
<p class="lead">Move the sliders to match your team. In the businesses we audit, manual work takes 25–40% of team time.</p>
{rng("cTeam","People on the team",2,200,1,15,"")}
{rng("cHours","Hours each spends on manual work, per week",1,25,1,8," h")}
{rng("cRate","Average cost per hour (AED)",20,300,5,60," AED")}
{rng("cCut","Share of that work a good system removes",10,80,5,50,"%")}</div>
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
