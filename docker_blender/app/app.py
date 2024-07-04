import os
import sys

from app_utils.parse_json import parse_json
from app_utils.get_job_action_path import get_job_action_path
from app_utils.execute_script_by_action import execute_script_by_action

job_action = os.environ['JOB_ACTION_TYPE']


def main():
    print(f'Running job action: {job_action}')
    
    ### TESTING ###

    # python3 /app/app.py

    ## Json from aws batch job command (container override)
    ## FRAME CYCLES ##
    # render_json_str = "{\r\n  \"render_config\": {\r\n    \"type\": \"frame\",\r\n    \"is_render_auto\": false,\r\n    \"use_denoise\": false,\r\n    \"engine\": \"CYCLES\",\r\n    \"use_gpu\": true,\r\n    \"use_compositor\": true,\r\n    \"use_sequencer\": false,\r\n    \"use_stamp_metadata\": true,\r\n    \"active_frame\": 50,\r\n    \"render_info\": {\r\n      \"scene_name\": \"cube_scene\",\r\n      \"layer_name\": \"cube_layer_001\",\r\n      \"camera_name\": \"Camera_Cube\",\r\n      \"aspect_ratio\": {\r\n        \"height\": 1,\r\n        \"width\": 1\r\n      },\r\n      \"resolution\": {\r\n        \"height\": 1080,\r\n        \"width\": 1920,\r\n        \"percentage\": 100\r\n      },\r\n      \"cycles_config\": {\r\n        \"denoise_config\": {\r\n          \"algorithm\": \"OPTIX\",\r\n          \"denoise_pass\": \"RGB_ALBEDO_NORMAL\",\r\n          \"denoise_prefilter\": \"ACCURATE\",\r\n          \"noise_threshold\": 0.01\r\n        },\r\n        \"light_paths\": {\r\n          \"caustics\": {\r\n            \"filter_glossy\": 1,\r\n            \"reflective\": true,\r\n            \"refractive\": false\r\n          },\r\n          \"clamping\": {\r\n            \"direct\": 0,\r\n            \"indirect\": 10\r\n          },\r\n          \"max_bounces\": {\r\n            \"diffuse_bounces\": 4,\r\n            \"glossy_bounces\": 4,\r\n            \"total\": 12,\r\n            \"transmission_bounces\": 12,\r\n            \"transparent_max_bounces\": 8,\r\n            \"volume_bounces\": 0\r\n          }\r\n        },\r\n        \"samples\": 500\r\n      },\r\n      \"output\": {\r\n        \"color\": {\r\n          \"color_depth\": \"8\",\r\n          \"color_mode\": \"RGBA\"\r\n        },\r\n        \"compression\": 15,\r\n        \"output_format\": \"PNG\",\r\n        \"project_name\": \"test-project\"\r\n      }\r\n    }\r\n  }\r\n}"
    
    ## FRAME EEVEE ##
    # render_json_str = "{\r\n  \"render_config\": {\r\n    \"type\": \"frame\",\r\n    \"is_render_auto\": false,\r\n    \"use_denoise\": true,\r\n    \"engine\": \"BLENDER_EEVEE\",\r\n    \"use_gpu\": true,\r\n    \"use_compositor\": true,\r\n    \"use_sequencer\": false,\r\n    \"use_stamp_metadata\": false,\r\n    \"active_frame\": 50,\r\n    \"render_info\": {\r\n      \"scene_name\": \"cube_scene\",\r\n      \"layer_name\": \"cube_layer_001\",\r\n      \"camera_name\": \"Camera_Cube\",\r\n      \"aspect_ratio\": {\r\n        \"height\": 1,\r\n        \"width\": 1\r\n      },\r\n      \"resolution\": {\r\n        \"height\": 1080,\r\n        \"width\": 1920,\r\n        \"percentage\": 100\r\n      },\r\n      \"eevee_config\": {\r\n       \"taa_samples\": 64,\r\n       \"shadows\": {\r\n        \"cube_size\": 512,\r\n        \"cascade_size\":512,\r\n        \"high_bitdepth\": true,\r\n        \"soft_shadows\": true\r\n       }\r\n      },\r\n      \"output\": {\r\n        \"color\": {\r\n          \"color_depth\": \"8\",\r\n          \"color_mode\": \"RGBA\"\r\n        },\r\n        \"compression\": 15,\r\n        \"output_format\": \"PNG\",\r\n        \"project_name\": \"test-project\"\r\n      }\r\n    }\r\n  }\r\n}"
    
    ## ANIMATION CYCLES ##
    # render_json_str = "\r\n{\r\n  \"render_config\": {\r\n    \"type\": \"animation\",\r\n    \"is_render_auto\": false,\r\n    \"use_denoise\": true,\r\n    \"engine\": \"CYCLES\",\r\n    \"use_gpu\": true,\r\n    \"use_compositor\": true,\r\n    \"use_sequencer\": false,\r\n    \"use_stamp_metadata\": true,\r\n    \"active_frame\": 50,\r\n    \"start_frame\": 1,\r\n    \"end_frame\": 50,\r\n    \"frame_step\": 1,\r\n    \"fps\": 24,\r\n    \"render_info\": {\r\n      \"scene_name\": \"Scene2\",\r\n      \"layer_name\": \"ViewLayer\",\r\n      \"camera_name\": \"Camera1.001\",\r\n      \"aspect_ratio\": {\r\n        \"height\": 1,\r\n        \"width\": 1\r\n      },\r\n      \"resolution\": {\r\n        \"height\": 1080,\r\n        \"width\": 1920,\r\n        \"percentage\": 100\r\n      },\r\n      \"cycles_config\": {\r\n        \"denoise_config\": {\r\n          \"algorithm\": \"OPTIX\",\r\n          \"denoise_pass\": \"RGB_ALBEDO_NORMAL\",\r\n          \"denoise_prefilter\": \"ACCURATE\",\r\n          \"noise_threshold\": 0.01\r\n        },\r\n        \"light_paths\": {\r\n          \"caustics\": {\r\n            \"filter_glossy\": 1,\r\n            \"reflective\": true,\r\n            \"refractive\": false\r\n          },\r\n          \"clamping\": {\r\n            \"direct\": 0,\r\n            \"indirect\": 10\r\n          },\r\n          \"max_bounces\": {\r\n            \"diffuse_bounces\": 4,\r\n            \"glossy_bounces\": 4,\r\n            \"total\": 12,\r\n            \"transmission_bounces\": 12,\r\n            \"transparent_max_bounces\": 8,\r\n            \"volume_bounces\": 0\r\n          }\r\n        },\r\n        \"samples\": 500\r\n      },\r\n      \"output\": {\r\n        \"color\": {\r\n          \"color_depth\": \"8\",\r\n          \"color_mode\": \"RGBA\"\r\n        },\r\n        \"compression\": 15,\r\n        \"output_format\": \"PNG\",\r\n        \"project_name\": \"test-project\"\r\n      }\r\n    }\r\n  }\r\n}"

    ## FRAME EEVEE ##
    # render_json_str = "{\r\n  \"render_config\": {\r\n    \"type\": \"frame\",\r\n    \"is_render_auto\": false,\r\n    \"use_denoise\": true,\r\n    \"engine\": \"BLENDER_EEVEE\",\r\n    \"use_gpu\": true,\r\n    \"use_compositor\": true,\r\n    \"use_sequencer\": false,\r\n    \"use_stamp_metadata\": false,\r\n    \"active_frame\": 50,\r\n    \"render_info\": {\r\n      \"scene_name\": \"cone_scene\",\r\n      \"layer_name\": \"cone_layer_001\",\r\n      \"camera_name\": \"Camera_Cone\",\r\n      \"aspect_ratio\": {\r\n        \"height\": 1,\r\n        \"width\": 1\r\n      },\r\n      \"resolution\": {\r\n        \"height\": 1080,\r\n        \"width\": 1920,\r\n        \"percentage\": 100\r\n      },\r\n      \"eevee_config\": {\r\n       \"taa_samples\": 64,\r\n       \"shadows\": {\r\n        \"cube_size\": 512,\r\n        \"cascade_size\":512,\r\n        \"high_bitdepth\": true,\r\n        \"soft_shadows\": true\r\n       }\r\n      },\r\n      \"output\": {\r\n        \"color\": {\r\n          \"color_depth\": \"8\",\r\n          \"color_mode\": \"RGBA\"\r\n        },\r\n        \"compression\": 15,\r\n        \"output_format\": \"PNG\",\r\n        \"project_name\": \"test-project\"\r\n      }\r\n    }\r\n  }\r\n}"

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