import os
import subprocess
import boto3
import logging
from botocore.exceptions import NoCredentialsError, ClientError
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename="backup_report.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Constants
LOCAL_DIR = "/path/to/local/directory"  # Directory to back up
REMOTE_DIR = "/path/to/remote/directory"  # Remote server directory
REMOTE_SERVER = "user@remote_server_ip"  # Replace with your SSH server info
BACKUP_METHOD = "s3"  # Options: 'rsync' or 's3'
BUCKET_NAME = "your-s3-bucket"  # S3 bucket name for cloud storage

# AWS S3 Config
AWS_ACCESS_KEY = "YOUR_AWS_ACCESS_KEY"
AWS_SECRET_KEY = "YOUR_AWS_SECRET_KEY"
AWS_REGION = "us-west-2"  # Specify your AWS region

def log_message(message):
    """Logs message to console and log file."""
    print(message)
    logging.info(message)

def backup_to_remote():
    """Backup local directory to remote server using rsync."""
    try:
        command = [
            "rsync",
            "-avz",
            LOCAL_DIR,
            f"{REMOTE_SERVER}:{REMOTE_DIR}"
        ]
        subprocess.check_call(command)
        log_message("Backup to remote server completed successfully.")
    except subprocess.CalledProcessError as e:
        log_message(f"Backup to remote server failed: {e}")
        return False
    return True

def backup_to_s3():
    """Backup local directory to S3 bucket."""
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )
    
    try:
        for root, dirs, files in os.walk(LOCAL_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                s3_key = os.path.relpath(file_path, LOCAL_DIR)
                
                try:
                    s3_client.upload_file(file_path, BUCKET_NAME, s3_key)
                    log_message(f"Uploaded {file_path} to s3://{BUCKET_NAME}/{s3_key}")
                except ClientError as e:
                    log_message(f"Failed to upload {file_path}: {e}")
                    return False
        log_message("Backup to S3 completed successfully.")
    except NoCredentialsError:
        log_message("AWS credentials not available.")
        return False
    except Exception as e:
        log_message(f"Backup to S3 failed: {e}")
        return False
    return True

def main():
    """Main function to select backup method and execute backup."""
    log_message("Starting backup operation.")
    success = False

    if BACKUP_METHOD == "rsync":
        success = backup_to_remote()
    elif BACKUP_METHOD == "s3":
        success = backup_to_s3()
    else:
        log_message("Invalid backup method selected. Choose 'rsync' or 's3'.")
        return

    if success:
        log_message("Backup operation completed successfully.")
    else:
        log_message("Backup operation failed.")
    
    log_message("Backup operation finished.\n")

if __name__ == "__main__":
    main()
