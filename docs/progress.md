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

## 2026-11-24 — fingerprint code, spec decisions, fourth fixture
- Application code: src/typed_browse/browser/fingerprint.py with
  compute_fingerprint(url, controls), and tests/test_fingerprint.py. Nine tests,
  including golden vectors G1, G2 and G3; G3 pins the non-ASCII rule, hashing
  raw UTF-8 characters.
- Merged on main since the last entry: PR #12 (non-ASCII fingerprint hashing),
  PR #13 (unknown element policy), PR #15 (control field values), PR #16 (submit
  and page values), PR #17 (section 8 input edge case tests) and PR #18 (input
  edge cases fixture). Main is at 1bf532f, the merge of PR #18, where pytest
  shows 9 passed and ruff is clean.
- Spec decisions since the last entry, all logged in docs/decisions.md:
  2026-11-18 non-ASCII hashing; 2026-11-20 only mapped elements are indexed and
  unknown is never produced; 2026-11-20 (continued) per-type values for the five
  control fields; 2026-11-21 submit input label, page.text_summary and
  schema_version; 2026-11-22 new tests, the input_edge_cases fixture and the
  case-insensitive type rule.
- Spec section 8 now carries B1 to B11, H1 to H8, D1 to D7, G1 to G3 and I1 to
  I8 in the new section 8.5. Only the G tests exist as code.
- Fixtures: four files in tests/fixtures/, the three earlier ones plus
  input_edge_cases.html.
- Environment: Playwright Chromium is installed outside the repo, and a
  read-only check opened input_edge_cases.html by file URL: the browser treats a
  missing type as text and type SEARCH as search. The venv runs Python 3.14.10.
- Still not built: the snapshot data model, observe(), browser actions,
  stale-page detection, policy checks, the independent verifier, replay mode,
  and any Jev or Groq code.
- Not yet asserted by any test, from section 8.5: page.text_summary for a page
  with no rendered text, and the exclusion of scripts and styles from it.
- Next: the snapshot data model, written test-first from the B7 JSON round-trip,
  then observe().
- Housekeeping still open: pin the Python version; the stale CLAUDE.md status
  paragraph and its Commands: UNKNOWN section; the dev-context doc at the repo
  root; the license choice (D11); payment-field detection before a real-website
  run; the parent docs/snapshot-spec.md not yet matching this spec.
