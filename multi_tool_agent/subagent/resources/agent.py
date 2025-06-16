"""Resource Agent in a mental wellness support system that searches Google for relevant resources."""

from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from multi_tool_agent.shared_libraries.types import ResourceSearchResponse,json_response_config
from . import prompt
from multi_tool_agent.tools.search import google_search_grounding


MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"

resources_agent = LlmAgent(
    model=MODEL_GEMINI_2_0_FLASH,
    name="resources_agent",
    description="Gives the relevant resources to the user based on their query and use search tool to find resources.",
    instruction=prompt.RESOURCE_AGENT_INSTRUCTION,
    tools=[google_search_grounding]
)