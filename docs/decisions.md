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