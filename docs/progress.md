# Progress

## 2026-10-12 — T01 scaffold
- Created: pyproject.toml, README.md, NOTICE, .env.example, src/typed_browse package
  skeleton (10 empty subpackages), tests/, docs/progress.md, docs/decisions.md.
- No logic. No provider code. Jev contract still Unknown; client blocked on
  docs/jev-contract.md (not written — contract unverified).
- Development-context doc remains at repo root; move to docs/development-context.md
  pending owner approval.
- NOTICE license text pending owner decision (D11).
- Verification: uv sync, import check, pytest, ruff — output recorded in session report.

## 2026-11-14 — snapshot spec and fixtures
- Snapshot Milestone 1 spec is complete through section 8 (test cases, including two
  fingerprint golden vectors). Sections 7 and 8 merged to main in PRs #6 and #8.
- Three local HTML fixtures added under tests/fixtures/: basic_page.html,
  hidden_input_case.html, disabled_submit_page.html. Merged to main in 04d8814.
- Decisions are logged in docs/decisions.md through 2026-11-10.
- Still no application code, no tests, and no Playwright browser installed.
- Next: final review of the Milestone 1 spec, Playwright browser install (needs owner
  approval), then observe() with tests.
