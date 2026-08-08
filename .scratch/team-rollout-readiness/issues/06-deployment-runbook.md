# Write docs/agents/deployment.md — comparison + runbook

Type: task
Status: ready-for-agent
Blocked by: 03, 04, 05

## Question

Write the deployment & setup page at `docs/agents/deployment.md`, from **verified facts only**
(tickets 01–05), covering:

1. **Comparison vs upstream** across the three charted dimensions:
   - Install: official marketplace / public npx (upstream) vs private marketplace-add /
     authed npx (fork).
   - Update: upstream's marketplace behavior vs the fork's flow + the nudge mechanism from
     ticket 04.
   - Repo onboarding: `/setup` (local-markdown tracker, hooks) vs upstream's
     `setup-matt-pocock-skills`.
2. **Runbook**: the exact teammate install steps (from ticket 03's recorded sequence and
   ticket 05's Codex checklist), the update procedure, and troubleshooting for the known traps
   (snapshot-at-install, SSH flakiness → HTTPS, private-repo auth).
3. Keep install wording in lockstep with `.agents/install-block.md` — change it there first if
   the verified facts contradict it.

This is an internal docs/agents page (like issue-tracker.md), not a promoted-skill docs page —
the four-section template does not apply.

## Answer

(resolution pending)
