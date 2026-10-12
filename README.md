# TypedBrowse

Portfolio browser agent. Each page becomes an indexed table of visible controls; a
typed-decision model (Jev, via TypeSafe) picks the next operation and target; plain code
executes it on the observed DOM node; an independent verifier decides whether the goal
was met. Jev's DONE is a suggestion, never evidence.

**Status:** draft scaffold. No agent, provider, or browser logic exists yet.

## Attribution

- Inspired by Browser Use's MIT-licensed `jev-ultrafast` project. TypedBrowse is an
  original, independent reimplementation of the pattern — not affiliated with, endorsed
  by, or derived from Browser Use's code. No upstream source, prompts, CSS, or
  measurement data is copied.
- Uses the Jev typed-decision model by TypeSafe. Not affiliated with TypeSafe.

See `NOTICE` for details. License: pending decision (D11).
