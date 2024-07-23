import bpy
import os

output_path = os.environ.get('EFS_BLENDER_OUTPUT_FOLDER_PATH')


# Verify if the output path exists, if not, create it
if not os.path.exists(output_path):
    os.makedirs(output_path)
    print(f"Output folder {output_path} created.")
else:
    print(f"Output folder {output_path} already exists.")


def render_still(active_frame):
    # Set the active frame
    bpy.context.scene.frame_set(active_frame)

    print("OUTPUT PATH: ", output_path)

    # Set the render file path for the frame
    render_file_path = os.path.join(output_path, f"{active_frame:05d}")
    
    print("render_file_path:", render_file_path)

    # Set the render file path in the scene
    bpy.context.scene.render.filepath = render_file_path

    # Render the frame
    bpy.ops.render.render(write_still=True)


    