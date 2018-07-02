"""
Shows basic usage of the Drive v3 API.

Creates a Drive v3 API service and prints the names and ids of the last 10 files
the user has access to.
"""
from apiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file, client, tools
import io


def backup():
    # Setup the Drive v3 API
    SCOPES = 'https://www.googleapis.com/auth/drive'
    store = file.Storage('engine/credentials/credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('engine/credentials/drive_key.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # Call the Drive v3 API
    file_metadata = {
        'name': 'db.sqlite3',
        'parent': ['backup']
    }
    media = MediaFileUpload('db.sqlite3',
                            mimetype='application/sqlite3',
                            resumable=True)
    upload = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
    print('File ID: %s' % upload.get('id'))


def restore():
    # Setup the Drive v3 API
    SCOPES = 'https://www.googleapis.com/auth/drive'
    store = file.Storage('engine/credentials/credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('engine/credentials/drive_key.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # Call the Drive v3 API
    page_token = None
    done = None
    while True:
        response = service.files().list(q="name='db.sqlite3'",
                                        spaces='drive',
                                        fields='nextPageToken, files(id, name)',
                                        pageToken=page_token).execute()
        for current_file in response.get('files', []):
            # Process change
            print('Found file: %s (%s)' % (current_file.get('name'), current_file.get('id')))
            file_id = current_file.get('id')

            request = service.files().get_media(fileId=file_id)
            fh = io.FileIO('db.sqlite3', 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))
            break

        if done is not None:
            break

        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
