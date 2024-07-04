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
        
        
# Configurar el PYTHONPATH para incluir la ruta al directorio del proyecto
def setup_env_python_path(bucket_key):
    efs_project_path = f"/mnt/efs/projects/{bucket_key}"
    print('Ruta al directorio del proyecto:', efs_project_path)
    
    # Añade la ruta de los paquetes de Python
    python_site_packages = '/usr/local/lib/python3.10/dist-packages'
    os.environ['PYTHONPATH'] = f"{efs_project_path}:{python_site_packages}:{os.environ.get('PYTHONPATH', '')}"
    
    # Imprimir PYTHONPATH para depuración
    print("PYTHONPATH:", os.environ['PYTHONPATH'])
    

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
