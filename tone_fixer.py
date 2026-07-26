"""
services/tone_fixer.py
Core service — all Claude API calls for tone fixing and analysis.
"""

import json
import anthropic
from config import LLM_MODEL, LLM_MAX_TOKENS
from core.tones import get_tone
from core.models import FixToneResponse, AnalyseToneResponse, ToneAnalysis

client = anthropic.Anthropic()

# ── System prompts ─────────────────────────────────────────

FIX_SYSTEM_PROMPT = """
You are an expert email communication coach specialising in tone and style.
Your job is to rewrite emails to match a specific tone while preserving the core message.

Rules:
- Preserve the original meaning and intent completely
- Only change tone, style, and phrasing — not the facts or requests
- Never add information that wasn't in the original email
- Never remove key information from the original email
- Keep the rewrite concise — don't pad unnecessarily

Respond ONLY with a valid JSON object in this exact format:
{
  "rewritten_email": "<the full rewritten email>",
  "changes_made": ["<change 1>", "<change 2>", "<change 3>"],
  "confidence": <float between 0.0 and 1.0>
}

No preamble. No explanation. JSON only.
""".strip()

ANALYSE_SYSTEM_PROMPT = """
You are an expert email communication analyst.
Your job is to analyse the tone of an email and provide actionable feedback.

Respond ONLY with a valid JSON object in this exact format:
{
  "detected_tone": "<the dominant tone of this email>",
  "confidence": <float between 0.0 and 1.0>,
  "tone_issues": ["<issue 1>", "<issue 2>"],
  "suggestions": ["<suggestion 1>", "<suggestion 2>"]
}

No preamble. No explanation. JSON only.
""".strip()


# ── Service functions ──────────────────────────────────────

def fix_tone(email: str, target_tone: str, context: str = None) -> FixToneResponse:
    """
    Rewrite an email in the requested tone using Claude.
    Returns the rewritten email with metadata.
    """
    tone_def = get_tone(target_tone)

    context_block = f"\nContext: {context}" if context else ""

    user_message = (
        f"Tone instruction: {tone_def['prompt']}"
        f"{context_block}\n\n"
        f"Original email to rewrite:\n{email}"
    )

    response = client.messages.create(
        model=LLM_MODEL,
        max_tokens=LLM_MAX_TOKENS,
        system=FIX_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    raw = response.content[0].text.strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {
            "rewritten_email": email,
            "changes_made":    ["Unable to process — returning original email"],
            "confidence":      0.0,
        }

    return FixToneResponse(
        original_email=email,
        rewritten_email=result.get("rewritten_email", email),
        target_tone=target_tone,
        tone_label=tone_def["label"],
        changes_made=result.get("changes_made", []),
        confidence=result.get("confidence", 0.0),
        word_count_before=len(email.split()),
        word_count_after=len(result.get("rewritten_email", email).split()),
    )


def analyse_tone(email: str) -> AnalyseToneResponse:
    """
    Analyse the current tone of an email.
    Returns detected tone, issues, and suggestions.
    """
    response = client.messages.create(
        model=LLM_MODEL,
        max_tokens=LLM_MAX_TOKENS,
        system=ANALYSE_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"Analyse the tone of this email:\n\n{email}"}],
    )

    raw = response.content[0].text.strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {
            "detected_tone": "unknown",
            "confidence":    0.0,
            "tone_issues":   ["Unable to analyse tone"],
            "suggestions":   ["Please try again"],
        }

    return AnalyseToneResponse(
        email=email,
        analysis=ToneAnalysis(
            detected_tone=result.get("detected_tone", "unknown"),
            confidence=result.get("confidence", 0.0),
            tone_issues=result.get("tone_issues", []),
            suggestions=result.get("suggestions", []),
        ),
    )
