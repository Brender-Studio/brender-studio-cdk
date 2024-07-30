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


def render_still_without_compositor(scene_name, layer_name, active_frame):
    
    if scene_name in bpy.data.scenes:
        scene = bpy.data.scenes[scene_name]
        bpy.context.window.scene = scene
    else:
        print(f"Error: Scene '{scene_name}' not found.")
        return

    # Configure the active layer
    for layer in scene.view_layers:
        layer.use = (layer.name == layer_name)

    scene.use_nodes = True
    render_layer_node = scene.node_tree.nodes.get("Render Layers")
    if render_layer_node:
        render_layer_node.layer = layer_name
    else:
        print("Error: Render Layer node not found.")
        return

    # Set the active frame 
    scene.frame_set(active_frame)

    print("output_path:", output_path)

    output_file = os.path.join(output_path, f"{layer_name}_{active_frame:05d}")
    scene.render.filepath = output_file

    bpy.ops.render.render(write_still=True)

    print(f"Rendered frame {active_frame} of layer {layer_name}.")
    