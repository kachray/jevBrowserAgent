# Snapshot Specification: Milestone 1 Subset

This document narrows `docs/snapshot-spec.md` (v0.1, Proposed) for Milestone 1 only. It does not replace the full spec. Sections are added one at a time.

## Milestone 1 scope

```
local HTML fixture -> Playwright opens it -> visible controls observed -> snapshot is serializable -> hidden and password fields excluded -> disabled controls represented -> fingerprint generated -> tests pass
```

**Labels used throughout:** every statement below is marked **Narrowed from v0.1** or **Simplified for Milestone 1**. Decisions the parent spec leaves open are marked **Owner decision (not in v0.1)**.

## 1. Top-level schema (parent section 3)

| Field | Milestone 1 | Label |
|---|---|---|
| `schema_version` | Kept | Narrowed from v0.1 |
| `page.url` | Kept | Narrowed from v0.1 |
| `page.title` | Kept | Narrowed from v0.1 |
| `page.text_summary` | Kept | Narrowed from v0.1 |
| `controls` | Kept | Narrowed from v0.1 |
| `fingerprint` | Kept | Narrowed from v0.1 |
| `control_count` | Kept | Narrowed from v0.1 |
| `observation_id` | Deferred — left null for now | Simplified for Milestone 1 |
| `timestamp` | Deferred | Simplified for Milestone 1 |
| `page.text_truncated` | Deferred | Simplified for Milestone 1 |
| `control_count_truncated` | Deferred | Simplified for Milestone 1 |

Milestone 1 enforces no cap on page text or control count; the truncation flags return when caps are added. **Simplified for Milestone 1**

## 2. Control fields (parent section 4)

| Field | Milestone 1 | Label |
|---|---|---|
| `index` | Kept | Narrowed from v0.1 |
| `control_type` | Kept | Narrowed from v0.1 |
| `accessible_label` | Kept | Narrowed from v0.1 |
| `visible_text` | Kept | Narrowed from v0.1 |
| `role` | Kept | Narrowed from v0.1 |
| `input_type` | Kept | Narrowed from v0.1 |
| `current_value` | Kept | Owner decision (not in v0.1) |
| `disabled` | Kept | Narrowed from v0.1 |
| `visible` | Kept | Narrowed from v0.1 |
| `actionable` | Kept | Narrowed from v0.1 |
| `text_input_allowed` | Kept | Narrowed from v0.1 |
| `stable_id` | Deferred | Simplified for Milestone 1 |
| `options` | Deferred | Simplified for Milestone 1 |
| `required` | Deferred | Simplified for Milestone 1 |

**Owner decisions:**
- `visible`: kept. Always true in Milestone 1, because hidden elements are excluded from controls entirely (parent section 6). **Owner decision (not in v0.1)**
- `role`: the element's explicit `role` attribute if present, otherwise null. **Owner decision (not in v0.1)**
- `current_value` for a checkbox: the string "checked" or "unchecked". **Owner decision (not in v0.1)**

## 3. Control types (parent section 5)

| Type | Milestone 1 | Label |
|---|---|---|
| `link` | Kept | Narrowed from v0.1 |
| `button` | Kept | Narrowed from v0.1 |
| `text_input` | Kept | Narrowed from v0.1 |
| `checkbox` | Kept | Narrowed from v0.1 |
| `unknown` | Kept | Narrowed from v0.1 |
| `textarea` | Deferred | Simplified for Milestone 1 |
| `select` | Deferred | Simplified for Milestone 1 |
| `radio` | Deferred | Simplified for Milestone 1 |

- `unknown` is the fallback for any control the extraction logic cannot confidently classify. An `unknown` control may still appear in the snapshot (so Jev and the verifier can see it exists) but should default to `actionable: false` and `text_input_allowed: false` unless a later revision adds explicit handling. **Narrowed from v0.1**
- Drag-and-drop, file upload, payment, CAPTCHA, and arbitrary-JavaScript controls are excluded. **Narrowed from v0.1**

**Open for owner decision:**
- How HTML elements map to the five supported types (for example a, button, input type=submit, div with role=button) is not defined in the parent spec.

## 4. Indexing rules (parent section 6)

| Rule | Milestone 1 | Label |
|---|---|---|
| 1. **Traversal order:** document order (DOM pre-order traversal) at observation time. This is deterministic for a given page state, satisfying the determinism principle in parent §2. | Kept | Narrowed from v0.1 |
| 2. **Hidden elements:** excluded from `controls[]` entirely per the visibility rules in parent §7 — they do not receive an index at all, rather than appearing with `visible: false`. | Kept | Narrowed from v0.1 |
| 3. **Disabled controls:** remain in the snapshot, with `disabled: true`. They are not hidden, because Jev and the verifier need to know a control exists and why it can't currently be used (e.g. distinguishing "no submit button" from "submit button, disabled"). | Kept | Narrowed from v0.1 |
| 4. **Duplicate labels:** represented as separate control entries, each with its own `index`. No deduplication or merging occurs. | Kept | Narrowed from v0.1 |
| 5. **Index assignment:** indexes are assigned sequentially (0, 1, 2, ...) in traversal order at the time of the snapshot, after hidden elements are excluded. | Kept | Narrowed from v0.1 |
| 6. **Stability scope:** an index is stable **only within the snapshot that produced it.** It must not be treated as a durable identity across snapshots or across page mutations. | Kept | Narrowed from v0.1 |
| 7. **Why an index must not be reused after a page mutation:** any DOM change (a new element inserted, one removed, order changed, visibility changed) can shift which control occupies a given index. Acting on an index captured from an earlier snapshot risks acting on the wrong control. | Kept | Narrowed from v0.1 |
| 8. Disambiguation guidance for duplicate labels | Deferred | Simplified for Milestone 1 |

**Adjusted for earlier decisions:**
- Rule 4 omits the parent's mention of a stable_id per control, because stable_id is deferred (section 2). **Simplified for Milestone 1**
- Rule 5 omits "after the control cap is applied", because Milestone 1 enforces no control cap (section 1). **Simplified for Milestone 1**
- Rule 7 omits the parent's statement that the fingerprint is re-checked before act() uses an index, because act() is deferred. **Simplified for Milestone 1**
- Rule 2 omits the parent's open-decision note about including hidden elements with a flag, because section 2 decided that hidden elements are excluded and `visible` is always true. **Simplified for Milestone 1**

## 5. Visibility and text rules (parent section 7)

| Rule | Milestone 1 | Label |
|---|---|---|
| 1. **Visible controls:** a control is visible if it has non-zero rendered size, is not `display: none`, is not `visibility: hidden`. | Kept | Narrowed from v0.1 |
| 2. **Hidden controls (`display: none`):** excluded from `controls[]` (parent section 6). | Kept | Narrowed from v0.1 |
| 3. **`visibility: hidden`:** treated the same as `display: none` — excluded, not included-with-flag. (This differs from `disabled`, which is included-with-flag; the distinction is that a disabled control is still meaningful to a user looking at the page, while a hidden one is not visible at all.) | Kept | Narrowed from v0.1 |
| 4. **Disabled controls:** included, with `disabled: true` (parent section 6). | Kept | Narrowed from v0.1 |
| 5. **Inner text:** `visible_text` is the control's own rendered text content (e.g. a button's label text), kept separate from `accessible_label` because they can differ. | Kept | Narrowed from v0.1 |
| 6. **Placeholder text:** used only as a fallback source for `accessible_label` when nothing else is available, never as `current_value`. | Kept | Narrowed from v0.1 |
| 7. **Whitespace normalization:** collapse runs of whitespace (including newlines) to a single space, and trim leading/trailing whitespace, for both `page.text_summary` and any control text field. | Kept | Narrowed from v0.1 |
| 8. **Accessible names:** `accessible_label` comes from the associated `<label>` element's text, then `placeholder` as a last resort for inputs. | Simplified | Simplified for Milestone 1 |
| 9. **Maximum text length** | Deferred | Simplified for Milestone 1 |
| 10. **Truncation markers** | Deferred | Simplified for Milestone 1 |
| 11. **Full ARIA accessible-name computation** | Deferred | Simplified for Milestone 1 |

**Adjusted for earlier decisions:**
- Rule 1 omits the parent's off-screen clause; the off-screen decision is recorded under Owner decisions below. **Simplified for Milestone 1**
- Rule 9 is deferred because Milestone 1 enforces no cap on page text (section 1). **Simplified for Milestone 1**
- Rule 10 is deferred because page.text_truncated is deferred (section 1). **Simplified for Milestone 1**
- Rule 8 ignores `aria-label`, because full ARIA accessible-name computation is deferred (rule 11). **Simplified for Milestone 1**
- Rule 5 keeps the parent's rationale that `visible_text` and `accessible_label` can differ. For buttons and links they now hold the same value (see Owner decisions below); they still differ for inputs. **Simplified for Milestone 1**

**Owner decisions:**
- An element that is off-screen but reachable by scrolling counts as visible and is indexed. **Owner decision (not in v0.1)**
- `accessible_label` for buttons and links is the element's own rendered text, the same value as `visible_text`. Known gap: an icon-only control that has only an `aria-label` gets a null label. **Owner decision (not in v0.1)**

## 6. Fingerprint (parent section 9)

| Element | Milestone 1 | Label |
|---|---|---|
| 1. The page URL contributes to the fingerprint. | Kept | Narrowed from v0.1 |
| 2. For each control in index order, `control_type` contributes. | Kept | Narrowed from v0.1 |
| 3. For each control, `accessible_label` contributes. | Kept | Narrowed from v0.1 |
| 4. For each control, `disabled` contributes, so a control changing between disabled and enabled changes the fingerprint. | Kept | Owner decision (not in v0.1) |
| 5. Control order contributes, so reordering or relabeling controls changes the fingerprint. | Kept | Narrowed from v0.1 |
| 6. `timestamp` and `observation_id` never contribute, since they change on every observation by construction and would make the fingerprint useless for staleness comparison. | Kept | Narrowed from v0.1 |
| 7. The facts are hashed with SHA-256, producing the `fingerprint` string. | Kept | Narrowed from v0.1 |
| 8. `current_value` does not contribute. | Excluded | Owner decision (not in v0.1) |
| 9. `visible` does not contribute, because it is always true in Milestone 1 (section 2). | Excluded | Simplified for Milestone 1 |
| 10. `required` does not contribute, because the field is deferred (section 2). | Excluded | Simplified for Milestone 1 |
| 11. `page.title` and `page.text_summary` do not contribute. | Excluded | Narrowed from v0.1 |
| 12. **What happens when the fingerprint changes:** any decision (a Jev choice, a planned `field_text` call) that was computed against an earlier fingerprint becomes invalid. It must not be executed. | Deferred | Simplified for Milestone 1 |
| 13. **When a Jev choice must be discarded:** immediately before `act()` runs, the executor re-observes (or re-checks) the current fingerprint. If it does not match the fingerprint the decision was made against, the decision is discarded and the loop re-observes fresh rather than acting. | Deferred | Simplified for Milestone 1 |
| 14. **How a new observation is requested:** the agent loop calls `observe()` again; there is no separate refresh operation distinct from a normal observation. | Deferred | Simplified for Milestone 1 |

All three deferred items depend on `act()` and the agent loop, which Milestone 1 defers. **Simplified for Milestone 1**

**Owner decisions:**
- `disabled` contributes to the fingerprint (row 4). **Owner decision (not in v0.1)**
- The hashed text is a compact JSON array of the page URL and, for each control in index order, its `control_type`, `accessible_label` and `disabled`, in the form `[url, [[control_type, accessible_label, disabled], ...]]`, with no extra whitespace and encoded as UTF-8. A null `accessible_label` stays `null` and is not converted to an empty string. The control count is not hashed separately, because the array length already carries it. **Owner decision (not in v0.1)**
- The fingerprint keeps the "sha256:" prefix, followed by the hex digest. **Owner decision (not in v0.1)**

## 7. Security and privacy (parent section 13)

| Rule | Milestone 1 | Label |
|---|---|---|
| 1. No API keys, in any provider's format. | Kept | Narrowed from v0.1 |
| 2. No cookies. | Kept | Narrowed from v0.1 |
| 3. No authorization headers or tokens. | Kept | Narrowed from v0.1 |
| 4. No browser profile data (history, saved passwords, autofill data). | Kept | Narrowed from v0.1 |
| 5. **No raw passwords:** password-type inputs are excluded from `controls[]` entirely (parent sections 4 and 6). | Kept | Narrowed from v0.1 |
| 6. **Hidden inputs** are excluded from `controls[]` entirely (parent section 14, hidden-input case). | Kept | Narrowed from v0.1 |
| 7. **Untrusted page content:** everything in `page.text_summary`, `accessible_label`, and `visible_text` originates from a third-party page and must be treated as untrusted data by every consumer. The snapshot format itself does not sanitize for injection attempts (e.g. text that reads like an instruction) — that is a prompt-construction and policy concern, not a schema concern, and is handled outside the snapshot. | Kept | Narrowed from v0.1 |
| 8. **No sensitive form values:** payment-related fields are excluded the same way as passwords (this is only the payment part of the parent's "sensitive form values" bullet; the "only when safe" part is covered by the first owner decision below). | Deferred | Simplified for Milestone 1 |
| 9. **Page text is bounded** (parent section 7), both to keep snapshots a manageable size and to limit how much untrusted page content is ever forwarded to a provider. | Deferred | Simplified for Milestone 1 |
| 10. **Prompt-injection handling:** out of scope for this document. The snapshot only carries data; how `jev/` frames that data in a request, and how `policy/`-equivalent checks prevent injected page text from being treated as an instruction, are handled elsewhere. | Deferred | Simplified for Milestone 1 |
| 11. **URL and label policy enforcement** (allowlist, blocklist) happens outside the snapshot, in executor policy immediately before `act()` (the `policy_denial` category in parent section 10 is where that shows up in this contract). The snapshot itself does not encode or enforce policy — it only reports facts (e.g. `accessible_label`) that policy code can check. | Deferred | Simplified for Milestone 1 |

Rows 8 to 11 are deferred: Milestone 1 uses only local fixtures with no payment fields, and the parent does not define how payment-related fields are detected (row 8); Milestone 1 enforces no text cap (row 9, section 1); there is no Jev integration yet (row 10); and act() is deferred (row 11). **Simplified for Milestone 1**

**Owner decisions:**
- `current_value` is populated only for checkbox controls (the string "checked" or "unchecked") and for `text_input` controls whose `input_type` is "text" or "search". It is null for every other control type and input type. **Owner decision (not in v0.1)**
- File inputs are excluded from `controls` entirely, like password and hidden inputs. **Owner decision (not in v0.1)**

**Status: Proposed.** Scope: Milestone 1 only. Sections completed: 7 (top-level schema, control fields, control types, indexing rules, visibility and text rules, fingerprint, security).
