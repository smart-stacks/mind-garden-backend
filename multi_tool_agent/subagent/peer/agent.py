"""Peer Agent in a mental wellness support system.

This agent facilitates connections with peer support options when appropriate
based on user needs and preferences.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from multi_tool_agent.shared_libraries.types import json_response_config
from multi_tool_agent.shared_libraries.mcp_context import mcp_context_tool
from multi_tool_agent.shared_libraries.mcp_schemas import PeerSupportMatch
from . import prompt

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"

# Create the peer agent without tools since we're using output_schema
peer_agent = Agent(
    model=MODEL_GEMINI_2_0_FLASH,
    name="peer_agent",
    description="Agent specialized in matching users with appropriate peer support options.",
    instruction=prompt.PEER_AGENT_PROMPT,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=PeerSupportMatch,
    output_key="peer_match",
    generate_content_config=json_response_config
)

# Note: We can't use both output_schema and tools in the same agent
# The MCP context will be accessed through the root agent instead
