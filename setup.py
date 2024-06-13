import os
import platform
import subprocess
import sys
import requests
from urllib.parse import urljoin
import shutil

# Define base URL and list of file names (modify if needed)
BASE_URL = "http://www.bearware.dk/teamtalksdk/v5.15a/"
FILE_NAMES = {
    "Linux": "tt5sdk_v5.15a_ubuntu22_x86_64.7z",
    "Darwin": "tt5sdk_v5.15a_macos_x86_64.7z",
    "Windows": "tt5sdk_v5.15a_win64.7z"
}

def install_requirements():
    """Install Python packages from requirements.txt."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def install_p7zip():
    """Install p7zip based on the operating system."""
    if platform.system() == "Linux":
        print("Installing p7zip on Linux...")
        #subprocess.check_call(["sudo", "apt-get", "update"])
        subprocess.check_call(["sudo", "apt-get", "install", "-y", "p7zip-full"])
    elif platform.system() == "Darwin":
        print("Installing p7zip on macOS...")
        #subprocess.check_call(["brew", "update"])
        subprocess.check_call(["brew", "install", "p7zip"])
    else:
        print(f"Unsupported OS type: {platform.system()}")
        sys.exit(1)

def download_file(url, filename):
    """Downloads a file from the specified URL and saves it locally."""
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise exception for failed downloads

    with open(filename, 'wb') as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)
    print(f"Downloaded {filename} successfully.")

def extract_archive(filename, extract_dir):
    """Extracts the contents of an archive to the specified directory."""
    os.makedirs(extract_dir, exist_ok=True)  # Create extraction directory if needed
    # Use subprocess to call 7z for extraction
    subprocess.check_call(["7z", "x", filename, f"-o{extract_dir}"])
    print(f"Extracted {filename} to {extract_dir}.")
    os.remove(filename)  # Delete the archive file after extraction
    print(f"Deleted {filename}.")

def move_files_to_sdk(extracted_dir, sdk_dir):
    """Move files from extracted directory to sdk directory, preserving structure."""
    extracted_subdir = next(os.path.join(extracted_dir, d) for d in os.listdir(extracted_dir) if os.path.isdir(os.path.join(extracted_dir, d)))
    for item in os.listdir(extracted_subdir):
        s = os.path.join(extracted_subdir, item)
        d = os.path.join(sdk_dir, item)
        if os.path.isdir(s):
            shutil.move(s, d)
        else:
            shutil.move(s, sdk_dir)
    shutil.rmtree(extracted_subdir)  # Remove the now-empty extracted subdirectory
    print(f"Moved all files from {extracted_subdir} to {sdk_dir} and removed the extracted subdirectory.")

def essential_sdk(sdk_dir):
    """Keeps only the essential files and directories in the sdk directory."""
    essential_paths = [
        os.path.join(sdk_dir, "Library"),
        os.path.join(sdk_dir, "License.txt")
    ]
    
    for item in os.listdir(sdk_dir):
        item_path = os.path.join(sdk_dir, item)
        if item_path not in essential_paths:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
    print(f"Kept only essential files and directories in {sdk_dir}.")

def install_sdk():
    """Downloads, extracts, and installs the TeamTalk SDK."""
     # Check if the 'sdk' directory exists
    if os.path.exists("sdk"):
        print("SDK directory already exists. Skipping installation.")
        return  # Exit the function if directory exists
    else:
        sdk_dir = os.path.join(os.getcwd(), "sdk")  # Create directory for downloaded SDKs
        os.makedirs(sdk_dir, exist_ok=True)

        # Determine the appropriate filename based on the platform
        system = platform.system()
        filename = FILE_NAMES.get(system)
        
        if not filename:
            print(f"No SDK available for the current platform: {system}")
            sys.exit(1)

        download_url = urljoin(BASE_URL, filename)
        local_path = os.path.join(sdk_dir, filename)
        extract_dir = os.path.join(sdk_dir, "extracted_temp")

        download_file(download_url, local_path)
        extract_archive(local_path, extract_dir)
        move_files_to_sdk(extract_dir, sdk_dir)  # Move files to sdk directory
        essential_sdk(sdk_dir)  # Keep only the essential files and directories

        print("TeamTalk SDK installation complete!")
        print("You can run command\n python radio.py --devices\n define your sound device and save ID in config.py")

if __name__ == "__main__":
    # Install Python packages from requirements.txt
    install_requirements()
    
    # Install p7zip
    install_p7zip()
    
    # Install the TeamTalk SDK
    install_sdk()
