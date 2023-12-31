import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


class GoogleApiClient:
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

    def __init__(self):
        self.credentials = self.authenticate()

    def authenticate(self):
        credentials = None
        if os.path.exists('token.json'):
            credentials = Credentials.from_authorized_user_file('token.json')

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                credentials = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(credentials.to_json())

        return credentials

