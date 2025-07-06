
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive.file']

class GoogleDocsTool:
    def __init__(self, creds_file='credentials.json', token_file='token_docs.json'):
        self.creds = None
        if os.path.exists(token_file):
            self.creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            self.creds = flow.run_local_server(port=0)
            with open(token_file, 'w') as token:
                token.write(self.creds.to_json())
        self.service = build('docs', 'v1', credentials=self.creds)

    def save_research_to_doc(self, task_desc, content):
        doc_title = task_desc[:40]
        doc = self.service.documents().create(body={"title": doc_title}).execute()
        doc_id = doc['documentId']

        self.service.documents().batchUpdate(
            documentId=doc_id,
            body={
                "requests": [
                    {
                        "insertText": {
                            "location": {"index": 1},
                            "text": content
                        }
                    }
                ]
            }
        ).execute()

        return f"https://docs.google.com/document/d/{doc_id}"
