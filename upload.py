import os
import time
import shutil
import subprocess

# Configuration (consider using a configuration file for sensitive data)
WATCH_FOLDER = "/home/fab/Pictures/PinterPics"  # Path to the folder containing new cheese app pictures
UPLOADED_FOLDER = "./uploaded"  # Path to the folder for storing uploaded pictures
UPLOAD_URL = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"  # URL for image upload
ATTRIBUTE = "imageFile"  # Key attribute for the curl command (matches the upload script's parameter name)
UPLOAD_INTERVAL = 30  # Time interval (seconds) between checks for new images

# Ensure the uploaded folder exists
os.makedirs(UPLOADED_FOLDER, exist_ok=True)  # Create the uploaded folder if it doesn't exist

def upload_image(file_path):
    """Uploads an image to the specified URL and returns success status.

    Args:
        file_path (str): Path to the image file to upload.

    Returns:
        bool: True if upload is successful, False otherwise.
    """

    try:
        command = [
            "curl", "-X", "POST",
            "-F", f"{ATTRIBUTE}=@{file_path}",  # Format the attribute correctly
            UPLOAD_URL
        ]
        # Execute the upload command
        result = subprocess.run(command, capture_output=True, text=True)
        # Check for successful upload (assuming HTTP status code 200)
        if result.returncode == 0:
            print(f"Successfully uploaded: {file_path}")
            return True
        else:
            print(f"Failed to upload: {file_path}\nError: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error uploading {file_path}: {e}")
        return False

def monitor_and_upload():
    """Monitors the watch folder, uploads new images, and moves them."""

    while True:
        # Get a list of all files in the watch folder
        files = [f for f in os.listdir(WATCH_FOLDER) if os.path.isfile(os.path.join(WATCH_FOLDER, f))]

        for file_name in files:
            file_path = os.path.join(WATCH_FOLDER, file_name)

            # Upload the image and handle success/failure
            if upload_image(file_path):
                # Move the uploaded file to the designated folder
                shutil.move(file_path, os.path.join(UPLOADED_FOLDER, file_name))

        # Wait before the next iteration
        time.sleep(UPLOAD_INTERVAL)

if __name__ == "__main__":
    print("Starting folder monitoring...")
    monitor_and_upload()