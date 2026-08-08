# Codex end-to-end test on David's other machine

Type: task
Status: ready-for-human
Blocked by: 02

## Question

Run the skills.sh install on the real Codex machine, using the triple-checked checklist ticket
02 produced. This machine is a pain to use — the checklist must be tight enough that one visit
suffices:

- Pre-flight: verify the auth preconditions from ticket 02 *before* running the install.
- Install one skill (`setup` plus one more) via
  `npx skills@latest add DenaliAI-Automation/Denali-DEV --skill=<name>`.
- Confirm Codex actually loads/uses the installed skill (the `agents/openai.yaml` invocation
  policy behaves: user-invoked skills don't fire implicitly).
- Run `npx skills update <name>` once to prove the update path.
- Record outcomes verbatim — they become the runbook's Codex section, and update
  `.agents/install-block.md`'s "Not yet verified end-to-end" caveat to a verified statement
  (or a documented failure).

## Answer

(resolution pending)
