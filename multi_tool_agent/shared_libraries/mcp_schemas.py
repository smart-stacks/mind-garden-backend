"""MCP Schema definitions for the Mind Garden crisis response system.

This module defines the structured schemas used for context sharing between agents
using the Model Context Protocol (MCP).
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    """Risk level enumeration for standardized risk assessment."""
    NONE = "none"
    MILD = "mild"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class UserIdentity(BaseModel):
    """User identity information."""
    user_id: str
    session_id: str
    timestamp_created: datetime = Field(default_factory=datetime.now)
    

class ConversationHistory(BaseModel):
    """Conversation history entry."""
    message_id: str
    timestamp: datetime
    speaker: str  # "user" or "system"
    message: str
    detected_emotions: Optional[List[str]] = None
    

class RiskAssessment(BaseModel):
    """Comprehensive risk assessment information."""
    risk_level: RiskLevel
    confidence_score: float = Field(ge=0.0, le=1.0)
    reasoning: str
    risk_factors: List[str]
    protective_factors: Optional[List[str]] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    assessed_by: str  # Agent ID that performed the assessment
    requires_immediate_action: bool = False
    

class EscalationDecision(BaseModel):
    """Escalation decision information."""
    escalation_level: str  # "none", "resource_recommendation", "peer_support", "professional", "emergency"
    priority: int = Field(ge=1, le=10)  # 1-10 scale, 10 being highest priority
    reasoning: str
    timestamp: datetime = Field(default_factory=datetime.now)
    decided_by: str  # Agent ID that made the decision
    

class ResourceRecommendation(BaseModel):
    """Resource recommendation information."""
    resource_id: str
    resource_name: str
    resource_type: str  # "article", "video", "hotline", "app", "professional", etc.
    description: str
    url: Optional[str] = None
    phone: Optional[str] = None
    relevance_score: float = Field(ge=0.0, le=1.0)
    timestamp_recommended: datetime = Field(default_factory=datetime.now)
    

class AppointmentInformation(BaseModel):
    """Appointment booking information."""
    appointment_id: Optional[str] = None
    provider_name: str
    provider_type: str  # "therapist", "psychiatrist", "counselor", etc.
    datetime_scheduled: Optional[datetime] = None
    status: str = "pending"  # "pending", "confirmed", "completed", "cancelled"
    notes: Optional[str] = None
    

class PeerSupportMatch(BaseModel):
    """Peer support matching information."""
    match_id: Optional[str] = None
    peer_type: str  # "group", "individual", "moderated", etc.
    compatibility_score: float = Field(ge=0.0, le=1.0)
    match_reasons: List[str]
    connection_status: str = "pending"  # "pending", "connected", "completed"
    

class FollowUpPlan(BaseModel):
    """Follow-up monitoring plan."""
    plan_id: str
    check_in_frequency: str  # "daily", "weekly", "biweekly", etc.
    next_check_in: datetime
    monitoring_focus: List[str]  # Areas to monitor
    escalation_threshold: Optional[Dict[str, Any]] = None  # Conditions that trigger escalation
    

class MCPContext(BaseModel):
    """Complete MCP context for the Mind Garden crisis response system."""
    context_id: str
    user_identity: UserIdentity
    conversation_history: List[ConversationHistory] = []
    risk_assessments: List[RiskAssessment] = []
    current_risk_level: RiskLevel = RiskLevel.NONE
    escalation_decisions: List[EscalationDecision] = []
    resource_recommendations: List[ResourceRecommendation] = []
    appointments: List[AppointmentInformation] = []
    peer_support_matches: List[PeerSupportMatch] = []
    follow_up_plans: List[FollowUpPlan] = []
    last_updated: datetime = Field(default_factory=datetime.now)
    last_updated_by: str  # Agent ID that last updated the context
    
    def add_conversation_entry(self, message_id: str, speaker: str, message: str, 
                              detected_emotions: Optional[List[str]] = None) -> None:
        """Add a new conversation entry to the history."""
        entry = ConversationHistory(
            message_id=message_id,
            timestamp=datetime.now(),
            speaker=speaker,
            message=message,
            detected_emotions=detected_emotions
        )
        self.conversation_history.append(entry)
        self.last_updated = datetime.now()
        
    def add_risk_assessment(self, risk_assessment: RiskAssessment) -> None:
        """Add a new risk assessment and update current risk level."""
        self.risk_assessments.append(risk_assessment)
        self.current_risk_level = risk_assessment.risk_level
        self.last_updated = datetime.now()
        self.last_updated_by = risk_assessment.assessed_by
        
    def add_escalation_decision(self, escalation_decision: EscalationDecision) -> None:
        """Add a new escalation decision."""
        self.escalation_decisions.append(escalation_decision)
        self.last_updated = datetime.now()
        self.last_updated_by = escalation_decision.decided_by
