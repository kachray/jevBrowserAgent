# Snapshot Specification: Milestone 1 Subset

This document narrows `docs/snapshot-spec.md` (v0.1, Proposed) for Milestone 1 only. It does not replace the full spec. Sections are added one at a time.

## Milestone 1 scope

```
local HTML fixture -> Playwright opens it -> visible controls observed -> snapshot is serializable -> hidden and password fields excluded -> disabled controls represented -> fingerprint generated -> tests pass
```

**Labels used throughout:** every statement below is marked **Narrowed from v0.1** or **Simplified for Milestone 1**. No new design beyond the parent spec.

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

**Status: Proposed.** Scope: Milestone 1 only. Sections completed: 1 (top-level schema).
