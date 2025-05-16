# workflow_automation-platform

The original version of the Genesis AI Agent that integrates with Google services (Gmail, Calendar, YouTube) using the Genesis model for content enhancement.

## Overview

This is the initial version of the Genesis AI Agent that provides basic integration with Google services. It uses the Ollama-hosted Genesis model to enhance content and improve user interactions.

## Features

1. **Gmail Integration**
   - Send emails through Gmail
   - Basic content enhancement
   - Simple email formatting

2. **Google Calendar**
   - Create calendar events
   - Basic event descriptions
   - Meeting scheduling

3. **YouTube Search**
   - Search for videos
   - Basic query enhancement
   - Video result display

## Setup

1. **Python Dependencies**
   ```bash
   pip install fastapi uvicorn google-api-python-client requests
   ```

2. **Ollama Setup**
   - Install Ollama
   - Pull the Genesis model
   - Ensure it's running on port 11434

3. **Google OAuth**
   - Place credentials.json in config/
   - Run the app and authenticate
   - Token will be saved automatically

## Running

```bash
uvicorn src.main:app --reload --port 8080
```

Then open http://localhost:8080 in your browser.

## Project Structure

```
genesis-agent/
├── config/
│   └── credentials.json    # Google OAuth credentials
├── frontend/
│   └── index.html         # Web interface
└── src/
    └── main.py           # FastAPI server
```

## Note

This is the original version (v1) of the Genesis AI Agent. For the enhanced version with improved features and better error handling, check out Genesis-Agentic-AI-application repository.

## Security

- Keep your credentials.json secure
- Never share your token.json
- Ensure secure OAuth flow

## Prerequisites

1. **Python Requirements**
   ```bash
   pip install fastapi uvicorn google-api-python-client requests
   ```

2. **Ollama Setup**
   - Make sure Ollama is running with the Genesis model
   - It should be accessible at `http://localhost:11434`
   - Test with: `curl http://localhost:11434/api/generate -d '{"model": "genesis", "prompt": "Hello"}'`

## Running the Application

1. **Unzip the Project**
   ```bash
   cd ~/Downloads
   unzip genesis-agent-v2.zip
   cd genesis-agent
   ```

2. **Start the Server**
   ```bash
   uvicorn src.main:app --reload --port 8080
   ```

3. **Access the Web Interface**
   - Open your browser to `http://localhost:8080`
   - On first run, you'll need to authenticate with Google
   - After authentication, the token will be saved in `config/token.json`

## Features

1. **Enhanced Email Sending**
   - Write simple emails
   - Genesis AI will enhance them professionally
   - Sent through your Gmail account

2. **Smart Calendar Scheduling**
   - Create meeting events
   - AI enhances meeting descriptions
   - Automatically added to your Google Calendar

3. **Intelligent YouTube Search**
   - Enter basic search terms
   - AI expands them for better results
   - Get more relevant YouTube videos

## File Structure
```
genesis-agent/
├── config/
│   ├── credentials.json    # Google OAuth credentials
│   └── token.json         # Generated after authentication
├── frontend/
│   └── index.html         # Web interface
└── src/
    └── main.py           # FastAPI server code
```

## Troubleshooting

1. If you get authentication errors:
   - Delete `config/token.json`
   - Restart the server
   - Authenticate again with Google

2. If Ollama isn't responding:
   - Check if Ollama is running
   - Verify the Genesis model is available
   - Make sure port 11434 is accessible

3. If the server won't start:
   - Check if port 8080 is in use
   - Try a different port: `uvicorn src.main:app --reload --port 8081`

## Security Note
- Keep your `credentials.json` and `token.json` secure
- Never share these files publicly
- They contain sensitive OAuth credentials
