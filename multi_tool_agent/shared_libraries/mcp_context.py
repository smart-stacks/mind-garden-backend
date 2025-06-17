"""MCP Context Manager for the Mind Garden crisis response system.

This module provides functionality for managing context using the Model Context Protocol (MCP).
It handles context creation, retrieval, updating, and persistence across agent interactions.
"""

import json
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types

from .mcp_schemas import MCPContext, UserIdentity, RiskAssessment, EscalationDecision, ResourceRecommendation


class MCPContextManager:
    """Manager for MCP context operations in the Mind Garden crisis response system."""
    
    def __init__(self):
        """Initialize the MCP context manager."""
        self._active_contexts: Dict[str, MCPContext] = {}
    
    def create_context(self, user_id: str, session_id: str) -> MCPContext:
        """Create a new MCP context for a user session.
        
        Args:
            user_id: Unique identifier for the user
            session_id: Unique identifier for the current session
            
        Returns:
            A new MCPContext object
        """
        context_id = str(uuid.uuid4())
        user_identity = UserIdentity(
            user_id=user_id,
            session_id=session_id
        )
        
        context = MCPContext(
            context_id=context_id,
            user_identity=user_identity,
            last_updated_by="system"
        )
        
        self._active_contexts[context_id] = context
        return context
    
    def get_context(self, context_id: str) -> Optional[MCPContext]:
        """Retrieve an existing MCP context.
        
        Args:
            context_id: Unique identifier for the context
            
        Returns:
            The MCPContext if found, None otherwise
        """
        return self._active_contexts.get(context_id)
    
    def update_context(self, context: MCPContext) -> None:
        """Update an existing MCP context.
        
        Args:
            context: The updated context object
        """
        context.last_updated = datetime.now()
        self._active_contexts[context.context_id] = context
    
    def serialize_context(self, context_id: str) -> str:
        """Serialize an MCP context to JSON.
        
        Args:
            context_id: Unique identifier for the context
            
        Returns:
            JSON string representation of the context
        """
        context = self.get_context(context_id)
        if not context:
            raise ValueError(f"Context with ID {context_id} not found")
        
        return context.json()
    
    def deserialize_context(self, json_str: str) -> MCPContext:
        """Deserialize an MCP context from JSON.
        
        Args:
            json_str: JSON string representation of the context
            
        Returns:
            Deserialized MCPContext object
        """
        context = MCPContext.parse_raw(json_str)
        self._active_contexts[context.context_id] = context
        return context


class MCPContextTool:
    """Tool for accessing and manipulating MCP context."""
    
    # Add __name__ attribute required by Google ADK
    __name__ = "mcp_context_tool"
    
    def __init__(self, context_manager: MCPContextManager):
        """Initialize the MCP context tool.
        
        Args:
            context_manager: The MCP context manager to use
        """
        self._context_manager = context_manager
        
    # These properties will be used when registering the tool with an agent
    @property
    def name(self) -> str:
        """Return the name of the tool."""
        return "mcp_context_tool"
        
    @property
    def description(self) -> str:
        """Return the description of the tool."""
        return "Tool for accessing and manipulating MCP context"
    
    def __call__(self, context_id: str, operation: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute an operation on the MCP context.
        
        Args:
            context_id: Unique identifier for the context
            operation: The operation to perform ("get", "update", etc.)
            data: Optional data for the operation
            
        Returns:
            Result of the operation
        """
        context = self._context_manager.get_context(context_id)
        if not context:
            return {"error": f"Context with ID {context_id} not found"}
        
        if operation == "get":
            return {"context": json.loads(context.json())}
        
        elif operation == "update_risk":
            if not data:
                return {"error": "No risk assessment data provided"}
            
            risk_assessment = RiskAssessment(**data)
            context.add_risk_assessment(risk_assessment)
            self._context_manager.update_context(context)
            return {"success": True, "context_id": context_id}
        
        elif operation == "update_escalation":
            if not data:
                return {"error": "No escalation decision data provided"}
            
            escalation_decision = EscalationDecision(**data)
            context.add_escalation_decision(escalation_decision)
            self._context_manager.update_context(context)
            return {"success": True, "context_id": context_id}
        
        elif operation == "add_conversation":
            if not data:
                return {"error": "No conversation data provided"}
            
            context.add_conversation_entry(
                message_id=data.get("message_id", str(uuid.uuid4())),
                speaker=data.get("speaker", "system"),
                message=data.get("message", ""),
                detected_emotions=data.get("detected_emotions")
            )
            self._context_manager.update_context(context)
            return {"success": True, "context_id": context_id}
        
        else:
            return {"error": f"Unknown operation: {operation}"}


# Global instance of the MCP context manager
mcp_context_manager = MCPContextManager()

# Create the MCP context tool
mcp_context_tool = MCPContextTool(mcp_context_manager)


def get_mcp_context_for_agent(agent: Agent, context_id: Optional[str] = None) -> MCPContext:
    """Get or create an MCP context for an agent interaction.
    
    Args:
        agent: The agent requesting the context
        context_id: Optional existing context ID
        
    Returns:
        An MCPContext object
    """
    if context_id:
        context = mcp_context_manager.get_context(context_id)
        if context:
            return context
    
    # Create a new context if none exists or the provided ID wasn't found
    user_id = f"user_{uuid.uuid4().hex[:8]}"
    session_id = f"session_{uuid.uuid4().hex[:8]}"
    return mcp_context_manager.create_context(user_id, session_id)


def update_mcp_context_from_agent(agent: Agent, context: MCPContext) -> None:
    """Update the MCP context after an agent interaction.
    
    Args:
        agent: The agent that modified the context
        context: The modified context
    """
    context.last_updated_by = agent.name
    mcp_context_manager.update_context(context)
