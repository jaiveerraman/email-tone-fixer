"""
core/tones.py
Tone definitions, descriptions, and system prompts for each tone.
"""

TONE_DEFINITIONS = {
    "professional": {
        "label":       "Professional",
        "description": "Clear, confident, and respectful. Suitable for workplace communication.",
        "keywords":    ["clear", "concise", "respectful", "confident", "objective"],
        "prompt":      (
            "Rewrite this email in a professional tone. "
            "Use clear, confident, and respectful language. "
            "Avoid slang, overly casual phrases, and emotional language. "
            "Be direct and get to the point quickly. "
            "Maintain a courteous and objective tone throughout."
        ),
    },
    "friendly": {
        "label":       "Friendly",
        "description": "Warm, approachable, and conversational. Great for colleagues you know well.",
        "keywords":    ["warm", "approachable", "casual", "personable", "positive"],
        "prompt":      (
            "Rewrite this email in a friendly tone. "
            "Use warm, approachable, and conversational language. "
            "It's okay to use light contractions and casual phrases. "
            "Show genuine interest and positivity. "
            "Keep it natural and human — avoid sounding robotic or overly formal."
        ),
    },
    "formal": {
        "label":       "Formal",
        "description": "Highly structured and traditional. Ideal for legal, executive, or official communication.",
        "keywords":    ["structured", "traditional", "official", "polished", "precise"],
        "prompt":      (
            "Rewrite this email in a formal tone. "
            "Use highly structured, traditional, and polished language. "
            "Avoid contractions, slang, and casual phrases entirely. "
            "Address the recipient with appropriate titles where applicable. "
            "Maintain a tone suitable for official, legal, or executive communication."
        ),
    },
    "assertive": {
        "label":       "Assertive",
        "description": "Direct, confident, and action-oriented. Useful for follow-ups and negotiations.",
        "keywords":    ["direct", "confident", "action-oriented", "firm", "decisive"],
        "prompt":      (
            "Rewrite this email in an assertive tone. "
            "Be direct, confident, and action-oriented. "
            "State expectations and deadlines clearly. "
            "Avoid passive language — use active voice. "
            "Be firm without being aggressive or rude. "
            "Make it clear what you need and by when."
        ),
    },
    "empathetic": {
        "label":       "Empathetic",
        "description": "Compassionate and understanding. Best for difficult conversations or complaints.",
        "keywords":    ["compassionate", "understanding", "supportive", "caring", "considerate"],
        "prompt":      (
            "Rewrite this email in an empathetic tone. "
            "Show genuine understanding and compassion for the recipient's situation. "
            "Acknowledge their feelings or concerns before addressing the matter. "
            "Use supportive and considerate language. "
            "Avoid blunt or dismissive phrasing. "
            "Make the recipient feel heard and valued."
        ),
    },
}


def get_tone(tone: str) -> dict:
    """Return tone definition by name. Raises ValueError if not found."""
    tone = tone.lower().strip()
    if tone not in TONE_DEFINITIONS:
        raise ValueError(
            f"Invalid tone '{tone}'. "
            f"Available tones: {', '.join(TONE_DEFINITIONS.keys())}"
        )
    return TONE_DEFINITIONS[tone]


def list_tones() -> list[dict]:
    """Return all available tones with their labels and descriptions."""
    return [
        {
            "tone":        key,
            "label":       value["label"],
            "description": value["description"],
            "keywords":    value["keywords"],
        }
        for key, value in TONE_DEFINITIONS.items()
    ]
