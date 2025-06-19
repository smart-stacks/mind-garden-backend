from multi_tool_agent.shared_libraries.types import RiskDetectionResponse

def route_based_on_risk(response: RiskDetectionResponse) -> str:
    if response.risk_level == "high":
        return "crisis_support_agent"
    elif response.risk_level == "medium":
        return "wellness_coach_agent"
    else:
        return "companion_agent"