import os
import boto3
import tarfile


bucket_name = os.environ['BUCKET_NAME']
bucket_key = os.environ['BUCKET_KEY']
efs_path = os.environ['EFS_BLENDER_FOLDER_PATH']


print(bucket_name)
print(bucket_key)
print(efs_path)

print(f"Copying project folder from S3: {bucket_name}/{bucket_key}")


s3_client = boto3.client('s3')

try:
    # List objects in the bucket with the specified prefix
    response = s3_client.list_objects(Bucket=bucket_name, Prefix=bucket_key)

    # Get the list of objects from the response
    objects = response.get('Contents', [])

    if not objects:
        raise Exception(f"No objects found in S3 with prefix: {bucket_key}")

    # Copy each object to the EFS folder
    for obj in objects:
        obj_key = obj['Key']
        dest_path = os.path.join(efs_path, obj_key)

        print(f"Copying {obj_key} to {dest_path}")

        # Extract the folder name from the destination path
        extract_folder = os.path.splitext(os.path.basename(dest_path))[0]

        # Create the extraction path by joining the EFS path with the folder name
        extract_path = os.path.join(efs_path, os.path.dirname(obj_key))

        # If the extraction path does not exist, create it
        os.makedirs(extract_path, exist_ok=True)

        # Download the object from S3 to the destination path
        s3_client.download_file(bucket_name, obj_key, dest_path)

        # Verify if the downloaded object is a .tar.gz or .blend file
        if obj_key.endswith('.tar.gz'):
            try:
                # Try to open the tar.gz file
                with tarfile.open(dest_path, mode="r:gz") as tar:
                    # If the file is a valid tar.gz file, extract it to the extraction path
                    print(f"Extracting {obj_key} to {extract_path}")
                    tar.extractall(path=extract_path)
            except tarfile.ReadError:
                # If the file is not a valid tar.gz file, print an error message
                print(f"Error: {obj_key} is not a valid tar.gz file")
        elif obj_key.endswith('.blend'):
            # If the object is a .blend file, rename it to the extraction
            print(f"{obj_key} is a .blend file, copying directly")
            os.rename(dest_path, os.path.join(extract_path, os.path.basename(dest_path)))
            print(f"{obj_key} copied to {extract_path}")
        else:
            print(f"{obj_key} is not a .tar.gz or .blend file, ignoring")
       

    print(f"Project folder copied to {efs_path}")
except Exception as e:
    print(f"Error: {e}")