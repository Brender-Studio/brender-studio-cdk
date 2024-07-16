import sys
import os
import subprocess

from app_utils.parse_json import parse_json
from render_utils.environment.configure_virtual_display import configure_virtual_display
from render_utils.environment.build_sys_args_by_render_type import build_sys_args_by_render_type

blender_file_path = os.environ['EFS_BLENDER_FILE_PATH']
output_path = os.environ['EFS_BLENDER_OUTPUT_FOLDER_PATH']
blender_executable_path = os.environ['BLENDER_EXECUTABLE']

# Parse JSON 
render_json_str = sys.argv[1]

if len(sys.argv) > 2:
    print("Error, no json string provided")
    sys.exit(1)

json_blender_render = parse_json(render_json_str)
# print("Parsed JSON:", json_blender_render)

# Call the function that sets up the virtual display
configure_virtual_display(json_blender_render)

# Build the sys args for the render command
sys_args = build_sys_args_by_render_type(json_blender_render)
# print("Sys args:", sys_args)

custom_script = '/app/render/render_background.py'

# Build the Blender command

blender_command = [
    blender_executable_path,
    '-b',
    blender_file_path,
    '-P',
    custom_script,
    '--', 
    *sys_args
]

print("Blender command:", blender_command)

# Run the Blender command
subprocess.run(blender_command)
