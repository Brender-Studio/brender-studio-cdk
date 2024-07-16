import bpy
import os

output_path = os.environ['EFS_BLENDER_OUTPUT_FOLDER_PATH']

def set_scene_name(scene_name):
    bpy.context.scene.name = scene_name

def set_layer_name(layer_name):
    # bpy.context.scene.render.layers.active.name = layer_name
    if layer_name in bpy.context.scene.view_layers:
            bpy.context.scene.view_layers[layer_name].use = True
    else:
        print(f"Error: View layer '{layer_name}' not found in the scene.")

def set_camera(camera_name):
    try:
        bpy.context.scene.camera = bpy.data.objects[camera_name]
    except KeyError as e:
        print(f"Error: No camera named '{camera_name}' found in the scene.")
        print("Error:", e)

def set_resolution(resolution_width, resolution_height, resolution_percentage):
    bpy.context.scene.render.resolution_x = resolution_width
    bpy.context.scene.render.resolution_y = resolution_height
    bpy.context.scene.render.resolution_percentage = resolution_percentage

def set_aspect_ratio(aspect_ratio_width, aspect_ratio_height):
    bpy.context.scene.render.pixel_aspect_x = aspect_ratio_width
    bpy.context.scene.render.pixel_aspect_y = aspect_ratio_height

def set_output_settings(output_color_depth, output_color_mode, output_compression, output_format):
    bpy.context.scene.render.image_settings.color_depth = output_color_depth
    bpy.context.scene.render.image_settings.color_mode = output_color_mode
    bpy.context.scene.render.image_settings.compression = output_compression
    bpy.context.scene.render.image_settings.file_format = output_format

def configure_compositor_nodes():
    
    compositor_context = bpy.context.scene.node_tree
    print(compositor_context)

    if compositor_context:
        file_output_nodes = [node for node in compositor_context.nodes if node.bl_idname == "CompositorNodeOutputFile"]

        for index, file_output_node in enumerate(file_output_nodes):
            file_output_node.base_path = os.path.join(output_path, "")
            print(f"Render file path: {file_output_node.base_path}")
            for slot_index, file_slot in enumerate(file_output_node.file_slots):
                file_slot.path = ""
                prefix = f"compositor/FO_{index}_S_{slot_index}_#####"
                file_slot.path += f"{prefix}"