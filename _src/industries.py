# Industry pages — captured verbatim. "Other industries" = first three of ORDER excluding self.
ORDER = ["real-estate","professional-services","media-advertising","events-communities","retail-ecommerce","b2b-sales-distribution","smes-growing-enterprises"]
IND = {}
IND["real-estate"] = dict(doc="Real Estate, CRM & Operations Systems | OPSMO", v="REAL_ESTATE", name="Real Estate", img="skyline",
 tagline="From portal enquiry to signed contract, without losing a lead.",
 intro="Property enquiries arrive from portals, websites and brokers within minutes. We build the capture, assignment, qualification and deal structure that turns volume into transactions.",
 flow=["Lead generation: portals, website, paid channels and broker network","Capture and deduplication: one record per buyer, source preserved","Assignment: round-robin, project or territory rules","Qualification: budget, intent, timeline and requirement captured","Viewings scheduled, logged and followed up","Deal management: unit, price, payment plan and approvals","Contract, documentation and handover to finance","Reporting on source-to-deal conversion and agent performance"],
 spec=["Portals such as Property Finder and Bayut, where API access permits, alongside website forms and campaign leads","Broker and agent management with visibility rules per team","Property and unit inventory structures linked to opportunities","Response-time automation, since enquiry speed determines conversion","Developer, agency and secondary-market process variants"])
IND["professional-services"] = dict(doc="Professional Services, CRM & Operations Systems | OPSMO", v="SERVICES", name="Professional Services", img="team",
 tagline="Pipeline, delivery and billing connected as one engagement.",
 intro="Consultancies and advisory firms sell expertise, then manage delivery and billing in different tools. We connect the commercial lifecycle end to end.",
 flow=["Enquiry and qualification against engagement criteria","Proposal, scope and approval workflow","Engagement setup with resourcing and milestones","Delivery tracking and utilisation visibility","Change requests and scope control","Invoicing and collection visibility","Client retention and account expansion"],
 spec=["Opportunity-to-project conversion without re-entry","Utilisation and billability reporting","Proposal approval by value and partner","Recurring retainer billing structures","Client portal access to approved deliverables"])
IND["media-advertising"] = dict(doc="Media & Advertising, CRM & Operations Systems | OPSMO", v="MEDIA", name="Media & Advertising", img="monitor",
 tagline="Campaign operations from brief to reconciliation.",
 intro="Media businesses run on campaign data moving between sales, planning, delivery and finance. We make that movement reliable.",
 flow=["Client and brand hierarchy","Brief and proposal management","Campaign booking and approvals","Insertion orders and rate cards","Delivery and performance data ingestion","Billing reconciliation against booked value","Renewal and client reporting"],
 spec=["Campaign and media plan objects with versioning","Rate card and discount approval control","Integration of platform delivery data where APIs allow","Client-facing performance reporting","Retainer and project billing side by side"])
IND["events-communities"] = dict(doc="Events & Communities, CRM & Operations Systems | OPSMO", v="EVENTS", name="Events & Communities", img="events",
 tagline="Registrations, sponsors and members in one operating system.",
 intro="Event and community businesses juggle registrations, sponsors and membership in parallel. We unify them into a single commercial record.",
 flow=["Registration capture and ticketing","Attendee and member records with lifecycle status","Sponsor and partner pipeline","Programme and speaker management","Check-in and attendance tracking","Post-event reporting and renewal campaigns"],
 spec=["Registration platforms integrated to CRM records","Membership tiers and renewal automation","Sponsor packages managed as opportunities","Attendee segmentation for follow-up campaigns","Event P&L visibility"])
INTEGRATION_NOTE = "Third-party integrations are built only where the provider's API or documented interface allows it. No partnership with any portal, marketplace or channel is implied."
IND["retail-ecommerce"] = dict(doc="Retail & E-commerce, CRM & Operations Systems | OPSMO", v="RETAIL", name="Retail & E-commerce", img="retail",
 tagline="Storefront, stock and service on the same customer record.",
 intro="We connect commerce platforms, ERP and customer service so orders, inventory and support history stay consistent.",
 flow=["Customer identity across storefront, marketplace and store","Order capture and fulfilment status","Inventory and availability visibility","Service requests linked to order history","Retention and repeat-purchase campaigns","Returns, refunds and reconciliation"],
 spec=["Commerce and ERP integration with conflict handling","Customer service records with order context","Segment and lifecycle automation","Stock-aware sales process for B2B and wholesale","Revenue and margin reporting by channel"])
IND["b2b-sales-distribution"] = dict(doc="B2B Sales & Distribution, CRM & Operations Systems | OPSMO", v="B2B", name="B2B Sales & Distribution", img="warehouse",
 tagline="Territories, quotations and repeat orders under control.",
 intro="Distribution businesses live on order frequency and margin discipline. We give sales teams a process they can execute and management a reliable view.",
 flow=["Account and contact hierarchy","Territory and coverage assignment","Quotation and pricing control","Order capture and fulfilment handoff","Approval of discounts and credit terms","Collection visibility","Account review and repeat order cadence"],
 spec=["Price lists, tiers and discount governance","Multi-branch and multi-warehouse structures","Field sales activity tracking","Quotation-to-order automation","Channel and product performance reporting"])
IND["smes-growing-enterprises"] = dict(doc="SMEs & Growing Enterprises, CRM & Operations Systems | OPSMO", v="SME", name="SMEs & Growing Enterprises", img="sme",
 tagline="The systems a growing company can actually run.",
 intro="Growing businesses need structure without enterprise overhead. We deliver a right-sized core that supports the next stage of growth.",
 flow=["Diagnose current tools and process gaps","Design a right-sized CRM and data model","Implement with adoption from day one","Connect the website and communication channels","Build management visibility on real data","Operate and improve as the team grows"],
 spec=["Phased delivery that fits cash flow","Configuration without unnecessary customisation","Founder-level dashboards","Documented processes so knowledge stays in the business","A clear path to managed operations after go-live"])
