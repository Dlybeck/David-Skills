# Web report

Use the snapshot from `SKILL.md` as the content source. A webpage is a presentation of that
snapshot, not a live dashboard or an additional status authority.

- Reuse an existing report page or private project hub when the request authorizes updating it.
- For a local webpage, produce a self-contained HTML file in the project's report location,
  falling back to `.reports/status/<timestamp>-<topic>.html`. A Markdown companion is optional,
  not a prerequisite. Keep styles and any necessary scripts inline; avoid external fonts,
  analytics, or CDNs.
- For hosting, use the environment's available website-building and hosting workflow within
  the user's authorized destination and visibility. Without a configured or authorized hosting
  route, deliver the local file and explain what is needed for a remotely accessible URL.

Make the opening view show the project name, as-of time, overall assessment, current milestone,
and next action. Put the project-outcome mapping below it, followed by expandable evidence and
history only where they improve scanning. Use readable type, responsive layout, semantic
headings, and text labels alongside status colors. Support narrow phone screens and printing.

Escape source text when embedding it in HTML. Omit secrets and private local paths from a
hosted report; provide links only when they are suitable for the intended audience. Distinguish
unavailable evidence from a broken link. Verify the rendered page and links with available
browser tooling; if unavailable, check the file structure and disclose the visual-check limit.

Return the key conclusions in chat with the file or page link. State whether it is a local
file or an accessible hosted page. Keep the as-of timestamp visible; do not imply automatic
refresh or add recurring AI monitoring.
