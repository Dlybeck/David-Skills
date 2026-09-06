# Matt Pocock skills philosophy: selectable practices, not a universal pipeline

Research snapshot: 2026-09-06. Scope: primary-source upstream philosophy, not a review of David Skills or an implementation/testing proposal. Current upstream pages can differ from the historical version this repository forked.

## Finding

The user's core understanding is supported: the collection preserves the engineer's control through small, adaptable, composable skills. However, “no workflows” is too absolute. Upstream explicitly offers recommended flows and strict discipline within selected skills. A more evidence-faithful distinction is **no single mandatory global pipeline; selected skills still have meaningful contracts and prerequisites**. This formulation is a synthesis, not a verbatim author declaration.

## Primary evidence

- **Control and composability.** The repository introduction criticizes GSD, BMAD, and Spec-Kit for owning the process and reducing user control. It describes its alternative as “small, easy to adapt, and composable” and encourages personal adaptation. This directly supports a toolkit interpretation, not a framework that must own every task. [Upstream README](https://github.com/mattpocock/skills#skills-for-real-engineers)
- **Choose your entry, with recommended routes available.** AIHero's homepage says “Start anywhere,” while also presenting a main idea-to-shipping flow. The skills catalog encourages selective installation and describes individual skills as reusable engineering habits whose outputs can compose. These pages support choice and chaining simultaneously, not the absence of process. [Homepage](https://www.aihero.dev/), [skills catalog](https://www.aihero.dev/skills)
- **Concrete evidence against obligatory spec/tickets.** The actual `ask-matt` skill branches on whether a build spans sessions: its small-build branch goes directly from understanding to implementation in the same context. It explicitly permits standalone TDD without a full spec and standalone code review. Prototype can be used whenever a runnable answer is needed; `wait-what` can interrupt another skill. Yet the router also recommends ordered preparation for larger efforts and warns that skipping synthesis after a large wayfinding exercise loses detail. Thus arbitrary ordering is not an upstream guarantee. [Router source](https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/ask-matt/SKILL.md)
- **Internal discipline remains intentional.** `implement` expects specified work, invokes TDD where possible, checks the result, requests code review, and commits. `tdd` requires agreed public test seams and a failing test before implementation. These are obligations of selected practices, not evidence that every request must traverse the entire catalog. [Implementation source](https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/implement/SKILL.md), [TDD source](https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/tdd/SKILL.md)

## Tensions and limits

Matt's first-party article *5 Agent Skills I Use Every Day* argues that memory-limited agents benefit from strict, well-defined processes encoded in skills. It then describes his own sequence of understanding, specification, tickets, and test-driven implementation. This is real evidence of an opinionated engineering process; it should not be erased to agree with a blanket anti-workflow interpretation. [Article](https://www.aihero.dev/5-agent-skills-i-use-every-day)

The router's accompanying documentation nevertheless explains why a fixed sequence would be wrong for most situations: the useful decisions are conditional branches. It also states that the router only recommends; the human chooses what to invoke next. [Router documentation](https://www.aihero.dev/skills-ask-matt)

No inspected source establishes that every skill works with any input, in any order, or that all one-shot tasks need no clarification. Nor do these sources establish a required plugin-wide state machine. Greater autonomous discretion in David Skills is a separate fork design choice, not a claim about upstream's exact behavior.
