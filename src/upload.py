import sys
import dropbox
from dropbox.exceptions import ApiError, AuthError
import os

TOKEN = 'FvWjZpwuN3AAAAAAAAAQVan5YL6uEkh9FluFUOq3ZD106BjN07ipDB6ZWQBInm5i'


def upload_images(image_name):
    name_file = image_name + ".jpeg"
    # Check that access tocken added
    if len(TOKEN) == 0:
        sys.exit("ERROR: Missing access token. "
                 "try re-generating an access token from the app console at dropbox.com.")
    dbx = dropbox.Dropbox(TOKEN)
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit("ERROR: Invalid access token; try re-generating an "
                 "access token from the app console at dropbox.com.")

    uploadPath = "C:/Users/Haryanto/Documents/github/Smart-Security-Camera/" + name_file
    # Read in file and upload
    with open(uploadPath, 'rb') as f:
        print("Uploading " + name_file + " to Dropbox ...")
        try:
            dbx.files_upload(f.read(), "/" + name_file, mute=True)
        except ApiError as err:
            # Check user has enough Dropbox space quota
            if (err.error.is_path() and
                    err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERROR: Cannot upload; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()

    print("find file to delete")
    os.system("rm " + name_file)
    print("File: " + name_file + " deleted ...")

