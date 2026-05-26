import pytest
from pydantic import ValidationError

from app.schemas import ClassificationOut


def test_valid_classification_output() -> None:
    out = ClassificationOut(category="billing", confidence=0.95, rationale="Duplicate charge identified.")
    assert out.category == "billing"


def test_invalid_category_rejected() -> None:
    with pytest.raises(ValidationError):
        ClassificationOut(category="sales", confidence=0.7, rationale="Wrong label")


def test_invalid_confidence_rejected() -> None:
    with pytest.raises(ValidationError):
        ClassificationOut(category="other", confidence=1.7, rationale="Out of range")
