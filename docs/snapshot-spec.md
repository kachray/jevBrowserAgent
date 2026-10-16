# Snapshot Specification

**Status: Proposed.** Version 0.1. No implementation exists yet. Every schema, field name, and algorithm below is a design proposal for review, not a description of working code.

**Labels used throughout:**
- **Project-context fact** — reported as verified in `project-context.md` (PC), about the upstream `jev-ultrafast` project. Not a claim about TypedBrowse's own code, which does not exist yet.
- **Approved assumption** — an owner-approved default from the 2026-09-24 decisions.
- **Proposed design** — a new choice made in this document, not sourced from PC or an owner decision. Open to review.
- **Open decision** — deliberately left unresolved. Implementation must not depend on it until it is resolved.

---

## 1. Purpose and scope

The snapshot is the single observation TypedBrowse's agent loop builds from the live page at each step. It is the only representation of the page passed to two consumers: Jev, which chooses the next operation and target from it, and the independent verifier, which reads final-state facts from it (or from a similarly-shaped final observation) to decide pass or fail without consulting Jev's `DONE`.

The snapshot must be a plain, serializable data structure: JSON-compatible primitives, lists, and objects only. **Proposed design:** it must never contain a Playwright handle, a live DOM reference, a browser page object, a database connection, a provider client, an API key, or any other object that only makes sense inside a running process. This is what makes replay possible (§12) and what keeps `jev/` and `verify/` from ever needing a `browser/` import (module boundary, CLAUDE.md §"Proposed module boundaries").

The snapshot is not executable. It carries no selectors, no scripts, and no callables. `act()` (§10) resolves a snapshot's `index` back to a live node inside `browser/`; the snapshot itself never crosses that boundary.

This document defines the contract, not the extraction algorithm. How `browser/` builds a snapshot from a real Chromium page is an implementation detail behind this contract (T03 and later).

## 2. Design principles

- **Deterministic representation.** The same page state, observed twice with no page mutation in between, must produce the same snapshot, field for field, except for anything explicitly excluded as dynamic (§9).
- **Stable indexing within an observation.** Within one snapshot, an index always refers to the same control. Indexes are not guaranteed stable *across* snapshots (§6).
- **No hidden controls.** Only controls a real user could currently see and act on are included, with disabled controls handled explicitly (§6, §7) rather than silently hidden.
- **No secrets.** Passwords, file inputs, and other sensitive fields are excluded outright (§4, §13), not merely masked.
- **No executable code.** No scripts, selectors, or event handlers appear anywhere in the structure.
- **Bounded text.** Page and control text are capped and truncated (§7) so a snapshot cannot grow unboundedly or become a channel for large payloads.
- **Explicit page identity.** URL and title are first-class fields, not inferred from context, so policy checks (allowlist) and the verifier can act on them directly.
- **Explicit stale-page detection.** A fingerprint (§9) lets the loop detect that the page changed between when a decision was made and when it would be executed, and discard the decision instead of acting on stale information.
- **Compatibility with replay fixtures.** The schema must be plain enough to serialize to a file, load back, and feed through the same validation and policy code used for a live run (§12).

## 3. Snapshot schema

**Proposed design (v0.1).** No TypedBrowse implementation exists to compare this against. Field names are illustrative and listed as an open decision (§15).

```json
{
  "schema_version": "typedbrowse.snapshot.v0.1",
  "observation_id": "obs_000042",
  "timestamp": "2026-09-25T10:15:30.123Z",
  "page": {
    "url": "https://example.com/search?q=lisbon",
    "title": "Search results — Example Hotels",
    "text_summary": "Showing 12 properties in Lisbon, sorted by rating...",
    "text_truncated": false
  },
  "controls": [
    {
      "index": 0,
      "control_type": "text_input",
      "accessible_label": "Search hotels",
      "visible_text": null,
      "role": "textbox",
      "input_type": "search",
      "current_value": "lisbon",
      "options": null,
      "disabled": false,
      "visible": true,
      "required": false,
      "stable_id": "ctrl_a1b2c3",
      "actionable": true,
      "text_input_allowed": true
    },
    {
      "index": 1,
      "control_type": "button",
      "accessible_label": "Search",
      "visible_text": "Search",
      "role": "button",
      "input_type": null,
      "current_value": null,
      "options": null,
      "disabled": false,
      "visible": true,
      "required": false,
      "stable_id": "ctrl_d4e5f6",
      "actionable": true,
      "text_input_allowed": false
    }
  ],
  "fingerprint": "sha256:9f3a...c1",
  "control_count": 2,
  "control_count_truncated": false
}
```

Top-level fields:

| Field | Type | Meaning | Label |
|---|---|---|---|
| `schema_version` | string | Identifies this contract version, for replay compatibility checks. | Proposed design |
| `observation_id` | string or null | Optional identifier for tracing/logging one observation. | Proposed design (§15: "if needed") |
| `timestamp` | string (ISO 8601) | When the observation was taken. Excluded from the fingerprint (§9). | Proposed design |
| `page.url` | string | Full current URL. Used by policy allowlist and the verifier. | Proposed design |
| `page.title` | string | Document title. | Proposed design |
| `page.text_summary` | string | Bounded, normalized visible page text (§7). | Proposed design |
| `page.text_truncated` | boolean | Whether `text_summary` was cut to the max length. | Proposed design |
| `controls` | array | See §4. | Proposed design |
| `fingerprint` | string | See §9. | Proposed design |
| `control_count` | integer | Number of controls included after any cap. | Proposed design |
| `control_count_truncated` | boolean | Whether more controls existed than the cap allowed (reference cap: 250, Project-context fact, PC). | Proposed design |

**Project-context facts used as reference values, not as this schema:** the upstream snapshot is reported to cap at roughly 250 indexed controls and 6,000 characters of visible text, exclude password/file/hidden inputs, and include a fingerprint (PC §3, §9, summarizer-derived — see PC reliability note). This document reuses those as starting numbers (§7, §15) without claiming they are TypedBrowse's implemented behavior.

## 4. Control schema

**Proposed design.** One object per control in `controls[]`.

| Field | Type | May be null? | Notes |
|---|---|---|---|
| `index` | integer | No | Position in this snapshot's `controls[]`. See §6 for stability rules. |
| `control_type` | string | No | One of §5's enum, or `unknown`. |
| `accessible_label` | string | Yes | Best available accessible name (§7). Null if none could be determined. |
| `visible_text` | string | Yes | Rendered text content, when distinct from the accessible label (e.g. a button's inner text). Null for controls with no visible text (e.g. a text input). |
| `role` | string | Yes | ARIA role or closest equivalent, when available. Null if not determinable. |
| `input_type` | string | Yes | HTML input type (`text`, `search`, `email`, etc.) for input-like controls; null otherwise. |
| `current_value` | string or null | Yes, "only when safe" | Included only for non-sensitive fields (§13). Always null for password/file/hidden inputs, which are excluded from `controls[]` entirely (§6) rather than value-masked here. |
| `options` | array of strings or null | Yes, "only when safe" | Populated only for `select` and similar controls; null otherwise. Capped in length (open decision, §15). |
| `disabled` | boolean | No | Whether the control is currently disabled. Disabled controls are included, not hidden (§6). |
| `visible` | boolean | No | Whether the control is currently visible per §7's rules. |
| `required` | boolean | No | Whether the control is marked required, when determinable; defaults to `false` if unknown. |
| `stable_id` | string | Yes | An implementation-derived identity hint for debugging/tracing only. Never used by policy or the verifier as an authority. Null if not derivable. See §6 on why `index` alone is not identity across snapshots. |
| `actionable` | boolean | No | Whether the executor is allowed to treat this control as a valid `act()` target at all (combines visibility, disabled state, and control-type support). |
| `text_input_allowed` | boolean | No | Whether this control may be the target of `field_text` (§8). |

Bounding-box or positional data is **not** included in v0.1. **Open decision (§15):** whether position data is ever needed (e.g. for occlusion checks) is unresolved; nothing in the current loop design (CLAUDE.md §"Browser and DOM-control representation": "stale or occluded target: re-observe, drop the decision") requires exposing coordinates to Jev, only requires the executor to detect occlusion internally before acting.

## 5. Supported control types

**Proposed design, smallest useful set for v0.1:**

- `link`
- `button`
- `text_input`
- `textarea`
- `select`
- `checkbox`
- `radio`
- `unknown`

`unknown` is the fallback for any control the extraction logic cannot confidently classify. An `unknown` control may still appear in the snapshot (so Jev and the verifier can see it exists) but should default to `actionable: false` and `text_input_allowed: false` unless a later revision adds explicit handling.

Per the request, this v0.1 set deliberately excludes drag-and-drop, file upload, payment, CAPTCHA, and arbitrary-JavaScript controls. Nothing in `project-context.md` requires them for the in-scope tasks (Wikipedia, hotel fixture, best-effort Flights), and they are explicitly out of non-goals (context doc §1.3: no payment, no CAPTCHA handling).

## 6. Indexing rules

**Proposed design**, since no upstream indexing algorithm was extracted into `project-context.md` beyond the existence of an "indexed table" (Project-context fact, PC §1).

- **Traversal order:** document order (DOM pre-order traversal) at observation time. This is deterministic for a given page state, satisfying §2's determinism principle.
- **Hidden elements:** excluded from `controls[]` entirely per the visibility rules in §7 — they do not receive an index at all, rather than appearing with `visible: false`. (Open decision: whether "hidden" should instead be included-but-flagged, matching how disabled controls are handled below — see §15.)
- **Disabled controls:** remain in the snapshot, with `disabled: true`. They are not hidden, because Jev and the verifier need to know a control exists and why it can't currently be used (e.g. distinguishing "no submit button" from "submit button, disabled").
- **Duplicate labels:** represented as separate control entries, each with its own `index` and `stable_id`. No deduplication or merging occurs. Jev disambiguates using index, position in traversal order, and any other visible distinguishing field; exact disambiguation guidance for duplicate labels is an open decision (§15).
- **Index assignment:** indexes are assigned sequentially (0, 1, 2, ...) in traversal order at the time of the snapshot, after hidden elements are excluded and the control cap (§3, control_count_truncated) is applied.
- **Stability scope:** an index is stable **only within the snapshot that produced it.** It must not be treated as a durable identity across snapshots or across page mutations.
- **Why an index must not be reused after a page mutation:** any DOM change (a new element inserted, one removed, order changed, visibility changed) can shift which control occupies a given index. Acting on an index captured from an earlier snapshot risks acting on the wrong control. This is precisely what the fingerprint and staleness check (§9) exist to catch: any decision must be re-validated against a fresh snapshot's fingerprint before `act()` uses its index.

## 7. Visibility and text rules

**Proposed design**, kept deliberately simple per the instruction not to overengineer browser semantics. Rules not resolved here are pushed to §15 as open decisions.

- **Visible controls:** a control is visible if it has non-zero rendered size, is not `display: none`, is not `visibility: hidden`, and is not scrolled fully outside the viewport's scrollable area in a way that makes it unreachable without a scroll action the executor doesn't yet know to take. (Exact "off-screen but scrollable" handling is an open decision.)
- **Hidden controls (`display: none`):** excluded from `controls[]` (§6).
- **`visibility: hidden`:** treated the same as `display: none` — excluded, not included-with-flag. (This differs from `disabled`, which is included-with-flag; the distinction is that a disabled control is still meaningful to a user looking at the page, while a hidden one is not visible at all.)
- **Disabled controls:** included, with `disabled: true` (§6).
- **Off-screen elements:** open decision — whether "off-screen but otherwise visible" counts as `visible: true` (since a real user could scroll to it) or is excluded like `display: none`. v0.1 leans toward including it as visible, since scrolling is one of the supported action types, but this is not settled.
- **Accessible names:** `accessible_label` should prefer, in order: an explicit ARIA label, associated `<label>` text, then `placeholder` as a last resort for inputs. The exact algorithm (matching a full ARIA accessible-name computation) is an open decision (§15) — v0.1 does not commit to implementing the full spec.
- **Inner text:** `visible_text` is the control's own rendered text content (e.g. a button's label text), kept separate from `accessible_label` because they can differ.
- **Placeholder text:** used only as a fallback source for `accessible_label` when nothing else is available, never as `current_value`.
- **Whitespace normalization:** collapse runs of whitespace (including newlines) to a single space, and trim leading/trailing whitespace, for both `page.text_summary` and any control text field.
- **Maximum text length:** `page.text_summary` is capped; **proposed starting point, borrowed as a reference number from the upstream project (Project-context fact, PC §3/§9):** 6,000 characters. The exact cap for TypedBrowse is an open decision (§15) pending its own measurement.
- **Truncation markers:** when text is cut to the cap, `page.text_truncated` is set to `true`. No inline ellipsis or marker string is inserted into the text itself, so the text stays a clean prefix.

## 8. `field_text` rules

**Proposed rule, not an established fact** (this section restates and slightly expands the rule already labeled as a proposed assumption in the context document, A14):

- Exactly one text-capable target may be filled per `field_text` call. There is no batch or multi-field mode.
- The value produced is a string, or `null`. Any other shape is invalid output and results in nothing being typed.
- Maximum length: 2,000 characters. Longer output is rejected outright (not truncated and typed), since silently truncating could produce a value the caller didn't intend.
- Reject as targets: any control excluded from the snapshot as sensitive (§13) — password, file upload, or anything else classified as a secret-bearing field. These should never even reach `field_text` because they are excluded from `controls[]` in the first place (§4, §6); this rule is a second, defensive check at the point of use.
- Reject invisible or disabled controls as targets — `field_text` must check `visible: true`, `disabled: false`, and `text_input_allowed: true` on the target control before proceeding.
- Reject ambiguous targets: if the chosen index does not resolve to exactly one control with `text_input_allowed: true` in the current snapshot, treat this as invalid output (no typing), the same as an out-of-range index.
- Whitespace: preserve the value's internal whitespace as produced; only trim leading/trailing whitespace before validating length. This is separate from the page-text normalization in §7, which applies to *observed* text, not to values TypedBrowse itself writes.

## 9. Fingerprint and stale-page detection

**Proposed algorithm.** No fingerprint algorithm was extracted from upstream beyond its existence (Project-context fact, PC §3/§9 report a fingerprint field but not its formula).

- **Contributing facts:** page URL, control count, and, for each control in index order: `control_type`, `accessible_label`, `disabled`, `visible`, `required`. Concatenated (with a stable field separator) and hashed (e.g. SHA-256), producing the `fingerprint` string.
- **Control order and labels:** contribute to the fingerprint (per the list above), since a reorder or a relabeling of controls is exactly the kind of change staleness detection needs to catch.
- **Values contribute:** open decision. Including `current_value` would make the fingerprint change on every keystroke into an unrelated field, which may be too sensitive; excluding it risks missing some real page changes. v0.1 proposes **excluding** `current_value` from the fingerprint, but this is not settled (§15).
- **Dynamic timestamps excluded:** `timestamp` and `observation_id` never contribute to the fingerprint, since they change on every observation by construction and would make the fingerprint useless for staleness comparison.
- **What happens when the fingerprint changes:** any decision (a Jev choice, a planned `field_text` call) that was computed against an earlier fingerprint becomes invalid. It must not be executed.
- **When a Jev choice must be discarded:** immediately before `act()` runs, the executor re-observes (or re-checks) the current fingerprint. If it does not match the fingerprint the decision was made against, the decision is discarded and the loop re-observes fresh rather than acting (Project-context fact for the underlying behavior, PC §3.7: stale page means re-observe and drop the decision; the fingerprint-based check here is TypedBrowse's own proposed mechanism for detecting that condition).
- **How a new observation is requested:** the agent loop simply calls `observe()` again; there is no separate "refresh" operation distinct from a normal observation (§1, §3.1 of the context document's loop description).

## 10. Action contract

**Proposed design** for `act()`'s input and output shape. No implementation exists.

**Input:**

```json
{
  "target_index": 1,
  "action_type": "click",
  "value": null,
  "expected_fingerprint": "sha256:9f3a...c1"
}
```

| Field | Type | Notes |
|---|---|---|
| `target_index` | integer | Must resolve against the *current* snapshot, not a cached one. |
| `action_type` | string | One of the supported action kinds (click, fill, select, scroll, wait — reference set per Project-context fact, PC §3). |
| `value` | string or null | Used for `fill`/`select`; null for `click`/`scroll`/`wait`. |
| `expected_fingerprint` | string | Must match the current snapshot's fingerprint (§9) or the action is refused before touching the browser. |

**Output:**

```json
{
  "success": false,
  "resulting_url": "https://example.com/search?q=lisbon",
  "resulting_fingerprint": "sha256:1a2b...ff",
  "changed_page": false,
  "error_category": "stale_page"
}
```

| Field | Type | Notes |
|---|---|---|
| `success` | boolean | Whether the action executed. |
| `resulting_url` | string | URL after the attempt (unchanged on failure before navigation). |
| `resulting_fingerprint` | string | Fingerprint of the page immediately after the attempt, for the next loop iteration. |
| `changed_page` | boolean | Whether the page state changed as a result — used for the "repeated inert actions" check (Project-context fact, PC §3.7: three consecutive non-wait actions with no page change ends in BLOCKED). |
| `error_category` | string or null | One of the safe error categories below, or null on success. |

**Safe error categories:**

| Category | Meaning |
|---|---|
| `invalid_index` | `target_index` does not exist in the current snapshot. |
| `unsupported_control` | The control type does not support the requested `action_type`. |
| `disabled_control` | The target is currently disabled. |
| `stale_page` | `expected_fingerprint` did not match the current page. |
| `policy_denial` | Executor policy (allowlist/blocklist) refused the action — never a model decision. |
| `timeout` | The action did not complete within the configured timeout. |
| `browser_failure` | An underlying Playwright/browser error not covered above. |

No raw exception text or stack trace is included in this contract; only the category. Full internal error detail, if logged at all, stays server-side (CLAUDE.md: "do not expose internal stack traces").

## 11. Independent verifier input

**Proposed design.** The verifier must be able to answer "did this run reach its goal" from plain data, without importing anything from `browser/`, `jev/`, or `llm/` (module boundary already stated in CLAUDE.md and the context document, §3.3/§3.9).

Minimal facts proposed for verifier input, drawn directly from the snapshot schema (§3) plus the action contract's tail state (§10) — no new object type is introduced:

- `page.url` (final)
- `page.title` (final)
- `page.text_summary` (final)
- relevant `controls[]` entries (e.g., to check a filter checkbox's state, or that a results list is present) — matched by `accessible_label`/`role`, not by `index`, since indexes are not stable across snapshots (§6)
- the run's declared goal (supplied by the agent loop, not part of the snapshot itself)

The verifier is explicitly **not** given: Jev's chosen operation, Jev's confidence or probabilities, or Jev's `DONE`/`BLOCKED` recommendation. This is the mechanism by which "verification remains independent of Jev's `DONE` recommendation" (context document §3.9, CLAUDE.md "Jev's DONE is recorded as 'suggested'"): the verifier's function signature simply has no parameter through which that information could arrive, rather than relying on the verifier choosing to ignore it.

What exact per-task verifier logic looks like (e.g. the Flights/Wikipedia/hotel checks) is out of scope for this document and remains an open item tracked separately (context document §6, item 6: "verifier behavior for Flights, Wikipedia, and hotel fixtures").

## 12. Replay representation

**Proposed design.** Since the snapshot (§3) and action result (§10) are already plain serializable structures, a replay fixture is proposed as a sequence of them plus expected outcomes — no separate serialization format is introduced.

```json
{
  "fixture_id": "hotel_lisbon_basic",
  "schema_version": "typedbrowse.snapshot.v0.1",
  "snapshot_sequence": [
    { "...": "one snapshot object per step, as in §3" }
  ],
  "action_sequence": [
    { "...": "one act() input/output pair per step, as in §10" }
  ],
  "expected_verifier_result": {
    "pass": true,
    "notes": "Lisbon property with three filters applied"
  },
  "expected_failure_result": null
}
```

| Field | Meaning |
|---|---|
| `fixture_id` | A stable name for the fixture, referenced by eval cases (context document §4). |
| `snapshot_sequence` | The recorded snapshots for each step, in order. |
| `action_sequence` | The recorded `act()` input/output pairs, in order, aligned with `snapshot_sequence`. |
| `expected_verifier_result` | What the verifier should return when run against the final snapshot in this fixture. |
| `expected_failure_result` | Set instead of `expected_verifier_result` for fixtures designed to fail (e.g. a blocked-label case), or null. |

This is a proposed shape only; exact fixture file format (single JSON file vs. directory per fixture, naming convention) is an open decision (§15).

## 13. Security and privacy

The following must never appear in a snapshot, at any field, under any circumstance:

- No API keys, in any provider's format.
- No cookies.
- No authorization headers or tokens.
- No browser profile data (history, saved passwords, autofill data).
- No raw passwords — password-type inputs are excluded from `controls[]` entirely (§4, §6), consistent with the Project-context fact that upstream excludes password/file/hidden inputs (PC §3/§9).
- No sensitive form values — `current_value` is populated "only when safe" (§4); payment-related fields are excluded the same way as passwords.
- Page text is bounded (§7), both to keep snapshots a manageable size and to limit how much untrusted page content is ever forwarded to a provider.
- **Untrusted page content:** everything in `page.text_summary`, `accessible_label`, and `visible_text` originates from a third-party page and must be treated as untrusted data by every consumer (context document §3.8, CLAUDE.md "Tool-use rules"). The snapshot format itself does not sanitize for injection attempts (e.g. text that reads like an instruction) — that is a prompt-construction and policy concern, not a schema concern, and is handled outside the snapshot (next point).
- **Prompt-injection handling:** out of scope for this document. The snapshot only carries data; how `jev/` frames that data in a request, and how `policy/`-equivalent checks (§6 of the readiness report; CLAUDE.md "Prompt-injection and security") prevent injected page text from being treated as an instruction, are handled elsewhere.
- **URL and label policy enforcement** (allowlist, blocklist) happens outside the snapshot, in executor policy immediately before `act()` (§10's `policy_denial` category is where that shows up in this contract). The snapshot itself does not encode or enforce policy — it only reports facts (e.g. `accessible_label`) that policy code can check.

## 14. Test cases

**Proposed design**, restating the minimum fixture set already listed in the context document (§6, item 10) with the schema elements each one is meant to exercise:

| Fixture | Exercises |
|---|---|
| `hotel_page` | Full happy-path snapshot/act/verify sequence; `select`/`checkbox` controls; multi-filter verifier input (§11). |
| `injection_page` | Untrusted `page.text_summary`/`accessible_label` content designed to look like an instruction; must not affect policy or produce a blocked-label action (§13). |
| `disabled_submit_page` | `disabled: true` control present and correctly excluded from `actionable` targets (§4, §10 `disabled_control` error). |
| `overlay_page` | A control temporarily covered by another element; exercises whatever "visible but currently occluded" handling exists (open decision territory, §4/§7/§15). |
| `stale_page_case` | Fingerprint mismatch between decision time and act time; exercises `expected_fingerprint` and the `stale_page` error category (§9, §10). |
| `duplicate_label_case` | Two or more controls sharing the same `accessible_label`; exercises index-based disambiguation (§6). |
| `hidden_input_case` | A hidden or password-type input present in the DOM; must not appear in `controls[]` (§6, §13). |
| `long_text_case` | Page text exceeding the max length; exercises `text_truncated` (§7). |
| `unsupported_control_case` | A control type outside §5's set, or a supported type asked to perform an action it doesn't support; exercises `control_type: "unknown"` and/or the `unsupported_control` error category (§5, §10). |

## 15. Open decisions

- Exact snapshot field names (§3) — the names above are illustrative, not final.
- Exact fingerprint algorithm, including whether `current_value` contributes (§9).
- Whether position/bounding-box data is ever needed, e.g. for occlusion checks (§4).
- Exact accessible-name computation algorithm — how closely to follow the full ARIA accessible-name spec versus a simplified label/placeholder fallback (§7).
- Whether `page.url` and `page.title` are always available, or can be null/absent in some page states (e.g. mid-navigation).
- Whether values are included for non-sensitive fields beyond the "only when safe" principle — exact rules for which field types count as safe (§4).
- Maximum page text size for TypedBrowse specifically, versus the borrowed upstream reference value of 6,000 characters (§7).
- Whether hidden elements should be excluded entirely or included-but-flagged, matching how disabled controls are handled (§6, §7).
- Whether off-screen-but-scrollable elements count as visible (§7).
- Exact disambiguation guidance for duplicate labels beyond "index and traversal order" (§6).
- Fixture file format: single JSON file per fixture versus a directory structure (§12).
- License and attribution requirements for this document and any fixture content derived from real websites (e.g. whether a hotel-booking fixture must avoid resembling any specific real hotel site's markup or branding) — ties back to the attribution and legal stance already recorded in the context document (§1.5) but not yet resolved at the fixture-authoring level.

## 16. Status

- **Status:** Proposed
- **Owner:** Prash
- **Review required before T03**
- **No implementation should depend on unresolved fields.** Where this document says "open decision," `browser/` code (T03 onward) must either treat the field as absent/optional or stop and ask, rather than silently assuming a resolution.
