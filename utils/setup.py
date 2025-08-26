import os
import sys

def setup_environment(mount_gdrive=True):
    # Google Colab specific setup
    if mount_gdrive:
        from google.colab import drive
        drive.mount('/content/drive')
        base_path = "/content/drive/MyDrive/pose-estimation-research"
    else:
        base_path = os.path.abspath("pose-estimation-research")

    if base_path not in sys.path:
        sys.path.append(base_path)

    print(f"✅ Environment set. Project base path: {base_path}")
    return base_path
