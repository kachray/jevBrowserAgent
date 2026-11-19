"""Fingerprint of a page snapshot, used to detect a stale page."""

import hashlib
import json
from collections.abc import Sequence


def compute_fingerprint(
    url: str,
    controls: Sequence[tuple[str, str | None, bool]],
) -> str:
    """Return ``sha256:`` plus the hex SHA-256 of the snapshot's control facts.

    The hashed text is the compact JSON array
    ``[url, [[control_type, accessible_label, disabled], ...]]`` with no extra
    whitespace, encoded as UTF-8. A null label stays ``null``. Non-ASCII text
    is written with raw UTF-8 characters, not with unicode escape sequences, so
    it is hashed as those characters themselves, per section 6 of
    docs/snapshot-spec-milestone1.md.
    """
    facts = [
        [control_type, label, disabled]
        for control_type, label, disabled in controls
    ]
    text = json.dumps([url, facts], separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()