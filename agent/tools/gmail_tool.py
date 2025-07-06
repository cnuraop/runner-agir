
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class GmailTool:
    def __init__(self, creds_file='credentials.json', token_file='token_gmail.json'):
        self.creds = None
        if os.path.exists(token_file):
            self.creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            self.creds = flow.run_local_server(port=0)
            with open(token_file, 'w') as token:
                token.write(self.creds.to_json())
        self.service = build('gmail', 'v1', credentials=self.creds)

    def send_email_from_task(self, task_desc):
        to = "Srikanth8605@gmail.com"
        subject = "Automated Email"
        body = task_desc

        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        message = {'raw': raw}

        sent = self.service.users().messages().send(userId="me", body=message).execute()
        return f"Email sent. ID: {sent['id']}"
