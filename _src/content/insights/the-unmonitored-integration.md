title: The integration nobody monitors is the one that breaks revenue | OPSMO Insights
cat: AUTOMATION
read: 6 MIN READ
date: 2026-10-19
h1: The integration nobody monitors is the one that breaks revenue
deck: A sync that fails silently is worse than no sync at all: decisions keep being made on data that stopped updating weeks ago. What a monitored integration looks like.
---
Integrations fail quietly. An API token expires, a field is renamed on one side, a rate limit is hit during a campaign spike , and nothing in the business notices for weeks, because the visible symptom is not an error. It is a number that stopped moving.
That is worse than no integration at all. Without one, someone re-types data and eventually notices the gap. With a silent one, the process looks automated while decisions are made on stale records.
### The three failure modes worth designing for
**Authentication and permission drift.** Credentials expire, scopes change, an admin leaves and their token is revoked. The integration worked for nine months and then stopped.
**Shape change.** A field is added, renamed or made mandatory upstream. The payload still arrives; it just no longer maps correctly. Records sync with empty fields rather than failing loudly.
**Volume and timing.** A campaign or month-end batch pushes more records than the endpoint accepts, records queue, retries collide, and duplicates appear.
### What a monitored integration includes
- A health check that runs independently of the data flow. Not "did the last sync succeed" but "has anything been received in the expected window". Silence is a failure state.
- Structured error logging. Which record, which field, which response code. An alert that says "integration failed" generates a support ticket; one that says "record 48213 rejected: stage value not in target picklist" generates a fix.
- Retry with backoff, and a dead-letter path. Transient failures should self-heal. Persistent ones should stop retrying and surface, with the record preserved for replay.
- Idempotency. Every record carries a stable external identifier so a retried message cannot create a duplicate.
- Reconciliation, not just synchronisation. A daily or weekly count and checksum between source and target. This is the control that catches the failures monitoring misses.
- A named owner. Not "IT" , a person who receives the alert and knows what the integration is supposed to do.
### The commercial cost
In practice, the damage shows up as commercial rather than technical: an invoice batch that never reached finance, a closed deal that never appeared in reporting, a customer whose service history didn't follow them into the support system.
None of these look like integration failures in the monthly review. They look like a finance discrepancy, a forecasting miss and an unhappy customer.
### A reasonable standard
If you cannot answer, today, when the integration last successfully processed a record and how many records are pending, then it is not monitored , it is hoped for. That is the standard worth holding implementations to, including our own.
