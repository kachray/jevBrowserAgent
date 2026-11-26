"""Tests for the snapshot data model (docs/snapshot-spec-milestone1.md)."""

import json

import pytest
from pydantic import ValidationError
from typed_browse.snapshot import Control, Page, Snapshot

FINGERPRINT = "sha256:" + "0" * 64
SCHEMA_VERSION = "typedbrowse.snapshot.v0.1-m1"
NULLABLE = ("accessible_label", "visible_text", "role", "input_type", "current_value")
DEFERRED = (
    ("snapshot", "timestamp"),
    ("snapshot", "control_count_truncated"),
    ("page", "text_truncated"),
    ("control", "stable_id"),
    ("control", "options"),
    ("control", "required"),
)
BAD_FINGERPRINTS = (
    "sha1:" + "0" * 64,
    "sha256:" + "A" * 64,
    "sha256:" + "0" * 63,
    "sha256:" + "0" * 65,
    "",
)
BAD_CONTROL_TYPES = ("radio", "textarea", "select", "link ", "")


def _control(**overrides: object) -> dict:
    """Return a valid control payload with the overrides applied."""
    payload: dict = {
        "index": 0,
        "control_type": "text_input",
        "accessible_label": "City",
        "visible_text": None,
        "role": None,
        "input_type": "text",
        "current_value": "",
        "disabled": False,
        "visible": True,
        "actionable": True,
        "text_input_allowed": True,
    }
    payload.update(overrides)
    return payload


def _page(**overrides: object) -> dict:
    """Return a valid page payload with the overrides applied."""
    payload: dict = {
        "url": "https://example.test/",
        "title": "Basic page",
        "text_summary": "Basic page",
    }
    payload.update(overrides)
    return payload


def _snapshot(**overrides: object) -> dict:
    """Return a valid snapshot payload with the overrides applied."""
    payload: dict = {
        "schema_version": SCHEMA_VERSION,
        "page": _page(),
        "controls": [_control()],
        "fingerprint": FINGERPRINT,
        "control_count": 1,
    }
    payload.update(overrides)
    return payload


def _b7_snapshot() -> Snapshot:
    """Build the hand-made snapshot the B7 round-trip tests use."""
    controls = [
        Control(
            index=0,
            control_type="text_input",
            accessible_label="City",
            visible_text=None,
            role=None,
            input_type="text",
            current_value="",
            disabled=False,
            visible=True,
            actionable=True,
            text_input_allowed=True,
        ),
        Control(
            index=1,
            control_type="button",
            accessible_label=None,
            visible_text=None,
            role=None,
            input_type=None,
            current_value=None,
            disabled=False,
            visible=True,
            actionable=True,
            text_input_allowed=False,
        ),
        Control(
            index=2,
            control_type="checkbox",
            accessible_label="Remember me",
            visible_text=None,
            role=None,
            input_type="checkbox",
            current_value="unchecked",
            disabled=False,
            visible=True,
            actionable=True,
            text_input_allowed=False,
        ),
    ]
    return Snapshot(
        page=Page(
            url="https://example.test/",
            title="Basic page",
            text_summary="Basic page",
        ),
        controls=controls,
        fingerprint=FINGERPRINT,
        control_count=3,
    )


def test_b7_json_round_trip_is_unchanged() -> None:
    """B7: the snapshot converts to JSON and back with no change."""
    original = _b7_snapshot()
    reloaded = Snapshot.model_validate_json(original.model_dump_json())
    assert reloaded == original


def test_b7_nulls_survive_the_round_trip() -> None:
    """B7: every null is written as null and is still present after reloading."""
    controls = json.loads(_b7_snapshot().model_dump_json())["controls"]
    for key in NULLABLE:
        assert key in controls[1]
        assert controls[1][key] is None
    assert controls[0]["current_value"] == ""
    assert controls[0]["current_value"] is not None
    assert controls[2]["current_value"] == "unchecked"


def test_observation_id_defaults_to_null() -> None:
    """B1: observation_id is null in Milestone 1 and is written as null."""
    snapshot = Snapshot.model_validate(_snapshot())
    assert snapshot.observation_id is None
    assert json.loads(snapshot.model_dump_json())["observation_id"] is None


def test_schema_version_defaults_and_is_a_literal() -> None:
    """B1: schema_version defaults to the decided string and rejects others."""
    payload = _snapshot()
    del payload["schema_version"]
    assert Snapshot.model_validate(payload).schema_version == SCHEMA_VERSION
    with pytest.raises(ValidationError):
        Snapshot.model_validate(_snapshot(schema_version="typedbrowse.snapshot.v0.1"))


def test_control_count_must_equal_the_number_of_controls() -> None:
    """B1: control_count is stored and must equal len(controls), both ways."""
    assert Snapshot.model_validate(_snapshot(control_count=1)).control_count == 1
    with pytest.raises(ValidationError):
        Snapshot.model_validate(_snapshot(control_count=2))
    with pytest.raises(ValidationError):
        Snapshot.model_validate(_snapshot(control_count=0))


@pytest.mark.parametrize("key", NULLABLE)
def test_missing_nullable_key_is_rejected(key: str) -> None:
    """Section 2: a nullable field must be written, as a value or as null."""
    payload = _control()
    del payload[key]
    with pytest.raises(ValidationError):
        Control.model_validate(payload)


def test_extra_field_is_rejected_on_every_model() -> None:
    """Decision 5: Page, Control and Snapshot all forbid extra fields."""
    with pytest.raises(ValidationError):
        Page.model_validate(_page(surprise="x"))
    with pytest.raises(ValidationError):
        Control.model_validate(_control(surprise="x"))
    with pytest.raises(ValidationError):
        Snapshot.model_validate(_snapshot(surprise="x"))


@pytest.mark.parametrize(("target", "field"), DEFERRED)
def test_deferred_field_is_rejected(target: str, field: str) -> None:
    """Sections 1 and 2: the deferred fields do not exist on the models."""
    payloads = {"snapshot": _snapshot, "page": _page, "control": _control}
    models = {"snapshot": Snapshot, "page": Page, "control": Control}
    payload = payloads[target]()
    payload[field] = None
    with pytest.raises(ValidationError):
        models[target].model_validate(payload)


@pytest.mark.parametrize("value", BAD_CONTROL_TYPES)
def test_control_type_outside_the_literal_is_rejected(value: str) -> None:
    """Section 3: only link, button, text_input, checkbox and unknown exist."""
    with pytest.raises(ValidationError):
        Control.model_validate(_control(control_type=value))
    for allowed in ("link", "button", "text_input", "checkbox", "unknown"):
        control = Control.model_validate(_control(control_type=allowed))
        assert control.control_type == allowed


@pytest.mark.parametrize("value", BAD_FINGERPRINTS)
def test_malformed_fingerprint_is_rejected(value: str) -> None:
    """Section 6: the fingerprint is sha256: plus 64 lowercase hex digits."""
    with pytest.raises(ValidationError):
        Snapshot.model_validate(_snapshot(fingerprint=value))


def test_strict_mode_rejects_coerced_scalars() -> None:
    """Decision 5: strict mode refuses a string where a bool or int is required."""
    with pytest.raises(ValidationError):
        Control.model_validate(_control(disabled="yes"))
    with pytest.raises(ValidationError):
        Control.model_validate(_control(index="0"))
