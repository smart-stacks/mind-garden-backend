from multi_tool_agent.agent import root_agent

def test_root_agent_exists():
    assert root_agent is not None
    assert hasattr(root_agent, "name")
    assert root_agent.name == "root_agent"