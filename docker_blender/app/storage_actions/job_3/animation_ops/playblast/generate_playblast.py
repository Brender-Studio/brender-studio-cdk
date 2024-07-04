import os
import subprocess

blender_exec_path = os.environ['BLENDER_EXECUTABLE']
efs_path = os.environ['EFS_BLENDER_FOLDER_PATH']
bucket_key = os.environ['BUCKET_KEY']
efs_project_path = os.path.join(efs_path, bucket_key)
project_output_path = os.path.join(efs_project_path, 'output')

"""
Recibimos en los argumentos (animation_data)

En la funcion main() del script efs_to_s3.py, se recibe el json de ses y se parsea para obtener la informacion de animation_preview
animation_data = json_ses['ses']['animation_preview']

{
  "animation_preview_full_resolution": true,
  "fps": 24,
  "resolution_x": 1920,
  "resolution_y": 1080,
  "output_quality": "HIGH",
  "encoding_speed": "GOOD",
  "autosplit": true,
  "ffmpeg_format": "MPEG4"
},
"""


def generate_playblast(animation_data):
    print("Generating playblast...")
    print(animation_data)
    print(efs_project_path)
    """
    - {'animation_preview_full_resolution': True, 'fps': 24, 'resolution_x': 1920, 'resolution_y': 1080, 'output_quality': 'HIGH', 'encoding_speed': 'GOOD', 'autosplit': True, 'ffmpeg_format': 'MPEG4'}
    - /mnt/efs/projects/project_5
    """

    bpy_script_path = "/app/storage_actions/job_3/animation_ops/playblast/bpy_render_playblast.py"

    sys_args = [
        "-animation_preview_full_resolution", str(animation_data['animation_preview_full_resolution']),
        "-fps", str(animation_data['fps']),
        "-resolution_x", str(animation_data['resolution_x']),
        "-resolution_y", str(animation_data['resolution_y']),
        "-output_quality", animation_data['output_quality'],
        "-encoding_speed", animation_data['encoding_speed'],
        "-autosplit", str(animation_data['autosplit']),
        "-ffmpeg_format", animation_data['ffmpeg_format'],
        "-efs_project_path", efs_project_path,
    ]

    blender_command = [
        blender_exec_path,
        '-b',
        '-P', bpy_script_path,
        '--', 
        *sys_args
    ]

    print("Blender command:", blender_command)
    subprocess.run(blender_command)