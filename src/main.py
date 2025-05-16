from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import requests
from email.mime.text import MIMEText
import base64
import json

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("frontend/index.html")

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/youtube.readonly'
]

class EmailRequest(BaseModel):
    to: str
    subject: str
    message: str

class CalendarRequest(BaseModel):
    summary: str
    description: str
    start_time: str
    end_time: str

class YouTubeRequest(BaseModel):
    query: str

def get_google_creds():
    creds = None
    config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')
    token_path = os.path.join(config_dir, 'token.json')
    credentials_path = os.path.join(config_dir, 'credentials.json')

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    return creds

@app.post("/send-email")
async def send_email(request: EmailRequest):
    try:
        creds = get_google_creds()
        service = build('gmail', 'v1', credentials=creds)

        # Enhance email content using Ollama
        response = requests.post('http://localhost:11434/api/generate',
            json={
                'model': 'genesis',
                'prompt': f'Review and enhance this email: Subject: {request.subject}, Message: {request.message}'
            },
            stream=True
        )
        
        # Collect all response chunks
        enhanced_content = ''
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line)
                enhanced_content += json_response.get('response', '')

        message = MIMEText(enhanced_content)
        message['to'] = request.to
        message['subject'] = request.subject
        
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        service.users().messages().send(userId='me', body={'raw': raw}).execute()
        
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/schedule-meeting")
async def schedule_meeting(request: CalendarRequest):
    try:
        creds = get_google_creds()
        service = build('calendar', 'v3', credentials=creds)

        # Enhance meeting description using Ollama
        response = requests.post('http://localhost:11434/api/generate',
            json={
                'model': 'genesis',
                'prompt': f'Review and enhance this meeting description: {request.description}'
            },
            stream=True
        )
        
        # Collect all response chunks
        enhanced_description = ''
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line)
                enhanced_description += json_response.get('response', '')

        # Format datetime with timezone
        from datetime import datetime
        from zoneinfo import ZoneInfo

        # Parse the datetime strings and add timezone
        start_time = datetime.fromisoformat(request.start_time).replace(tzinfo=ZoneInfo('America/New_York'))
        end_time = datetime.fromisoformat(request.end_time).replace(tzinfo=ZoneInfo('America/New_York'))

        event = {
            'summary': request.summary,
            'description': enhanced_description,
            'start': {'dateTime': start_time.isoformat()},
            'end': {'dateTime': end_time.isoformat()},
            'timeZone': 'America/New_York'
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        return {"message": "Meeting scheduled successfully", "event": event}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search-youtube")
async def search_youtube(request: YouTubeRequest):
    try:
        creds = get_google_creds()
        youtube = build('youtube', 'v3', credentials=creds)

        # Enhance search query using Ollama
        response = requests.post('http://localhost:11434/api/generate',
            json={
                'model': 'genesis',
                'prompt': f'Enhance this YouTube search query: {request.query}'
            },
            stream=True
        )
        
        # Collect all response chunks
        enhanced_query = ''
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line)
                enhanced_query += json_response.get('response', '')

        search_response = youtube.search().list(
            q=enhanced_query,
            part='snippet',
            maxResults=5
        ).execute()

        return {"results": search_response.get('items', [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
