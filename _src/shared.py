# Shared data blocks captured verbatim from the original site
STAGES = [
    ("Define requirements", "Map the workflows that need improvement. Agree on must-haves, users and success measures.", "Requirements brief"),
    ("Build a shortlist", "Compare existing tools, standalone apps and connected suites. Ask vendors to demonstrate the same real workflow.", "Shortlist with trade-offs"),
    ("Compare the full cost", "Review licence seats, tiers, add-ons, usage limits and renewal terms. Include implementation, migration, integrations, training and ongoing administration.", "First-year cost comparison"),
    ("Validate integration and data", "Check native integrations, connectors and custom work. Identify which system owns each record, what syncs, what can be migrated and how failures are handled.", "Integration and migration map"),
    ("Pilot with users", "Test actual tasks with the people who will use the software. Check reporting, permissions, security and data handling.", "Pilot scorecard and decision"),
    ("Plan the rollout", "Agree what goes live first, who owns it, how users will be trained and what support they'll need.", "Phased rollout plan"),
]

FAQ = {
 "choose": [
  ("How does OPSMO help before we choose a vendor?", "We start with the workflows you need to improve and the outcomes you want. From there we define the requirements, build a shortlist, compare the full first-year cost, check how each option connects to the systems you already run, and support a pilot with the people who will use it. You end up with a documented recommendation your team can decide on."),
  ("Can we keep the software we already have?", "Often, yes. If your existing tools mostly fit, we say so and focus on the workflow and integration gaps instead of a replacement. Current systems are part of the evaluation, so a change is only recommended where it is justified by what the business needs to do."),
  ("Which costs should we compare beyond licences?", "Implementation, migration, integrations, training and ongoing administration usually outweigh the subscription itself. We compare licence seats, tiers, add-ons, usage limits and renewal terms, then add first-year implementation and running costs so the comparison reflects what you will actually spend."),
  ("Can Zoho CRM or Zoho Desk be implemented on its own?", "Yes. Zoho One is for teams that need sales, support, finance and operations to work as one suite, but Zoho CRM can be implemented as a standalone sales system and Zoho Desk as a standalone support system. Each can start small and connect to the other later."),
 ],
}

# Fit guide results (attention choice -> result); "Existing tools mostly fit" overrides
FIT = {
 "sales": ("Start with the sales process", "Leads, pipeline and follow-up usually point to CRM design: stages, ownership, assignment rules and reporting the team will use.", "Explore CRM implementation", "/solutions/crm-implementation"),
 "support": ("Start with customer support", "Requests without an owner or a response deadline are a help desk problem. Zoho Desk can be implemented on its own, then connected to sales later.", "Explore Zoho Desk implementation", "/solutions/zoho-desk-implementation"),
 "cross": ("Compare connected suites", "When several departments need the same records, a connected suite such as Zoho One is worth comparing against separate apps and integrations.", "Compare Zoho One", "/platforms/zoho"),
 "defining": ("Start with software selection", "If the problem is still taking shape, define what the software has to do before comparing products. That keeps the shortlist honest.", "Explore software selection", "/solutions/software-selection"),
 "mostly": ("Review the current setup first", "If your existing tools mostly fit, the next step is usually a workflow fix or an integration between the systems you already own rather than a replacement.", "Explore systems integration", "/solutions/api-systems-integration"),
}

ESTIMATE_NOTE = "An illustrative estimate, not a quote. Staff-hours measure combined effort across everyone involved, not calendar time. Testing, security review and procurement can be included under other work. Calendar time depends on scope and approvals."

CTA = {
 "default": ("NEXT STEP", "Let's find out what's slowing your business down.", "Tell us how your business operates today. We'll help you identify what needs to change, and what can stay as it is.",
             [("Book a Consultation", "/book"), ("Request an Operational Assessment", "/contact")]),
}

FOOTER_TAG = "Commercial operations and digital transformation. We help companies choose, implement and connect the software that runs the business."
LINKEDIN = "https://www.linkedin.com/in/mo-rashwan/"
ZOHO_REF = "https://go.zoho.com/9L1"

METHOD = [
 ("Diagnose","We map how the business actually runs today: lead sources, handoffs, approval paths, tools, data quality and reporting.",["OPERATING MAP","SYSTEMS INVENTORY","PRIORITY GAP REGISTER"]),
 ("Design","We design the target operating architecture, data model, pipeline stages, ownership, automation logic and reporting layers.",["SOLUTION ARCHITECTURE","PROCESS BLUEPRINTS","DATA & KPI MODEL"]),
 ("Implement","Configuration, custom modules, fields, permissions, forms and views, built to the design and tested against real scenarios.",["CONFIGURED SYSTEM","MIGRATION SCRIPTS","TEST SCRIPTS & SIGN-OFF"]),
 ("Integrate","We connect CRM to finance, marketing channels, websites, communication tools and enterprise applications over managed APIs.",["INTEGRATION MAP","WORKING DATA FLOWS","MONITORING & ALERTS"]),
 ("Operate","Administration, user management, troubleshooting and change control, the discipline that keeps the system trusted.",["SUPPORT PROCESS","ADMIN RUNBOOK","MONTHLY SYSTEM REVIEW"]),
 ("Optimize","We measure adoption and commercial performance, then improve workflows, automation and reporting on a planned cadence.",["ADOPTION METRICS","IMPROVEMENT BACKLOG","QUARTERLY ROADMAP"]),
]
RECEIVE = [
 "Operating process map, how the business runs today and how it will run after implementation",
 "Solution architecture and data model, documented field by field",
 "Configured, tested and permission-controlled system",
 "Integration map with field ownership, direction and failure handling",
 "Reporting layer built on agreed KPI definitions",
 "Admin runbook, workflow documentation and handover session",
 "Role-based training for every user group",
 "Post-go-live review with a prioritised improvement backlog",
]
CASES = "Published case studies appear here once clients approve them. We can discuss relevant completed work during a discovery call."
SS_TAGLINE = "Compare the real options, then choose with the team behind you."
