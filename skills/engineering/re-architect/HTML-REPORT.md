# HTML Report Format

Use this format when the architectural review needs a page or the user requests one. Write a
single HTML file in the OS temp directory, resolving `$TMPDIR` before `/tmp` (or `%TEMP%` on
Windows), with a timestamped `architecture-review-<timestamp>.html` name. Preview it through the
current host when possible and include a concise candidate summary in chat. Keep the file
portable with inline CSS and diagrams: it should remain readable offline and in a locked-down
browser. Use inline SVG for call graphs and hand-built HTML/CSS for cross-sections and mass
diagrams. An accessible text label accompanies each visual.

## Scaffold

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Architecture review — {{repo name}}</title>
    <style>
      :root { font: 16px/1.5 system-ui, sans-serif; color: #182338; background: #fafaf8; }
      body { margin: 0; }
      main { max-width: 72rem; margin: auto; padding: 2rem 1rem; }
      section { margin-block: 2.5rem; }
      article, figure { background: white; border: 1px solid #cbd5e1; border-radius: .6rem; }
      article { padding: 1.25rem; margin-block: 1.5rem; }
      .diagrams { display: grid; grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr)); gap: 1rem; }
      figure { margin: 0; padding: 1rem; overflow: auto; }
      svg { display: block; width: 100%; height: auto; }
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { fill: #1e293b; stroke: #0f172a; }
      .deep-label { fill: white; }
    </style>
  </head>
  <body>
    <main>
      <header>...</header>
      <section id="candidates">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## Header

Repo name, date, and a compact legend: solid box = module, dashed line = seam, red arrow = leakage, thick dark box = deep module. No introduction paragraph — straight into the candidates.

## Candidate card

The diagrams carry the weight. Prose is sparse, plain, and uses the glossary terms (from the `/codebase-design` skill) without ceremony.

Each candidate is one `<article>`:

- **Title** — short, names the deepening (e.g. "Collapse the Order intake pipeline").
- **Badge row** — recommendation strength (`Strong` = emerald, `Worth exploring` = amber, `Speculative` = slate), plus a tag for the dependency category (`in-process`, `local-substitutable`, `ports & adapters`, `mock`).
- **Files** — monospaced list.
- **Before / After diagram** — the centrepiece. Side by side on a wide screen; stacked on a narrow one. See patterns below.
- **Problem** — one sentence. What hurts.
- **Solution** — one sentence. What changes.
- **Wins** — bullets, ≤6 words each. e.g. "Tests hit one interface", "Pricing logic stops leaking", "Delete 4 shallow wrappers".
- **ADR callout** (if applicable) — one line in an amber-tinted box.

No paragraphs of explanation. If the diagram needs a paragraph to be understood, redraw the diagram.

## Diagram patterns

Pick the pattern that fits the candidate. Mix them. Don't make every diagram look the same — variety is part of the point.

### Inline SVG graph (dependencies and call flow)

Use labelled SVG boxes and paths when the point is "X calls Y calls Z, and look at the mess."
Colour leakage edges red and the deep module dark. Put a short plain-language summary in the
`<figcaption>` so the meaning survives if the diagram cannot be seen. Sequence diagrams work
well for "before: 6 round-trips; after: 1."

```html
<figure>
  <svg viewBox="0 0 440 130" role="img" aria-labelledby="flow-title">
    <title id="flow-title">Order intake passes through three shallow modules</title>
    <rect x="8" y="35" width="110" height="55" fill="#e2e8f0" stroke="#64748b" />
    <text x="18" y="67">Handler</text>
    <path d="M118 62 H165" stroke="#64748b" stroke-width="2" />
    <rect x="165" y="35" width="110" height="55" fill="#e2e8f0" stroke="#64748b" />
    <text x="175" y="67">Validator</text>
    <path d="M275 62 H322" class="leak" stroke-width="2" />
    <rect x="322" y="35" width="110" height="55" fill="#e2e8f0" stroke="#64748b" />
    <text x="332" y="67">Repository</text>
  </svg>
  <figcaption>Before: order intake crosses three module seams; the red path marks leakage.</figcaption>
</figure>
```

### Hand-built boxes and arrows

Modules as `<div>`s with borders and labels. Arrows as inline SVG `<line>` or `<path>` elements
positioned over a relative container. Reach for this when you want the "after" diagram to feel
like one thick-bordered deep module with greyed-out internals.

### Cross-section (good for layered shallowness)

Stack horizontal CSS bands to show modules a call passes through. Before: 6 thin bands each doing
little. After: 1 thick band labelled with the consolidated responsibility.

### Mass diagram (good for "interface as wide as implementation")

Two rectangles per module — one for interface surface area, one for implementation. Before: interface rectangle is nearly as tall as the implementation rectangle (shallow). After: interface rectangle is short, implementation rectangle is tall (deep).

### Call-graph collapse

Before: a tree of function calls rendered as nested boxes. After: the same tree collapsed into one box, with the now-internal calls shown faded inside it.

## Style guidance

- Lean editorial, not corporate-dashboard. Generous whitespace. Serif optional for headings.
- Colour sparingly: one accent (emerald or indigo) plus red for leakage and amber for warnings.
- Keep diagrams ~320px tall so before/after sits comfortably side by side without scrolling.
- Use small uppercase module labels inside diagrams — they should read as schematic, not as UI.
- Keep the report static unless interaction materially improves the comparison. Any needed script
  stays inside the file, and the comparison remains readable without it.

## Top recommendation section

One larger card. Candidate name, one sentence on why, anchor link to its card. That's it.

## Tone

Plain English, concise — but the architectural nouns and verbs come straight from the `/codebase-design` skill. Concision is not an excuse to drift.

**Use exactly:** module, interface, implementation, depth, deep, shallow, seam, adapter, leverage, locality.

**Never substitute:** component, service, unit (for module) · API, signature (for interface) · boundary (for seam) · layer, wrapper (for module, when you mean module).

**Phrasings that fit the style:**

- "Order intake module is shallow — interface nearly matches the implementation."
- "Pricing leaks across the seam."
- "Deepen: one interface, one place to test."
- "Two adapters justify the seam: HTTP in prod, in-memory in tests."

**Wins bullets** name the gain in glossary terms: *"locality: bugs concentrate in one module"*, *"leverage: one interface, N call sites"*, *"interface shrinks; implementation absorbs the wrappers"*. Don't write *"easier to maintain"* or *"cleaner code"* — those terms aren't in the glossary and don't earn their place.

No hedging, no throat-clearing, no "it's worth noting that…". If a sentence could be a bullet, make it a bullet. If a bullet could be cut, cut it. If a term isn't in the `/codebase-design` glossary, reach for one that is before inventing a new one.
