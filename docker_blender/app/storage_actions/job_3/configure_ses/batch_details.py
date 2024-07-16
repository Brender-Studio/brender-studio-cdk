import boto3
from datetime import datetime, timedelta, timezone

def get_batch_job_info(job_id, region, render_details, job_array_size):
    try:
        batch_client = boto3.client('batch', region_name=region)

        # Render type Animation or Still
        render_type = render_details['render_type']
        print(f"Render Type: {render_type}")

        if int(job_array_size) > 1:
            job_id = f"{job_id}:0"
        else:
            job_id = job_id

        # Get job details from AWS Batch
        response = batch_client.describe_jobs(jobs=[job_id])

        # Verify if the response contains job details
        if 'jobs' not in response or len(response['jobs']) == 0:
            raise ValueError(f"No se encontraron detalles para el trabajo con ID {job_id}")

        # Extract job information from the response
        job_info = response['jobs'][0]

        start_time_ms = None
        end_time_ms = None

        # Verify if the job has started and stopped times
        if 'startedAt' in job_info and 'stoppedAt' in job_info:
            start_time_ms = job_info['startedAt']
            end_time_ms = job_info['stoppedAt']
        elif 'createdAt' in job_info:
            created_at_ms = job_info['createdAt']
            current_time_ms = datetime.now().timestamp() * 1000
            start_time_ms = created_at_ms
            end_time_ms = current_time_ms
        else:
            raise ValueError("AWS Batch job does not have a start or end time")

        # Calculate runtime of the job
        if start_time_ms is not None and end_time_ms is not None:
            runtime_formatted = calculate_runtime(start_time_ms, end_time_ms)
        else:
            runtime_formatted = "N/A"

        # Get status information of the job
        status_info = get_status_info(job_info)

        return runtime_formatted, status_info
    
    except Exception as e:
        print(f"Error getting job details: {e}")
        return None, None

def calculate_runtime(start_time_ms, end_time_ms):
    # Convert milliseconds to seconds
    start_time_seconds = start_time_ms / 1000
    end_time_seconds = end_time_ms / 1000

    # Convert seconds to datetime objects
    start_datetime = datetime.fromtimestamp(start_time_seconds, tz=timezone.utc)
    end_datetime = datetime.fromtimestamp(end_time_seconds, tz=timezone.utc)

    # Calculate runtime in seconds
    runtime_seconds = (end_datetime - start_datetime).total_seconds()

    # Get hours, minutes, and seconds from runtime in seconds
    hours, remainder = divmod(runtime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Format runtime as HH:MM:SS
    runtime_formatted = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

    return runtime_formatted

def get_status_info(job_info):
    try:
        # Get the reason and log stream name from the first attempt of the job
        reason = job_info['attempts'][0]['container']['reason']
        log_stream_name = job_info['attempts'][0]['container']['logStreamName']
        status_info = {
            "reason": reason,
            "log_stream_name": log_stream_name
        } 

        # If the reason or log stream name are not available, set them to a default value
        if reason is None:
            status_info['reason'] = "Information not available for this job."
        if log_stream_name is None:
            status_info['log_stream_name'] = "Name not available for this job."


        return status_info
    except Exception as e:
        print(f"Error getting status info: {e}")
        return None