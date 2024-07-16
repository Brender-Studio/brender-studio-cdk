import os
import sys

# Configurar el display para usar Eevee
def setup_display(use_eevee):
    if use_eevee == True:
        print('Usando Eevee')
        print('Abriendo display')
        os.system('Xvfb :1 -screen 0 1280x720x16 &')
        os.environ['DISPLAY'] = ':1'
        print('Display abierto')
    else:
        print('No se está usando Eevee')
        
        
# Configure the Python path and sys.path to include the project directory and its subfolders
def setup_env_python_path(bucket_key):
    efs_project_path = f"/mnt/efs/projects/{bucket_key}"
    print('Project directory path:', efs_project_path)
    
    # Add the Python packages path
    python_site_packages = '/usr/local/lib/python3.10/dist-packages'
    current_pythonpath = os.environ.get('PYTHONPATH', '')
    
    # Add all project subfolders to PYTHONPATH
    project_dirs = []
    for root, dirs, files in os.walk(efs_project_path):
        project_dirs.append(root)
    
    new_pythonpath = f"{':'.join(project_dirs)}:{python_site_packages}:{current_pythonpath}"
    os.environ['PYTHONPATH'] = new_pythonpath
    
    # Print PYTHONPATH for debugging
    print("PYTHONPATH:", os.environ['PYTHONPATH'])

    # Add paths to sys.path
    for dir_path in project_dirs:
        if dir_path not in sys.path:
            sys.path.insert(0, dir_path)
    
    # Print sys.path for debugging
    print("sys.path:", sys.path)
    

# Obtener las variables de entorno
def get_environment_variables():
    env_vars = {
        'user_main_script_path': os.environ.get('EFS_MAIN_SCRIPT_PATH'),
        'blender_file_path': os.environ.get('EFS_BLENDER_FILE_PATH'),
        'output_path': os.environ.get('EFS_BLENDER_OUTPUT_FOLDER_PATH'),
        'blender_executable_path': os.environ.get('BLENDER_EXECUTABLE'),
        'use_eevee': os.environ.get('USE_EEVEE'),
        'bucket_key': os.environ.get('BUCKET_KEY')
    }
    return env_vars


# Validar que las variables de entorno estén configuradas correctamente
def validate_environment_variables(env_vars):
    if not all(env_vars.values()):
        print("Error: Una o más variables de entorno no están configuradas correctamente.")
        sys.exit(1)
