import datetime
import os
import asyncio
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from google.genai import types # For creating message Content/Parts
from dotenv import load_dotenv
from . import prompt
from .subagent.detection.agent import detection_agent
from .subagent.resources.agent import resources_agent
from .subagent.escalation.agent import escalation_agent

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

print("Libraries imported.")


# Load environment variables from .env file
load_dotenv()

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"

root_agent = LlmAgent(
    model=MODEL_GEMINI_2_0_FLASH,
    name="root_agent",
    description="A mental health support system using specialized subagents for user support.",
    instruction=prompt.WELLNESS_APP_AGENT_PROMPT,
    sub_agents=[detection_agent]
)