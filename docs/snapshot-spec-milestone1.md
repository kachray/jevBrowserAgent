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
| `current_value` | Kept | Narrowed from v0.1 |
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
| **Traversal order:** document order (DOM pre-order traversal) at observation time. This is deterministic for a given page state, satisfying the determinism principle in parent §2. | Kept | Narrowed from v0.1 |
| **Hidden elements:** excluded from `controls[]` entirely per the visibility rules in parent §7 — they do not receive an index at all, rather than appearing with `visible: false`. | Kept | Narrowed from v0.1 |
| **Disabled controls:** remain in the snapshot, with `disabled: true`. They are not hidden, because Jev and the verifier need to know a control exists and why it can't currently be used (e.g. distinguishing "no submit button" from "submit button, disabled"). | Kept | Narrowed from v0.1 |
| **Duplicate labels:** represented as separate control entries, each with its own `index`. No deduplication or merging occurs. | Kept | Narrowed from v0.1 |
| **Index assignment:** indexes are assigned sequentially (0, 1, 2, ...) in traversal order at the time of the snapshot, after hidden elements are excluded. | Kept | Narrowed from v0.1 |
| **Stability scope:** an index is stable **only within the snapshot that produced it.** It must not be treated as a durable identity across snapshots or across page mutations. | Kept | Narrowed from v0.1 |
| **Why an index must not be reused after a page mutation:** any DOM change (a new element inserted, one removed, order changed, visibility changed) can shift which control occupies a given index. Acting on an index captured from an earlier snapshot risks acting on the wrong control. | Kept | Narrowed from v0.1 |
| Disambiguation guidance for duplicate labels | Deferred | Simplified for Milestone 1 |

**Adjusted for earlier decisions:**
- Rule 4 omits the parent's mention of a stable_id per control, because stable_id is deferred (section 2). **Simplified for Milestone 1**
- Rule 5 omits "after the control cap is applied", because Milestone 1 enforces no control cap (section 1). **Simplified for Milestone 1**
- Rule 7 omits the parent's statement that the fingerprint is re-checked before act() uses an index, because act() is deferred. **Simplified for Milestone 1**
- Rule 2 omits the parent's open-decision note about including hidden elements with a flag, because section 2 decided that hidden elements are excluded and `visible` is always true. **Simplified for Milestone 1**

**Status: Proposed.** Scope: Milestone 1 only. Sections completed: 4 (top-level schema, control fields, control types, indexing rules).
