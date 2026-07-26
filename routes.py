"""
api/routes.py
FastAPI route definitions for the Email Tone Fixer API.
"""

from fastapi import APIRouter, HTTPException
from core.models import (
    FixToneRequest, FixToneResponse,
    AnalyseToneRequest, AnalyseToneResponse,
    ToneInfo, HealthResponse,
)
from core.tones import list_tones, get_tone
from services.tone_fixer import fix_tone, analyse_tone
from config import API_VERSION, LLM_MODEL

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["System"])
def health():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=API_VERSION,
        model=LLM_MODEL,
    )


@router.get("/tones", response_model=list[ToneInfo], tags=["Tones"])
def get_available_tones():
    """
    List all available tones with descriptions and keywords.
    """
    return list_tones()


@router.get("/tones/{tone}", response_model=ToneInfo, tags=["Tones"])
def get_tone_info(tone: str):
    """
    Get details about a specific tone.
    """
    try:
        tone_def = get_tone(tone)
        return ToneInfo(
            tone=tone,
            label=tone_def["label"],
            description=tone_def["description"],
            keywords=tone_def["keywords"],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/fix", response_model=FixToneResponse, tags=["Tone Fixer"])
def fix_email_tone(request: FixToneRequest):
    """
    Rewrite an email in the requested tone.

    - **email**: The original email text
    - **target_tone**: One of: professional, friendly, formal, assertive, empathetic
    - **context**: Optional context about the email situation
    """
    try:
        get_tone(request.target_tone)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return fix_tone(
        email=request.email,
        target_tone=request.target_tone,
        context=request.context,
    )


@router.post("/analyse", response_model=AnalyseToneResponse, tags=["Tone Fixer"])
def analyse_email_tone(request: AnalyseToneRequest):
    """
    Analyse the current tone of an email before fixing it.

    - **email**: The email text to analyse
    """
    return analyse_tone(email=request.email)
