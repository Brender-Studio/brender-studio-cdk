import subprocess

def run_blender_command(env_vars):
    blender_command = [
        env_vars['blender_executable_path'],
        '-b',
        env_vars['blender_file_path'],
        '-P',
        env_vars['user_main_script_path'],
    ]
    print("Blender command:", ' '.join(blender_command))
    
    subprocess.run(blender_command, check=True, text=True)
