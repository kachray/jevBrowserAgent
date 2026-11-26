"""Snapshot data model for the Milestone 1 subset."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

ControlType = Literal["link", "button", "text_input", "checkbox", "unknown"]
SCHEMA_VERSION = "typedbrowse.snapshot.v0.1-m1"
FINGERPRINT_PATTERN = r"^sha256:[0-9a-f]{64}$"


class Page(BaseModel):
    """Page-level facts: url, title and text_summary."""

    model_config = ConfigDict(extra="forbid", strict=True)

    url: str
    title: str
    text_summary: str


class Control(BaseModel):
    """One indexed control, with the eleven Milestone 1 fields."""

    model_config = ConfigDict(extra="forbid", strict=True)

    index: int
    control_type: ControlType
    accessible_label: str | None
    visible_text: str | None
    role: str | None
    input_type: str | None
    current_value: str | None
    disabled: bool
    visible: bool
    actionable: bool
    text_input_allowed: bool


class Snapshot(BaseModel):
    """A whole observation: schema version, page facts, controls and fingerprint."""

    model_config = ConfigDict(extra="forbid", strict=True)

    schema_version: Literal["typedbrowse.snapshot.v0.1-m1"] = SCHEMA_VERSION
    observation_id: str | None = None
    page: Page
    controls: list[Control]
    fingerprint: str = Field(pattern=FINGERPRINT_PATTERN)
    control_count: int

    @model_validator(mode="after")
    def _control_count_matches_controls(self) -> "Snapshot":
        """Reject a control_count that differs from len(controls)."""
        if self.control_count != len(self.controls):
            raise ValueError("control_count does not equal len(controls)")
        return self
