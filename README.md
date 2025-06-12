# mindGarden-backend

## Google ADK Agent

### Set Up Environment & Install ADK

#### Create Virtual Environment
```bash
python -m venv .venv
```

#### Activate Virtual Environment (Run in each new terminal)
- **macOS/Linux**: 
    ```bash
    source .venv/bin/activate
    ```
- **Windows CMD**: 
    ```cmd
    .venv\Scripts\activate.bat
    ```
- **Windows PowerShell**: 
    ```powershell
    .venv\Scripts\Activate.ps1
    ```

#### Install ADK
```bash
pip install google-adk -q
pip install litellm -q
```

### Set up the model
- Create .env file under multi_tool_agent and add the below content replacing your API key.
```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=PASTE_YOUR_ACTUAL_API_KEY_HERE
```

### To run the agents
- go to root path /mind-garden-backend
```
adk web
```
