from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load the API credentials
credentials = service_account.Credentials.from_service_account_file(
    'api.json',
    scopes=['https://www.googleapis.com/auth/androidpublisher']
)

# Build the service
androidpublisher = build('androidpublisher', 'v3', credentials=credentials)

# Define package name and track
package_name = 'my.awesome.package.id'
#track = 'internal'
track = 'My Custom Track'

# Start a new edit
edit = androidpublisher.edits().insert(body={}, packageName=package_name).execute()
edit_id = edit['id']

try:
    # Get the list of tracks
    tracks_response = androidpublisher.edits().tracks().list(
        editId=edit_id,
        packageName=package_name
    ).execute()

    # Extract the version code from the desired track
    for t in tracks_response['tracks']:
        if t['track'] == track:
            version_code = t['releases'][0]['versionCodes'][0]  # Adjust as per your release structure
            print(f"{version_code}")

finally:
    # Always clean up the edit after using it, even if we don't make any changes
    androidpublisher.edits().delete(
        editId=edit_id,
        packageName=package_name
    ).execute()
