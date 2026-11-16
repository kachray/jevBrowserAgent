"""Tests for the snapshot fingerprint function.

These tests pin the hashed text decided in section 6 of docs/snapshot-spec-milestone1.md
and the golden vectors in section 8.4.
"""

import re

from typed_browse.browser.fingerprint import compute_fingerprint

G1_URL = "https://example.test/"
G1_CONTROLS = [("button", "Save", False), ("link", None, True)]
G1_EXPECTED = "sha256:3e661f0bc93513b9557110dab29381e2792274dc138f4d5e237ad560e2c48b24"

G2_URL = "https://example.test/"
G2_CONTROLS = []
G2_EXPECTED = "sha256:f5cc5cee3342e5a39c5d61646932d63c9d67a9c5c61d6865c8858b1743f38c30"

G3_URL = "https://example.test/"
G3_CONTROLS = [("button", "Caf\u00e9", False)]
G3_EXPECTED = "sha256:56ff18fb9959747dc990fd8741e6b54b7b456e7bec72530d3f1176bbaf3d42cb"

PREFIX_AND_HEX = re.compile(r"^sha256:[0-9a-f]{64}$")


def test_g1_golden_vector() -> None:
    assert compute_fingerprint(G1_URL, G1_CONTROLS) == G1_EXPECTED


def test_g2_golden_vector() -> None:
    assert compute_fingerprint(G2_URL, G2_CONTROLS) == G2_EXPECTED


def test_g3_non_ascii_label_is_hashed_as_raw_utf8() -> None:
    assert compute_fingerprint(G3_URL, G3_CONTROLS) == G3_EXPECTED


def test_result_is_prefixed_sha256_and_lowercase_hex() -> None:
    result = compute_fingerprint(G1_URL, G1_CONTROLS)
    assert result.startswith("sha256:")
    assert PREFIX_AND_HEX.match(result) is not None
    assert len(result) == len("sha256:") + 64


def test_same_input_twice_is_stable() -> None:
    first = compute_fingerprint(G1_URL, G1_CONTROLS)
    second = compute_fingerprint(G1_URL, G1_CONTROLS)
    assert first == second


def test_null_label_differs_from_empty_string_label() -> None:
    with_null = compute_fingerprint(G1_URL, [("link", None, False)])
    with_empty = compute_fingerprint(G1_URL, [("link", "", False)])
    assert with_null != with_empty


def test_disabled_flag_changes_result() -> None:
    enabled = compute_fingerprint(G1_URL, [("button", "Save", False)])
    disabled = compute_fingerprint(G1_URL, [("button", "Save", True)])
    assert enabled != disabled


def test_url_changes_result() -> None:
    first = compute_fingerprint("https://example.test/", G1_CONTROLS)
    second = compute_fingerprint("https://example.test/other", G1_CONTROLS)
    assert first != second


def test_control_order_changes_result() -> None:
    forward = compute_fingerprint(
        G1_URL, [("button", "Save", False), ("link", "Home", False)]
    )
    reversed_order = compute_fingerprint(
        G1_URL, [("link", "Home", False), ("button", "Save", False)]
    )
    assert forward != reversed_order