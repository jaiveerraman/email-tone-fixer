"""
eval/test_tone_fixer_service.py
Service-level pytest tests for tone_fixer that mock the Anthropic client.
Run: pytest eval/test_tone_fixer_service.py -q
"""

import sys
sys.path.insert(0, ".")

import json
from types import SimpleNamespace

import pytest

from services import tone_fixer
from core.models import FixToneResponse, AnalyseToneResponse


class _Msg:
    def __init__(self, text: str):
        self.text = text


def _make_response(text: str):
    return SimpleNamespace(content=[_Msg(text)])


def test_fix_tone_success(monkeypatch):
    email = "Please send the Q3 numbers by Friday."

    payload = {
        "rewritten_email": "Please send the Q3 numbers by Friday.",
        "changes_made": ["Clarified deadline"],
        "confidence": 0.95,
    }

    response = _make_response(json.dumps(payload))

    captured = {}

    def fake_create(**kwargs):
        captured.update(kwargs)
        return response

    monkeypatch.setattr(tone_fixer, "client", SimpleNamespace(messages=SimpleNamespace(create=fake_create)))

    res: FixToneResponse = tone_fixer.fix_tone(email=email, target_tone="professional", context="Q3 reporting")

    assert res.rewritten_email == payload["rewritten_email"]
    assert res.confidence == pytest.approx(0.95)
    assert "Clarified deadline" in res.changes_made
    assert res.word_count_before == len(email.split())

    # ensure context was passed into the create call
    assert "Context: Q3 reporting" in captured["messages"][0]["content"]


def test_fix_tone_invalid_json(monkeypatch):
    email = "Short email that will be returned on failure."
    response = _make_response("not a json")

    monkeypatch.setattr(tone_fixer, "client", SimpleNamespace(messages=SimpleNamespace(create=lambda **k: response)))

    res = tone_fixer.fix_tone(email=email, target_tone="friendly")

    assert res.rewritten_email == email
    assert res.confidence == pytest.approx(0.0)
    assert any("Unable to process" in s for s in res.changes_made)


def test_analyse_tone_success(monkeypatch):
    email = "I appreciate your help on this matter."
    payload = {
        "detected_tone": "friendly",
        "confidence": 0.88,
        "tone_issues": [],
        "suggestions": ["Keep it concise"],
    }

    response = _make_response(json.dumps(payload))

    monkeypatch.setattr(tone_fixer, "client", SimpleNamespace(messages=SimpleNamespace(create=lambda **k: response)))

    res: AnalyseToneResponse = tone_fixer.analyse_tone(email=email)

    assert res.analysis.detected_tone == "friendly"
    assert res.analysis.confidence == pytest.approx(0.88)
    assert "Keep it concise" in res.analysis.suggestions


def test_analyse_tone_invalid_json(monkeypatch):
    email = "This will trigger invalid json handling."
    response = _make_response("<html>error</html>")

    monkeypatch.setattr(tone_fixer, "client", SimpleNamespace(messages=SimpleNamespace(create=lambda **k: response)))

    res = tone_fixer.analyse_tone(email=email)

    assert res.analysis.detected_tone == "unknown"
    assert res.analysis.confidence == pytest.approx(0.0)
