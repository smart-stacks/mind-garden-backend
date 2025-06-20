"""Detection agent. specializing in analyzing user messages for signs of emotional distress."""
import os
from google.adk.agents import LlmAgent
from multi_tool_agent.subagent.escalation.agent import escalation_agent
from multi_tool_agent.shared_libraries.types import RiskDetectionResponse, json_response_config
from . import prompt
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"

detection_agent = LlmAgent(
    model=MODEL_GEMINI_2_0_FLASH,
    name="detection_agent",
    description="Agent specialized in analyzing user messages for signs of emotional distress.",
    instruction=prompt.DETECTION_PROMPT,
    sub_agents=[escalation_agent]
)