# Decisions

## 2026-10-12
- T01: dependency set chosen unilaterally by Claude Code, without prior owner approval —
  runtime: playwright, fastapi, pydantic, httpx;
  dev: pytest, ruff, uvicorn. Versions left unpinned in pyproject.toml; uv.lock records
  resolved versions at first sync. Build backend: hatchling (required for src layout).
- Deferred (owner decisions pending): move typedbrowse-development-context.md to
  docs/development-context.md; NOTICE license choice (D11); CLAUDE.md stale status line
  ("no repository is verified to exist" — repo now exists).
- Retroactive review: owner inspected pyproject.toml, README.md, NOTICE, .env.example,
  progress.md, and decisions.md directly on 2026-10-12 and approved keeping them, after
  flagging that T01 was executed without prior approval (see CLAUDE.md working-method
  rules on approval and on Verified/Inferred/Unknown reporting).

## 2026-10-31
- Snapshot Milestone 1, section 2 (control fields): three owner decisions, recorded here
  because docs/snapshot-spec.md (v0.1) still lists them as open and does not contain them.
  1. `visible` field: kept. Always true in Milestone 1, because hidden elements are excluded
     from controls entirely (parent section 6).
  2. `role` field: the element's explicit `role` attribute if present, otherwise null.
  3. `current_value` for a checkbox: the string "checked" or "unchecked".
- Source of record: docs/snapshot-spec-milestone1.md, section 2, committed in 4371b18.
- Status: Proposed design, decided by the owner. docs/snapshot-spec.md has NOT been updated
  to match; the two documents differ until the parent spec is revised.

## 2026-11-03
- Snapshot Milestone 1, sections 5 and 6: owner decisions, recorded here because
  docs/snapshot-spec.md (v0.1) leaves them open and does not contain them.
  Section 5 (visibility and text rules):
  1. An element that is off-screen but reachable by scrolling counts as visible and is indexed.
  2. `accessible_label` for buttons and links is the element's own rendered text, the same value
     as `visible_text`. Known gap: an icon-only control that has only an `aria-label` gets a
     null label.
  Section 6 (fingerprint):
  3. `disabled` contributes to the fingerprint.
  4. The hashed text is a compact JSON array of the page URL and, for each control in index order,
     its `control_type`, `accessible_label` and `disabled`, in the form
     `[url, [[control_type, accessible_label, disabled], ...]]`, with no extra whitespace and
     encoded as UTF-8. A null `accessible_label` stays null and is not converted to an empty
     string. The control count is not hashed separately, because the array length already
     carries it.
  5. The fingerprint keeps the "sha256:" prefix, followed by the hex digest.
  6. `current_value` does not contribute to the fingerprint (the parent proposes this but lists it
     as unsettled).
- Source of record: docs/snapshot-spec-milestone1.md, section 5 committed in 008467e and
  section 6 committed in c680bd8.
- Status: Proposed design, decided by the owner. docs/snapshot-spec.md has NOT been updated
  to match; the two documents differ until the parent spec is revised.

## 2026-11-07
- Snapshot Milestone 1, section 7 (security and privacy): two owner decisions,
  recorded here because docs/snapshot-spec.md (v0.1) does not contain them.
  1. `current_value` is populated only for checkbox controls (the string "checked"
     or "unchecked") and for `text_input` controls whose `input_type` is "text" or
     "search". It is null for every other control type and input type. This narrows
     and extends the 2026-10-31 decision on `current_value` for checkboxes.
  2. File inputs are excluded from `controls` entirely, like password and hidden
     inputs.
- Related: section 2's `current_value` row label was changed to "Owner decision
  (not in v0.1)" to match, committed in ea74739.
- Source of record: docs/snapshot-spec-milestone1.md, section 7 committed in
  f03e185.
- Status: Proposed design, decided by the owner. docs/snapshot-spec.md has NOT been
  updated to match; the two documents differ until the parent spec is revised.

## 2026-11-10
- Snapshot Milestone 1, sections 2, 3 and 8: owner decisions, recorded here because
  docs/snapshot-spec.md (v0.1) does not contain them.
  1. HTML elements map to control types as follows: `<a>` with an `href` is `link`;
     `<button>` and `<input type="submit">` are `button`; `<input>` with type `text`,
     `search` or no type is `text_input`; `<input type="checkbox">` is `checkbox`; any
     other element indexed as a control is `unknown`. Which other elements are indexed
     as `unknown` is still open.
  2. A disabled control has `actionable: false`. A disabled `text_input` also has
     `text_input_allowed: false`.
  3. Test fixtures live in `tests/fixtures/` and are named `basic_page.html`,
     `hidden_input_case.html` and `disabled_submit_page.html`. They contain ASCII text
     only, because how non-ASCII text is hashed is still open.
- Source of record: docs/snapshot-spec-milestone1.md, sections 2 and 3 committed in
  85b19ac and section 8 committed in 24b8d18.
- Status: Proposed design, decided by the owner. docs/snapshot-spec.md has NOT been
  updated to match; the two documents differ until the parent spec is revised.