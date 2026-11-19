title: Lead response time is a systems problem, not a sales problem | OPSMO Insights
cat: COMMERCIAL OPERATIONS
read: 5 MIN READ
date: 2026-10-27
h1: Lead response time is a systems problem, not a sales problem
deck: When enquiries go cold, the instinct is to push the sales team harder. Usually the delay was decided upstream: in how leads are captured, deduplicated and assigned.
---
A common conversation: enquiries are arriving, the team is working hard, and conversion is falling. The proposed fix is accountability: a dashboard showing who responded late.
That dashboard will show the wrong culprit. By the time an enquiry reaches a named salesperson, most of the delay has already happened.
### Where the time actually goes
In a typical setup, an enquiry from a portal or website passes through several stages before anyone can act on it:
- The form is submitted and lands in an inbox, not a record.
- Someone checks the inbox at the end of the day.
- The enquiry is copied into a spreadsheet or the CRM, by hand.
- A manager decides who gets it, sometimes the next morning.
- The salesperson sees it, recognises a duplicate from three months ago, and treats it as cold.
None of that is a sales performance problem. It is a routing problem, and it is entirely solvable in configuration.
### Four controls that change the number
**Capture directly into the CRM.** Website forms, portal feeds and campaign leads should create records, not emails. Every hop through a human or a mailbox adds hours and loses attribution.
**Deduplicate at ingestion.** If the same buyer enquires twice, they should appear as one record with two activity entries. Without this, assignment rules assign the same person to two agents, and both calls go badly.
**Assign on arrival, on written rules.** Round-robin within a team, territory or language match, or by project — but the rule must be explicit and the fallback owner named. Unassigned is the most expensive status in any pipeline.
**Escalate on time, not on mood.** If no first contact is logged within the service window, the record escalates to the team lead automatically. That is a workflow, not a reminder.
### Real estate makes this visible
Property enquiries are the clearest example because response speed is the entire competition. A portal lead that reaches an agent in four minutes behaves differently from one that reaches them in four hours, and the difference compounds across thousands of enquiries.
A workable flow: portal and website feeds create a deduplicated lead record, assignment runs on project or territory with a named fallback, an SLA timer starts, first contact logs automatically, and uncontacted leads escalate to the sales manager. Every step is a configuration decision, not a training slide.
### What to measure
The operational indicator is time from enquiry creation to first logged activity, segmented by source. If it is measured from the moment a salesperson receives the lead, you are measuring the wrong interval and will keep holding the wrong people accountable.
Start by timing the whole path. The first fix is usually obvious once you can see it.
