import datetime
import os
import asyncio
import uuid
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from google.genai import types # For creating message Content/Parts
from dotenv import load_dotenv
from . import prompt
from .subagent.detection.agent import detection_agent
from .subagent.risk_assessment.agent import risk_assessment_agent
from .subagent.companion.agent import companion_agent
from .subagent.peer.agent import peer_agent
from .subagent.followup.agent import followup_agent
from .shared_libraries.mcp_context import mcp_context_tool, get_mcp_context_for_agent, update_mcp_context_from_agent
from .shared_libraries.mcp_schemas import MCPContext

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

# Initialize the root agent with appropriate subagents and MCP context tool
# Note: escalation_agent and resources_agent are already sub-agents of detection_agent
root_agent = LlmAgent(
    model=MODEL_GEMINI_2_0_FLASH,
    name="root_agent",
    description="A mental health support system using specialized subagents for user support.",
    instruction=prompt.WELLNESS_APP_AGENT_PROMPT,
    sub_agents=[
        companion_agent,
        peer_agent,
        followup_agent
    ],
    tools=[mcp_context_tool]
)

# Function to handle conversation with MCP context
async def handle_conversation_with_mcp(user_input: str, context_id: str = None) -> dict:
    """
    Handle a conversation turn with MCP context management.
    
    Args:
        user_input: The user's message
        context_id: Optional existing context ID
        
    Returns:
        Response dictionary with agent output and context ID
    """
    # Get or create MCP context
    context = get_mcp_context_for_agent(root_agent, context_id)
    
    # Add user message to context
    context.add_conversation_entry(
        message_id=str(uuid.uuid4()),
        speaker="user",
        message=user_input
    )
    
    # Pass context to agent via tool parameters
    tool_params = {
        "mcp_context_tool": {
            "context_id": context.context_id,
            "operation": "get"
        }
    }
    
    # Get response from agent
    response = await root_agent.generate_content_async(user_input, tool_parameters=tool_params)
    
    # Add agent response to context
    if response and hasattr(response, "text"):
        context.add_conversation_entry(
            message_id=str(uuid.uuid4()),
            speaker="system",
            message=response.text
        )
    
    # Update context
    update_mcp_context_from_agent(root_agent, context)
    
    return {
        "response": response,
        "context_id": context.context_id
    }
