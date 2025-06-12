"""Detection agent. specializing in analyzing user messages for signs of emotional distress."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from multi_tool_agent.shared_libraries.types import RiskDetectionResponse, json_response_config
from . import prompt

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"

detection_agent = Agent(
    model=MODEL_GEMINI_2_0_FLASH,
    name="detection_agent",
    description="Agent specialized in analyzing user messages for signs of emotional distress.",
    instruction=prompt.DETECTION_PROMPT,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=RiskDetectionResponse,
    output_key="risk_detection",
    generate_content_config=json_response_config,)