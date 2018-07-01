"""
Shows basic usage of the Drive v3 API.

Creates a Drive v3 API service and prints the names and ids of the last 10 files
the user has access to.
"""
from apiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools

# Setup the Drive v3 API
SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('credentials/credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials/drive_key.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v3', http=creds.authorize(Http()))

# Call the Drive v3 API
results = service.files().list(
    pageSize=10, fields="nextPageToken, files(id, name)").execute()

file_metadata = {
    'name': 'config.json',
    'parents': ['appDataFolder']
}
media = MediaFileUpload('config.json',
                        mimetype='application/json',
                        resumable=True)
file = service.files().create(body=file_metadata,
                              media_body=media,
                              fields='id').execute()
print('File ID: %s' % file.get('id'))
