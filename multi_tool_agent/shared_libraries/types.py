"""Common data schema and types for wellness agents."""

from typing import Optional, Union

from google.genai import types
from pydantic import BaseModel, Field


# Convenient declaration for controlled generation.
json_response_config = types.GenerateContentConfig(
    response_mime_type="application/json"
)

class RiskDetectionResponse(BaseModel):
    """Response model for risk detection."""
    risk_level: str = Field(
        ...,
        description="The level of risk detected in the user message. Possible values: 'none', 'mild', 'moderate', 'high'."
    )
    reason: Optional[str] = Field(
        None,
        description="A brief explanation of why this risk level was assigned."
    )

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