"""Escalation Agent in a mental wellness support system that escalates."""

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from multi_tool_agent.shared_libraries.types import ResourceSearchResponse,json_response_config
from . import prompt
from multi_tool_agent.tools.search import google_search_grounding
from multi_tool_agent.shared_libraries.types import ResourceSearchResponse,json_response_config

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"

escalation_agent = LlmAgent (
    model=MODEL_GEMINI_2_0_FLASH,
    name="escalation_agent",
    description="Share escalation contact information with the user.",
    instruction=prompt.ESCALATION_PROMPT,
    tools=[google_search_grounding]
    
    )