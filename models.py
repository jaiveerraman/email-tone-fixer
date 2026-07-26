"""
core/models.py
Pydantic models for API request and response validation.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class FixToneRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "email": "Hey, I need that report ASAP. You said it would be done by now and it's not. What's going on?",
            "target_tone": "professional",
            "context": "Following up with a colleague about a delayed report",
        }
    })

    email:       str = Field(..., min_length=10, description="The original email text to rewrite")
    target_tone: str = Field(..., description="The desired tone: professional, friendly, formal, assertive, empathetic")
    context:     Optional[str] = Field(None, description="Optional context about the email situation")


class AnalyseToneRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "email": "Hey, I need that report ASAP. You said it would be done by now and it's not. What's going on?",
        }
    })

    email: str = Field(..., min_length=10, description="The email text to analyse")


class ToneAnalysis(BaseModel):
    detected_tone:   str
    confidence:      float
    tone_issues:     list[str]
    suggestions:     list[str]


class FixToneResponse(BaseModel):
    original_email:  str
    rewritten_email: str
    target_tone:     str
    tone_label:      str
    changes_made:    list[str]
    confidence:      float
    word_count_before: int
    word_count_after:  int


class AnalyseToneResponse(BaseModel):
    email:          str
    analysis:       ToneAnalysis


class ToneInfo(BaseModel):
    tone:        str
    label:       str
    description: str
    keywords:    list[str]


class HealthResponse(BaseModel):
    status:  str
    version: str
    model:   str
