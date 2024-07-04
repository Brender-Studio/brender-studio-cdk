import os
import shutil

def clean_up_project_folder_efs(efs_path, bucket_key):
    """
    Clean up the EFS folder for the specified project
    """
    
    # Clean /mnt/projects/project_name folder
    try:
        shutil.rmtree(os.path.join(efs_path, bucket_key))
        print("EFS folder cleaned up")
    except FileNotFoundError:
        print("Error: EFS folder not found")
    except Exception as e:
        print(f"Error cleaning up EFS folder: {e}")