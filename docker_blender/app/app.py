import os
import sys

from app_utils.parse_json import parse_json
from app_utils.get_job_action_path import get_job_action_path
from app_utils.execute_script_by_action import execute_script_by_action

job_action = os.environ['JOB_ACTION_TYPE']


def main():
    print(f'Running job action: {job_action}')

    # Parse JSON from AWS Batch job command
    command_container_json_str = sys.argv[1] if len(sys.argv) > 1 else "{}"

    json_command_container = parse_json(command_container_json_str)
    print("Parsed JSON:", json_command_container)

    # Get job action path from job action type
    job_action_script_path = get_job_action_path(job_action)
    print("Job action script path:", job_action_script_path)

    # Execute script by job action type
    execute_script_by_action(json_command_container, job_action_script_path, job_action)


if __name__ == '__main__':
    main()