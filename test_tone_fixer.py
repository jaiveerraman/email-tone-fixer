"""
eval/test_tone_fixer.py
Pytest tests for the Email Tone Fixer service and API.
Run: pytest eval/test_tone_fixer.py -v
"""

import sys
sys.path.insert(0, ".")

import pytest
from core.tones import get_tone, list_tones, TONE_DEFINITIONS
from core.models import FixToneRequest, AnalyseToneRequest


# ── Tone definition tests ──────────────────────────────────

def test_all_tones_exist():
    tones = list_tones()
    assert len(tones) == 5
    tone_names = [t["tone"] for t in tones]
    assert "professional" in tone_names
    assert "friendly"     in tone_names
    assert "formal"       in tone_names
    assert "assertive"    in tone_names
    assert "empathetic"   in tone_names


def test_get_tone_valid():
    tone = get_tone("professional")
    assert tone["label"]       == "Professional"
    assert "prompt"            in tone
    assert "keywords"          in tone
    assert "description"       in tone


def test_get_tone_case_insensitive():
    tone = get_tone("PROFESSIONAL")
    assert tone["label"] == "Professional"


def test_get_tone_invalid():
    with pytest.raises(ValueError) as exc:
        get_tone("aggressive")
    assert "aggressive" in str(exc.value)


def test_all_tones_have_required_fields():
    for tone_name, tone_def in TONE_DEFINITIONS.items():
        assert "label"       in tone_def, f"{tone_name} missing label"
        assert "description" in tone_def, f"{tone_name} missing description"
        assert "keywords"    in tone_def, f"{tone_name} missing keywords"
        assert "prompt"      in tone_def, f"{tone_name} missing prompt"
        assert len(tone_def["keywords"]) > 0, f"{tone_name} has empty keywords"


def test_tone_prompts_not_empty():
    for tone_name, tone_def in TONE_DEFINITIONS.items():
        assert len(tone_def["prompt"]) > 50, f"{tone_name} prompt too short"


# ── Model validation tests ─────────────────────────────────

def test_fix_tone_request_valid():
    req = FixToneRequest(
        email="Hey need that thing done now",
        target_tone="professional",
    )
    assert req.email       == "Hey need that thing done now"
    assert req.target_tone == "professional"
    assert req.context     is None


def test_fix_tone_request_with_context():
    req = FixToneRequest(
        email="Hey need that thing done now",
        target_tone="professional",
        context="Following up with a manager",
    )
    assert req.context == "Following up with a manager"


def test_fix_tone_request_email_too_short():
    with pytest.raises(Exception):
        FixToneRequest(email="Hi", target_tone="professional")


def test_analyse_tone_request_valid():
    req = AnalyseToneRequest(email="Please find attached the report you requested.")
    assert req.email == "Please find attached the report you requested."


def test_analyse_tone_request_email_too_short():
    with pytest.raises(Exception):
        AnalyseToneRequest(email="Hi")


# ── List tones tests ───────────────────────────────────────

def test_list_tones_returns_all_fields():
    tones = list_tones()
    for tone in tones:
        assert "tone"        in tone
        assert "label"       in tone
        assert "description" in tone
        assert "keywords"    in tone


def test_list_tones_descriptions_not_empty():
    tones = list_tones()
    for tone in tones:
        assert len(tone["description"]) > 10


def test_tone_keywords_are_lists():
    tones = list_tones()
    for tone in tones:
        assert isinstance(tone["keywords"], list)
        assert len(tone["keywords"]) >= 3
