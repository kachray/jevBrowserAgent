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

**Status: Proposed.** Scope: Milestone 1 only. Sections completed: 2 (top-level schema, control fields).
