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

**Status: Proposed.** Scope: Milestone 1 only. Sections completed: 3 (top-level schema, control fields, control types).
