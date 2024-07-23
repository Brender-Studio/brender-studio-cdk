import os
import sys
from app_utils.parse_json import parse_json
from animation_ops.playblast.generate_playblast import generate_playblast
from animation_ops.full_preview.generate_full_preview import generate_full_preview
from output_ops.generate_thumbnail import generate_thumbnail
from output_ops.output_to_zip import output_to_zip
from output_ops.upload_s3 import upload_to_s3
from configure_ses.send_email import send_render_ok_email
from configure_ses.send_email_error import send_render_error_email
from clean_up.clean_project_efs import clean_up_project_folder_efs
from animation_ops.upload_videos_s3 import upload_animation_videos

def validate_env_vars(required_env_vars):
    for env_var in required_env_vars:
        if env_var not in os.environ:
            raise ValueError(f"Missing environment variable: {env_var}")

def parse_ses_json(ses_json_str):
    if len(sys.argv) > 2:
        raise ValueError("Error, no JSON string provided")
    return parse_json(ses_json_str)

def main():
    try:
        required_env_vars = ['BUCKET_NAME', 'BUCKET_KEY', 'EFS_BLENDER_FOLDER_PATH']
        validate_env_vars(required_env_vars)
        
        bucket_key = os.environ['BUCKET_KEY']
        efs_path = os.environ['EFS_BLENDER_FOLDER_PATH']
        efs_project_path = os.path.join(os.environ['EFS_BLENDER_FOLDER_PATH'], os.environ['BUCKET_KEY'])
        render_output_path = os.path.join(efs_path, bucket_key, 'output')
        thumbnail_output_path = os.path.join(efs_path, bucket_key) # example: /mnt/efs/projects/project_5
        ses_json_str = sys.argv[1]
        
        json_ses = parse_ses_json(ses_json_str)
        ses_details = json_ses['ses']
        ses_active = ses_details['ses_active']
        ses_config = ses_details['ses_config']
        render_details = ses_details['render_details']
        animation_data = ses_details['animation_preview']
        animation_full = animation_data['animation_preview_full_resolution']
        region = ses_config['region']
        job_id = ses_config['batch_job_2_id']
        job_array_size = render_details['job_array_size']

        render_type = render_details['render_type'] # Still , Animation , Custom Python
        print(f"Render Type: {render_type}")

        # Check if the specified EFS folder exists
        if not os.path.exists(render_output_path) or not os.listdir(render_output_path):
            print(f"EFS folder not found: {render_output_path}") # No files in the folder (renders failed)
            # If SES is active, send an email with the error message
            if ses_active:
                response = send_render_error_email(ses_config, render_details, job_id, region, job_array_size)
                print(f"Send email response: {response}")
                exit(0)
            
            # clean up project folder in EFS
            clean_up_project_folder_efs(efs_path, bucket_key)
        else:
            print(f"EFS folder found: {render_output_path}")
            
            output_zip_path, zip_size = output_to_zip(render_output_path)
            print(f"output.zip created path: {output_zip_path}")
            print(f"Size of output.zip: {zip_size} bytes")
                
            thumbnail_path = generate_thumbnail(render_output_path, thumbnail_output_path)
            print(f"Thumbnail created path: {thumbnail_path}")

            response = upload_to_s3(render_output_path, output_zip_path, thumbnail_path)
            print(f"Upload to S3 response: {response}")

        # Check if ses_active is True
        if not ses_active:
            print("SES is not active")
            exit(0)
        else:
            print("SES is active")
            if render_type == "Animation" and render_output_path:
                print("Animation Preview, playblast will be generated low resolution")
                generate_playblast(animation_data)
                if animation_full:
                    print("Animation Preview is True, generating full resolution preview")
                    generate_full_preview(animation_data)
                else:
                    print("Animation Not Full Resolution Preview, skipping full resolution preview generation")
            
            upload_animation_videos(efs_project_path)

            # Send email with render details
            response = send_render_ok_email(job_id, ses_config, render_details, zip_size, job_array_size, region)

            # Clean up project folder in EFS
            clean_up_project_folder_efs(efs_path, bucket_key)

            

    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
