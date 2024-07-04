import bpy
import os
import subprocess

output_path = os.environ.get('EFS_BLENDER_OUTPUT_FOLDER_PATH')


# Verificar si la carpeta de salida ya existe, si no, crearla
if not os.path.exists(output_path):
    os.makedirs(output_path)
    print(f"Carpeta de salida {output_path} creada correctamente.")
else:
    print(f"La carpeta de salida {output_path} ya existe.")


# Usar subpprocess para listar la ruta de los archivos en EFS
subprocess.run(['ls', '-l', '/mnt/efs'], check=True)
# Listar directorios y archivos en EFS con tree
subprocess.run(['tree', '/mnt/efs'], check=True) 

def render_still(active_frame):
    # Seteamos el frame a renderizar    
    bpy.context.scene.frame_set(active_frame)

    # Imprimimos el valor de output_path
    print("Valor de output_path:", output_path)

    # Seteamos el output path para renderizar según el tipo de render
    render_file_path = os.path.join(output_path, f"{active_frame:05d}")
    
    # Imprimimos el valor de render_file_path
    print("Valor de render_file_path:", render_file_path)

    # Seteamos el filepath para el renderizado
    bpy.context.scene.render.filepath = render_file_path

    # Renderizamos la imagen
    bpy.ops.render.render(write_still=True)


    