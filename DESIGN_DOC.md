# Mind Garden: Multi-Agent Crisis Response System

## Overview

Mind Garden is a modular, AI-powered mental health support system that uses a coordinated multi-agent architecture to detect, assess, and respond to users experiencing mental health crises. The system employs multiple specialized agents working together to provide appropriate support based on the severity and nature of the user's situation.

## System Architecture

The system is orchestrated by a **Root Orchestrator Agent** that manages the flow of information and delegates tasks to the following specialized subagents:

```
                  User Input
                        ↓
            Root Orchestrator Agent
   ↓                 ↓              ↓
[Companion Agent]  [Peer Agent]  [Follow-up Agent]

[Companion Agent] → [Detection Agent] → [Risk Assessment Agent] → [Escalation Agent]
   ↓
[Resource Agent]
```

- **Companion Agent**: Provides supportive conversation and can invoke Detection and Risk Assessment Agents if new risks are detected during chat.
- **Detection Agent**: Scans user input for signs of distress or risk and classifies risk level.
- **Risk Assessment Agent**: Performs detailed analysis if risk is detected, determining severity and urgency.
- **Escalation Agent**: Handles priority routing and escalation to human or emergency services when needed.
- **Resource Agent**: Recommends relevant resources, hotlines, and support services based on user needs and risk.
- **Peer Agent**: Connects users to local or online peer support groups and communities.
- **Follow-up Agent**: Schedules and manages ongoing check-ins and progress tracking.

### Orchestration Logic

The Root Orchestrator Agent:
- Receives and analyzes user input and context.
- Decides which subagents to invoke and in what order, based on user needs and prior agent results.
- Aggregates and passes relevant context/results between agents.
- Returns a final structured response with a summary, recommended actions, and next steps.

**Typical Workflow:**
1. **Initial Input:** User message received.
2. **Supportive Chat:** If the user requests a supportive chat, the Companion Agent is invoked.
   - If the Companion Agent detects risk, it invokes the Detection Agent.
   - If Detection Agent finds risk, the Risk Assessment Agent is invoked.
3. **Risk Handling:** If risk is 'moderate', 'high', or 'critical', Escalation Agent is invoked.
4. **Peer Support:** If risk is 'mild' or the user expresses a need for community, Peer Agent is invoked.
5. **Resource Recommendation:** Resource Agent is always invoked to recommend resources.
6. **Follow-up:** Follow-up Agent is always invoked to suggest or schedule follow-up.
7. **Response Compilation:** All agent outputs are compiled into a final, structured response.

**Nuance:** The system uses only the minimal set of agents required for the user's situation, always explaining escalations or recommendations clearly and respectfully.


---

## Specialized Agents

### Companion Agent
- **Purpose:** Provides ongoing supportive conversation and can trigger risk detection/escalation if needed.
- **Input:** User messages and context.
- **Output:** Supportive responses, and if risk is detected, invokes Detection and Risk Assessment Agents.

### Detection Agent
- **Purpose:** First line of analysis, scanning for emotional distress, crisis, or risk.
- **Input:** User messages and conversation history.
- **Output:** Risk classification (none, mild, moderate, high, critical) with reasoning.

### Risk Assessment Agent
- **Purpose:** Deep analysis of flagged cases to determine severity and response.
- **Input:** User messages, history, Detection Agent output.
- **Output:** Detailed risk assessment and recommended response level.

### Escalation Agent
- **Purpose:** Determines routing and escalation for high-risk cases.
- **Input:** Risk assessment details, user context.
- **Output:** Escalation decision and routing information.

### Appointment Booking Agent
- **Purpose:** Schedules appointments with mental health professionals when needed.
- **Input:** Risk assessment, escalation decision.
- **Output:** Appointment details or booking confirmation.

### Resource Agent
- **Purpose:** Recommends resources and support services.
- **Input:** User context, risk assessment, escalation decision.
- **Output:** Resource recommendations and information.

### Peer Agent
- **Purpose:** Connects users to peer support options.
- **Input:** User preferences, risk assessment, resource recommendations.
- **Output:** Peer support matches and connection details (local groups, online communities, e.g., 7 Cups).

### Follow-up Agent
- **Purpose:** Manages ongoing monitoring and follow-up.
- **Input:** User history, previous interactions, resource utilization.
- **Output:** Follow-up schedule, check-in messages, progress tracking.

---

## Data Flow

1. **User Input:** Received by Root Orchestrator.
2. **Risk Detection:** Detection Agent classifies risk.
3. **Risk Assessment:** If risk detected, Risk Assessment Agent performs detailed analysis.
4. **Escalation & Appointment:** For moderate/high/critical risk, Escalation and Appointment Booking Agents are invoked.
5. **Resource & Peer Support:** Resource Agent recommends resources; Peer Agent connects to support groups if appropriate.
6. **Follow-up:** Follow-up Agent schedules ongoing support.
7. **Companion Chat:** Companion Agent provides ongoing conversation and can re-trigger risk detection as needed.
8. **Final Response:** All outputs are aggregated and returned to the user.

---
## Extensibility & Future Enhancements

- **Personalization:** Adaptive recommendations based on user history and preferences.
- **Integration Expansion:** More resource databases, peer networks, and healthcare provider connections.
- **Modality Extensions:** Voice, image, and multi-platform support.
- **Additional Agents:** Mood Tracking, Psychoeducation, Mindfulness/CBT Exercise, Crisis Intervention, Feedback Collection.

---

## Conclusion

Mind Garden’s modular, multi-agent design enables safe, scalable, and user-centered mental health support. By orchestrating specialized agents and leveraging both AI and human expertise, the system delivers timely, personalized, and effective care for users in need.
