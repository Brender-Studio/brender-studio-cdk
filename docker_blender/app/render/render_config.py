import sys
import os
import subprocess

from app_utils.parse_json import parse_json
from render_utils.environment.configure_virtual_display import configure_virtual_display
from render_utils.environment.build_sys_args_by_render_type import build_sys_args_by_render_type

blender_file_path = os.environ['EFS_BLENDER_FILE_PATH']
output_path = os.environ['EFS_BLENDER_OUTPUT_FOLDER_PATH']
blender_executable_path = os.environ['BLENDER_EXECUTABLE']

"""
Aqui obtenemos la configuracion de renderizado de la escena por sys args.

1. Parseamos el JSON de la configuracion de renderizado.
2. Segun el engine de renderizado, debemos activar xvfb para que funcione el renderizado. (BLENDER_EEVEE)
3. Segun el type de renderizado, debemos obtener las caracteristicas unicas de cada uno. (Active frame correspondiente, etc.)
4. Creamos el comando de renderizado con las caracteristicas obtenidas. Corremos Blender en background con el comando de renderizado (sys args customizados).
"""

# REVISAR SI funciona el listado de archivos en EFS
def list_efs_contents(directory):
    """
    List and print all contents of a directory recursively.
    
    Args:
    directory (str): The directory path to list contents from.
    """
    print(f"Contents of {directory}:")
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(os.path.join(root, file))

list_efs_contents('/mnt/efs')

# Parse JSON 
render_json_str = sys.argv[1]

if len(sys.argv) > 2:
    print("Error, no json string provided")
    sys.exit(1)

json_blender_render = parse_json(render_json_str)
# print("Parsed JSON:", json_blender_render)

# Llamar a la funcion que configura el display virtual
configure_virtual_display(json_blender_render)

# Llamar a la funcion que construye los sys args segun el tipo de renderizado
sys_args = build_sys_args_by_render_type(json_blender_render)
# print("Sys args:", sys_args)

custom_script = '/app/render/render_background.py'

# Correr Blender en background con el comando de renderizado

blender_command = [
    # 'blender',
    blender_executable_path,
    '-b',
    blender_file_path,
    '-P',
    custom_script,
    '--', 
    *sys_args
]

print("Blender command:", blender_command)


# Correr el comando de renderizado
# os.system(' '.join(blender_command))
subprocess.run(blender_command)
