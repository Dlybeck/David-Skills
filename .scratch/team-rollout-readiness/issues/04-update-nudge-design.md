# Design the update-nudge mechanism

Type: grilling
Status: ready-for-human
Blocked by: 01

## Question

Charting decision: the plugin update story gets **mechanized**, not documented-only — a stale
installed plugin quietly running old skill text is the exact failure HANDOFF warns about, and
this repo's philosophy is hooks over prose for rules that must hold.

Design it with David (grilling + domain-modeling):
- Trigger: SessionStart hook comparing installed plugin version to the repo's latest release?
  Something else ticket 01's findings suggest?
- Version source: `gh api` latest release, git ls-remote tag, marketplace manifest? What does
  it cost per session start, and what's the offline/no-auth behavior (must fail open/silent)?
- Where it ships: inside the plugin itself (hooks/), so every installed teammate gets it?
- Nudge only, or offer the update command verbatim?
- Build now (inside this effort) or fast-follow after rollout? — resolves the fog entry.

## Answer

(resolution pending)
