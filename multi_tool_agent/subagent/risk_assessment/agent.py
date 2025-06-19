"""Risk Assessment Agent in a mental wellness support system.

This agent performs detailed analysis on cases flagged by the Detection Agent
to determine severity and appropriate response paths.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from multi_tool_agent.shared_libraries.types import json_response_config
from multi_tool_agent.shared_libraries.mcp_context import mcp_context_tool
from multi_tool_agent.shared_libraries.mcp_schemas import RiskAssessment
from . import prompt

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"

# Create the risk assessment agent without tools since we're using output_schema
risk_assessment_agent = Agent(
    model=MODEL_GEMINI_2_0_FLASH,
    name="risk_assessment_agent",
    description="Agent specialized in performing detailed risk assessment based on user messages and detection results.",
    instruction=prompt.RISK_ASSESSMENT_PROMPT,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=RiskAssessment,
    output_key="risk_assessment",
    generate_content_config=json_response_config
)

# Note: We can't use both output_schema and tools in the same agent
# The MCP context will be accessed through the root agent instead
