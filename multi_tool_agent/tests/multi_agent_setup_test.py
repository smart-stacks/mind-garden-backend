import pytest

def test_import_agent_module():
    import multi_tool_agent.agent

def test_import_prompt_module():
    import multi_tool_agent.prompt

def test_import_tools_search():
    import multi_tool_agent.tools.search

def test_import_resources_agent():
    import multi_tool_agent.subagent.resources.agent

def test_root_agent_exists():
    from multi_tool_agent.agent import root_agent
    assert root_agent is not None
    assert hasattr(root_agent, "name")   