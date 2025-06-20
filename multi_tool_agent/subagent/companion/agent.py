"""Escalation Agent in a mental wellness support system that escalates."""

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from multi_tool_agent.subagent.resources.agent import resources_agent
from multi_tool_agent.subagent.risk_assessment.agent import risk_assessment_agent
from multi_tool_agent.subagent.detection.agent import detection_agent

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"

companion_agent = LlmAgent(
    model=MODEL_GEMINI_2_0_FLASH,
    name="companion_agent",
    description="Provides supportive conversation and can invoke DetectionAgent if distress is detected.",
    instruction=("Engage in supportive, empathetic conversation. "
        "If you detect any signs of distress or risk in the user's input, immediately invoke DetectionAgent. "
        "If DetectionAgent determines the risk is moderate, high, or critical, invoke RiskAssessmentAgent for a detailed analysis. "
        "Always prioritize user safety and well-being."),
    sub_agents=[
        detection_agent,
        risk_assessment_agent
    ],
    tools=[AgentTool(agent=resources_agent)]
)