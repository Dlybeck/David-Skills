---
"david-skills": minor
---

Simpler authority and review. The stand-in, TPM and ready-signal machinery built for Duet is gone; what stays is one idea, written once in `implement`: a few things are the owner's alone (putting work on `main`, a credential, spending, deleting what can't be made again) and an agent can't give itself those, while everything else it decides by its own judgement. Review is by judgement too: whoever built a change tests what it could break, a fresh `independent-pr-review` comes in only when the change could really hurt something, and fixes are checked rather than re-reviewed in full. The start-of-chat hook that pointed Fable chats at `/delegate` is removed. The block on `main` and on commands that lose work is unchanged.

`writing-for-agents` now opens from that same thinking: say what a thing is for and why, so the agent can use judgement, and keep it as simple as what it's for. It points to the owner's own philosophy instead of aiming at the same process every run.
