import boto3
import json
from datetime import datetime, timedelta
from configure_ses.presigned_urls import generate_presigned_urls
from configure_ses.batch_details import get_batch_job_info
from configure_ses.get_ec2_details import get_ec2_instance_details

def convert_bytes_to_mb(bytes_size):
    """
    Converts the size in bytes to megabytes (MB)
    """
    mb_size = bytes_size / (1024 * 1024)
    return mb_size

def convert_bytes_to_gb(bytes_size):
    """
    Convierts the size in bytes to gigabytes (GB)
    """
    gb_size = bytes_size / (1024 * 1024 * 1024)
    return gb_size

def total_seconds(time_str):
    """
    Convierts the time string in the format HH:MM:SS to total seconds
    """
    if ':' in time_str:
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s
    else:
        return int(time_str) * 60 

def format_runtime(seconds):
    """
    Formats the total seconds to HH:MM:SS
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def format_expiration_datetime(expiration_datetime):
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    # Get the day, month, year, hour, and minute
    day = expiration_datetime.day
    month = months[expiration_datetime.month - 1]
    year = expiration_datetime.year
    hour = expiration_datetime.hour
    minute = expiration_datetime.minute
    
    # Format the datetime string
    formatted_datetime = f"{day} {month}, {year} at {hour:02d}:{minute:02d}"
    
    return formatted_datetime

def send_render_ok_email(job_id, ses_config, render_details, zip_size, job_array_size, region):
    """
    Send an email with the specified SES configuration and render details
    """
    try:
        ses = boto3.client('ses', region_name=ses_config['region'])
        source_email = ses_config['source_email']
        destination_email = ses_config['destination_email']
        render_ok_template_name = ses_config['render_ok_template_name']

        # Render details
        project_name = render_details['project_name']
        resolution = render_details['resolution']
        scene_name = render_details['scene_name']
        layer_name = render_details['layer_name']
        camera_name = render_details['camera_name']
        samples = render_details['samples']
        engine = render_details['engine']
        render_type = render_details['render_type']
        active_frame = render_details['active_frame']
        frame_range = render_details['frame_range']
        job_array_size = render_details['job_array_size']

        thumbnail_presigned_url, output_zip_presigned_url = generate_presigned_urls(region)
        print(f"Thumbnail presigned url: {thumbnail_presigned_url}")

        runtime, _ = get_batch_job_info(job_id, region, render_details, job_array_size)

        if runtime is None:
            runtime = "N/A"
        print(f"Runtime minutes: {runtime}")


        ec2_instance_details = get_ec2_instance_details(job_id, region, job_array_size)
        print(f"EC2 Instance Details: {ec2_instance_details}")

        # Verify if the response contains EC2 instance details
        if ec2_instance_details is None:
            instance_type = 'N/A'
            instance_lifecycle = 'N/A'
        else:
            # Extract instance type and lifecycle
            instance_type = ec2_instance_details.get('InstanceType', 'N/A')
            instance_lifecycle = ec2_instance_details.get('InstanceLifecycle', 'N/A')

        print(f"Instance Type: {instance_type}")
        print(f"Instance Lifecycle: {instance_lifecycle}")

        ## Rendering time calculated: array job x runtime
        if int(job_array_size) > 0:
            total_seconds_runtime = total_seconds(runtime) * int(job_array_size)
            total_runtime_formatted = format_runtime(total_seconds_runtime)
        else:
            total_runtime_formatted = runtime 

        if zip_size > 1024 * 1024 * 1024:  # 1 GB
            object_size_str = f"{convert_bytes_to_gb(zip_size):.2f} GB"
        else:
            object_size_str = f"{convert_bytes_to_mb(zip_size):.2f} MB"

        expiration_datetime = datetime.now() + timedelta(hours=12)

        # Define the template data for the email
        template_data = {
            'project_name': project_name,
            'resolution': resolution,
            'scene_name': scene_name,
            'layer_name': layer_name,
            'camera_name': camera_name,
            'samples': samples,
            'engine': engine,
            'render_type': render_type,
            'thumbnail_url': thumbnail_presigned_url,
            'brender_download_url': output_zip_presigned_url,
            'execution_time': runtime,
            'object_size': object_size_str,
            'current_year': str(datetime.now().year),
            'expiration_time': format_expiration_datetime(expiration_datetime),
            'active_frame': active_frame,
            'frame_range': frame_range,
            'job_array_size': job_array_size,
            'queue_type': instance_lifecycle,
            'aprox_execution_time': total_runtime_formatted,
            'instance_type': instance_type,
            'instance_pricing_url': f"https://instances.vantage.sh/aws/ec2/{instance_type}?region={region}&os=linux&cost_duration=hourly&reserved_term=Standard.noUpfront"
        }

        # Send the email using the SES client
        response = ses.send_templated_email(
            Source=source_email,
            Destination={'ToAddresses': [destination_email]},
            Template=render_ok_template_name,
            TemplateData=json.dumps(template_data)
        )

        print("Email sent successfully")
        print("Message ID: ", response['MessageId'])

        return response

    except Exception as e:
        print("Error sending render ok email:", e)
        return None
