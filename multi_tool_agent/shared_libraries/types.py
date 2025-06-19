"""Common data schema and types for wellness agents."""

from typing import Optional, Union

from google.genai import types
from pydantic import BaseModel, Field
from datetime import datetime


# Convenient declaration for controlled generation.
json_response_config = types.GenerateContentConfig(
    response_mime_type="application/json"
)

class RiskDetectionResponse(BaseModel):
    """Response model for risk detection."""
    risk_score: float  # 0.0 (no risk) to 1.0 (high risk)
    risk_level: str    # "low", "medium", "high"
    reason: Optional[str] = None
    timestamp: Optional[datetime] = None

class ResourceSearchResponse(BaseModel):
    """Response model for resource search."""
    resources: list[str] = Field(
        ...,
        description="List of resources found based on the user query."
    )
    query: Optional[str] = Field(
        None,
        description="The original query used to search for resources."
    )