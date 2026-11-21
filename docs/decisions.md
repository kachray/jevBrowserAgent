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

## 2026-11-18
- Snapshot spec section 6 (fingerprint) and section 8.4 (golden vectors): one owner
  decision, recorded here because docs/snapshot-spec.md (v0.1) does not contain it.
  1. The hashed text is written with raw UTF-8 characters, not with unicode escape
     sequences, so non-ASCII characters are hashed as their UTF-8 encoding.
- Related: golden vector G3 was added as a row in section 8.4 and as a test, and the
  open item about non-ASCII hashing was removed from the spec.
- Related: the 2026-11-10 entry said the fixtures contain ASCII text only because this
  question was still open; this entry closes it.
- Source of record: docs/snapshot-spec-milestone1.md committed in 2c02988; test
  committed in ed01433.
- Status: Proposed design, decided by the owner. docs/snapshot-spec.md has NOT been
  updated to match; the two documents differ until the parent spec is revised.

## 2026-11-20
- Snapshot spec section 3 (control types): one owner decision, recorded here
  because docs/snapshot-spec.md (v0.1) does not contain it.
  1. In Milestone 1 only the elements in the section 3 mapping are indexed as
     controls. Any other element, or any other input type, is not indexed. The
     type `unknown` stays defined in the schema but is never produced in
     Milestone 1. Examples of what is not indexed: an `a` element without an
     `href`, `textarea`, `select`, radio inputs, and input types other than
     `text`, `search`, `checkbox` and `submit`. Password, hidden and file inputs
     stay excluded as already decided. Real handling of unsupported controls is
     left to a later revision, together with the `unsupported_control_case`
     fixture.
- Related: the 2026-11-10 entry, decision 1, said which other elements are indexed
  as `unknown` was still open. This entry settles it: the fallback rule "any other
  element indexed as a control is `unknown`" is replaced with the not-indexed rule,
  and the open item was removed from section 3 of the spec.
- Source of record: docs/snapshot-spec-milestone1.md section 3, committed in
  9951b5e.
- Status: Proposed design, decided by the owner. docs/snapshot-spec.md has NOT been
  updated to match; the two documents differ until the parent spec is revised.

## 2026-11-20 (continued)
- Snapshot spec section 2 (control fields) and section 8.4 (open items): one
  owner decision, recorded here because docs/snapshot-spec.md (v0.1) does not
  contain it.
  1. `link` (an `a` element with an `href`): actionable true, text_input_allowed
     false, visible_text the rendered text, input_type null, current_value null.
  2. `button` (the `button` element): the same five values as `link`.
  3. `text_input`: actionable true, text_input_allowed true, visible_text null,
     input_type the type attribute lowercased, or `text` if the attribute is
     absent, current_value the value, or the empty string if the value is empty.
  4. `checkbox`: actionable true, text_input_allowed false, visible_text null,
     input_type `checkbox`, current_value `checked` or `unchecked` as a string.
  `visible` is always true in Milestone 1, so actionable for a supported control
  depends only on disabled. The disabled rule from the 2026-11-10 entry stays.
- Related: an empty text input has current_value as the empty string, not null,
  so an empty value stays distinct from the null that means not applicable.
  This adds to the 2026-11-07 decision on current_value and does not change it.
- Related: section 5 rule 5 says visible_text is the control's own rendered
  text. The spec reconciles it with a null visible_text for text inputs and
  checkboxes by a note in section 2; rule 5 itself was left unchanged.
- Related: the `input` element with type `submit` is not decided. Its
  accessible_label, visible_text and input_type stay open in the section 8.4
  open block. Three open items were removed from that block: the empty text
  input current_value; visible_text and input_type for other controls; and
  actionable and text_input_allowed. No test asserts the new values yet.
- Source of record: docs/snapshot-spec-milestone1.md sections 2 and 8.4,
  committed in dfd2134.
- Status: Proposed design, decided by the owner. docs/snapshot-spec.md has NOT been
  updated to match; the two documents differ until the parent spec is revised.

## 2026-11-21
- Snapshot spec sections 1, 2, 5 and 8.4: two owner decisions, recorded here
  because docs/snapshot-spec.md (v0.1) does not contain them.
  1. The `input` element with type `submit` is a `button` by the 2026-11-10
     mapping. Its `accessible_label` is the `value` attribute,
     whitespace-normalized as in section 5 rule 7, and null if the attribute is
     absent; its `visible_text` is the same value; its `input_type` is `submit`;
     and `actionable`, `text_input_allowed` and `current_value` are as for the
     `button` element, so true, false and null when it is enabled, with the
     disabled rule staying. A submit input shows its `value` attribute as its
     button text, which is the own-rendered-text rule already decided for
     buttons. With no `value` attribute the browser shows a default label that
     is not read, so the label is null. Section 5 rule 8, the label element and
     then `placeholder`, does not apply to a submit input; that carve-out is
     stated in the spec, and rule 8 itself was not changed.
  2. Page-level values:
     a. `page.text_summary` is the page's rendered visible text,
        whitespace-normalized as in section 5 rule 7. It excludes content that
        is `display: none` or `visibility: hidden`, and excludes scripts and
        styles. It includes the text of buttons and links, with no
        deduplication against the controls. It excludes input values and
        placeholders, including the value of a submit input. It is the empty
        string if the page has no rendered text. There is no length cap in
        Milestone 1.
     b. `schema_version` is the string `typedbrowse.snapshot.v0.1-m1`, because
        the Milestone 1 fingerprint formula differs from the parent spec's, so
        the string says this is the Milestone 1 subset and not plain v0.1.
- Related: the 2026-11-20 (continued) entry said the submit input was not
  decided; this entry settles it, and the open item about the submit input was
  removed from the section 8.4 open block. What remains there is one sentence
  saying the section 2 values and the page-level values in sections 1 and 5 are
  decided but not yet asserted by any test.
- Related: the section 1 rows for `schema_version` and `page.text_summary` still
  read "Kept, Narrowed from v0.1"; the values are recorded as separate owner
  decisions below them. The section 5 adjusted note that `visible_text` and
  `accessible_label` still differ for inputs was left unchanged, and the new
  section 5 bullet states the submit exception beside it.
- Source of record: docs/snapshot-spec-milestone1.md sections 1, 2, 5 and 8.4,
  committed in f3083ac.
- Status: Proposed design, decided by the owner. docs/snapshot-spec.md has NOT been
  updated to match; the two documents differ until the parent spec is revised.