import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Load the API credentials and initialize the API client
credentials = service_account.Credentials.from_service_account_file(
    'api.json',
    scopes=['https://www.googleapis.com/auth/androidpublisher']
)
androidpublisher = build('androidpublisher', 'v3', credentials=credentials)

# Define package name and track
package_name = 'my.awesome.package.id'
#track = 'internal'
track = 'My Custom Testing Track'

# Start a new edit
edit = androidpublisher.edits().insert(body={}, packageName=package_name).execute()
edit_id = edit['id']

try:
    # Get the new version code from the environment variable
    new_version_code = os.environ.get('NEW_BUILD_NUMBER')
    if new_version_code is None:
        raise ValueError("NEW_BUILD_NUMBER environment variable is not set")
    print(f"New version code: {new_version_code}")

    # Upload the .aab file
    media = MediaFileUpload('app-release.aab', mimetype='application/octet-stream')
    bundle_response = androidpublisher.edits().bundles().upload(
        editId=edit_id,
        packageName=package_name,
        media_body=media
    ).execute()
    uploaded_version_code = bundle_response['versionCode']
    print(f"Uploaded bundle with version code: {uploaded_version_code}")

    # Assign the track (e.g., internal, alpha, beta, production)
    androidpublisher.edits().tracks().update(
        editId=edit_id,
        packageName=package_name,
        track=track,
        body={'releases': [{
            'versionCodes': [uploaded_version_code],
            'status': 'completed',
        }]}
    ).execute()

    # Commit the edit
    androidpublisher.edits().commit(
        editId=edit_id,
        packageName=package_name
    ).execute()
    print("Upload successful!")
except Exception as e:
    print(f"An error occurred: {str(e)}")
    androidpublisher.edits().delete(
        editId=edit_id,
        packageName=package_name
    ).execute()
