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

def logo(c, name, alt="", cls=""):
    return f'<img src="{c.asset("img/logos/"+name+".png")}" alt="{E(alt)}" class="{cls}" loading="lazy">'

# ------------------------------------------------------------------ components
def marquee(c):
    row = "".join(logo(c, n, a, cl) for n, a, cl in CLIENT_LOGOS)
    row2 = "".join(logo(c, n, "", cl).replace('alt=""', 'alt="" aria-hidden="true"') for n, a, cl in CLIENT_LOGOS)
    return f'<div class="marquee" aria-label="Businesses OPSMO and its founder have built systems for"><div class="marquee__track">{row}{row2}</div></div>'

def videos_block(c, eyebrow="In his words", h="Hear it from the operator.", lead="Short videos from Mohamed on LinkedIn — on Zoho, operating models and why most problems aren't software problems."):
    cards = "".join(f'''<figure class="vid rv"><button class="vid__play" type="button" data-embed="https://www.linkedin.com/embed/feed/update/urn:li:activity:{i}" aria-label="Play video: {E(t)}">
<img src="{c.asset("img/"+p)}" alt="Video still from Mohamed Refaat's LinkedIn post" loading="lazy"><span class="vid__btn" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span><span class="vid__dur mono">{d}</span></button>
<figcaption><h3>{E(t)}</h3><p>{E(s)}</p><a class="mono" href="https://www.linkedin.com/feed/update/urn:li:activity:{i}/" target="_blank" rel="noopener">Watch on LinkedIn {EXT}</a></figcaption></figure>''' for i, p, d, t, s in VIDEOS)
    return sec(f'<div class="head head--split"><div>{chip(eyebrow)}<h2 class="h2 rv">{em_last(h)}</h2></div><p class="lead rv">{E(lead)}</p></div><div class="vids">{cards}</div>', "sec--videos")

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
    z = "".join(f'<a class="zc rv" href="{ZOHO[k]}" target="_blank" rel="noopener sponsored">{m}<h3>{E(t)}</h3><p>{E(d)}</p><span class="mono">Open Zoho {EXT}</span></a>' for k, t, d, m in cards)
    return sec(f'''<div class="head head--split"><div>{chip("Zoho references")}<h2 class="h2 rv">Start with the edition <em>that fits your team.</em></h2></div><p class="lead rv">The Zoho editions we implement most often. Pick one — we architect and implement from there.</p></div>
<div class="zcards">{z}</div><p class="fine rv">Referral links: OPSMO may earn a commission if you subscribe through a Zoho link on this page, at no extra cost to you. Our recommendations are the same either way.</p>''')

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

def render_home(c):
    sol_tabs, sol_panels = "", ""
    for i, s in enumerate(SOL_ORDER):
        sys_, name, short, desc, img = SOL_META[s]
        bul = SS_BULLETS if s == "software-selection" else (ZD_SCOPE if s == "zoho-desk-implementation" else SOL[s]["scope"][:4])
        sol_tabs += f'<button class="etab{" is-on" if i==0 else ""}" role="tab" id="st-{s}" aria-controls="sp-{s}" aria-selected="{"true" if i==0 else "false"}" data-i="{i}"><span>{i+1:02d}</span>{E(short)}</button>'
        sol_panels += f'''<div class="ep{" is-on" if i==0 else ""}" id="sp-{s}" role="tabpanel" aria-labelledby="st-{s}"{"" if i==0 else " hidden"}><div class="ep__img"><img src="{c.asset("img/"+img+".webp")}" alt="" loading="lazy"><div><span class="mono">[SYSTEM: {sys_}]</span><h3>{E(name)}</h3></div></div>
<div class="ep__body"><div><p>{E(desc)}</p><div class="btnrow">{btn(c,"Explore "+short,"/solutions/"+s,"fire",True)}{btn(c,"Book a consultation","/book","line",True)}</div></div><ul class="ticks">{"".join(f"<li>{E(b)}</li>" for b in bul)}</ul></div></div>'''
    reality = "".join(f'<li class="rv"><span class="pains__n mono">0{i+1}</span><div><h3>{E(t)}</h3><p>{E(d)}</p></div></li>' for i, (t, d) in enumerate(REALITY))
    leaks = "".join(f'<div class="leak rv"><span>{E(a)}</span><b>{E(b)}{f"<small>{E(s)}</small>" if s else ""}</b></div>' for a, b, s in LEAKS)
    steps = "".join(f'<li class="rv"><span class="mono">Step {i+1}</span><h3>{E(t)}</h3><p>{E(d)}</p></li>' for i, (t, d) in enumerate(STEPS4))
    ws = "".join(f'<div class="ws__row"><b>{E(a)}</b><span>{E(b)}</span></div>' for a, b in WS)
    return f'''
<section class="hero5"><div class="hero5__aura" aria-hidden="true"></div>
<div class="wrap hero5__grid"><div class="hero5__copy">
<p class="chip">Business transformation · Dubai since 2009</p>
<h1 class="hero5__h" data-split>Your business doesn't need more software. <span class="fire">It needs systems that work.</span></h1>
<p class="hero5__p" data-in>OPSMO designs, implements and runs the Zoho systems behind sales, customer support and daily operations for businesses across the UAE and GCC. It is led by Mohamed Refaat — the first Egyptian hire at Zoho, with two stints inside Property Finder Group.</p>
<div class="btnrow" data-in>{btn(c,"Book a free consultation","/book")}<a class="btn btn--line" href="{WA}" target="_blank" rel="noopener"><i class="dot"></i>WhatsApp Mohamed</a></div>
<div class="hero5__ex" data-in><span class="mono dim">Former</span><a class="ex ex--zoho" href="#zoho">Zoho</a><a class="ex" href="#career">Property Finder</a><a class="ex" href="#career">PropSpace</a><a class="ex" href="#career">Motivate Media Group</a></div>
</div>
<figure class="portrait" id="portrait"><img class="portrait__bg" src="{c.asset("img/zoho-tower.webp")}" alt="" fetchpriority="high"><div class="portrait__shade"></div>
<img class="portrait__cut" src="{c.asset("img/founder-cut.webp")}" alt="Mohamed Refaat, founder of OPSMO, in front of the Zoho tower" fetchpriority="high" width="820" height="979"></figure>
</div>{marquee(c)}</section>

<section class="zchap" id="zoho" aria-label="Zoho experience"><div class="zchap__pin"><img class="zchap__bg" src="{c.asset("img/zoho-tower.webp")}" alt="" loading="lazy"><div class="zchap__veil"></div>
<div class="wrap zchap__in"><p class="chip chip--zoho">Where the experience comes from</p>
<h2 class="zchap__word" aria-label="Zoho"><span>Z</span><span>o</span><span>h</span><span>o</span><em>.</em></h2>
<p class="zchap__lead">Zoho hired Mohamed in Dubai and relocated him to Egypt as its first Egyptian employee. He helped build the market from the inside — which is why OPSMO implements Zoho as an operator, not a reseller.</p>
<ol class="zchap__facts"><li><b>First</b><span>Egyptian hire at Zoho</span></li><li><b>First</b><span>team member in Zoho Egypt</span></li><li><b>500+</b><span>organisations advised while building Zoho's presence in Egypt</span></li><li><b>50%</b><span>growth in customer acquisition and annual revenue he contributed to</span></li></ol>
<div class="btnrow"><a class="btn btn--fire" href="{ZOHO["one"]}" target="_blank" rel="noopener sponsored">Explore Zoho One {EXT}</a><a class="btn btn--line" href="{UAE_STORIES}" target="_blank" rel="noopener">Read the UAE Stories feature {EXT}</a></div></div>
<div class="zchap__rail" aria-hidden="true"><span id="zRail"></span></div></div></section>

{sec(f"""<div class="head">{chip("Track record")}<h2 class="h2 rv">Built inside the companies <em>that shaped UAE tech.</em></h2><p class="lead rv">Seventeen years across sales, business development, commercial operations and CRM — at the platform, the portal and the media group. Every claim links to where you can check it.</p></div>
<div class="bento">
<a class="bt bt--zoho rv" href="{ZOHO["all"]}" target="_blank" rel="noopener sponsored"><div class="bt__logo">{logo(c,"zohoone-w","Zoho One")}</div><span class="bt__k mono">Zoho · Egypt</span><h3>The platform</h3><p>First Egyptian hire and first team member in Zoho Egypt. Advised 500+ organisations while helping build the market.</p><span class="bt__go mono">zoho.com {EXT}</span></a>
<a class="bt bt--pf rv" href="https://www.propertyfinder.ae/" target="_blank" rel="noopener"><div class="bt__logo">{logo(c,"propertyfinder-w","Property Finder")}</div><span class="bt__k mono">Property Finder Group · twice</span><h3>The portal</h3><div class="bt__stats"><div><b><span data-count="300">300</span>+</b><span>UAE real-estate accounts managed</span></div><div><b><span data-count="164">164</span>%</b><span>retention revenue growth in Q1</span></div></div><span class="bt__go mono">propertyfinder.ae {EXT}</span></a>
<a class="bt bt--ps rv" href="https://www.propspace.com/about" target="_blank" rel="noopener"><div class="bt__logo">{logo(c,"propspace-w","PropSpace")}</div><span class="bt__k mono">Post-acquisition transformation</span><p>Moved PropSpace from Property Finder's Salesforce environment to an integrated Zoho One operating model.</p><div class="bt__stats"><div><b><span data-count="150">150</span>+</b><span>UAE companies</span></div><div><b><span data-count="40">40</span>%</b><span>less manual effort</span></div></div><span class="bt__go mono">propspace.com {EXT}</span></a>
<a class="bt bt--mm rv" href="https://www.motivatemedia.com/" target="_blank" rel="noopener"><div class="bt__word">Motivate<br>Media Group</div><span class="bt__k mono">Media · events</span><p>Commercial work inside one of the UAE's best-known media and events groups.</p><span class="bt__go mono">motivatemedia.com {EXT}</span></a>
<div class="bt bt--stat rv"><b><span data-count="170">170</span>+</b><span>conferences planned and delivered across the UAE, Kuwait, Oman and Bahrain</span></div>
<a class="bt bt--li rv" href="{LI_RECS}" target="_blank" rel="noopener"><span class="bt__k mono">Verify</span><h3>Client recommendations</h3><p>What the people he has worked with say — on LinkedIn.</p><span class="bt__go mono">linkedin.com {EXT}</span></a>
</div>""", "", "career")}

{sec(f"""<div class="daily"><div class="head head--sticky">{chip("The daily reality")}<h2 class="h2 rv">You're not inefficient. <em>You're running a business with no operating system.</em></h2><p class="callout rv">This isn't a technology problem. It's an operations problem.</p></div><ol class="pains">{reality}</ol></div>""", "", "reality")}

<section class="sec impact"><div class="horizon" aria-hidden="true"></div><div class="wrap">
<div class="head head--center">{chip("The impact")}<h2 class="h2 rv">Every day without systems <em>is lost margin.</em></h2><p class="lead rv">We audit operational loss before we begin. This is what revenue leaks typically cost a mid-sized business.</p></div>
<div class="leaks">{leaks}</div><p class="note rv">It isn't about software. It's about operational precision. In 90 days, a competitor could remove the bottlenecks you're still firefighting.</p></div></section>

{stories_block(c)}
{videos_block(c)}
{portfolio_block(c)}

<section class="sec" id="solutions"><div class="wrap">
<div class="head head--split"><div>{chip("What we do")}<h2 class="h2 rv">Ten disciplines. <em>One operating system.</em></h2></div><div><p class="lead rv">Each solution is an operating capability, not a licence sale. Pick one to see what it covers.</p><a class="link rv" {a_attrs(c,"/solutions")}>All 10 solutions {ARROW}</a></div></div>
<div class="explorer rv"><div class="explorer__tabs" role="tablist" aria-label="OPSMO solutions">{sol_tabs}</div><div class="explorer__panel">{sol_panels}</div></div></div></section>

{sec(f"""<div class="head head--center">{chip("How we work")}<h2 class="h2 rv">From chaos to control <em>in 90 days.</em></h2></div><ol class="steps4" id="steps4">{steps}</ol><div class="steps4__line" aria-hidden="true"><span id="s4line"></span></div><p class="center rv"><a class="link" {a_attrs(c,"/approach")}>See the full six-stage methodology {ARROW}</a></p>""", "", "method")}

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
    old = B._orig_nav(c)
    old = old.replace(f'src="{c.asset("img/logo.png")}"', f'src="{c.asset("img/opsmo-logo.png")}"').replace(f'src="{c.asset("img/logo-white.png")}"', f'src="{c.asset("img/opsmo-logo-w.png")}"')
    old = old.replace('width="320" height="48"', 'width="700" height="120"')
    old = old.replace(f'<a class="nav__a" {a_attrs(c,"/insights")}>Insights</a>', f'<a class="nav__a" {a_attrs(c,"/success-stories")}>Success Stories</a><a class="nav__a" {a_attrs(c,"/insights")}>Insights</a>')
    old = old.replace(f'<a class="sheet__a" {a_attrs(c,"/insights")}>Insights</a>', f'<a class="sheet__a" {a_attrs(c,"/success-stories")}>Success Stories</a><a class="sheet__a" {a_attrs(c,"/insights")}>Insights</a>')
    old = old.replace(f'<a class="btn btn--fire btn--sm nav__cta" {a_attrs(c,"/book")}>Book a Consultation {ARROW}</a>', f'<a class="btn btn--fire btn--sm nav__cta" {a_attrs(c,"/book")}>Book a Call {ARROW}</a>')
    return old

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
    company = [("/about","About OPSMO"),("/founder","The Founder"),("/approach","Our Methodology"),("/packages","Implementation Packages"),("/managed-services","Managed Services"),(LI_RECS,"Client Recommendations"),("/contact","Contact Us")]
    services = [("/solutions","All Solutions")] + [("/solutions/"+s, SOL_META[s][2]) for s in SOL_ORDER]
    explore = [("/platforms/zoho","Zoho One Implementation"),("/platforms","Platforms"),("/industries","Industry Solutions"),("/success-stories","Success Stories"),("/insights","Insights"),(UAE_STORIES,"UAE Stories Feature"),(ZOHO["all"],"Zoho Products")]
    return f'''<footer class="ft"><div class="wrap">
<div class="ft__top"><div class="ft__brand"><a {a_attrs(c,"/")} aria-label="OPSMO home"><img class="logo-l" src="{c.asset("img/opsmo-logo.png")}" alt="opsmo.tech" width="700" height="120" loading="lazy"><img class="logo-d" src="{c.asset("img/opsmo-logo-w.png")}" alt="" width="700" height="120" loading="lazy"></a>
<p class="ft__tag">Systems that work.</p><p>Zoho implementation, integration and commercial operations for ambitious teams across the UAE and GCC — led by Zoho's first Egyptian hire.</p>
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
<a class="wa-fab" href="{WA}" target="_blank" rel="noopener" aria-label="Chat with OPSMO on WhatsApp">{SOC["wa"]}<span>Chat with us</span></a>
<div class="mbar"><a class="btn btn--fire btn--sm" {a_attrs(c,"/book")}>Book a Call</a><a class="btn btn--line btn--sm" href="{WA}" target="_blank" rel="noopener">WhatsApp</a></div>'''

# ------------------------------------------------------------------ SEO head
def jsonld(c, title, desc, route, body):
    org = {"@context":"https://schema.org","@type":"ProfessionalService","@id":SITE+"/#org","name":"OPSMO","alternateName":"opsmo.tech","url":SITE+"/",
           "logo":SITE+"/assets/img/opsmo-logo.png","image":SITE+"/assets/img/zoho-tower.webp","description":DEFAULT_DESC,"telephone":"+"+PHONE_RAW,
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
<link rel="icon" href="{c.asset("img/mark.png")}" type="image/png"><link rel="apple-touch-icon" href="{c.asset("img/mark.png")}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&family=Geist:wght@300..700&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{c.asset("css/style.css")}"><link rel="stylesheet" href="{c.asset("css/v5.css")}">
{jsonld(c, title, desc, route, body)}
</head>
<body id="top">
<a class="skip" href="#main">Skip to content</a><div class="progress" aria-hidden="true"><span id="progressBar"></span></div><div class="cursor-glow" id="glow" aria-hidden="true"></div>
{nav_html(c)}
<main id="main">{body}</main>
{footer_html(c)}
{B.SPRITE}
<script src="{c.asset("js/main.js")}" defer></script><script src="{c.asset("js/v5.js")}" defer></script>
</body></html>'''

# ------------------------------------------------------------------ wire up + build
B._orig_nav = B.nav_html
_of = B.render_founder
def render_founder(c):
    h = _of(c)
    i = h.rfind('<section class="ctax"')
    return h[:i] + videos_block(c) + h[i:] if i > 0 else h + videos_block(c)
B.render_founder = render_founder
B.nav_html = nav_html; B.footer_html = footer_html; B.cta_block = cta_block; B.render_home = render_home; B.THEME_BOOT = THEME_BOOT

ROUTES = []
def write(route, title, body, desc=None):
    c = Ctx(route)
    out_dir = B.OUT if route == "/" else os.path.join(B.OUT, route.strip("/"))
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w") as f:
        f.write(page(c, title, body(c), desc, route))
    ROUTES.append(route); return route
B.write = write

def main():
    B.main.__globals__["write"] = write
    # page-specific titles that read better in search
    B.main()
    write("/", "OPSMO — Zoho One & CRM Implementation in Dubai, UAE | Ex-Zoho Founder", render_home, DEFAULT_DESC)
    write("/success-stories", "Success Stories — Zoho One Transformations in the UAE & GCC | OPSMO", render_stories_page,
          "How PropSpace, Elnaggar & Partners, R1 Performance and Fawry Microfinance moved from spreadsheets and WhatsApp to one Zoho One operating system.")
    c = Ctx("/")
    # 404
    p404 = page(c, "Page not found | OPSMO", f'<section class="phero"><div class="wrap"><div class="phero__copy">{chip("404")}<h1 class="phero__h">This page <em>isn\'t here.</em></h1><p class="phero__p">The link may be out of date. Try the homepage or book a call.</p>{btns(c,[("Back to home","/"),("Book a Call","/book")])}</div></div></section>', "The page you were looking for could not be found.", "/404")
    p404 = p404.replace('href="./', 'href="/').replace('src="assets', 'src="/assets').replace('href="assets', 'href="/assets').replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
    open(os.path.join(B.OUT, "404.html"), "w").write(p404)
    # sitemap + robots
    pri = lambda r: "1.0" if r == "/" else ("0.9" if r.count("/") == 1 else "0.7")
    urls = sorted(set(ROUTES))
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f'  <url><loc>{SITE}{"/" if r=="/" else r+"/"}</loc><lastmod>2026-11-19</lastmod><priority>{pri(r)}</priority></url>\n' for r in urls) + "</urlset>\n"
    open(os.path.join(B.OUT, "sitemap.xml"), "w").write(sm)
    open(os.path.join(B.OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print(len(urls), "pages + sitemap")

if __name__ == "__main__":
    main()
