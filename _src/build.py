#!/usr/bin/env python3
"""OPSMO static site generator — renders every route of the original site from captured content."""
import os, re, html, shutil, json
from shared import *
from solutions import SOL
from industries import IND, ORDER as IND_ORDER, INTEGRATION_NOTE
from founder_data import *

OUT = os.environ.get("OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
HERE = os.path.dirname(os.path.abspath(__file__))
import sys; sys.path.insert(0, HERE)
E = lambda s: html.escape(s, quote=True)

SOL_ORDER = ["software-selection","crm-implementation","crm-migration","business-process-automation","api-systems-integration",
             "commercial-revenue-operations","business-intelligence-reporting","digital-transformation","managed-crm-operations","zoho-desk-implementation"]
SOL_META = {  # index-card copy (from /solutions), short names (from nav/footer)
 "software-selection": ("SELECTION","Software Selection","Software Selection","A structured evaluation of the software you are considering: requirements, shortlist, the full cost, integration, a user pilot and a phased rollout plan.","workshop"),
 "crm-implementation": ("CRM_ARCHITECTURE","CRM Implementation & Architecture","CRM Implementation","We design the data model, pipeline, permissions and adoption path, then implement and roll out the CRM your commercial team will actually use.","office"),
 "crm-migration": ("MIGRATION","CRM Migration & Reimplementation","CRM Migration","A structured migration from an inherited or failing CRM: audit, data mapping, clean rebuild, reconciliation and controlled cutover.","servers"),
 "business-process-automation": ("WORKFLOW","Business Process Automation","Process Automation","Routing, approvals, notifications, task creation and follow-ups designed as governed workflows with error handling and monitoring.","workshop"),
 "api-systems-integration": ("INTEGRATION","API & Systems Integration","Systems Integration","We connect CRM, ERP, finance, websites, marketing and communication platforms so records stay consistent without re-typing.","servers"),
 "commercial-revenue-operations": ("REVOPS","Commercial & Revenue Operations","Revenue Operations","Sales process architecture, pipeline governance, customer lifecycle design and the visibility leadership needs to run the commercial engine.","team"),
 "business-intelligence-reporting": ("ANALYTICS","Business Intelligence & Reporting","Analytics & Reporting","Governed data models, automated reporting and management dashboards built on KPI definitions the business has agreed to.","analytics"),
 "digital-transformation": ("TRANSFORMATION","Digital Transformation","Digital Transformation","Multi-application transformation with architecture, governance and phased delivery across departments.","sme"),
 "managed-crm-operations": ("OPERATE","Managed CRM & Digital Operations","Managed Operations","Administration, support, monitoring, optimisation and continuous improvement delivered as a monthly retainer.","monitor"),
 "zoho-desk-implementation": ("ZOHO_DESK","Zoho Desk Implementation","Zoho Desk","We set up Zoho Desk so requests from every support channel land with the right team, with response targets, a help centre and customer history from Zoho CRM.","team"),
}
SS_BULLETS = ["Requirements brief covering workflows, users, must-haves and success measures","Shortlist comparing existing tools, standalone apps and connected suites","First-year cost comparison across licences, add-ons, implementation and administration","Integration and migration map showing which system owns each record"]
ZD_SCOPE = ["Ticket intake and routing across email, forms and support channels","Response targets, reminders and escalation rules","Help centre, knowledge base and customer self-service","Zoho CRM integration for customer history and open issues"]
PLATS = [("zoho","Zoho","ZOHO_ONE","A connected commercial stack on one platform."),("salesforce","Salesforce","SALESFORCE","Architecture discipline for a powerful platform."),
         ("odoo","Odoo","ODOO_ERP","ERP and CRM operating as one commercial system."),("automation-integration","Automation & Integration","N8N_API","The connective layer between your applications."),
         ("analytics","Analytics & BI","POWER_BI","One governed version of the numbers.")]
IND_META = {"real-estate":("Real Estate","From portal enquiry to signed contract, without losing a lead."),"professional-services":("Professional Services","Pipeline, delivery and billing connected as one engagement."),
 "media-advertising":("Media & Advertising","Campaign operations from brief to reconciliation."),"events-communities":("Events & Communities","Registrations, sponsors and members in one operating system."),
 "retail-ecommerce":("Retail & E-commerce","Storefront, stock and service on the same customer record."),"b2b-sales-distribution":("B2B Sales & Distribution","Territories, quotations and repeat orders under control."),
 "smes-growing-enterprises":("SMEs & Growing Enterprises","The systems a growing company can actually run.")}
COMPANY = [("/about","About OPSMO","Who we are and how we work."),("/founder","The Founder","Mohamed Refaat's story."),("/approach","Our Approach","Six stages, defined deliverables."),
           ("/packages","Implementation Packages","Scoped to your operating reality."),("/contact","Contact","Request an operational assessment.")]

# ---------------------------------------------------------------- paths
class Ctx:
    def __init__(self, route):
        self.route = route  # e.g. "/" or "/solutions/crm-implementation"
        depth = 0 if route == "/" else route.strip("/").count("/") + 1
        self.up = "../" * depth
    def href(self, target):
        if re.match(r"^(https?:|mailto:|tel:)", target): return target
        if target.startswith("#"): return target
        path, _, frag = target.partition("#")
        path = path.strip("/")
        h = self.up + (path + "/" if path else "")
        if not h: h = "./"
        return h + ("#" + frag if frag else "")
    def asset(self, p): return self.up + "assets/" + p

def ext(url): return re.match(r"^https?:", url) is not None
def a_attrs(c, url):
    return f'href="{E(c.href(url))}"' + (' target="_blank" rel="noopener"' if ext(url) else "")

ARROW = '<svg class="i" aria-hidden="true"><use href="#i-arrow"/></svg>'
EXT = '<svg class="i" aria-hidden="true"><use href="#i-ext"/></svg>'
def btn(c, label, url, kind="fire", small=False):
    icon = EXT if ext(url) else ARROW
    return f'<a class="btn btn--{kind}{" btn--sm" if small else ""}" {a_attrs(c,url)}>{E(label)} {icon}</a>'
def btns(c, pairs, small=False):
    return '<div class="btnrow">' + "".join(btn(c, l, u, "fire" if i == 0 else "line", small) for i, (l, u) in enumerate(pairs)) + "</div>"
def chip(text, dark=False): return f'<p class="chip{" chip--dark" if dark else ""} rv">{E(text)}</p>'
def mono(t): return f'<span class="mono">{E(t)}</span>'
def em_last(h):
    """Render h2 with the final sentence (if 2+) in the serif accent."""
    parts = re.split(r"(?<=[.?!])\s+(?=[A-Z])", h.strip())
    if len(parts) >= 2:
        return E(" ".join(parts[:-1])) + " <em>" + E(parts[-1]) + "</em>"
    return E(h)

# ---------------------------------------------------------------- shared blocks
def sec(inner, cls="", id_=""):
    return f'<section class="sec {cls}"{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}><div class="wrap">{inner}</div></section>'
def head(eyebrow, h2, lead="", dark=False, center=False, split=False):
    out = (chip(eyebrow, dark) if eyebrow else "") + (f'<h2 class="h2 rv">{em_last(h2)}</h2>' if h2.strip() else "")
    if split and lead:
        return f'<div class="sechead sechead--split"><div>{out}</div><p class="lead rv">{E(lead)}</p></div>'
    return f'<div class="sechead{" sechead--center" if center else ""}">{out}{f"<p class={chr(34)}lead rv{chr(34)}>{E(lead)}</p>" if lead else ""}</div>'

def faq_html(items):
    return '<div class="faq__list">' + "".join(f'<details class="qa rv"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in items) + "</div>"

def stages_html():
    tabs = "".join(f'<button class="stg__tab{" is-on" if i==0 else ""}" role="tab" aria-selected="{"true" if i==0 else "false"}" data-i="{i}"><span class="mono">0{i+1}</span>{E(n)}</button>' for i,(n,_,_) in enumerate(STAGES))
    data = json.dumps([{"t":t,"d":d} for _,t,d in STAGES])
    n,t,d = STAGES[0]
    return f'''<div class="stg rv" data-stages='{E(data)}'>
<div class="stg__tabs" role="tablist" aria-label="Software selection stages">{tabs}</div>
<div class="stg__panel" role="tabpanel"><div><span class="mono">THE BUYER'S TASK</span><p class="stg__task">{E(t)}</p></div>
<div class="stg__deliv"><span class="mono">DELIVERABLE</span><p class="stg__d">{E(d)}</p></div></div></div>'''

def tools_html(c, full_cta=True):
    fields = [("VENDOR DEMOS","demos",4),("HOURS PER DEMO","hpd",1),("PEOPLE ON THE REVIEW TEAM","people",3),("REVIEW HOURS PER PERSON","rev",2),("DECISION MEETING HOURS","dec",1),("OTHER WORK IN STAFF-HOURS","other",0)]
    inputs = "".join(f'<label class="num"><span class="mono">{l}</span><span class="num__ctl"><button type="button" data-step="-1" aria-label="Decrease">−</button><input type="number" min="0" step="0.5" value="{v}" data-k="{k}"><button type="button" data-step="1" aria-label="Increase">+</button></span></label>' for l,k,v in fields)
    att = [("sales","Sales and follow-up"),("support","Customer support and tickets"),("cross","Work across departments"),("defining","Still defining the problem")]
    fitq = [("mostly","Existing tools mostly fit"),("partly","They partly fit"),("unsure","Not sure yet")]
    r = FIT["defining"]
    fitdata = E(json.dumps({k:[v[0],v[1],v[2],c.href(v[3])] for k,v in FIT.items()}))
    cta = btns(c, [("Book a Software Selection Consultation","/book"),("See the full service page","/solutions/software-selection")]) if full_cta else ""
    return f'''<div class="tools">
<div class="est card rv" id="estimate"><span class="mono acc">INTERACTIVE ESTIMATE</span><h3>How much team time goes into the search?</h3>
<div class="est__grid">{inputs}</div>
<div class="est__out"><span class="mono">ESTIMATED EFFORT</span><b><span id="estTotal">21</span><small>STAFF-HOURS</small></b>
<ul class="est__bars"><li><span>Vendor demos</span><i><s data-b="demo"></s></i><em id="bDemo">12</em></li><li><span>Reviews</span><i><s data-b="rev"></s></i><em id="bRev">6</em></li><li><span>Decision meeting</span><i><s data-b="dec"></s></i><em id="bDec">3</em></li><li><span>Other work</span><i><s data-b="oth"></s></i><em id="bOth">0</em></li></ul></div>
<p class="fine">{E(ESTIMATE_NOTE)}</p></div>
<div class="fit card rv" id="fitGuide" data-fit="{fitdata}"><span class="mono acc">FIT GUIDE</span><h3>Where should your team start?</h3>
<fieldset><legend class="mono">WHAT NEEDS ATTENTION?</legend>{"".join(f'<label class="pill"><input type="radio" name="att" value="{k}"{" checked" if k=="defining" else ""}><span>{E(l)}</span></label>' for k,l in att)}</fieldset>
<fieldset><legend class="mono">HOW WELL DO YOUR EXISTING TOOLS FIT?</legend>{"".join(f'<label class="pill"><input type="radio" name="fitq" value="{k}"{" checked" if k=="unsure" else ""}><span>{E(l)}</span></label>' for k,l in fitq)}</fieldset>
<div class="fit__res" aria-live="polite"><h4 id="fitT">{E(r[0])}</h4><p id="fitP">{E(r[1])}</p><a id="fitA" class="link" href="{E(c.href(r[3]))}">{E(r[2])} {ARROW}</a></div>
<span class="mono fit__foot">A STARTING POINT FOR DISCUSSION</span></div>
</div>{cta}'''

def method_steps(full=True):
    return '<ol class="msteps">' + "".join(
        f'<li class="mstep rv"><span class="mstep__k mono">0{i+1}</span><div><h3>{E(n)}</h3><p>{E(d)}</p>' +
        (('<ul class="docs">' + "".join(f"<li>{E(x)}</li>" for x in dl) + "</ul>") if full else "") + "</div></li>"
        for i,(n,d,dl) in enumerate(METHOD)) + "</ol>"
def method_block():
    return sec(head("METHODOLOGY", "The same six-stage discipline, applied to this solution.") + '<div class="mgrid">' + "".join(
        f'<div class="mcard rv"><span class="mono acc">0{i+1}</span><h3>{E(n)}</h3><p>{E(d)}</p></div>' for i,(n,d,_) in enumerate(METHOD)) + "</div>")
def receive_list():
    return '<ol class="nlist nlist--2">' + "".join(f'<li class="rv"><span class="mono">0{i+1}</span>{E(x)}</li>' for i,x in enumerate(RECEIVE)) + "</ol>"
def receive_block():
    return sec(head("", "What you receive") + receive_list(), "sec--paper")
def cases_block(c):
    return sec(f'<div class="cases rv"><span class="mono acc">SUCCESS STORIES</span><p>PropSpace, Elnaggar &amp; Partners, R1 Performance and Fawry Microfinance: four Zoho One transformations, from spreadsheets and WhatsApp to one operating system.</p><a class="btn btn--line btn--sm" {a_attrs(c,"/success-stories")}>Read the success stories {ARROW}</a></div>', "sec--tight")
def related_block(c, slugs):
    def tl(s): return SS_TAGLINE if s=="software-selection" else SOL[s]["tagline"]
    cards = "".join(f'<a class="rcard rv" {a_attrs(c,"/solutions/"+s)}><span class="mono acc">[SYSTEM: {SOL_META[s][0]}]</span><h3>{E(SOL_META[s][2])}</h3><p>{E(tl(s))}</p><span class="rcard__go">{ARROW}</span></a>' for s in slugs)
    return sec(head("RELATED SOLUTIONS","") + f'<div class="grid3">{cards}</div>', "sec--paper")
def others_block(c, slug):
    cards = "".join(f'<a class="rcard rv" {a_attrs(c,"/platforms/"+s)}><span class="mono acc">[STACK: {st}]</span><h3>{E(n)}</h3><p>{E(t)}</p><span class="rcard__go">VIEW {ARROW}</span></a>' for s,n,st,t in PLATS if s != slug)
    return sec(head("OTHER PLATFORMS","") + f'<div class="grid4">{cards}</div>', "sec--paper")
def cta_block(c, key="default", eyebrow=None, h=None, p=None, pairs=None):
    e,hh,pp,pr = CTA[key]
    e = eyebrow or e; hh = h if h is not None else hh; pp = p or pp; pr = pairs or pr
    return f'''<section class="cta"><img class="cta__bg" src="{c.asset("img/skyline.webp")}" alt="" loading="lazy"><canvas class="trails" data-dark="1" aria-hidden="true"></canvas>
<div class="wrap cta__in">{chip(e, True)}{f'<h2 class="h2 h2--light rv">{em_last(hh)}</h2>' if hh.strip() else ""}<p class="cta__p rv">{E(pp)}</p>{btns(c, pr)}</div></section>'''

def fit_box(text, tags=None):
    return f'<div class="fitbox rv"><span class="mono acc">TYPICAL FIT</span><p>{E(text)}</p></div>'

# ---------------------------------------------------------------- DSL renderer
def parse_md(path):
    raw = open(path).read()
    fm, _, body = raw.partition("\n---\n")
    meta = dict(l.split(": ", 1) for l in fm.strip().split("\n") if ": " in l)
    return meta, body

def inline(s):
    s = E(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s

def render_links(c, line):
    pairs = re.findall(r"\[\[(.+?) -> (.+?)\]\]", line)
    return btns(c, pairs)

def card_html(c, line, kind):
    actions_pre = None
    if " => " in line:
        line, actions_pre = line.split(" => ", 1)
    m = re.match(r"\*\s+(?:\[(.+?)\]\s+)?(.+?)(?:\s+::\s+(.+?))?(?:\s+=>\s+(.+?))?(?:\s+->\s+(\S+))?(?:\s+>>\s+(.+))?$", line)
    tag, title, text, actions, link, foot = m.groups()
    actions = actions or actions_pre
    num = ""
    mm = re.match(r"^(\d\d) · (.+)$", title)
    if mm: num, title = mm.groups()
    body = (f'<span class="mono acc">{E(tag)}</span>' if tag else "") + (f'<span class="card__n">{num}</span>' if num else "") + f"<h3>{E(title)}</h3>" + (f"<p>{inline(text)}</p>" if text else "")
    if actions:
        acts = [a.split(" -> ") for a in actions.split(" ;; ")]
        body += '<div class="card__acts">' + "".join((btn(c,l,u,"fire" if i==0 else "line",True)) for i,(l,u) in enumerate(acts)) + "</div>"
    if kind == "mosaic":
        slug = link.rsplit("/",1)[-1]
        img = IND.get(slug, {}).get("img", "skyline")
        return f'<a class="mtile rv" {a_attrs(c,link)}><img src="{c.asset("img/"+img+".webp")}" alt="" loading="lazy"><div>{body}<span class="mtile__go mono">VIEW WORKFLOW {ARROW}</span></div></a>'
    if kind == "articles":
        return f'<a class="article-card rv" {a_attrs(c,link)}>{body}<span class="mono article-card__foot">{E(foot or "")} {ARROW}</span></a>'
    if link:
        go = "VIEW SOLUTION" if "/solutions/" in link else ("VIEW" if "/platforms/" in link else "")
        return f'<a class="card card--link rv" {a_attrs(c,link)}>{body}<span class="card__go mono">{go} {ARROW}</span></a>'
    return f'<div class="card rv">{body}</div>'

def tier_html(c, line):
    parts = [p.strip() for p in line[1:].split(" :: ")]
    m = re.match(r"\[(.+?)\]\s+(.+)", parts[0]); tag, name = m.groups()
    desc, items = parts[1], [x.strip() for x in parts[2].split(";")]
    excl = parts[3] if len(parts) > 3 and parts[3] else ""
    summary = parts[4] if len(parts) > 4 else ""
    is_pkg = "CATEGORY" in tag
    price = ('<div class="tier__price"><span class="mono">PRICING</span><b>Custom Quote</b></div>' if is_pkg else
             f'<div class="tier__price"><span class="mono">MONTHLY FEE</span><a class="link" {a_attrs(c,"/contact")}>Request a Tailored Plan {ARROW}</a></div>')
    label = "Request an Implementation Assessment" if is_pkg else "Request a Tailored Plan"
    return f'''<article class="tier rv"><span class="mono acc">[{E(tag)}]</span><h3>{E(name)}</h3><p class="tier__d">{E(desc)}</p>{price}
{f'<p class="tier__s">{E(summary)}</p>' if summary else ""}<ul class="ticks">{"".join(f"<li>{E(i)}</li>" for i in items)}</ul>
{f'<p class="tier__x"><span class="mono">NOT INCLUDED</span> {E(excl)}</p>' if excl else ""}{btn(c,label,"/contact","line",True)}</article>'''

def widget(c, name, meta):
    if name == "stages": return stages_html()
    if name == "tools": return tools_html(c, full_cta=False)
    if name.startswith("faq:"): return faq_html(FAQ[name[4:]])
    if name.startswith("cta:"): return "__CTA__" + name[4:]
    if name == "method": return "__RAW__" + method_block()
    if name == "receive": return "__RAW__" + receive_block()
    if name == "receivelist": return receive_list()
    if name == "methodfull": return method_steps(True)
    if name == "cases": return "__RAW__" + cases_block(c)
    if name.startswith("related:"): return "__RAW__" + related_block(c, name[8:].split(","))
    if name.startswith("others:"): return "__RAW__" + others_block(c, name[7:])
    if name.startswith("fit:"): return fit_box(name[4:])
    if name == "leader": return leader_html(c)
    return ""

def render_body(c, meta, body, hero_img=None):
    blocks = re.split(r"\n(?=\^ |## |\{\{cta|\{\{method\}\}|\{\{receive\}\}|\{\{cases\}\}|\{\{related|\{\{others)", "\n" + body.strip())
    merged = []
    for b in blocks:
        if merged and re.fullmatch(r"\s*\^ [^\n]*\s*", merged[-1]):
            merged[-1] = merged[-1].rstrip("\n") + "\n" + b.lstrip("\n")
        else:
            merged.append(b)
    html_out, first = [], True
    for blk in merged:
        lines = [l for l in blk.strip().split("\n")]
        if not lines or not lines[0].strip(): continue
        eyebrow = ""
        if lines[0].startswith("^ "):
            eyebrow = lines[0][2:].strip(); lines = lines[1:]
        if first and lines and lines[0].startswith("# "):
            html_out.append(render_hero(c, eyebrow, lines, meta)); first = False; continue
        first = False
        h2 = ""
        if lines and lines[0].startswith("## "):
            h2 = lines[0][3:]; lines = lines[1:]
        elif lines and lines[0].strip() == "##":
            lines = lines[1:]
        mods = [l[1:].strip() for l in lines if re.match(r"^@\w", l)]
        lines = [l for l in lines if not re.match(r"^@\w", l)]
        dark = "dark" in mods
        kind = next((m for m in mods if m in ("cards3","cards4","mosaic","articles")), "cards3")
        parts, buf_cards, buf_list, buf_steps, buf_tiers, lead_done = [], [], [], [], [], False
        col_groups = []
        def flush():
            nonlocal buf_cards, buf_list, buf_steps, buf_tiers
            if buf_cards:
                cls = {"cards3":"grid3","cards4":"grid4","mosaic":"mosaic","articles":"articles"}[kind]
                parts.append(f'<div class="{cls}">' + "".join(card_html(c, l, kind) for l in buf_cards) + "</div>"); buf_cards = []
            if buf_list:
                parts.append('<ul class="ticks rv">' + "".join(f"<li>{inline(x)}</li>" for x in buf_list) + "</ul>"); buf_list = []
            if buf_steps:
                if "legal" in mods:
                    parts.append('<ol class="legal">' + "".join(f'<li class="rv"><span class="mono acc">0{i+1}</span><div><h3>{E(t)}</h3><p>{E(d)}</p></div></li>' for i,(t,d) in enumerate(buf_steps)) + "</ol>")
                elif any(d for _,d in buf_steps):
                    parts.append('<ol class="steps">' + "".join(f'<li class="rv"><span class="steps__n mono">0{i+1}</span><h3>{E(t)}</h3><p>{E(d)}</p></li>' for i,(t,d) in enumerate(buf_steps)) + "</ol>")
                else:
                    cls = "nlist nlist--2" if ("grid2" in mods or len(buf_steps) > 5) else "nlist"
                    parts.append(f'<ol class="{cls}">' + "".join(f'<li class="rv"><span class="mono">{i+1:02d}</span>{E(t)}</li>' for i,(t,_) in enumerate(buf_steps)) + "</ol>")
                buf_steps = []
            if buf_tiers:
                parts.append('<div class="tiers">' + "".join(tier_html(c, l) for l in buf_tiers) + "</div>"); buf_tiers = []
        for l in lines:
            s = l.strip()
            if not s: continue
            if s.startswith("* "): buf_cards.append(s); continue
            if s.startswith("- "): buf_list.append(s[2:]); continue
            if re.match(r"^1\. ", s):
                t, _, d = s[3:].partition(" :: "); buf_steps.append((t, d)); continue
            if s.startswith("$ "): buf_tiers.append(s); continue
            flush()
            if s.startswith("### "):
                col_groups.append(len(parts)); parts.append(f'<h4 class="subh mono acc">{E(s[4:])}</h4>'); continue
            if s.startswith("[["): parts.append(render_links(c, s)); continue
            if s.startswith("{{"):
                w = widget(c, s[2:-2], meta)
                if w.startswith("__CTA__"): html_out.append(cta_block(c, w[7:])); parts = None; break
                if w.startswith("__RAW__"): html_out.append(w[7:]); parts = None; break
                parts.append(w); continue
            if s.startswith("& "):
                parts.append('<div class="tags rv">' + "".join(f"<span>{E(x.strip())}</span>" for x in s[2:].split(";")) + "</div>"); continue
            if s.startswith("! "): parts.append(f'<p class="fine rv">{E(s[2:])}</p>'); continue
            if s.startswith("> "): parts.append(f'<p class="pull rv">{E(s[2:])}</p>'); continue
            cls = "lead" if not lead_done and h2 else "para"
            lead_done = True
            parts.append(f'<p class="{cls} rv">{inline(s)}</p>')
        if parts is None: continue
        flush()
        if "cols2" in mods and len(col_groups) == 2:
            a, b = col_groups
            pre, c1, c2 = parts[:a], parts[a:b], parts[b:]
            parts = pre + [f'<div class="cols2"><div class="colbox rv">{"".join(c1)}</div><div class="colbox colbox--alt rv">{"".join(c2)}</div></div>']
        if dark:
            pr = re.findall(r'<a class="btn.*?</a>', "".join(parts))
            text = re.findall(r'<p class="(?:lead|para) rv">(.*?)</p>', "".join(parts))
            html_out.append(f'''<section class="cta"><img class="cta__bg" src="{c.asset("img/skyline.webp")}" alt="" loading="lazy"><canvas class="trails" data-dark="1" aria-hidden="true"></canvas>
<div class="wrap cta__in">{chip(eyebrow, True) if eyebrow else ""}{f'<h2 class="h2 h2--light rv">{em_last(h2)}</h2>' if h2.strip() else ""}{"".join(f'<p class="cta__p rv">{t}</p>' for t in text)}<div class="btnrow">{"".join(pr)}</div></div></section>''')
            continue
        lead_html = ""
        if parts and parts[0].startswith('<p class="lead rv">') and "split" not in mods and "founder" not in mods:
            lead_html = parts.pop(0)
        hd = ""
        if eyebrow or h2.strip():
            hd = chip(eyebrow) if eyebrow else ""
            hd += f'<h2 class="h2 rv">{em_last(h2)}</h2>' if h2.strip() else ""
            hd = f'<div class="sechead">{hd}{lead_html}</div>'
        elif lead_html:
            parts.insert(0, lead_html)
        alt = " sec--paper" if len(html_out) % 2 == 0 else ""
        if "founder" in mods:
            inner = f'<div class="fband"><figure class="fband__img rv"><img src="{c.asset("img/founder.webp")}" alt="Mohamed Refaat" loading="lazy"></figure><div>{hd}{"".join(parts)}</div></div>'
            html_out.append(sec(inner, alt)); continue
        if "split" in mods:
            inner = f'<div class="split">{hd}<div>{"".join(parts)}</div></div>'
            html_out.append(sec(inner, alt)); continue
        html_out.append(sec(hd + "".join(parts), alt))
    return "\n".join(html_out)

def render_hero(c, eyebrow, lines, meta, extra_side=""):
    h1 = lines[0][2:]
    rest = lines[1:]
    paras, links, notes = [], "", []
    for l in rest:
        s = l.strip()
        if not s: continue
        if s.startswith("[["): links = render_links(c, s)
        elif s.startswith("! "): notes.append(s[2:])
        else: paras.append(s)
    img = meta.get("img")
    side = extra_side
    if img and not side:
        side = f'<div class="pstack rv" aria-hidden="true"><span class="pstack__a"></span><span class="pstack__b"></span><figure><img src="{c.asset("img/"+img+".webp")}" alt="" fetchpriority="high"></figure></div>'
    return f'''<section class="phero{" phero--img" if side else ""}"><canvas class="trails" aria-hidden="true"></canvas><div class="wrap phero__grid"><div class="phero__copy">
{chip(eyebrow) if eyebrow else ""}<h1 class="phero__h rv">{em_last(h1)}</h1>{"".join(f'<p class="phero__p rv">{inline(p)}</p>' for p in paras)}{links}{"".join(f'<p class="fine rv">{E(n)}</p>' for n in notes)}</div>{side}</div></section>'''

# ---------------------------------------------------------------- templates
def leader_html(c):
    return f'''<div class="leader rv"><figure class="leader__img"><img src="{c.asset("img/founder.webp")}" alt="Mohamed Refaat" loading="lazy"></figure>
<div><h3>Mohamed Refaat</h3><p class="mono acc">FOUNDER &amp; PRINCIPAL CONSULTANT</p>
<div class="leader__facts"><div><span class="mono">ZOHO</span><b>First Egyptian hire at Zoho</b></div><div><span class="mono">ZOHO EGYPT</span><b>First team member in Zoho Egypt</b></div></div>
<p>{E(LEADER_BIO)}</p><p class="fine">{E(LEADER_NOTE)}</p>
<div class="btnrow">{btn(c,"READ THE FOUNDER STORY","/founder","fire",True)}{btn(c,"START A CONVERSATION","/contact","line",True)}</div></div></div>'''

def render_solution(c, slug):
    s = SOL[slug]
    out = [f'''<section class="phero phero--img"><canvas class="trails" aria-hidden="true"></canvas><div class="wrap phero__grid"><div class="phero__copy">
{chip("SOLUTION · [SYSTEM: "+s["sys"]+"]")}<h1 class="phero__h rv">{E(s["name"])}</h1><p class="phero__p rv">{E(s["tagline"])}</p>
{btns(c,[("Request an Operational Assessment","/contact"),("Book a Consultation","/book")])}</div>
<div class="pstack rv" aria-hidden="true"><span class="pstack__a"></span><span class="pstack__b"></span><figure><img src="{c.asset("img/"+s["img"]+".webp")}" alt="" fetchpriority="high"></figure></div></div></section>''']
    ch = '<ol class="probs">' + "".join(f'<li class="rv"><span class="mono acc">0{i+1}</span><p>{E(x)}</p></li>' for i,x in enumerate(s["challenges"])) + "</ol>"
    aside = f'''<aside class="sidecard rv"><span class="mono">WHO THIS IS FOR</span><ul class="ticks">{"".join(f"<li>{E(w)}</li>" for w in s["who"])}</ul>
<span class="mono">SUPPORTED TECHNOLOGY</span><div class="tags">{"".join(f"<span>{E(t)}</span>" for t in s["tech"])}</div><p>{E(s["summary"])}</p></aside>'''
    out.append(sec(f'<div class="probgrid"><div>{head("","Business challenges we solve")}{ch}</div>{aside}</div>'))
    out.append(sec(head("SCOPE OF SERVICES","What the engagement actually covers.") + '<ol class="nlist nlist--2">' + "".join(f'<li class="rv"><span class="mono">0{i+1}</span>{E(x)}</li>' for i,x in enumerate(s["scope"])) + "</ol>", "sec--paper"))
    out.append(method_block()); out.append(receive_block())
    out.append(sec(head("","Typical use cases") + '<div class="grid3">' + "".join(f'<div class="card rv"><span class="card__n">0{i+1}</span><p>{E(u)}</p></div>' for i,u in enumerate(s["uses"])) + "</div>"))
    out.append(cases_block(c))
    out.append(sec(f'<div class="faq">{head("FAQ","Questions we\'re asked before this engagement.")}{faq_html(s["faq"])}</div>', "sec--paper"))
    out.append(related_block(c, s["related"]).replace("sec--paper", ""))
    out.append(cta_block(c))
    return "\n".join(out)

def render_industry(c, slug):
    s = IND[slug]
    others = [x for x in IND_ORDER if x != slug][:3]
    out = [f'''<section class="phero phero--img"><canvas class="trails" aria-hidden="true"></canvas><div class="wrap phero__grid"><div class="phero__copy">
{chip("INDUSTRY · [VERTICAL: "+s["v"]+"]")}<h1 class="phero__h rv">{E(s["name"])}</h1><p class="phero__p rv">{E(s["tagline"])}</p>
{btns(c,[("Request an Operational Assessment","/contact"),("Book a Discovery Call","/book")])}</div>
<div class="pstack rv" aria-hidden="true"><span class="pstack__a"></span><span class="pstack__b"></span><figure><img src="{c.asset("img/"+s["img"]+".webp")}" alt="" fetchpriority="high"></figure></div></div></section>''']
    flow = '<ol class="flow">' + "".join(f'<li class="rv"><span class="flow__n mono">0{i+1}</span><p>{E(x)}</p></li>' for i,x in enumerate(s["flow"])) + "</ol>"
    out.append(sec(head("THE OPERATING REALITY","What the workflow looks like.", s["intro"]) + f'<p class="mono acc flowlabel">TYPICAL OPERATING FLOW</p>{flow}'))
    out.append(sec(head("IMPLEMENTATION SPECIFICS","What we configure for this sector.") + '<ol class="nlist">' + "".join(f'<li class="rv"><span class="mono">0{i+1}</span>{E(x)}</li>' for i,x in enumerate(s["spec"])) + f'</ol><p class="fine rv">{E(INTEGRATION_NOTE)}</p>', "sec--paper"))
    cards = "".join(f'<a class="mtile rv" {a_attrs(c,"/industries/"+o)}><img src="{c.asset("img/"+IND[o]["img"]+".webp")}" alt="" loading="lazy"><div><h3>{E(IND_META[o][0])}</h3><p>{E(IND_META[o][1])}</p><span class="mtile__go mono">VIEW {ARROW}</span></div></a>' for o in others)
    out.append(sec(head("OTHER INDUSTRIES","") + f'<div class="mosaic mosaic--3">{cards}</div>'))
    out.append(cta_block(c, pairs=[("Book a Consultation","/book"),("Request an Operational Assessment","/contact")]))
    return "\n".join(out)

def render_article(c, path):
    meta, body = parse_md(path)
    paras = []
    ul = []
    def fl():
        nonlocal ul
        if ul: paras.append('<ul class="ticks">' + "".join(f"<li>{inline(x)}</li>" for x in ul) + "</ul>"); ul = []
    for l in body.strip().split("\n"):
        s = l.strip()
        if not s: continue
        if s.startswith("- "): ul.append(s[2:]); continue
        fl()
        if s.startswith("### "): paras.append(f"<h2>{E(s[4:])}</h2>")
        else: paras.append(f"<p>{inline(s)}</p>")
    fl()
    return f'''<article class="art"><header class="art__head wrap"><a class="mono back" {a_attrs(c,"/insights")}>← ALL INSIGHTS</a>
<p class="mono acc art__meta">{E(meta["cat"])} · {E(meta["read"])} · {E(meta["date"])}</p><h1 class="phero__h">{E(meta["h1"])}</h1><p class="phero__p">{E(meta["deck"])}</p>
<div class="byline"><img src="{c.asset("img/founder.webp")}" alt=""><span class="mono">MOHAMED REFAAT</span></div></header>
<div class="art__body wrap">{"".join(paras)}</div></article>''' + cta_block(c, eyebrow="APPLY THIS", h="Want this working in your business, not just described?",
        p="We can review your current setup and tell you what would change, and what wouldn't.")

def render_founder(c):
    story = "".join((f'<p class="pull rv">{E(p[1:])}</p>' if p.startswith(">") else f'<p class="rv">{E(p)}</p>') for p in STORY)
    career = "".join(f"<li>{E(x)}</li>" for x in CAREER)
    else_ = "".join(f'<a class="card card--link rv" {a_attrs(c,u)}><span class="mono acc">{E(k)}</span><h3>{E(t)}</h3><p>{E(d)}</p><span class="card__go mono">{EXT}</span></a>' for k,t,d,u in ELSEWHERE)
    zl = "".join(f'<a class="card card--link rv" {a_attrs(c,u)}><h3>{E(t)}</h3><p>{E(d)}</p><span class="card__go mono">OPEN ZOHO {EXT}</span></a>' for t,d,u in ZOHO_LINKS)
    return f'''<section class="phero phero--img fhero"><canvas class="trails" aria-hidden="true"></canvas><div class="wrap phero__grid"><div class="phero__copy">
{chip("THE FOUNDER")}<h1 class="phero__h rv">Meet <em>Mohamed Refaat</em></h1><p class="phero__p rv">Not a software consultant. An operator who happens to know the software.</p>
<p class="mono career__l rv">CAREER ACROSS</p><ul class="career rv">{career}</ul></div>
<div class="founder__visual rv"><div class="ftile ftile--back"></div><div class="ftile ftile--mid"></div><figure class="ftile ftile--photo"><img src="{c.asset("img/founder.webp")}" alt="Mohamed Refaat, founder of OPSMO"></figure>
<div class="founder__tag"><b>Mohamed Refaat</b><span>FOUNDER &amp; PRINCIPAL CONSULTANT</span></div></div></div></section>
{sec('<div class="story">' + head("THE STORY","", "A decade inside commercial teams, sales operations and technology, and one conclusion that shaped OPSMO.") + f'<div class="story__body">{story}</div></div>', "sec--paper")}
{sec(head("ELSEWHERE","Read, verify, connect.") + f'<div class="grid3">{else_}</div>')}
{sec(head("ZOHO","Zoho product links","The Zoho editions we implement most often. Choose the one that fits your team; we architect and implement from there.") + '<p class="mono acc">OUTBOUND PRODUCT LINKS</p>' + f'<div class="grid4">{zl}</div><p class="fine rv">Referral links: OPSMO may earn a commission if you subscribe through a Zoho link on this page, at no extra cost to you. Our recommendations are the same either way.</p>', "sec--paper")}
{cta_block(c, eyebrow="WORK WITH OPSMO", h="Let's look at how your business actually operates.", p="A short conversation is usually enough to identify where the systems and the process stop matching.")}'''

def opts(xs, placeholder=None):
    return (f'<option value="">{E(placeholder)}</option>' if placeholder else "") + "".join(f"<option>{E(x)}</option>" for x in xs)
SERVICES = [SOL_META[s][1] for s in SOL_ORDER]
INDUSTRIES = [IND_META[s][0] for s in IND_ORDER]

def render_contact(c):
    return f'''<section class="phero phero--form"><canvas class="trails" aria-hidden="true"></canvas><div class="wrap formgrid">
<div class="phero__copy">{chip("REQUEST AN ASSESSMENT · RESPONSE WITHIN ONE BUSINESS DAY")}<h1 class="phero__h rv">{em_last("Let's find out what's slowing your business down.")}</h1>
<p class="phero__p rv">Tell us how your business operates today. We'll help you identify what needs to change, and what can stay as it is.</p>
<div class="next rv"><span class="mono acc">WHAT HAPPENS NEXT</span>
<div><b>Within one business day</b><p>A person reviews your request, not a routing queue.</p></div>
<div><b>A discovery call</b><p>30–45 minutes to understand the process and the constraints.</p></div>
<div><b>A written recommendation</b><p>Scope, approach and indicative range before any commitment.</p></div></div>
<div class="prefer rv"><b>Prefer to talk first?</b><p>Book a discovery call and we'll confirm a time by email.</p>{btn(c,"Book a Discovery Call","/book","line",True)}</div></div>
<form class="form wizard rv" id="leadForm" novalidate data-steps="3">
<div class="wizard__bar"><span class="mono" id="stepLbl">1/3</span><i><s id="stepFill"></s></i></div>
<fieldset class="step is-on" data-step="1">
<div class="field"><label for="c1">FULL NAME *</label><input id="c1" name="name" autocomplete="name" required></div>
<div class="field"><label for="c2">BUSINESS EMAIL *</label><input id="c2" name="email" type="email" autocomplete="email" required></div>
<div class="field"><label for="c3">COMPANY *</label><input id="c3" name="company" autocomplete="organization" required></div>
<div class="field"><label for="c4">WEBSITE</label><input id="c4" name="website" type="url" placeholder="https://"></div>
<div class="field"><label for="c5">COUNTRY</label><select id="c5" name="country">{opts(["United Arab Emirates","Saudi Arabia","Qatar","Kuwait","Egypt","United Kingdom","Other"])}</select></div>
<div class="field"><label for="c6">PHONE</label><input id="c6" name="phone" type="tel" autocomplete="tel"></div></fieldset>
<fieldset class="step" data-step="2">
<div class="field"><label for="c7">INDUSTRY</label><select id="c7" name="industry">{opts(INDUSTRIES,"Select industry")}</select></div>
<div class="field"><label for="c8">COMPANY SIZE</label><select id="c8" name="size">{opts(["1–10 people","11–50 people","51–200 people","201–500 people","500+ people"],"Select size")}</select></div>
<div class="field field--full"><label for="c9">CRM / SYSTEMS IN USE</label><input id="c9" name="systems"></div>
<div class="field"><label for="c10">NUMBER OF USERS</label><input id="c10" name="users" type="number" min="0"></div>
<div class="field"><label for="c11">TIMELINE</label><select id="c11" name="timeline">{opts(["Immediately","1–3 months","3–6 months","6–12 months","Exploring options"],"Select timeline")}</select></div></fieldset>
<fieldset class="step" data-step="3">
<div class="field field--full"><label for="c12">REQUIRED SERVICE *</label><select id="c12" name="service" required>{opts(SERVICES,"Select a service")}</select></div>
<div class="field field--full"><label for="c13">MAIN OPERATIONAL CHALLENGE *</label><textarea id="c13" name="challenge" rows="3" required></textarea></div>
<div class="field"><label for="c14">INDICATIVE BUDGET (OPTIONAL)</label><select id="c14" name="budget">{opts(["To be discussed","Under 25k","25k – 75k","75k – 200k","200k+"])}</select></div>
<div class="field field--full"><label for="c15">ADDITIONAL REQUIREMENTS</label><textarea id="c15" name="additional" rows="2"></textarea></div></fieldset>
<div class="wizard__nav"><button type="button" class="btn btn--line btn--sm" id="wBack">Back</button><button type="button" class="btn btn--fire btn--sm" id="wNext">Continue {ARROW}</button><button type="submit" class="btn btn--fire btn--sm" id="wSubmit">Submit request {ARROW}</button></div>
<p class="fine">By submitting you agree to our <a class="ul" {a_attrs(c,"/privacy")}>privacy policy</a>. We use your details only to respond to this request.</p>
<p class="form__msg" role="status" aria-live="polite"></p>
<p class="fine">Submissions are stored securely and visible only to the OPSMO team. CRM synchronisation is queued and shown as pending until the integration is configured.</p></form></div></section>'''

def render_book(c):
    tzs = ["Asia/Dubai","Asia/Riyadh","Asia/Qatar","Africa/Cairo","Europe/London","Europe/Berlin","America/New_York","Asia/Kolkata","Asia/Singapore"]
    cover = "".join(f'<li><span class="mono acc">0{i+1}</span><div><b>{E(n)}</b><p>{E(d)}</p></div></li>' for i,(n,d,_) in enumerate(METHOD[:3]))
    return f'''<section class="phero phero--form"><canvas class="trails" aria-hidden="true"></canvas><div class="wrap formgrid">
<div class="phero__copy">{chip("DISCOVERY CALL · 30–45 MINUTES")}<h1 class="phero__h rv">{em_last("A focused conversation about how your business actually runs.")}</h1>
<p class="phero__p rv">No pitch deck. We map the current process, identify where the friction is, and tell you honestly whether a system change would help.</p>
<div class="next rv"><span class="mono acc">WHAT WE'LL COVER</span><ol class="cover">{cover}</ol></div>
<div class="prefer rv"><b>Not ready for a call?</b><p>Send a written request instead and we'll come back with a scoped recommendation.</p>{btn(c,"Request an assessment","/contact","line",True)}</div></div>
<form class="form rv" id="bookForm" novalidate>
<p class="para">Tell us what you're evaluating or what you'd like to improve. Choose a preferred time and OPSMO will confirm your consultation by email.</p>
<p class="notice mono">NO CALENDAR PROVIDER IS CONNECTED YET. THE TIME YOU CHOOSE IS A REQUEST, NOT A CONFIRMED SLOT.</p>
<div class="field field--full"><label for="b1">MEETING TYPE *</label><select id="b1" name="meeting" required>{opts(["Discovery call, 30 minutes","Software selection consultation","Operational assessment, 45 minutes","Implementation review, 45 minutes","Managed services review, 30 minutes","Zoho One consultation","Zoho Desk consultation"])}</select></div>
<div class="field field--full"><label for="b2">SERVICE CATEGORY</label><select id="b2" name="service">{opts(SERVICES,"Select a service")}</select></div>
<div class="field"><label for="b3">PREFERRED DATE *</label><input id="b3" name="date" type="date" required></div>
<div class="field"><label for="b4">PREFERRED WINDOW *</label><select id="b4" name="window" required>{opts(["09:00 – 11:00","11:00 – 13:00","13:00 – 15:00","15:00 – 17:00","17:00 – 19:00"])}</select></div>
<div class="field field--full"><label for="b5">TIMEZONE *</label><select id="b5" name="tz" required>{opts(tzs)}</select></div>
<div class="field"><label for="b6">FULL NAME *</label><input id="b6" name="name" autocomplete="name" required></div>
<div class="field"><label for="b7">BUSINESS EMAIL *</label><input id="b7" name="email" type="email" autocomplete="email" required></div>
<div class="field"><label for="b8">COMPANY *</label><input id="b8" name="company" autocomplete="organization" required></div>
<div class="field"><label for="b9">PHONE</label><input id="b9" name="phone" type="tel" autocomplete="tel"></div>
<div class="field field--full"><label for="b10">WHAT WOULD YOU LIKE TO COVER?</label><textarea id="b10" name="cover" rows="3"></textarea></div>
<button class="btn btn--fire btn--full" type="submit">Request this call {ARROW}</button><p class="form__msg" role="status" aria-live="polite"></p></form></div></section>'''

# ---------------------------------------------------------------- home
REALITY = [
 ("The CRM is deployed, but the team works around it.","Adoption is a design problem. We rebuild stages, fields and views around how your sellers actually qualify and close."),
 ("Leads arrive from several channels and disappear between them.","We consolidate capture, deduplicate at source, and enforce assignment and response-time rules automatically."),
 ("Spreadsheets, exports and reminders are holding the process together.","Repetitive routing, approvals, notifications and follow-ups move into governed workflow automation."),
 ("Applications don't talk to each other, so data is re-typed.","We design the integration layer: what syncs, in which direction, how conflicts resolve, and how failures are caught."),
 ("Reporting takes days and still doesn't reconcile.","One governed data model with definitions leadership agrees on, then dashboards built on top of it."),
 ("Sales and customer journeys have no clear ownership or stage logic.","We architect the commercial process end to end: pipeline, lifecycle, service levels and handoffs."),
 ("Automation breaks quietly and someone has to babysit it.","Every workflow ships with logging, error paths and monitoring, plus a documented change process."),
 ("Technology spend rises without measurable operational improvement.","We define the operating outcome first, then measure adoption and process performance against it."),
]
def render_home(c):
    stacks = [("Zoho","STACK: ZOHO_ONE","/platforms/zoho"),("Salesforce","STACK: SALESFORCE","/platforms/salesforce"),("Odoo","STACK: ODOO_ERP","/platforms/odoo"),
              ("Automation & Integration","STACK: N8N_API","/platforms/automation-integration"),("Analytics & BI","STACK: POWER_BI","/platforms/analytics"),("Custom & API","INTEGRATION LAYER","/platforms")]
    stack_html = "".join(f'<a class="stk rv" {a_attrs(c,u)}><b>{E(n)}</b><span class="mono">{E(t)}</span>{ARROW}</a>' for n,t,u in stacks)
    real = "".join(f'<article class="fcard"><span class="fcard__n">0{i+1}</span><h3>{E(p)}</h3><p><span class="mono acc">OPSMO ·</span> {E(f)}</p></article>' for i,(p,f) in enumerate(REALITY))
    # explorer
    sol_data = []
    for s in SOL_ORDER:
        sys_, name, short, desc, img = SOL_META[s]
        bullets = SS_BULLETS if s == "software-selection" else (ZD_SCOPE if s == "zoho-desk-implementation" else SOL[s]["scope"][:4])
        sol_data.append({"sys":sys_,"name":name,"short":short,"desc":desc,"img":c.asset("img/"+img+".webp"),"href":c.href("/solutions/"+s),"bul":bullets})
    tabs = "".join(f'<button class="etab{" is-on" if i==0 else ""}" role="tab" aria-selected="{"true" if i==0 else "false"}" data-i="{i}"><span>{i+1:02d}</span>{E(d["short"])}</button>' for i,d in enumerate(sol_data))
    d0 = sol_data[0]
    career = "".join(f"<li>{E(x)}</li>" for x in CAREER)
    msteps = method_steps(True)
    mimgs = ["workshop","sme","office","servers","monitor","analytics"]
    return f'''
<section class="hero" id="top"><canvas class="trails" aria-hidden="true"></canvas>
<div class="wrap hero__grid"><div class="hero__copy">
<p class="chip rv">COMMERCIAL OPERATIONS <b>|</b> DIGITAL TRANSFORMATION</p>
<h1 class="hero__h" id="heroH"><span class="ln"><span>Your business</span></span><span class="ln"><span>doesn't need</span></span><span class="ln"><span>more software.</span></span><span class="ln ln--serif"><span><em>It needs systems</em></span></span><span class="ln ln--serif"><span><em>that work.</em></span></span></h1>
<p class="hero__sub rv">OPSMO helps companies choose, implement and connect the software behind sales, customer support and daily operations. We help you compare options, set up the right tools and make them work together.</p>
{btns(c,[("Book a Consultation","/book"),("See How We Help You Choose","#software-selection")])}</div>
<div class="stack" id="stack" aria-label="Workflow examples"><span class="stack__label mono">WORKFLOW EXAMPLES</span>
<div class="tile tile--photo" data-depth="1"><img src="{c.asset("img/hero.webp")}" alt="" fetchpriority="high"></div>
<div class="tile tile--wf" data-depth="3" style="--x:-4%;--y:6%"><span class="mono acc">WORKFLOW EXAMPLE</span><b>New enquiry assigned</b><span class="mono">CRM · ROUND ROBIN</span><i class="wf__ok"></i></div>
<div class="tile tile--wf" data-depth="2" style="--x:58%;--y:40%"><span class="mono acc">WORKFLOW EXAMPLE</span><b>Support ticket routed</b><span class="mono">ZOHO DESK · SLA</span><i class="wf__ok"></i></div>
<div class="tile tile--wf" data-depth="4" style="--x:6%;--y:78%"><span class="mono acc">WORKFLOW EXAMPLE</span><b>Invoice created after approval</b><span class="mono">FINANCE · HANDOFF</span><i class="wf__ok"></i></div>
</div></div></section>

<section class="sec" id="ecosystem"><div class="wrap eco">
<div>{chip("TECHNOLOGY ECOSYSTEM")}<h2 class="h2 rv">{em_last("The right technology. Built around your business.")}</h2>
<p class="lead rv">We are technology-independent. The platform follows the operating requirement, and we will tell you when you don't need a new one.</p>
<p class="note rv"><b>Zoho:</b> our founder was the first Egyptian hire at Zoho and the first team member in Zoho Egypt.</p></div>
<div class="stks">{stack_html}</div></div></section>

<section class="reality" id="reality"><div class="reality__pin"><img class="reality__bg" src="{c.asset("img/hero.webp")}" alt=""><canvas class="trails" data-dark="1" aria-hidden="true"></canvas>
<div class="reality__inner"><div class="wrap reality__head"><div>{chip("THE REALITY · 08 COMMON FAILURE MODES", True)}<h2 class="h2 h2--light">{em_last("Disconnected systems. Disconnected teams. Lost opportunities.")}</h2></div>
<p class="reality__p">Most operational problems aren't software problems. They're design gaps: systems that were installed rather than architected, and processes no one owns end to end.</p></div>
<div class="hscroll"><div class="htrack" id="htrack">{real}</div></div><div class="wrap hbar"><span id="hbar"></span></div></div></div></section>

<section class="sec sec--paper" id="software-selection"><div class="wrap">
{head("SOFTWARE SELECTION · SIX STAGES","From software shortlist to a decision your team can stand behind.","Choosing software takes time. Your team has to agree on what it needs, attend demos, compare pricing, test integrations and work out who will run the system after launch. OPSMO helps you see which option fits, what it will cost and what it takes to roll out.")}
{stages_html()}{tools_html(c)}</div></section>

<section class="sec" id="solutions"><div class="wrap">
<div class="sechead sechead--split"><div>{chip("WHAT WE ACTUALLY DO")}<h2 class="h2 rv">{em_last("We build the systems behind better operations.")}</h2></div>
<div><p class="lead rv">Each solution is an operating capability, not a licence sale. Pick a discipline to see what it covers.</p><a class="link rv" {a_attrs(c,"/solutions")}>ALL 10 SOLUTIONS {ARROW}</a></div></div>
<div class="explorer rv" data-sol='{E(json.dumps(sol_data))}' data-book="{E(c.href("/book"))}"><div class="explorer__tabs" role="tablist" aria-label="OPSMO solutions">{tabs}</div>
<div class="explorer__panel" id="solPanel" role="tabpanel"></div></div></div></section>

<section class="sec sec--paper" id="zoho-one"><div class="wrap zoho">
<div>{chip("FEATURED PLATFORM · ZOHO ONE")}<h2 class="h2 rv">Zoho One: <em>The Operating System for Businesses</em></h2>
<p class="lead rv">Zoho One brings sales, customer support, finance, marketing and operations apps into one suite. OPSMO helps you choose which apps to start with, configure them around your processes and roll them out in phases.</p>
{btns(c,[("Book a Zoho One Consultation","/book"),("Explore Zoho One on Zoho",ZOHO_REF)])}
<p class="fine rv"><span class="mono acc">OPSMO REFERRAL LINK ·</span> OPSMO may earn a commission, at no extra cost to you.</p></div>
<div class="zflow rv"><span class="mono acc">WORKFLOW EXAMPLE</span><p>Sales closes a deal in Zoho CRM. Finance invoices through Zoho Books, and support can access relevant customer history in Zoho Desk. OPSMO configures the handoffs, permissions and reporting.</p>
<div class="zflow__row"><span>ZOHO CRM</span><i></i><span>ZOHO BOOKS</span><i></i><span>ZOHO DESK</span></div><span class="mono zflow__foot">ONE CUSTOMER RECORD · CONNECTED HANDOFFS</span></div></div></section>

<section class="sec" id="method"><div class="wrap">
{head("HOW WE OPERATE · METHODOLOGY","From business challenges to fully operational systems.","Six stages, each with defined deliverables. You always know what is being produced and what decision comes next.")}
<div class="method"><div class="method__visual"><div class="mstack" id="mstack">{"".join(f'<img src="{c.asset("img/"+m+".webp")}" alt=""{" class=is-on" if i==0 else ""} loading="lazy">' for i,m in enumerate(mimgs))}<span class="mstack__badge mono" id="mBadge">01 / 06 · Diagnose</span></div></div>
<div>{msteps}{btn(c,"See how an engagement runs","/approach","line")}</div></div></div></section>

<section class="sec sec--paper founder" id="founder"><div class="wrap founder__grid">
<div class="founder__visual rv"><div class="ftile ftile--back"></div><div class="ftile ftile--mid"></div><figure class="ftile ftile--photo"><img src="{c.asset("img/founder.webp")}" alt="Mohamed Refaat, founder of OPSMO" loading="lazy"></figure><div class="founder__tag"><b>Mohamed Refaat</b><span>FOUNDER &amp; PRINCIPAL CONSULTANT</span></div></div>
<div class="founder__copy">{chip("THE FOUNDER")}<h2 class="h2 rv">An operator who knows the software, <em>not a reseller.</em></h2>
<p class="rv">Mohamed Refaat was the first Egyptian hire at Zoho and the first team member in Zoho Egypt. That experience sits behind every system OPSMO designs: what the platform can do, what it will take to roll out, and where a business is better served by the tools it already owns.</p>
<p class="mono career__l rv">CAREER ACROSS</p><ul class="career rv">{career}</ul>
{btns(c,[("Read the founder story","/founder"),("See the success stories","/success-stories")])}</div></div></section>

<section class="sec" id="faq"><div class="wrap faq"><div>{chip("FAQ · BEFORE YOU CHOOSE")}<h2 class="h2 rv">{em_last("Questions we hear before a decision.")}</h2><p class="lead rv">How we work before a vendor is chosen, and what to compare beyond the licence price.</p></div>{faq_html(FAQ["choose"])}</div></section>
{cta_block(c, eyebrow="CONSULTATION", h="Tell us what you're evaluating.", p="Bring the tools you are comparing, or the process that isn't working. We'll tell you what is worth changing and what can stay.")}'''

# ---------------------------------------------------------------- layout
def nav_html(c):
    def dd(label, items, all_href, all_label, wide=False):
        lis = "".join(f'<a {a_attrs(c,u)}><b>{E(n)}</b><span>{E(t)}</span></a>' for u,n,t in items)
        return f'''<div class="dd"><button class="dd__btn" aria-expanded="false">{label}<svg class="i" aria-hidden="true"><use href="#i-down"/></svg></button>
<div class="dd__menu{" dd__menu--wide" if wide else ""}"><div class="dd__grid">{lis}</div><a class="dd__all mono" {a_attrs(c,all_href)}>{all_label} {ARROW}</a></div></div>'''
    sols = [("/solutions/"+s, SOL_META[s][2], (SS_TAGLINE if s=="software-selection" else (SOL[s]["tagline"] if s in SOL else "Give every customer request a clear owner."))) for s in SOL_ORDER]
    plats = [("/platforms/"+s, n, t) for s,n,_,t in PLATS]
    inds = [("/industries/"+s, IND_META[s][0], IND_META[s][1]) for s in IND_ORDER]
    comp = [(u,n,t) for u,n,t in COMPANY]
    links = (dd("Solutions", sols, "/solutions", "All solutions", True) + dd("Platforms", plats, "/platforms", "All platforms") +
             dd("Industries", inds, "/industries", "All industries", True) +
             f'<a class="nav__a" {a_attrs(c,"/managed-services")}>Managed Services</a><a class="nav__a" {a_attrs(c,"/insights")}>Insights</a>' +
             dd("Company", comp, "/about", "About OPSMO"))
    sheet_groups = [("Solutions", sols, "/solutions"), ("Platforms", plats, "/platforms"), ("Industries", inds, "/industries"), ("Company", comp, "/about")]
    sheet = "".join(f'<details><summary>{g}</summary>' + "".join(f'<a {a_attrs(c,u)}>{E(n)}</a>' for u,n,_ in it) + f'<a class="mono" {a_attrs(c,h)}>View all</a></details>' for g,it,h in sheet_groups)
    sheet += f'<a class="sheet__a" {a_attrs(c,"/managed-services")}>Managed Services</a><a class="sheet__a" {a_attrs(c,"/insights")}>Insights</a>' + btn(c,"Book a Consultation","/book")
    return f'''<header class="nav" id="nav"><div class="nav__bar">
<a {a_attrs(c,"/")} class="nav__logo" aria-label="OPSMO home"><img class="logo-l" src="{c.asset("img/logo.png")}" alt="opsmo.tech" width="320" height="48"><img class="logo-d" src="{c.asset("img/logo-white.png")}" alt="" width="320" height="48"></a>
<nav class="nav__links" aria-label="Primary">{links}</nav>
<button class="theme" id="themeBtn" type="button" aria-label="Switch to dark theme"><svg class="i i--sun" aria-hidden="true"><use href="#i-sun"/></svg><svg class="i i--moon" aria-hidden="true"><use href="#i-moon"/></svg></button>
<a class="btn btn--fire btn--sm nav__cta" {a_attrs(c,"/book")}>Book a Consultation {ARROW}</a>
<button class="nav__burger" id="burger" aria-label="Open menu" aria-expanded="false"><i></i><i></i></button></div>
<div class="nav__sheet" id="sheet">{sheet}</div></header>'''

def footer_html(c):
    col = lambda title, items: f'<div><h4 class="mono">{title}</h4>' + "".join(f'<a {a_attrs(c,u)}>{E(n)}</a>' for u,n in items) + "</div>"
    sols = [("/solutions/"+s, SOL_META[s][2]) for s in SOL_ORDER]
    plats = [("/platforms/"+s, n) for s,n,_,_ in PLATS]
    inds = [("/industries/"+s, IND_META[s][0]) for s in IND_ORDER[:5]]
    comp = [("/about","About OPSMO"),("/founder","The Founder"),("/approach","Our Approach"),("/managed-services","Managed Services"),("/packages","Implementation Packages"),("/insights","Insights"),("/contact","Contact")]
    return f'''<footer class="foot"><div class="wrap foot__grid"><div class="foot__brand">
<img src="{c.asset("img/logo-white.png")}" alt="opsmo.tech" class="foot__logo" width="300" height="45"><p>{E(FOOTER_TAG)}</p>{btn(c,"Book a Consultation","/book","fire",True)}</div>
<div class="foot__cols">{col("SOLUTIONS", sols)}{col("PLATFORMS", plats)}{col("INDUSTRIES", inds)}{col("COMPANY", comp)}</div></div>
<div class="wrap foot__base"><span class="mono">© 2026 OPSMO · COMMERCIAL OPERATIONS · DIGITAL TRANSFORMATION</span>
<span class="foot__legal"><a class="mono" {a_attrs(c,"/privacy")}>PRIVACY</a><a class="mono" {a_attrs(c,"/terms")}>TERMS</a><a class="mono" {a_attrs(c,LINKEDIN)}>LINKEDIN</a><span class="sys"><i></i><span class="mono">SYSTEMS OPERATIONAL</span></span></span></div>
<p class="wrap foot__credit">Photography: Unsplash.</p></footer>'''

SPRITE = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></symbol>
<symbol id="i-ext" viewBox="0 0 24 24"><path d="M7 17L17 7M9 7h8v8"/></symbol>
<symbol id="i-down" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></symbol>
<symbol id="i-sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></symbol>
<symbol id="i-moon" viewBox="0 0 24 24"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></symbol>
</defs></svg>'''

THEME_BOOT = """<script>(function(){try{var q=new URLSearchParams(location.search).get('theme');var t=q||localStorage.getItem('opsmo-theme')||'light';if(q)localStorage.setItem('opsmo-theme',q);document.documentElement.dataset.theme=t==='dark'?'dark':'light';}catch(e){document.documentElement.dataset.theme='light';}})();</script>"""

def page(c, title, body, desc="OPSMO helps companies choose, implement and connect the software behind sales, customer support and daily operations."):
    return f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta name="theme-color" content="#0B111E">
{THEME_BOOT}
<link rel="icon" href="{c.asset("img/mark.png")}" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,500..900&family=Instrument+Serif:ital@0;1&family=Manrope:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{c.asset("css/style.css")}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a><div class="progress" aria-hidden="true"><span id="progressBar"></span></div>
{nav_html(c)}
<main id="main">{body}</main>
{footer_html(c)}
{SPRITE}
<script src="{c.asset("js/main.js")}" defer></script>
</body></html>'''

# ---------------------------------------------------------------- build
def write(route, title, body, desc=None):
    c = Ctx(route)
    out_dir = OUT if route == "/" else os.path.join(OUT, route.strip("/"))
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w") as f:
        f.write(page(c, title, body(c), desc) if desc else page(c, title, body(c)))
    return route

def md_route(rel):
    p = rel[:-3]
    p = p[:-6] if p.endswith("/index") else p
    return "/" + p

def main():
    routes = []
    routes.append(write("/", "OPSMO, Commercial Operations & Digital Transformation", render_home))
    cdir = os.path.join(HERE, "content")
    for root, _, files in os.walk(cdir):
        for fn in files:
            if not fn.endswith(".md"): continue
            rel = os.path.relpath(os.path.join(root, fn), cdir)
            route = md_route(rel)
            full = os.path.join(root, fn)
            if rel.startswith("insights/") and fn != "index.md":
                meta, _ = parse_md(full)
                routes.append(write(route, meta["title"], lambda c, f=full: render_article(c, f), meta["deck"]))
                continue
            meta, body = parse_md(full)
            if "{{founderpage}}" in body:
                routes.append(write(route, meta["title"], render_founder)); continue
            routes.append(write(route, meta["title"], lambda c, m=meta, b=body: render_body(c, m, b)))
    for s in SOL:
        routes.append(write("/solutions/" + s, SOL[s]["doc"], lambda c, s=s: render_solution(c, s), SOL[s]["tagline"]))
    for s in IND:
        routes.append(write("/industries/" + s, IND[s]["doc"], lambda c, s=s: render_industry(c, s), IND[s]["tagline"]))
    routes.append(write("/contact", "Contact & Operational Assessment | OPSMO", render_contact))
    routes.append(write("/book", "Book a Discovery Call | OPSMO", render_book))
    # 404
    c = Ctx("/")
    open(os.path.join(OUT, "404.html"), "w").write(page(c, "Page not found | OPSMO", f'<section class="phero"><div class="wrap"><div class="phero__copy">{chip("404")}<h1 class="phero__h">This page <em>isn\'t here.</em></h1><p class="phero__p">The link may be out of date.</p>{btns(c,[("Back to home","/"),("Book a Consultation","/book")])}</div></div></section>').replace('href="./', 'href="/').replace('src="assets', 'src="/assets').replace('href="assets', 'href="/assets'))
    print(len(routes), "pages")
    print("\n".join(sorted(routes)))

if __name__ == "__main__":
    main()
