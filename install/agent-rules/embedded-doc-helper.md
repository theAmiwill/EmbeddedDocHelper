# EmbeddedDocHelper Rules

When working on vehicle embedded hardware/software/code documents:

- Use `.vehicle-embedded-docs/` first. Run `vehicle-embedded-doc-indexer` when it is missing or stale; use `vehicle-embedded-doc-curator` for answers, crossrefs, features, and lessons.
- If PDF retrieval is weak, prefer a reliable PDF skill such as Anthropic's official `skills/pdf`; otherwise keep PDF-derived indexes `metadata-only`.
- Keep the authority order fixed: hardware documents prove correctness, software documents guide configuration, and code is only context.
- Keep portable knowledge under `portable/`, project-specific knowledge under `project/`, and never commit `.vehicle-embedded-docs/`.
- Cite source locations for engineering claims and keep new relationships `candidate` until source-verified and user-approved.
