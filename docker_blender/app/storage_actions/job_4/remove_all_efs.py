import os
import shutil

efs_path = os.environ['EFS_BLENDER_FOLDER_PATH']

# Clean /mnt/projects

def clean_up_project_folder_efs(efs_path):
    """
    Clean up the EFS folder all projects
    """
    
    # Clean /mnt/projects folder
    try:
        shutil.rmtree(efs_path)
        print("EFS folder cleaned up")
    except FileNotFoundError:
        print("Error: EFS folder not found")
    except Exception as e:
        print(f"Error cleaning up EFS folder: {e}")

clean_up_project_folder_efs(efs_path)