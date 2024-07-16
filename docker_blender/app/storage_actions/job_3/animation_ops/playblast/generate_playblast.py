import os
import subprocess

blender_exec_path = os.environ['BLENDER_EXECUTABLE']
efs_path = os.environ['EFS_BLENDER_FOLDER_PATH']
bucket_key = os.environ['BUCKET_KEY']
efs_project_path = os.path.join(efs_path, bucket_key)
project_output_path = os.path.join(efs_project_path, 'output')


def generate_playblast(animation_data):
    print("Generating playblast...")
    print(animation_data)
    print(efs_project_path)

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