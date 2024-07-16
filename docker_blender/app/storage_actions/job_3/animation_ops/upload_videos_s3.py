import os
import boto3
from botocore.exceptions import ClientError

bucket_name = os.environ.get('BUCKET_NAME')
bucket_key = os.environ.get('BUCKET_KEY')

def find_files_with_prefix(directory, prefix):
    files = []
    for file_name in os.listdir(directory):
        if file_name.startswith(prefix):
            files.append(os.path.join(directory, file_name))
    return files

def upload_animation_videos(efs_project_path):

    # Upload the /output folder and output.zip to the specified S3 bucket
    s3 = boto3.client('s3')

    try:
        playblast_files = find_files_with_prefix(efs_project_path, 'bs_playblast')
        full_resolution_files = find_files_with_prefix(efs_project_path, 'bs_full_resolution')

        for playblast_file in playblast_files:
            s3_key = f"{bucket_key}/{os.path.basename(playblast_file)}"
            s3.upload_file(playblast_file, bucket_name, s3_key)
            print(f"File uploaded: {playblast_file} to {s3_key}")

        for full_resolution_file in full_resolution_files:
            s3_key = f"{bucket_key}/output/{os.path.basename(full_resolution_file)}"
            s3.upload_file(full_resolution_file, bucket_name, s3_key)
            print(f"File uploaded: {full_resolution_file} to {s3_key}")

        print("Upload complete to S3")
        return True
    except ClientError as e:
        print(f"Error uploading files to s3 {e}")
        return False