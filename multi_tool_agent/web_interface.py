"""Web interface for the Mind Garden crisis response system with MCP."""

import asyncio
from google.adk.web import WebApp
from .agent import root_agent, handle_conversation_with_mcp

# Create a dictionary to store context IDs for different sessions
session_contexts = {}

# Create a web app instance
app = WebApp(title="Mind Garden Crisis Response System")

@app.route("/")
async def index(request):
    """Handle the main index route."""
    session_id = request.session_id
    
    # Get or create a context ID for this session
    context_id = session_contexts.get(session_id)
    
    # Process the user message if provided
    user_message = request.query.get("message", "")
    if user_message:
        # Use the MCP-enabled conversation handler
        result = await handle_conversation_with_mcp(user_message, context_id)
        
        # Store the context ID for future interactions
        session_contexts[session_id] = result["context_id"]
        
        # Get the response text
        response_text = result["response"].text if result["response"] else "No response generated."
        
        return {
            "response": response_text,
            "context_id": result["context_id"]
        }
    
    # Return a welcome message if no user message
    return {
        "response": "Welcome to Mind Garden Crisis Response System. How can I help you today?",
        "context_id": context_id
    }

# Make the app available to the ADK web command
web_app = app
