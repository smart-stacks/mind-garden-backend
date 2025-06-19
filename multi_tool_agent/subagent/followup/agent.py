"""Follow-up Agent in a mental wellness support system.

This agent manages ongoing monitoring and follow-up for users after initial crisis response.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from multi_tool_agent.shared_libraries.types import json_response_config
from multi_tool_agent.shared_libraries.mcp_context import mcp_context_tool
from multi_tool_agent.shared_libraries.mcp_schemas import FollowUpPlan
from . import prompt

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"

# Create the followup agent without tools since we're using output_schema
followup_agent = Agent(
    model=MODEL_GEMINI_2_0_FLASH,
    name="followup_agent",
    description="Agent specialized in managing ongoing monitoring and follow-up for users after initial crisis response.",
    instruction=prompt.FOLLOWUP_AGENT_PROMPT,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=FollowUpPlan,
    output_key="followup_plan",
    generate_content_config=json_response_config
)

# Note: We can't use both output_schema and tools in the same agent
# The MCP context will be accessed through the root agent instead
