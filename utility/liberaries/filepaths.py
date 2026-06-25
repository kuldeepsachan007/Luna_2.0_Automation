from test_data import download, upload, screenshots

class FilePaths:
    """
    Simple data container for file paths used in the mobile testing framework.
    download_dir: Directory path for downloads
    upload_dir: Directory path for uploads
    screenshot_dir: Directory path for screenshots
    """
    download_dir: str = download
    upload_dir: str = upload
    screenshot_dir: str = screenshots