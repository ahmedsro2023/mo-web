#!/usr/bin/env python3
"""OPSMO v5 — new dark identity, Zoho-led storytelling, SEO, wanasapps-style footer.
Reuses the content + renderers from build.py and overrides layout pieces."""
import os, re, json, html
import build as B
from build import E, ARROW, EXT, btn, btns, chip, em_last, sec, head, faq_html, a_attrs, Ctx, SOL_META, SOL_ORDER, SOL, IND, IND_ORDER, IND_META, PLATS, SS_BULLETS, ZD_SCOPE
from shared import FAQ, LINKEDIN, ZOHO_REF, METHOD

SITE = "https://opsmo.tech"
PHONE = "+971 58 596 4224"; PHONE_RAW = "971585964224"
WA = f"https://wa.me/{PHONE_RAW}?text=" + "Hi%20OPSMO%2C%20I%27d%20like%20to%20talk%20about%20our%20systems."
UAE_STORIES = "https://uaestories.com/how-mohamed-refaat-built-smarter-businesses/"
LI_RECS = "https://www.linkedin.com/in/mo-rashwan/details/recommendations/"
ZOHO = {"one": "https://go.zoho.com/9L1", "crm": "https://go.zoho.com/JUB4", "desk": "https://go.zoho.com/yTcH", "all": "https://go.zoho.com/D8l"}
DEFAULT_DESC = "OPSMO designs, implements and runs Zoho One and CRM systems for UAE and GCC businesses — led by Mohamed Refaat, the first Egyptian hire at Zoho."

VIDEOS = [
 ("7500105370468675585", "v/video1.webp", "1:23", "Most companies don't have a software problem.", "Zoho hired him in Dubai and relocated him to Egypt as its first Egyptian employee. Why CRM is only the door."),
 ("7460259360573808641", "v/video2.webp", "3:14", "A message to Zoho — and the whole ecosystem.", "Partners, developers, consultants and operators: what made Zoho different was never the software."),
 ("7515661274500947968", "v/video3.webp", "1:51", "Once at Zoho, always carrying the Zoho mindset.", "Turning strategy into execution, and execution into results."),
]
CLIENT_LOGOS = [("propertyfinder-w","Property Finder",""),("propspace-w","PropSpace",""),("r1-w","R1 Performance","tall"),("elnaggar-w","Elnaggar & Partners",""),
                ("ndc-w","NDC Portal",""),("twaasol-w","TWAASOL Connect",""),("heale-w","heale","short"),("lucky-w","lucky","tall"),("fawry","Fawry MSME Finance","chip")]

CASES = [
 dict(slug="propspace", logo="propspace-w", name="PropSpace", sector="PropTech · Real estate", k="Reduced complexity. Increased visibility. Scaled revenue.", rev="650K+ USD", sub="annual revenue",
      frm=["Salesforce","Tableau","NetSuite","Zendesk","Workplace","Slack","Zapier","DocuSign"],
      ch="Eight separate subscriptions and heavy customisation across them made the setup expensive to run and impractical to scale.",
      so="A unified revenue operating system on Zoho One, replacing the patchwork of tools.",
      goal="Run sales, online subscriptions, support and finance in one place — with every client conversation, online and offline, in a single CRM.",
      take=["Lower running costs", "Simpler workflows", "One scalable operating system"]),
 dict(slug="elnaggar", logo="elnaggar-w", name="Elnaggar & Partners", sector="Legal", k="Transforming Elnaggar & Partners with Zoho One", rev="500K+ USD", sub="annual revenue generated",
      frm=["Excel","Paper files","WhatsApp"],
      ch="Client onboarding, due diligence and proposal approvals ran on Excel, paper files and WhatsApp — with poor tracking and constant follow-ups.",
      so="Zoho One with a fully automated deal lifecycle: Qualification → KYC → Due diligence → Proposal → Engagement letter → Proforma → Payment → Close. Every step tracked and approved through custom workflows.",
      goal="Digitise the full client engagement, from KYC and compliance to engagement letter and payment, with accuracy, traceability and faster closes.",
      take=["Client lifecycle centralised in one CRM", "Fewer manual errors and delays", "Stronger compliance and documentation flow", "Faster time-to-close"]),
 dict(slug="r1-performance", logo="r1-w", name="R1 Performance", sector="Automotive", k="From Excel & WhatsApp to one platform", rev="4M+ AED", sub="annual recurring revenue",
      frm=["Excel","WhatsApp"],
      ch="Operations ran on Excel and WhatsApp, causing delays, errors and no room to scale. Disconnected tools drove costs up.",
      so="Zoho One with a custom blueprint for the full service cycle — diagnosis, estimates, payments, parts, repairs, QC and delivery — in one platform.",
      goal="Centralise every business function in one streamlined system for control, efficiency and scale.",
      take=["Lower costs and less manual work", "Full operational visibility", "Scalable, digital-first operations", "4M+ AED annual recurring revenue"]),
 dict(slug="fawry", logo="fawry", name="Fawry Microfinance", sector="Financial services", k="From fragmented operations to one scalable lending platform", rev="2.7M+ USD", sub="annual revenue",
      frm=["3CX","Outlook","Excel","WhatsApp","SurveyMonkey"],
      ch="Loan processing was fragmented across tools, and data was hard to manage or trust.",
      so="One secure, connected lending operation on Zoho, giving Fawry Microfinance a platform it can scale on.",
      goal="Centralise data and processes on a single platform that is easy to access and efficient to run.",
      take=["Transformed workflows", "Better decision-making", "Greater capacity to serve clients"]),
]
SECTORS = [("r1-w","4M+ AED ARR","Automotive"),("elnaggar-w","500K+ USD ARR","Legal"),("fawry","2M+ USD ARR","Financial services"),("ndc-w","4M+ USD ARR","Travel & tourism"),
           ("propspace-w","650K+ USD ARR","PropTech · real estate"),("twaasol-w","30M+ USD revenue","IT services & consulting"),("lucky-w","2M+ USD revenue","Financial services")]

# ---- client confidentiality: set True to show client names and sharp logos again
SHOW_CLIENT_NAMES = True
PUBLIC_LOGOS = {"propertyfinder-w", "propspace-w", "zohoone-w", "zohoone-c", "uaestories"}   # employers / public partners
ANON = {"elnaggar": ("Corporate law firm", "the firm"),
        "r1-performance": ("Performance car workshop", "the workshop"), "fawry": ("Microfinance lender", "the lender")}
if not SHOW_CLIENT_NAMES:
    for _k in CASES:
        if _k["slug"] not in ANON: continue
        _full, _short = ANON[_k["slug"]]
        for _f in ("k", "ch", "so", "goal"):
            _k[_f] = _k[_f].replace(_k["name"], _short).replace("Fawry Microfinance", _short)
        _k["k"] = _k["k"][0].upper() + _k["k"][1:]
        _k["name"] = _full

def logo(c, name, alt="", cls=""):
    if not SHOW_CLIENT_NAMES and name not in PUBLIC_LOGOS:
        return f'<img src="{c.asset("img/logos/"+name+".png")}" alt="" aria-hidden="true" class="{cls} is-blur" loading="lazy">'

    return f'<img src="{c.asset("img/logos/"+name+".png")}" alt="{E(alt)}" class="{cls}" loading="lazy">'

# ------------------------------------------------------------------ components
def marquee(c):
    row = "".join(logo(c, n, a, cl) for n, a, cl in CLIENT_LOGOS)
    row2 = "".join(logo(c, n, "", cl).replace('alt=""', 'alt="" aria-hidden="true"') for n, a, cl in CLIENT_LOGOS)
    return f'<div class="marquee" aria-label="Businesses OPSMO and its founder have built systems for"><div class="marquee__track">{row}{row2}</div></div>'

def videos_block(c, eyebrow="In his words", h="Hear it from the operator.", lead="Short videos from Mohamed on Zoho, operating models and why most problems aren't software problems."):
    PLAY = '<span class="vid__btn" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span>'
    def card(i, p, d, t, s, n):
        li = f"https://www.linkedin.com/feed/update/urn:li:activity:{i}/"
        poster = c.asset("img/"+p)
        if os.path.exists(os.path.join(os.path.dirname(__file__), "assets", "video", f"video{n}.mp4")):
            media = (f'<div class="vid__frame"><video class="vid__v" playsinline preload="none" poster="{poster}" src="{c.asset(f"video/video{n}.mp4")}" aria-label="{E(t)}"></video>'
                     f'<button class="vid__play" type="button" aria-label="Play video: {E(t)}">{PLAY}<span class="vid__dur mono">{d}</span></button>'
                     f'<button class="vid__sound mono" type="button" aria-label="Turn sound on" hidden>Sound on</button></div>')
        else:
            media = (f'<a class="vid__frame vid__play" href="{li}" target="_blank" rel="noopener" aria-label="Watch on LinkedIn: {E(t)}">'
                     f'<img src="{poster}" alt="" loading="lazy">{PLAY}<span class="vid__dur mono">{d}</span></a>')
        return (f'<figure class="vid rv">{media}<figcaption><h3>{E(t)}</h3><p>{E(s)}</p>'
                f'<a class="mono" href="{li}" target="_blank" rel="noopener">Comments on LinkedIn {EXT}</a></figcaption></figure>')
    cards = "".join(card(*v, n+1) for n, v in enumerate(VIDEOS))
    return sec(f'<div class="head head--split"><div>{chip(eyebrow)}<h2 class="h2 rv">{em_last(h)}</h2></div><p class="lead rv">{E(lead)}</p></div><div class="vids">{cards}</div>', "sec--videos")

PROOF = [("950","+","organisations supported"),("500","+","advised at Zoho Egypt"),("300","+","Property Finder accounts"),("164","%","Q1 retention revenue growth"),("170","+","conferences delivered"),("17"," yrs","in commercial operations")]
def proof_strip(c):
    items = "".join(f'<li class="rv"><b class="num-big">{n}{u}</b><span>{E(t)}</span></li>' for n, u, t in PROOF)
    return sec(f'<ul class="proof">{items}</ul>', "sec--proof")

def stories_block(c, full=False):
    tabs = "".join(f'<button role="tab" class="stab{" is-on" if i==0 else ""}" aria-selected="{"true" if i==0 else "false"}" aria-controls="story-{k["slug"]}" id="tab-{k["slug"]}" data-i="{i}">{logo(c,k["logo"])}<span>{E(k["name"])}</span></button>' for i, k in enumerate(CASES))
    panels = "".join(f'''<article class="sty{" is-on" if i==0 else ""}" id="story-{k["slug"]}" role="tabpanel" aria-labelledby="tab-{k["slug"]}"{"" if i==0 else " hidden"}>
<div class="sty__top"><div><p class="mono acc">{E(k["k"])}</p><p class="sty__rev">{E(k["rev"])}<small>{E(k["sub"])}</small></p></div>{logo(c,k["logo"],k["name"],"sty__logo")}</div>
<div class="flowx"><div><p class="mono dim">Previous systems</p><div class="flowx__from">{"".join(f"<span>{E(f)}</span>" for f in k["frm"])}</div></div><i class="flowx__arrow" aria-hidden="true"></i><div class="flowx__to">{logo(c,"zohoone-w","Zoho One")}</div></div>
<div class="sty__grid"><div><h4>Challenge</h4><p>{E(k["ch"])}</p></div><div><h4>Solution</h4><p>{E(k["so"])}</p></div><div><h4>Goal</h4><p>{E(k["goal"])}</p></div><div><h4>Results</h4><ul>{"".join(f"<li>{E(x)}</li>" for x in k["take"])}</ul></div></div></article>''' for i, k in enumerate(CASES))
    more = "" if full else f'<a class="link rv" {a_attrs(c,"/success-stories")}>All success stories {ARROW}</a>'
    return sec(f'''<div class="head head--split"><div>{chip("Success stories")}<h2 class="h2 rv">From Excel and WhatsApp <em>to one Zoho One system.</em></h2></div><div><p class="lead rv">Four transformations in four industries — with the same platform underneath.</p>{more}</div></div>
<div class="storybox"><div class="storybox__tabs" role="tablist" aria-label="Success stories">{tabs}</div><div class="storybox__panels">{panels}</div></div>''', "", "stories")

def portfolio_block(c):
    sect = "".join(f'<div class="rv">{logo(c,l,s)}<b>{E(v)}</b><span>{E(s)}</span></div>' for l, v, s in SECTORS)
    return sec(f'''<div class="port"><div class="port__big rv"><span class="pill"><i class="dot"></i>Track record</span><b class="port__n">$<span data-count="50">50</span>M+</b><span class="port__sub">revenue portfolio supported — real results from real businesses</span></div>
<div class="port__list rv"><h2 class="h3">The numbers behind the work</h2><ul>
<li><b><span data-count="950">950</span>+</b><span>organisations supported through transformation and growth</span></li>
<li><b><span data-count="1000">1,000</span>+</b><span>users across multi-country operations</span></li>
<li><b><span data-count="17">17</span> yrs</b><span>across revenue operations, business development, CRM and analytics</span></li>
<li><b>2009</b><span>the year Dubai became home</span></li></ul></div></div><div class="sectors">{sect}</div>''')

def zoho_refs(c):
    cards = [("one","Zoho One","45+ integrated apps on one platform — the operating system for business.",logo(c,"zohoone-c","")),
             ("crm","Zoho CRM","Pipeline, automation and forecasting for sales teams.",'<span class="zc__mark">CRM</span>'),
             ("desk","Zoho Desk","Support tickets, service levels and customer history.",'<span class="zc__mark">Desk</span>'),
             ("all","Zoho.com","Browse the full Zoho product catalogue.",'<span class="zc__mark">All</span>')]
    z = "".join(f'<a class="zc rv" href="{ZOHO[k]}" target="_blank" rel="noopener sponsored">{m}<h3>{E(t)}</h3><p>{E(d)}</p><span class="mono">Start free trial {EXT}</span></a>' for k, t, d, m in cards)
    return sec(f'''<div class="head head--split"><div>{chip("Zoho references")}<h2 class="h2 rv">Start with the edition <em>that fits your team.</em></h2></div><p class="lead rv">Start a free trial on Zoho, then let us set it up properly. Not sure which edition fits? Ask before you subscribe.</p></div>
<div class="zcards">{z}</div><div class="btnrow center">{btn(c,"Help me choose an edition","/book")}</div><p class="fine rv">Referral links: OPSMO may earn a commission if you subscribe through a Zoho link on this page, at no extra cost to you. Our recommendations are the same either way.</p>''')

def contact_paths(c, eyebrow="Next step", h="Tell us what you're evaluating.", p="Bring the tools you're comparing, or the process that isn't working. We'll tell you what is worth changing — and what can stay."):
    return f'''<section class="ctax" id="contact-paths"><div class="ctax__glow" aria-hidden="true"></div><div class="wrap">
<div class="head head--center">{chip(eyebrow)}<h2 class="h2 rv">{em_last(h)}</h2><p class="lead rv">{E(p)}</p></div>
<div class="paths">
<a class="path path--hot rv" {a_attrs(c,"/book")}><span class="mono">Recommended · 30 minutes</span><h3>Book a free consultation</h3><p>Pick a time. We map the process, the tools and the gaps — and tell you honestly whether a change would help.</p><span class="path__go">Choose a time {ARROW}</span></a>
<a class="path rv" href="{WA}" target="_blank" rel="noopener"><span class="mono">Fastest · usually same day</span><h3>Message on WhatsApp</h3><p>Send a quick note about your setup and get a direct reply from Mohamed.</p><span class="path__go">{PHONE} {EXT}</span></a>
<a class="path rv" {a_attrs(c,"/contact")}><span class="mono">Most detailed · written reply</span><h3>Request an operational assessment</h3><p>Three short steps about your systems, users and timeline. You get a scoped recommendation, not a brochure.</p><span class="path__go">Start the assessment {ARROW}</span></a>
</div></div></section>'''

# ------------------------------------------------------------------ home
REALITY = [("Excel sheets everywhere","No single source of truth. Teams work in silos across Excel, WhatsApp and email."),
           ("Approvals stuck in WhatsApp","Critical decisions wait in chat threads, and nobody can see where they're held up."),
           ("No real-time visibility","No live view of sales, cash flow, margins or team performance."),
           ("Workarounds instead of systems","Teams duplicate effort, data is unreliable, and decisions run on gut feel rather than facts.")]
LEAKS = [("Missed leads & revenue","AED 500K+","per year"),("Manual processes","25–40%","of team time"),("Decision delays","2–3 weeks","per cycle"),("Reporting accuracy","< 60%","")]
STEPS4 = [("Operator Diagnostic Sprint","We map how the business really runs — lead sources, handoffs, approvals, tools and data quality — and size the gaps."),
          ("Transformation Blueprint","Target architecture, data model and process design, agreed on paper before anything is built."),
          ("Implementation","Zoho configured, integrated, tested and adopted by the people who use it every day."),
          ("Optimisation & Growth","A monthly retainer that keeps the system healthy and improving as the business grows.")]
WS = [("CRM setup & customisation","Sales and leasing pipelines, user permissions and property / client records"),
      ("Property portal integration","Property Finder and Bayut enquiry capture into Zoho CRM"),
      ("Social media integration","Advertising lead forms connected, with source and campaign tracking"),
      ("Lead assignment & follow-up","Agent routing, duplicate checks, notifications and automated reminders"),
      ("Management visibility","Dashboards for lead sources, agent activity and sales performance"),
      ("Launch & team adoption","Integration testing, team training and 30-day post-launch support")]

MONTHS = ["J","F","M","A","M","J","J","A","S","O","N","D"]
def impact_board():
    bars = "".join(f'<span style="--i:{i}"><i></i><em>{m}</em></span>' for i, m in enumerate(MONTHS))
    steps = "".join(f'<li style="--i:{i}"><b>{t}</b><span>{d}</span></li>' for i, (t, d) in enumerate([("Day 1","Question raised"),("Day 4","Data pulled by hand"),("Day 9","Numbers disputed"),("Day 15","Meeting held"),("Day 18","Decision made")]))
    return f'''<div class="lk2" id="impactBoard">
<article class="lk lk--money"><p class="lk__k">Missed leads &amp; revenue</p><p class="lk__big"><span class="lk__cur">AED</span><b id="lkMoney">0</b><span class="lk__suf">K+</span></p><p class="lk__s">lost per year, about <b>AED 1,370 a day</b></p>
<div class="lk__bars" aria-hidden="true">{bars}</div></article>
<article class="lk lk--time"><p class="lk__k">Manual processes</p><div class="lk__donut" aria-hidden="true"><svg viewBox="0 0 120 120"><circle class="d0" cx="60" cy="60" r="50"/><circle class="d1" cx="60" cy="60" r="50"/><circle class="d2" cx="60" cy="60" r="50"/></svg><div><b>25–40%</b><span>of team time</span></div></div>
<p class="lk__s">That's <b>10 to 16 hours</b> a week, per person, on copy-paste and chasing.</p></article>
<article class="lk lk--acc"><p class="lk__k">Reporting accuracy</p><div class="lk__gauge" aria-hidden="true"><svg viewBox="0 0 200 110"><path class="g0" d="M20 100 A80 80 0 0 1 180 100"/><path class="g1" d="M20 100 A80 80 0 0 1 180 100"/><line class="g2" x1="100" y1="100" x2="100" y2="34"/><circle cx="100" cy="100" r="6"/></svg></div>
<p class="lk__mid"><b>Under 60%</b></p><p class="lk__s">Around <b>4 in 10</b> report figures can't be trusted without checking.</p></article>
<article class="lk lk--delay"><div class="lk__dh"><p class="lk__k">Decision delays</p><p class="lk__big lk__big--sm"><b>2–3</b><span class="lk__suf"> weeks per decision</span></p></div>
<ol class="lk__line">{steps}</ol></article>
</div>'''

def render_home(c):
    sol_tabs, sol_panels = "", ""
    for i, s in enumerate(SOL_ORDER):
        sys_, name, short, desc, img = SOL_META[s]
        bul = SS_BULLETS if s == "software-selection" else (ZD_SCOPE if s == "zoho-desk-implementation" else SOL[s]["scope"][:4])
        sol_tabs += f'<button class="etab{" is-on" if i==0 else ""}" role="tab" id="st-{s}" aria-controls="sp-{s}" aria-selected="{"true" if i==0 else "false"}" data-i="{i}"><span>{i+1:02d}</span>{E(short)}</button>'
        sol_panels += f'''<div class="ep ep--scr{" is-on" if i==0 else ""}" id="sp-{s}" role="tabpanel" aria-labelledby="st-{s}"{"" if i==0 else " hidden"}>
<div class="ep__stage">{screen(s)}</div>
<div class="ep__body"><h3 class="ep__h">{E(name)}</h3><p>{E(desc)}</p><ul class="ticks">{"".join(f"<li>{E(b)}</li>" for b in bul[:4])}</ul>
<div class="btnrow">{btn(c,"Explore "+short,"/solutions/"+s,"fire",True)}{btn(c,"Book a consultation","/book","line",True)}</div></div></div>'''
    reality = "".join(f'<li class="rv"><span class="pains__n mono">0{i+1}</span><div><h3>{E(t)}</h3><p>{E(d)}</p></div></li>' for i, (t, d) in enumerate(REALITY))
    leaks = "".join(f'<div class="leak rv"><span>{E(a)}</span><b>{E(b)}{f"<small>{E(s)}</small>" if s else ""}</b></div>' for a, b, s in LEAKS)
    steps = "".join(f'<li class="rv"><span class="mono">Step {i+1}</span><h3>{E(t)}</h3><p>{E(d)}</p></li>' for i, (t, d) in enumerate(STEPS4))
    ws = "".join(f'<div class="ws__row"><b>{E(a)}</b><span>{E(b)}</span></div>' for a, b in WS)
    return f'''
<section class="hero5"><div class="hero5__aura" aria-hidden="true"></div>
<div class="wrap hero5__grid"><div class="hero5__copy">
<p class="chip">Zoho One &amp; CRM · Dubai</p>
<h1 class="hero5__h" data-split>Business systems <span class="fire">that work.</span></h1>
<p class="hero5__p" data-in>Zoho, implemented by Zoho's first Egyptian hire.</p>
<div class="btnrow" data-in>{btn(c,"Book a free consultation","/book")}<a class="btn btn--line" href="{WA}" target="_blank" rel="noopener"><i class="dot"></i>WhatsApp</a></div>
<div class="hero5__ex" data-in><span class="mono dim">Ex</span><a class="ex ex--zoho" href="#zoho">Zoho</a><a class="ex" href="#career">Property Finder</a><a class="ex" href="#career">PropSpace</a><a class="ex" href="#career">Motivate Media Group</a></div>
</div>
<figure class="portrait" id="portrait"><img class="portrait__bg" src="{c.asset("img/zoho-tower.webp")}" alt="" fetchpriority="high"><div class="portrait__shade"></div>
<img class="portrait__cut" src="{c.asset("img/founder-cut.webp")}" alt="Mohamed Refaat, founder of OPSMO, in front of the Zoho tower" fetchpriority="high" width="820" height="979"></figure>
</div>{marquee(c)}</section>

<section class="zchap" id="zoho" aria-label="Zoho experience"><div class="zchap__pin"><img class="zchap__bg" src="{c.asset("img/zoho-tower.webp")}" alt="" loading="lazy"><div class="zchap__veil"></div>
<div class="wrap zchap__in"><p class="chip chip--zoho">Where the experience comes from</p>
<h2 class="zchap__word" aria-label="Zoho"><span>Z</span><span>o</span><span>h</span><span>o</span><em>.</em></h2>
<p class="zchap__lead">Hired by Zoho in Dubai. Its first employee in Egypt. Now building Zoho systems for UAE and GCC teams.</p>
<ol class="zchap__facts"><li><b>First</b><span>Egyptian hire at Zoho</span></li><li><b>First</b><span>team member in Zoho Egypt</span></li><li><b>500+</b><span>organisations advised while building Zoho's presence in Egypt</span></li><li><b>50%</b><span>growth in customer acquisition and annual revenue he contributed to</span></li></ol>
<div class="btnrow">{btn(c,"How we implement Zoho One","/platforms/zoho")}<a class="btn btn--line" href="{UAE_STORIES}" target="_blank" rel="noopener">His story on UAE Stories {EXT}</a></div></div>
<div class="zchap__rail" aria-hidden="true"><span id="zRail"></span></div></div></section>

{sec(f"""<div class="head">{chip("Track record")}<h2 class="h2 rv">Built inside the companies <em>that shaped UAE tech.</em></h2><p class="lead rv">Seventeen years across sales, business development, commercial operations and CRM — at the platform, the portal and the media group. Every claim links to where you can check it.</p></div>
<div class="bento">
<a class="bt bt--zoho rv" {a_attrs(c,"/platforms/zoho")}><div class="bt__logo">{logo(c,"zohoone-w","Zoho One")}</div><span class="bt__k mono">Zoho · Egypt</span><h3>The platform</h3><p>First Egyptian hire and first team member in Zoho Egypt. Advised 500+ organisations while helping build the market.</p><span class="bt__go mono">Zoho One implementation {ARROW}</span></a>
<a class="bt bt--pf rv" href="https://www.propertyfinder.ae/" target="_blank" rel="noopener"><div class="bt__logo">{logo(c,"propertyfinder-w","Property Finder")}</div><span class="bt__k mono">Property Finder Group · twice</span><h3>The portal</h3><div class="bt__stats"><div><b><span data-count="300">300</span>+</b><span>UAE real-estate accounts managed</span></div><div><b><span data-count="164">164</span>%</b><span>retention revenue growth in Q1</span></div></div><span class="bt__go mono">propertyfinder.ae {EXT}</span></a>
<a class="bt bt--ps rv" href="https://www.propspace.com/about" target="_blank" rel="noopener"><div class="bt__logo">{logo(c,"propspace-w","PropSpace")}</div><span class="bt__k mono">Post-acquisition transformation</span><p>Moved PropSpace from Property Finder's Salesforce environment to an integrated Zoho One operating model.</p><div class="bt__stats"><div><b><span data-count="150">150</span>+</b><span>UAE companies</span></div><div><b><span data-count="40">40</span>%</b><span>less manual effort</span></div></div><span class="bt__go mono">propspace.com {EXT}</span></a>
<a class="bt bt--mm rv" href="https://www.motivatemedia.com/" target="_blank" rel="noopener"><div class="bt__word">Motivate<br>Media Group</div><span class="bt__k mono">Media · events</span><p>Commercial work inside one of the UAE's best-known media and events groups.</p><span class="bt__go mono">motivatemedia.com {EXT}</span></a>
<div class="bt bt--stat rv"><b><span data-count="170">170</span>+</b><span>conferences planned and delivered across the UAE, Kuwait, Oman and Bahrain</span></div>
<a class="bt bt--li rv" href="{LI_RECS}" target="_blank" rel="noopener"><span class="bt__k mono">Verify</span><h3>Client recommendations</h3><p>What the people he has worked with say — on LinkedIn.</p><span class="bt__go mono">linkedin.com {EXT}</span></a>
</div>""", "", "career")}

{sec(f"""<div class="daily"><div class="head head--sticky">{chip("The daily reality")}<h2 class="h2 rv">You're not inefficient. <em>You're running a business with no operating system.</em></h2><p class="callout rv">This isn't a technology problem. It's an operations problem.</p></div><ol class="pains">{reality}</ol></div>""", "", "reality")}

<section class="sec impact"><div class="horizon" aria-hidden="true"></div><div class="wrap">
<div class="head head--center">{chip("The impact")}<h2 class="h2 rv">Every day without systems <em>is lost margin.</em></h2><p class="lead rv">We audit operational loss before we begin. This is what revenue leaks typically cost a mid-sized business.</p></div>
{impact_board()}<p class="note rv">It isn't about software. It's about operational precision. In 90 days, a competitor could remove the bottlenecks you're still firefighting.</p></div></section>

{before_after(c)}
{live_demo(c)}
{stories_block(c)}
{videos_block(c)}
{portfolio_block(c)}

<section class="sec" id="solutions"><div class="wrap">
<div class="head head--split"><div>{chip("What we do")}<h2 class="h2 rv">Ten services. <em>One connected system.</em></h2></div><div><p class="lead rv">Pick a service to see what it looks like inside your business, and what we set up.</p><a class="link rv" {a_attrs(c,"/solutions")}>All 10 solutions {ARROW}</a></div></div>
<div class="explorer rv"><div class="explorer__tabs" role="tablist" aria-label="OPSMO solutions">{sol_tabs}</div><div class="explorer__panel">{sol_panels}</div></div></div></section>

{sec(f"""<div class="head head--center">{chip("How we work")}<h2 class="h2 rv">From chaos to control <em>in 90 days.</em></h2></div><ol class="steps4" id="steps4">{steps}</ol><div class="steps4__line" aria-hidden="true"><span id="s4line"></span></div><p class="center rv"><a class="link" {a_attrs(c,"/approach")}>See the full six-stage methodology {ARROW}</a></p>""", "", "method")}
{savings_calc(c)}

{sec(f"""<div class="pack"><div class="head head--sticky">{chip("Zoho implementation & integration")}<h2 class="h2 rv">One owner, <em>from setup to adoption.</em></h2><p class="lead rv">A real-estate Zoho CRM rollout as we scope it: hands-on ownership from setup and customisation through testing, launch and team adoption — in Arabic and English.</p><div class="btnrow">{btn(c,"Scope your rollout","/book")}{btn(c,"Real estate workflow","/industries/real-estate","line")}</div></div><div class="ws rv">{ws}</div></div>""")}

{sec(f"""<div class="fgrid"><div class="fcopy">{chip("The founder")}<blockquote class="quote rv">“I do not separate strategy from <em>execution.</em>”</blockquote>
<p class="rv"><b>Mohamed Refaat</b> has spent more than a decade inside commercial teams — at Meeting Minds, Property Finder, Zoho, Motivate Media Group and PropSpace. He built OPSMO to bring commercial understanding and technical execution together.</p>
<p class="rv">Technology is the infrastructure. Business performance is the outcome.</p>
<div class="btnrow rv">{btn(c,"Read his story","/founder")}<a class="btn btn--line" href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn profile {EXT}</a></div>
<a class="press rv" href="{UAE_STORIES}" target="_blank" rel="noopener">{logo(c,"uaestories","UAE Stories")}<span>How Mohamed Refaat built smarter businesses across the UAE</span>{EXT}</a></div>
<figure class="fphoto rv"><img src="{c.asset("img/founder-cut.webp")}" alt="Mohamed Refaat" loading="lazy" width="820" height="979"><figcaption class="tag">Founder &amp; Principal Consultant</figcaption></figure></div>""", "", "founder")}

{zoho_refs(c)}
{sec(f'<div class="faq">{head("FAQ","Questions we hear before a decision.","How we work before a vendor is chosen, and what to compare beyond the licence price.")}{faq_html(FAQ["choose"])}</div>', "", "faq")}
{contact_paths(c)}'''

def render_stories_page(c):
    return f'''<section class="phero phero--img"><div class="wrap phero__grid"><div class="phero__copy">{chip("Success stories")}<h1 class="phero__h rv">Real results from <em>real businesses.</em></h1>
<p class="phero__p rv">How companies in real estate, legal, automotive and financial services moved from spreadsheets and WhatsApp to one connected Zoho One operating system.</p>{btns(c,[("Book a free consultation","/book"),("Request an Operational Assessment","/contact")])}</div>
<div class="pstack rv" aria-hidden="true"><span class="pstack__a"></span><span class="pstack__b"></span><figure><img src="{c.asset("img/zoho-tower.webp")}" alt="" fetchpriority="high"></figure></div></div></section>
{stories_block(c, full=True)}{portfolio_block(c)}{videos_block(c)}{contact_paths(c)}'''

# ------------------------------------------------------------------ overrides: CTA band
def cta_block(c, key="default", eyebrow=None, h=None, p=None, pairs=None):
    from shared import CTA
    e, hh, pp, pr = CTA[key]
    return contact_paths(c, eyebrow or e, h if h is not None else hh, p or pp)

# ------------------------------------------------------------------ nav & footer
def nav_html(c):
    sols = "".join(f'<a {a_attrs(c,"/solutions/"+x)}><b>{E(SOL_META[x][2])}</b><span>{E(B.SS_TAGLINE if x=="software-selection" else (SOL[x]["tagline"] if x in SOL else "Give every customer request a clear owner."))}</span></a>' for x in SOL_ORDER)
    main = [("/platforms/zoho","Zoho One"),("/industries","Industries"),("/success-stories","Success Stories"),("/approach","How We Work"),("/about","About")]
    links = (f'''<div class="dd"><button class="dd__btn" aria-expanded="false">Solutions<svg class="i" aria-hidden="true"><use href="#i-down"/></svg></button>
<div class="dd__menu dd__menu--wide"><div class="dd__grid">{sols}</div><a class="dd__all mono" {a_attrs(c,"/solutions")}>All solutions {ARROW}</a></div></div>''' +
             "".join(f'<a class="nav__a" {a_attrs(c,u)}>{n}</a>' for u, n in main))
    sheet = (f'<details><summary>Solutions</summary>' + "".join(f'<a {a_attrs(c,"/solutions/"+x)}>{E(SOL_META[x][2])}</a>' for x in SOL_ORDER) + f'<a class="mono" {a_attrs(c,"/solutions")}>All solutions</a></details>' +
             "".join(f'<a class="sheet__a" {a_attrs(c,u)}>{n}</a>' for u, n in main + [("/insights","Insights"),("/contact","Contact")]) + btn(c,"Book a Call","/book"))
    return f'''<header class="nav" id="nav"><div class="nav__bar">
<a {a_attrs(c,"/")} class="nav__logo" aria-label="OPSMO home"><img class="logo-l" src="{c.asset("img/opsmo-logo.png")}" alt="opsmo.tech" width="1400" height="243"><img class="logo-d" src="{c.asset("img/opsmo-logo-w.png")}" alt="" width="1400" height="243"></a>
<nav class="nav__links" aria-label="Primary">{links}</nav>
<button class="theme" id="themeBtn" type="button" aria-label="Switch theme"><svg class="i i--sun" aria-hidden="true"><use href="#i-sun"/></svg><svg class="i i--moon" aria-hidden="true"><use href="#i-moon"/></svg></button>
<a class="btn btn--fire btn--sm nav__cta" {a_attrs(c,"/book")}>Book a Call {ARROW}</a>
<button class="nav__burger" id="burger" aria-label="Open menu" aria-expanded="false"><i></i><i></i></button></div>
<div class="nav__sheet" id="sheet">{sheet}</div></header>'''

SOC = {
 "li": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.06c.53-1 1.84-2.06 3.8-2.06C20.6 8.64 21 11.2 21 14.5V21h-4v-5.7c0-1.36-.02-3.1-1.9-3.1-1.9 0-2.2 1.48-2.2 3V21H9z"/></svg>',
 "wa": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2.1 1-2.4c.3-.3.6-.3.8-.3h.6c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .6l-.4.6-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1c.2-.3.4-.2.7-.1l2 1c.3.1.5.2.5.3.1.1.1.6-.1 1.2z"/></svg>',
 "ph": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
}
def footer_html(c):
    def col(title, items):
        lis = "".join(f'<a {a_attrs(c,u)}>{E(n)}{"<span aria-hidden=true> ↗</span>" if u.startswith("http") else ""}</a>' for u, n in items)
        return f'<div class="ft__col"><h3 class="ft__h">{title}</h3>{lis}</div>'
    company = [("/about","About OPSMO"),("/about#founder","Mohamed Refaat, Founder"),("/approach","How We Work"),("/approach#packages","Packages"),("/solutions/managed-crm-operations#retainers","Monthly Support"),(LI_RECS,"Client Recommendations"),("/contact","Contact Us")]
    services = [("/solutions","All Solutions")] + [("/solutions/"+s, SOL_META[s][2]) for s in SOL_ORDER]
    explore = [("/platforms/zoho","Zoho One Implementation"),("/industries/real-estate","Zoho for Real Estate"),("/industries","Industries"),("/platforms","Salesforce, Odoo & BI"),("/success-stories","Success Stories"),("/insights","Insights"),(UAE_STORIES,"UAE Stories Feature"),(ZOHO["all"],"Zoho Products")]
    return f'''<footer class="ft"><div class="wrap">
<div class="ft__top"><div class="ft__brand"><a {a_attrs(c,"/")} aria-label="OPSMO home"><img class="logo-l" src="{c.asset("img/opsmo-logo.png")}" alt="opsmo.tech" width="1400" height="243" loading="lazy"><img class="logo-d" src="{c.asset("img/opsmo-logo-w.png")}" alt="" width="1400" height="243" loading="lazy"></a>
<p class="ft__tag">Systems that work.</p><p>We set up and run Zoho for sales, service and operations teams across the UAE and GCC. Led by Zoho's first Egyptian hire.</p>
<div class="ft__soc"><a href="{LINKEDIN}" target="_blank" rel="noopener" aria-label="LinkedIn">{SOC["li"]}</a><a href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp">{SOC["wa"]}</a><a href="tel:+{PHONE_RAW}" aria-label="Call">{SOC["ph"]}</a></div>
<a class="ft__badge" href="{UAE_STORIES}" target="_blank" rel="noopener"><img src="{c.asset("img/logos/uaestories.png")}" alt="UAE Stories" loading="lazy"><span>Featured: how Mohamed Refaat built smarter businesses across the UAE ↗</span></a></div>
<div class="ft__cols">{col("Company", company)}{col("Solutions", services)}{col("Explore", explore)}
<div class="ft__col"><h3 class="ft__h">Get in touch</h3>
<div class="office office--uae"><p class="office__t">{SOC["pin"]}<b>UAE</b><span>Dubai</span></p><a href="tel:+{PHONE_RAW}">{SOC["ph"]}{PHONE}</a><a href="{WA}" target="_blank" rel="noopener">{SOC["wa"]}WhatsApp</a><a href="{LINKEDIN}" target="_blank" rel="noopener">{SOC["li"]}Mohamed Refaat</a></div>
<div class="office office--gcc"><p class="office__t">{SOC["pin"]}<b>GCC &amp; MENA</b></p><span class="office__s">Served remotely and on-site from Dubai</span></div>
{btn(c,"Book a Call","/book","fire",True)}</div></div></div>
<div class="ft__base"><span>© 2026 OPSMO · opsmo.tech · Commercial operations &amp; digital transformation</span>
<span class="ft__legal"><a {a_attrs(c,"/privacy")}>Privacy Policy</a><a {a_attrs(c,"/terms")}>Terms of Use</a><a href="{c.asset("../sitemap.xml")}">Sitemap</a><a href="#top" class="ft__top-btn">Back to top ↑</a></span></div>
<p class="ft__fine">Logos belong to their respective owners and describe past roles and client work. Zoho, Property Finder, PropSpace and Motivate Media Group are not affiliated with OPSMO unless stated in writing. Photography: Unsplash and OPSMO.</p>
</div></footer>
<div class="hook" id="hook" role="dialog" aria-label="Message from Mohamed Refaat" aria-hidden="true">
<button class="hook__x" type="button" aria-label="Close message">×</button>
<div class="hook__head"><img src="{c.asset("img/mohamed-avatar.webp")}" alt="Mohamed Refaat" width="48" height="48"><div><b>Mohamed Refaat</b><span><i class="dot"></i>Founder · usually replies in minutes</span></div></div>
<div class="hook__msgs"><p class="hook__typing" aria-hidden="true"><i></i><i></i><i></i></p><p class="hook__m" id="hookM1"></p><p class="hook__m" id="hookM2"></p></div>
<div class="hook__cta"><a class="btn btn--fire btn--sm" {a_attrs(c,"/book")} data-hook="book">Book my free call {ARROW}</a><a class="btn btn--line btn--sm" href="{WA}" target="_blank" rel="noopener" data-hook="wa">{SOC["wa"]}WhatsApp me</a></div>
<p class="hook__fine">Free · 30 minutes · no sales pitch</p></div>
<button class="hook-fab" id="hookFab" type="button" aria-label="Chat with Mohamed" aria-expanded="false"><img src="{c.asset("img/mohamed-avatar.webp")}" alt="" width="56" height="56"><span class="hook-fab__n" aria-hidden="true">1</span><span class="hook-fab__t">Talk to Mohamed</span></button>
<div class="mbar"><a class="btn btn--fire btn--sm" {a_attrs(c,"/book")}>Book a Call</a><a class="btn btn--line btn--sm" href="{WA}" target="_blank" rel="noopener">WhatsApp</a></div>'''

# ------------------------------------------------------------------ SEO head
def jsonld(c, title, desc, route, body):
    org = {"@context":"https://schema.org","@type":"ProfessionalService","@id":SITE+"/#org","name":"OPSMO","alternateName":"opsmo.tech","url":SITE+"/",
           "logo":SITE+"/assets/img/icon-512.png","image":SITE+"/assets/img/zoho-tower.webp","description":DEFAULT_DESC,"telephone":"+"+PHONE_RAW,
           "areaServed":["United Arab Emirates","Saudi Arabia","Qatar","Kuwait","Oman","Bahrain","Egypt"],"address":{"@type":"PostalAddress","addressLocality":"Dubai","addressCountry":"AE"},
           "founder":{"@type":"Person","@id":SITE+"/founder/#person","name":"Mohamed Refaat","jobTitle":"Founder & Principal Consultant","sameAs":[LINKEDIN, UAE_STORIES],
                      "alumniOf":[{"@type":"Organization","name":"Zoho"},{"@type":"Organization","name":"Property Finder"}]},
           "sameAs":[LINKEDIN],"knowsAbout":["Zoho One","Zoho CRM","Zoho Desk","CRM implementation","Business process automation","Revenue operations","Digital transformation"]}
    out = [org]
    parts = [p for p in route.strip("/").split("/") if p]
    if parts:
        items = [{"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"}]
        acc = ""
        for i, p in enumerate(parts):
            acc += "/" + p
            items.append({"@type":"ListItem","position":i+2,"name":(title.split("|")[0].strip() if i==len(parts)-1 else p.replace("-"," ").title()),"item":SITE+acc+"/"})
        out.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items})
    qa = re.findall(r'<details class="qa rv"><summary>(.*?)</summary><p>(.*?)</p></details>', body)
    if qa:
        out.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":html.unescape(q),"acceptedAnswer":{"@type":"Answer","text":html.unescape(a)}} for q, a in qa]})
    if route.startswith("/insights/") and route.strip("/") != "insights":
        out.append({"@context":"https://schema.org","@type":"Article","headline":title.split("|")[0].strip(),"description":desc,"author":{"@id":SITE+"/founder/#person"},"publisher":{"@id":SITE+"/#org"},"mainEntityOfPage":SITE+route+"/"})
    if route == "/founder":
        out.append({"@context":"https://schema.org","@type":"ProfilePage","mainEntity":{"@id":SITE+"/founder/#person"}})
    return "".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>' for o in out)

THEME_BOOT = """<script>(function(){try{var q=new URLSearchParams(location.search).get('theme');var t=q||localStorage.getItem('opsmo-theme')||'dark';if(q)localStorage.setItem('opsmo-theme',q);document.documentElement.dataset.theme=t==='light'?'light':'dark';}catch(e){document.documentElement.dataset.theme='dark';}})();</script>"""

def page(c, title, body, desc=None, route="/"):
    body = re.sub(r'<canvas class="trails"[^>]*></canvas>', '', body)
    body = re.sub(r'<img class="cta__bg"[^>]*>', '', body)
    if not desc:
        m = re.search(r'<p class="(?:phero__p|hero5__p)[^"]*"[^>]*>(.*?)</p>', body, re.S)
        desc = html.unescape(re.sub("<.*?>", "", m.group(1))).strip() if m else DEFAULT_DESC
    if len(desc) > 158: desc = desc[:155].rsplit(" ", 1)[0] + "…"
    url = SITE + ("/" if route == "/" else route + "/")
    img = SITE + "/assets/img/og.jpg"
    return f'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}"><meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="{"article" if route.startswith("/insights/") else "website"}"><meta property="og:site_name" content="OPSMO"><meta property="og:url" content="{url}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:image" content="{img}"><meta property="og:locale" content="en_AE">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{img}">
<meta name="geo.region" content="AE-DU"><meta name="geo.placename" content="Dubai">
<meta name="theme-color" content="#050506"><meta name="view-transition" content="same-origin">
{THEME_BOOT}
<link rel="icon" href="{c.asset("img/mark.png")}" type="image/png" sizes="64x64"><link rel="icon" href="{c.asset("../favicon.ico")}" sizes="any"><link rel="apple-touch-icon" href="{c.asset("img/apple-touch-icon.png")}">
<link rel="preload" href="{c.asset("fonts/sora-latin-wght-normal.woff2")}" as="font" type="font/woff2" crossorigin><link rel="preload" href="{c.asset("fonts/geist-latin-wght-normal.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{c.asset("css/style.css")}"><link rel="stylesheet" href="{c.asset("css/v5.css")}">
{jsonld(c, title, desc, route, body)}
</head>
<body id="top">
<a class="skip" href="#main">Skip to content</a><div class="progress" aria-hidden="true"><span id="progressBar"></span></div><div class="cursor-glow" id="glow" aria-hidden="true"></div>
{nav_html(c)}
<main id="main">{body}</main>
{footer_html(c)}
{B.SPRITE}
<canvas class="globe" id="globe" aria-hidden="true"></canvas>
<script src="{c.asset("js/main.js")}" defer></script><script src="{c.asset("js/v5.js")}" defer></script><script src="{c.asset("js/globe.js")}" defer></script><script src="{c.asset("js/showcase.js")}" defer></script><script src="{c.asset("js/hook.js")}" defer></script>
</body></html>'''


# ================================================================== v6: merged structure
REDIR = {
 "/founder": "/about#founder", "/book": "/contact#book", "/packages": "/approach#packages",
 "/managed-services": "/solutions/managed-crm-operations#retainers",
 "/platforms/salesforce": "/platforms#salesforce", "/platforms/odoo": "/platforms#odoo",
 "/platforms/analytics": "/platforms#analytics-bi", "/platforms/automation-integration": "/platforms#automation-integration",
}
for _s in IND_ORDER:
    if _s != "real-estate": REDIR["/industries/" + _s] = "/industries#" + _s
_orig_href = Ctx.href
def _href(self, target):
    if not re.match(r"^(https?:|mailto:|tel:|#)", target):
        path, _, frag = target.partition("#")
        key = "/" + path.strip("/")
        if key in REDIR:
            target = REDIR[key] if not frag else REDIR[key].split("#")[0] + "#" + frag
    return _orig_href(self, target)
Ctx.href = _href

def tier_html(c, line):
    parts = [p.strip() for p in line[1:].split(" :: ")]
    m = re.match(r"\[(.+?)\]\s+(.+)", parts[0]); tag, name = m.groups()
    desc, items = parts[1], [x.strip() for x in parts[2].split(";")]
    excl = parts[3] if len(parts) > 3 and parts[3] else ""
    summary = parts[4] if len(parts) > 4 else ""
    if excl.startswith("::"): summary, excl = excl[2:].strip(), ""
    pkg = tag.startswith("PACKAGE")
    price = ('<div class="tier__price"><span class="mono">Price</span><b>Quoted after a free call</b></div>' if pkg else
             '<div class="tier__price"><span class="mono">Monthly fee</span><b>Agreed per business</b></div>')
    return f'''<article class="tier rv"><span class="mono acc">{E(tag.title())}</span><h3>{E(name)}</h3><p class="tier__d">{E(desc)}</p>{price}
{f'<p class="tier__s">{E(summary)}</p>' if summary else ""}<ul class="ticks">{"".join(f"<li>{E(i)}</li>" for i in items)}</ul>
{f'<p class="tier__x"><span class="mono">Not included</span> {E(excl)}</p>' if excl else ""}{btn(c,"Get a quote" if pkg else "Ask about this plan","/contact","line",True)}</article>'''
B.tier_html = tier_html

from founder_data import STORY, ELSEWHERE
def founder_section(c):
    story = "".join((f'<p class="pull rv">{E(p[1:])}</p>' if p.startswith(">") else f'<p class="rv">{E(p)}</p>') for p in STORY)
    links = "".join(f'<a class="card card--link rv" {a_attrs(c,u)}><span class="mono acc">{E(k.title())}</span><h3>{E(t)}</h3><p>{E(d)}</p><span class="card__go mono">Open {EXT}</span></a>' for k,t,d,u in ELSEWHERE)
    return f'''<section class="sec" id="founder"><div class="wrap"><div class="fgrid fgrid--story">
<figure class="fphoto rv"><img src="{c.asset("img/founder-cut.webp")}" alt="Mohamed Refaat, founder of OPSMO" loading="lazy" width="820" height="979"><figcaption class="tag">Founder &amp; Principal Consultant</figcaption></figure>
<div class="fcopy">{chip("The founder")}<h2 class="h2 rv">Mohamed <em>Refaat</em></h2>
<p class="mono dim rv">Meeting Minds · Property Finder · Zoho · Motivate Media Group · PropSpace</p>
<div class="fstory">{story}</div></div></div></div></section>
{proof_strip(c)}
{sec(head("Check for yourself","Read, verify, connect.") + f'<div class="grid3">{links}</div>')}
{videos_block(c)}'''

def render_about(c):
    meta, body = B.parse_md(os.path.join(B.HERE, "content", "about.md"))
    h = B.render_body(c, meta, body)
    i = h.rfind('<section class="ctax"')
    return h[:i] + founder_section(c) + h[i:]

_orig_solution = B.render_solution
def render_solution(c, slug):
    h = _orig_solution(c, slug)
    if slug == "managed-crm-operations":
        meta, body = B.parse_md(os.path.join(B.HERE, "partials", "retainers.md"))
        extra = B.render_body(c, meta, body).replace('<section class="sec ', '<section id="retainers" class="sec ', 1)
        i = h.find('<div class="faq">'); i = h.rfind('<section', 0, i)
        h = h[:i] + extra + h[i:]
    return h
B.render_solution = render_solution

INTRO_CLEAN = {
 "real-estate": "Enquiries arrive from portals, your website and brokers within minutes. We set up how leads are captured, assigned, followed up and turned into deals.",
}
def render_industries(c):
    others = [x for x in IND_ORDER if x != "real-estate"]
    tabs = "".join(f'<button class="etab{" is-on" if i==0 else ""}" role="tab" id="it-{x}" aria-controls="{x}" aria-selected="{"true" if i==0 else "false"}"><span>{i+1:02d}</span>{E(IND[x]["name"])}</button>' for i, x in enumerate(others))
    panels = ""
    for i, x in enumerate(others):
        d = IND[x]
        flow = "".join(f"<li>{E(f)}</li>" for f in d["flow"])
        spec = "".join(f"<li>{E(f)}</li>" for f in d["spec"])
        panels += f'''<div class="ep ind{" is-on" if i==0 else ""}" id="{x}" role="tabpanel" aria-labelledby="it-{x}"{"" if i==0 else " hidden"}>
<div class="ep__img"><img src="{c.asset("img/"+d["img"]+".webp")}" alt="" loading="lazy"><div><span class="mono">{E(d["tagline"])}</span><h3>{E(d["name"])}</h3></div></div>
<div class="ind__body"><p class="lead">{E(d["intro"])}</p><div class="ind__cols"><div><h4 class="mono acc">How the work flows</h4><ol class="ind__flow">{flow}</ol></div>
<div><h4 class="mono acc">What we set up</h4><ul class="ticks">{spec}</ul></div></div>
<div class="btnrow">{btn(c,"Talk about your business","/book")}{btn(c,"Request an assessment","/contact","line")}</div></div></div>'''
    re_ = IND["real-estate"]
    feature = f'''<a class="refeat rv" {a_attrs(c,"/industries/real-estate")}><img src="{c.asset("img/skyline.webp")}" alt="" loading="lazy"><div class="refeat__in">
<span class="mono acc">Our deepest experience</span><h2 class="h2">Real estate</h2><p>Two stints at Property Finder and the PropSpace move to Zoho One. See how we set up Zoho for brokerages and developers, with Property Finder and Bayut leads.</p>
<span class="btn btn--fire">See Zoho for real estate {ARROW}</span></div></a>'''
    return f'''<section class="phero phero--img"><div class="wrap phero__grid"><div class="phero__copy">{chip("Industries")}
<h1 class="phero__h rv">The same CRM ideas. <em>Your industry's way of working.</em></h1>
<p class="phero__p rv">Every sector sells, delivers and bills differently. We start from how your industry actually works, then set up the system around it.</p>
{btns(c,[("Book a free consultation","/book"),("Request an assessment","/contact")])}</div>
<div class="pstack rv" aria-hidden="true"><span class="pstack__a"></span><span class="pstack__b"></span><figure><img src="{c.asset("img/team.webp")}" alt="" fetchpriority="high"></figure></div></div></section>
{sec(feature)}
<section class="sec" id="sectors"><div class="wrap">{head("Other industries","Pick your sector.","Each tab shows how the work usually flows and what we set up.")}
<div class="explorer rv"><div class="explorer__tabs" role="tablist" aria-label="Industries">{tabs}</div><div class="explorer__panel">{panels}</div></div>
<p class="fine rv">{E(B.INTEGRATION_NOTE)}</p></div></section>
{contact_paths(c)}'''

RE_PAINS = [("Leads come from everywhere","Property Finder, Bayut, your website, Meta ads and WhatsApp all send enquiries. Without one inbox, some are answered twice and some never."),
            ("Speed decides the deal","The agent who calls back first usually wins the client. Manual assignment means minutes become hours."),
            ("Agents keep their own lists","When follow-ups live in personal phones and spreadsheets, the company loses the history when an agent leaves."),
            ("Managers can't see the pipeline","Which source brings real buyers? Which agent converts? Without clean data, nobody knows.")]
RE_FAQ = [("Can Zoho receive Property Finder and Bayut leads automatically?","Yes, where the portal gives API or email-lead access for your account. Leads land in Zoho CRM with the listing, source and campaign attached, and are assigned to an agent straight away."),
          ("We already have a CRM. Do we have to start over?","No. We review what you have first. If it can do the job, we fix it. If it can't, we move your contacts, deals and history to Zoho and check them record by record."),
          ("How long does a real-estate setup take?","A standard brokerage setup usually takes four to six weeks, including testing and team training. Larger developers with several projects are rolled out in phases."),
          ("Can the team work in Arabic and English?","Yes. Zoho supports both, and we train teams in Arabic and English.")]
def render_real_estate(c):
    d = IND["real-estate"]
    pains = "".join(f'<li class="rv"><span class="pains__n mono">0{i+1}</span><div><h3>{E(t)}</h3><p>{E(x)}</p></div></li>' for i, (t, x) in enumerate(RE_PAINS))
    flow = "".join(f'<li class="rv"><span class="flow__n mono">0{i+1}</span><p>{E(x)}</p></li>' for i, x in enumerate(d["flow"]))
    ws = "".join(f'<div class="ws__row"><b>{E(a)}</b><span>{E(b)}</span></div>' for a, b in WS)
    return f'''<section class="phero phero--img"><div class="wrap phero__grid"><div class="phero__copy">{chip("Zoho for real estate · Dubai")}
<h1 class="phero__h rv">From portal enquiry to signed deal, <em>without losing a lead.</em></h1>
<p class="phero__p rv">{E(INTRO_CLEAN["real-estate"])} Built by a team that worked inside Property Finder.</p>
{btns(c,[("Book a free consultation","/book"),("Request an assessment","/contact")])}</div>
<div class="pstack rv" aria-hidden="true"><span class="pstack__a"></span><span class="pstack__b"></span><figure><img src="{c.asset("img/skyline.webp")}" alt="" fetchpriority="high"></figure></div></div></section>
{sec(f'<div class="daily"><div class="head head--sticky">{chip("The problem")}<h2 class="h2 rv">Why real-estate teams <em>lose good leads.</em></h2><p class="callout rv">It is rarely the agents. It is the missing system behind them.</p></div><ol class="pains">{pains}</ol></div>')}
{before_after(c, pick=False)}
{live_demo(c, pick=False)}
{sec(head("How it works","One path for every enquiry.", "This is the flow we set up in Zoho CRM. Every step is tracked, so nothing depends on memory.") + f'<ol class="flow">{flow}</ol>')}
{sec(f"""<div class="pack"><div class="head head--sticky">{chip("What we set up")}<h2 class="h2 rv">Six parts, <em>one owner.</em></h2><p class="lead rv">We own the whole rollout, from setup to training your team in Arabic and English.</p><div class="btnrow">{btn(c,"Scope your rollout","/book")}</div></div><div class="ws rv">{ws}</div></div>""")}
{sec(f"""<div class="head">{chip("Why us")}<h2 class="h2 rv">We have worked <em>on the portal side.</em></h2><p class="lead rv">Mohamed spent two stints at Property Finder Group and led PropSpace's move from Salesforce to Zoho One.</p></div>
<ul class="proof"><li class="rv"><b class="num-big">300+</b><span>UAE real-estate accounts managed at Property Finder</span></li><li class="rv"><b class="num-big">164%</b><span>retention revenue growth in Q1</span></li><li class="rv"><b class="num-big">150+</b><span>UAE companies moved to the new PropSpace model</span></li><li class="rv"><b class="num-big">40%</b><span>less manual effort after the Zoho One move</span></li><li class="rv"><b class="num-big">650K+</b><span>USD annual revenue on PropSpace's Zoho One system</span></li><li class="rv"><b class="num-big">8 → 1</b><span>separate tools replaced by one platform</span></li></ul>
<div class="btnrow">{btn(c,"Read the PropSpace story","/success-stories")}</div>""")}
{sec(f'<div class="faq">{head("FAQ","Questions real-estate teams ask us.")}{faq_html(RE_FAQ)}</div>')}
<p class="wrap fine">{E(B.INTEGRATION_NOTE)}</p>
{contact_paths(c)}'''

def render_contact_merged(c):
    book = B.render_book(c).replace('<h1 class="phero__h', '<h2 class="phero__h').replace('</h1>', '</h2>', 1)
    book = book.replace('<section class="phero phero--form">', '<section class="phero phero--form phero--book" id="book">', 1)
    form = B.render_contact(c).replace('<section class="phero phero--form">', '<section class="phero phero--form" id="assessment">', 1)
    form = form.replace('<h1 class="phero__h', '<h2 class="phero__h').replace('</h1>', '</h2>', 1)
    top = f'''<section class="phero phero--contact"><div class="wrap"><div class="phero__copy">{chip("Contact")}
<h1 class="phero__h rv">Let's talk about <em>how your business runs.</em></h1>
<p class="phero__p rv">Choose the way that suits you. Every request is read by a person, usually within one business day.</p></div>
<div class="paths paths--top">
<a class="path path--hot rv" href="#book"><span class="mono">30 minutes · free</span><h3>Book a call</h3><p>Pick a day and time. We confirm by email or WhatsApp.</p><span class="path__go">Choose a time {ARROW}</span></a>
<a class="path rv" href="{WA}" target="_blank" rel="noopener"><span class="mono">Fastest</span><h3>WhatsApp</h3><p>Send a short message and get a direct reply from Mohamed.</p><span class="path__go">{PHONE} {EXT}</span></a>
<a class="path rv" href="#assessment"><span class="mono">Written reply</span><h3>Operational assessment</h3><p>Three short steps about your systems and goals. We reply with a scoped recommendation.</p><span class="path__go">Start {ARROW}</span></a>
</div></div></section>'''
    return top + book + form

def add_anchor_ids(html_):
    def rep(m):
        slug = re.sub(r"[^a-z0-9]+", "-", html.unescape(m.group(2)).lower()).strip("-")
        return f'<section id="{slug}" class="sec {m.group(1)}"><div class="wrap"><div class="sechead"><p class="chip rv">{m.group(2)}</p>'
    return re.sub(r'<section class="sec ([^"]*)"><div class="wrap"><div class="sechead"><p class="chip rv">([^<]+)</p>', rep, html_)

CLEAN = [
 (r" · \[(SYSTEM|STACK|VERTICAL|CATEGORY|TIER): [^\]]*\]", ""), (r"\[(SYSTEM|STACK|VERTICAL|CATEGORY|TIER): [^\]]*\]\s*", ""),
 (r'<p class="notice mono">NO CALENDAR PROVIDER IS CONNECTED YET\. THE TIME YOU CHOOSE IS A REQUEST, NOT A CONFIRMED SLOT\.</p>', '<p class="notice mono">We confirm the exact time with you by email or WhatsApp.</p>'),
 (r'<p class="fine">Submissions are stored securely and visible only to the OPSMO team\. CRM synchronisation is queued and shown as pending until the integration is configured\.</p>', ''),
]
_page5 = page
def page(c, title, body, desc=None, route="/"):
    for pat, rep in CLEAN: body = re.sub(pat, rep, body)
    body = add_anchor_ids(body)
    return _page5(c, title, body, desc, route)

# ------------------------------------------------------------------ wire up + build
B._orig_nav = B.nav_html
_of = B.render_founder
def render_founder(c):
    h = _of(c)
    i = h.rfind('<section class="ctax"')
    return h[:i] + proof_strip(c) + videos_block(c) + h[i:] if i > 0 else h + proof_strip(c) + videos_block(c)
B.render_founder = render_founder
B.nav_html = nav_html; B.footer_html = footer_html; B.cta_block = cta_block; B.render_home = render_home; B.THEME_BOOT = THEME_BOOT

# ---- v6 plain-English copy
import copy6, shared
from screens import screen
from showcase import live_demo, before_after, savings_calc, rollout, suite_map
for _k, _v in copy6.SOL_COPY.items():
    if _k in SOL: SOL[_k].update(_v)
B.METHOD[:] = copy6.METHOD; B.RECEIVE[:] = copy6.RECEIVE
B.CTA["default"] = copy6.CTA; shared.CTA["default"] = copy6.CTA
for _k, _d in copy6.SOL_HUB:
    if _k in SOL_META: SOL_META[_k] = SOL_META[_k][:3] + (_d,) + SOL_META[_k][4:]
CLEAN += [(re.escape(a), b) for a, b in copy6.LABELS] + [(r'<span class="mono acc"></span>', ''),
 (r"The same six-stage discipline, applied to this solution\.", "Our six-step method."), (r"What you receive", "What you get")]

ROUTES = []
def write(route, title, body, desc=None):
    c = Ctx(route)
    out_dir = B.OUT if route == "/" else os.path.join(B.OUT, route.strip("/"))
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w") as f:
        f.write(page(c, title, body(c), desc, route))
    ROUTES.append(route); return route
B.write = write

INJECT = {"/platforms/zoho": [("before", '<p class="chip rv">HOW WE SET IT UP</p>', lambda c: suite_map(c)), ("before", '<section class="ctax"', lambda c: rollout(c) + savings_calc(c))],
          "/approach": [("after_stages", None, lambda c: rollout(c))]}
def inject(c, route, h):
    for where, marker, fn in INJECT.get(route, []):
        if where == "after_stages":
            j = h.find('<p class="chip rv">HOW WE THINK</p>'); i = h.rfind('<section', 0, j) if j > 0 else -1
        else:
            if marker.startswith('<section class="ctax"'): i = h.rfind(marker)
            else: i = h.rfind('<section', 0, h.find(marker)) if h.find(marker) > 0 else -1
        if i > 0: h = h[:i] + fn(c) + h[i:]
    return h

def write_redirect(old, new):
    c = Ctx(old)
    target = c.href(new)
    out_dir = os.path.join(B.OUT, old.strip("/")); os.makedirs(out_dir, exist_ok=True)
    url = SITE + "/" + new.split("#")[0].strip("/") + ("/" if new.split("#")[0].strip("/") else "") + ("#" + new.split("#")[1] if "#" in new else "")
    open(os.path.join(out_dir, "index.html"), "w").write(f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Moved | OPSMO</title><meta name="robots" content="noindex"><link rel="canonical" href="{url}"><meta http-equiv="refresh" content="0; url={target}"><script>location.replace("{target}")</script></head><body><p>This page moved: <a href="{target}">{url}</a></p></body></html>')

def main():
    cdir = os.path.join(B.HERE, "content")
    write("/", "OPSMO — Zoho One & CRM Implementation in Dubai, UAE | Ex-Zoho Founder", render_home, DEFAULT_DESC)
    for root, _, files in os.walk(cdir):
        for fn in files:
            if not fn.endswith(".md"): continue
            rel = os.path.relpath(os.path.join(root, fn), cdir); route = B.md_route(rel); full = os.path.join(root, fn)
            if route in ("/about", "/industries"): continue
            meta, body = B.parse_md(full)
            if rel.startswith("insights/") and fn != "index.md":
                write(route, meta["title"], lambda c, f=full: B.render_article(c, f), meta["deck"]); continue
            write(route, meta["title"], lambda c, m=meta, b=body, r=route: inject(c, r, B.render_body(c, m, b)))
    for x in SOL:
        write("/solutions/" + x, SOL[x]["doc"], lambda c, x=x: render_solution(c, x), SOL[x]["tagline"])
    write("/about", "About OPSMO & Founder Mohamed Refaat — Ex-Zoho, Dubai | OPSMO", render_about,
          "OPSMO is a Dubai company that sets up and runs Zoho for sales, service and operations teams. Founded by Mohamed Refaat, Zoho's first Egyptian hire.")
    write("/industries", "Industries — CRM & Zoho Systems by Sector | OPSMO", render_industries,
          "How OPSMO sets up Zoho and CRM systems for real estate, professional services, media, events, retail, B2B distribution and growing SMEs.")
    write("/industries/real-estate", "Zoho CRM for Real Estate in Dubai — Property Finder & Bayut Leads | OPSMO", render_real_estate,
          "Zoho CRM for UAE brokerages and developers: Property Finder and Bayut leads, instant agent assignment, follow-ups and pipeline reports. Built by an ex-Property Finder team.")
    write("/contact", "Contact OPSMO — Book a Call or WhatsApp | Dubai", render_contact_merged,
          "Book a free 30-minute call, message OPSMO on WhatsApp, or request a written operational assessment. Dubai, serving the UAE and GCC.")
    write("/success-stories", "Success Stories — Zoho One Transformations in the UAE & GCC | OPSMO", render_stories_page,
          ("How PropSpace, Elnaggar & Partners, R1 Performance and Fawry Microfinance moved from spreadsheets and WhatsApp to one Zoho One system." if SHOW_CLIENT_NAMES else "How a PropTech platform, a law firm, a performance car workshop and a microfinance lender moved from spreadsheets and WhatsApp to one Zoho One system."))
    for old, new in REDIR.items(): write_redirect(old, new)
    c = Ctx("/")
    p404 = page(c, "Page not found | OPSMO", f'<section class="phero"><div class="wrap"><div class="phero__copy">{chip("404")}<h1 class="phero__h">This page <em>isn\'t here.</em></h1><p class="phero__p">The link may be out of date. Try the homepage or book a call.</p>{btns(c,[("Back to home","/"),("Book a Call","/book")])}</div></div></section>', "The page you were looking for could not be found.", "/404")
    p404 = p404.replace('href="./', 'href="/').replace('src="assets', 'src="/assets').replace('href="assets', 'href="/assets').replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
    open(os.path.join(B.OUT, "404.html"), "w").write(p404)
    pri = lambda r: "1.0" if r == "/" else ("0.9" if r.count("/") == 1 else "0.7")
    urls = sorted(set(ROUTES))
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f'  <url><loc>{SITE}{"/" if r=="/" else r+"/"}</loc><lastmod>2026-11-20</lastmod><priority>{pri(r)}</priority></url>\n' for r in urls) + "</urlset>\n"
    open(os.path.join(B.OUT, "sitemap.xml"), "w").write(sm)
    open(os.path.join(B.OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    vr = {"cleanUrls": False, "trailingSlash": True, "redirects": [{"source": o + "/", "destination": n.split("#")[0] + ("/" if not n.split("#")[0].endswith("/") else ""), "permanent": True} for o, n in REDIR.items()]}
    open(os.path.join(B.OUT, "vercel.json"), "w").write(json.dumps(vr, indent=2))
    print(len(urls), "pages,", len(REDIR), "redirects")

if __name__ == "__main__":
    main()
