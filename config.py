"""
config.py
All project-wide constants and settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = Path(__file__).parent

# LLM
LLM_MODEL      = "claude-sonnet-4-6"
LLM_MAX_TOKENS = 1024

# API
API_TITLE       = "AI Email Tone Fixer"
API_DESCRIPTION = "Rewrite emails in any tone using Claude"
API_VERSION     = "1.0.0"

# Anthropic
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Available tones
AVAILABLE_TONES = [
    "professional",
    "friendly",
    "formal",
    "assertive",
    "empathetic",
]
