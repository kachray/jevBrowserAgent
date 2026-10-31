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