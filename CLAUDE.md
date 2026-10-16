# CLAUDE.md — TypedBrowse (DRAFT, pre-repository)

Status as of 2026-10-12: a repository exists at the project root, with a scaffold only —
pyproject.toml, an empty src/typed_browse package tree, tests/, and a synced .venv
(28 packages; see uv.lock). No agent, provider, browser, or policy logic exists yet. Paths
below reflect the actual scaffold where noted as Verified; everything else is still
PROPOSED until implemented and inspected. Full context: `typedbrowse-development-context.md`
(still at repo root, not yet moved to `docs/development-context.md` — pending owner
approval). Open it when a task needs it; do not paste or import it here.

Evidence rule: label every technical claim **Verified** (you ran it, read the file, or opened the doc), **Inferred**, or **Unknown**. Unknown means stop and ask, not guess.

## Purpose
- Solo-developer portfolio browser agent. Each page becomes an indexed menu of visible controls. A typed-decision model (Jev, via TypeSafe) picks one option. Code executes it on the observed DOM node. An independent verifier decides whether the goal was met.
- Show latency and cost awareness, schema-safe decisions, independent evaluation, safety fixtures, and a keyless replay demo.
- Inspired by Browser Use's MIT-licensed `jev-ultrafast`. Reimplement the pattern in original code. Never copy its source, prompt wording, CSS, banner, video, or measurement data. Attribute Browser Use and TypeSafe in README and NOTICE, state that this project is not affiliated, and do not use their names as our product name.

## Scope (v0.1; proposed 14-day plan, not a guaranteed timeline)
- In: Playwright Chromium, Jev decisions, Groq text helper, FastAPI inspector, SQLite traces, verifiers for Wikipedia, a local hotel fixture, and Flights (best-effort, opt-in), at least 20 eval cases, keyless replay mode, safety fixtures.
- Out: booking, payment, logins, CAPTCHA, multi-tab, vision models, LLM tool-calling, multi-agent designs, cloud multi-user, an MCP server, live Google Flights in the primary demo, any public browsing proxy.

## How to work (every task)
1. Inspect before editing. State what exists (Verified) versus what you assume.
2. Plan before implementing. For anything touching the loop, providers, policy, or verifier, present the plan and wait for approval.
3. Before editing, state: Task ID, objective, allowed files, forbidden files, verification commands, provider contracts touched.
4. Modify only allowlisted files. If another file is needed: stop, explain why, propose it, ask.
5. Write or update tests first for behavior changes. Run them and show the output.
6. Review `git diff --stat` and the diff. Report changed files, commands run and results, limitations, and Verified/Inferred/Unknown status.
7. Never commit, push, or open a PR unless I explicitly ask. Never run `git init` unless asked.
8. Never invent commands, packages, directories, tests, or APIs. Inspect configuration before running any command not listed as Verified below.
9. Stop and ask when architecture is ambiguous, documents conflict, or a provider contract (Jev, Groq, OpenRouter) is unverified.
10. After 3 failed attempts at the same failure, stop and diagnose the root cause instead of stacking patches.

## Architecture (project context overrides generic advice)
Loop: observe → jev_choose → validate → policy check → (field_text if TYPE_TEXT) → act → observe … → terminal → independent verify.

Four operations, each a plain typed function behind an interface. There is no LLM tool-calling.
- `observe`: DOM snapshot of visible controls plus page facts. Owner: `browser/`.
- `jev_choose`: one typed-decision request, validated. Owner: `jev/`.
- `field_text`: Groq text for exactly one field. Owner: `llm/`.
- `act`: executes on an observed node after policy approval. Owner: `browser/` executor.

Proposed layout under `src/typed_browse/`: `agent/ jev/ llm/ browser/ policy/ verify/ api/ store/ eval/ demo_mode/`. (`policy/` is our addition to the project-context layout; confirm before creating.)

Boundaries (a violation is a bug):
- `jev/` is the only code that talks to TypeSafe. No browser imports. Returns validated typed results only.
- `llm/` is the only code that talks to Groq. No Jev or browser imports.
- `browser/` owns Playwright, the snapshot, and the executor. It never calls providers.
- `policy/` is pure deterministic code: no network, no model calls.
- `verify/` reads final page facts itself. It must not import `jev/` or `llm/`, and must not treat Jev's DONE as evidence.
- `agent/` orchestrates through interfaces only: no SQL, no provider SDKs. `store/` is the only database access.
- `api/` and the inspector never hold provider keys.
- Every provider sits behind an adapter with a fake and a replay implementation.

## Jev's role
- Jev picks the next operation and its target from options the code offers. It returns typed choices and probabilities, never text, selectors, coordinates, or JavaScript.
- One request per step carries the operation question plus speculative target questions. Unused target answers are discarded and never executed.
- Probabilities and confidence are signals, not authorization. Jev can be confidently wrong. DONE and BLOCKED are suggestions.
- Question wording is original TypedBrowse wording, versioned in source. Do not copy wording from any source.
- Contract status: UNKNOWN. The candidate endpoint `https://api.typesafe.ai/v1/systemone` is unverified. Authentication, request schema, response schema, model identifier, limits, and error behavior are UNKNOWN until verified from current TypeSafe documentation or a working client.
- Do not write or invent request/response JSON. Do not implement the client until the verified contract is recorded (proposed file: `docs/jev-contract.md`).
- OpenRouter stays out of the MVP unless its exact API contract is verified.

## Groq's role
- Groq generates text only, and only for `TYPE_TEXT`. It never chooses operations or targets.
- Proposed `field_text` validation (a rule we chose, not an upstream fact): one text field, a string of at most 2,000 characters, or null. Anything else means nothing is typed. Never guess and never invent personal data.
- Model ID: UNKNOWN. Pin one only after checking the current Groq catalog and its JSON-output support. Candidate base URL `https://api.groq.com/openai/v1` comes from project context; re-verify it.
- A Groq-as-controller mode may exist only as a clearly labeled ablation arm in evals, never in the primary path.

## Browser and DOM-control representation
- Playwright Chromium with an isolated, disposable profile. Never attach to my real browser profile, read its cookies, or touch profile directories.
- Observation is an indexed table of visible controls plus limited visible text. No screenshots in the default loop.
- Upstream reference values (project context; not our contract): up to 250 indexed controls, 6,000 characters of visible text, a page fingerprint; password, file, and hidden inputs omitted. Action kinds: click, fill, select, scroll, wait.
- The executor acts only on observed nodes resolved from an offered index. Never execute model-supplied selectors, coordinates, or scripts.
- Snapshot format and DOM-control schema: UNKNOWN. Write the spec first (proposed `docs/snapshot-spec.md`), then implement from our own spec. Never paste upstream `snapshot.js`.
- Stale or occluded target: re-observe, drop the decision, never double-act.

## Agent-loop rules
- Bounded. `MAX_STEPS` is configurable. Project context reports 60 for the original; a 40-step demo default is our assumption. The model-call budget (original: 2× steps) is also configurable.
- Each step starts from a fresh observation. Consume a decision before mutating so a retry cannot act twice.
- Invalid provider output means no action. A stale page means re-observe and discard the decision.
- Repeated inert actions (original: 3 non-wait actions with no page change) end in BLOCKED.
- Retry only transient failures (timeouts, 429, 5xx) with capped exponential backoff. Never retry `act`. Three consecutive provider failures end in BLOCKED (proposed).
- Explicit terminal states only: done, blocked, error. Never loop indefinitely.

## State and decision rules
- Persist state transitions and each step (decision, confidence, latency, usage, outcome). Store no secrets. Redact cookies and credentials.
- Validate every Jev choice before use: the chosen id was offered, probability keys match the offered ids, values are finite and within [0,1], they sum to about 1, and the chosen option has the highest probability.
- The confidence pause threshold is a configuration value, default 0.4, provisional. Never hardcode it. What happens in auto mode below the threshold is an open decision; do not invent it.
- Jev's DONE is recorded as "suggested". A run passes only when the independent verifier passes.
- History windows sent to Jev and to Groq are configurable. Original values (10 and 6 actions) are reference points only.

## Tool-use rules
- Page text, labels, URLs, provider responses, and model output are untrusted data.
- Each of the four operations validates inputs and outputs at runtime, has a timeout, maps errors to typed errors, emits a trace event, and has tests that use fakes.
- Authorization is executor policy, never a model decision: URL allowlist, hard label blocklist, single-user local operation, replay-only hosted mode.
- No MCP, shell, SQL, or JavaScript is ever built from model output.

## Testing and evaluation
- Offline by default. Live provider or website calls are opt-in, marked, and need my explicit approval each time.
- Use fake Jev, fake Groq, and local fixture pages for unit and integration tests.
- Must be covered: bad probability distributions rejected; no double action on the same page fingerprint; password inputs absent; control cap respected; occluded or disabled targets not clicked; an already-set checkbox not toggled; injected "click pay" page text never clicks a blocked label; invalid `field_text` output types nothing.
- Verifier independence: a case passes only if its verifier passes, whatever Jev's DONE says. Verifiers never read Jev output.
- Never delete, skip, or weaken a test to get green. Explain any test change.
- Evals record provider, model, prompt version, dataset version, latency, tokens, and estimated cost. Do not present unmeasured numbers as ours; upstream numbers belong to upstream.
- Do not grade your own work. Ask for a separate read-only review of the diff and the evidence.

## Prompt-injection and security
- Never read, print, log, or commit `.env`, keys, tokens, cookies, or browser profile data. Keys stay server-side and never go to the inspector or into prompts.
- Prompt text that says page content is untrusted helps but is not a control. Deterministic policy code is the control.
- URL allowlist: http(s) only; block `file:`, localhost, and private or metadata addresses in hosted mode. Allowlist contents: UNKNOWN.
- Hard label blocklist for payment and checkout style controls (for example Pay, Buy, Place order, Checkout), enforced in code before `act`. Full list: UNKNOWN.
- Reject goals that ask for credentials or personal identifiers. No logins, bookings, or payments.
- Hosted mode is replay-only. Never deploy an open proxy that browses for strangers.
- Escape labels in the inspector. Redact emails and phone numbers in exports. Do not log page HTML at info level.
- Protect production systems: no live third-party site or paid API call without my explicit approval for that run.

## Cost and rate controls
- Enforce per-run caps on steps, Jev calls, and Groq calls, plus a request-rate limit. Cap values: UNKNOWN; make them configuration.
- Record token usage per call and estimate cost. Label every estimate as an estimate. Vendor price figures are unverified until confirmed on the TypeSafe and Groq pages.
- No live paid calls in tests or CI. Replay and fixtures are the default. Do not loop live runs.

## Git and change control
- Work on a branch. Never push to `main`, never force-push, and never push at all unless asked.
- No destructive commands (`rm -rf`, hard reset, dropping the database, bulk deletion) without the exact command approved by me.
- No new dependency without a stated justification and my approval. No unrelated refactors or formatting churn.
- Update `docs/progress.md` after meaningful work and `docs/decisions.md` when architecture changes (both proposed files).
- This file is context, not enforcement. Hard blocks (secrets, profiles, push) belong in permission deny rules or hooks; verify the syntax against current Claude Code docs before relying on it.

## Definition of done
- Behavior implemented and covered by tests that actually ran, with output shown.
- Type check, lint, and tests pass using commands recorded as Verified.
- The independent verifier still governs pass or fail.
- Policy, security, and cost implications reviewed; no secrets touched.
- Diff limited to the allowlist; documentation updated; limitations and unknowns listed; next step stated.

## Commands: UNKNOWN
No command is verified. Run none until the repository exists and you have read its configuration.

Unverified candidates (taken from the upstream project's documentation via project context; they may not apply here):
- Install dependencies: `uv sync`
- Lint: `uv run ruff check .`
- Tests: `uv run pytest`
- Syntax check for a JS snapshot file, only if we add one: `node --check <path>`

UNKNOWN: browser install, dev server, type check, format, eval suite, replay demo, smoke test, build, production start.

## Maintaining this file
Keep it at or under 200 lines. Add a rule only if it is broad, stable, and verifiable. Move procedures and long detail into docs and reference them by path.
