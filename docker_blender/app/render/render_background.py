import bpy
import sys
import os

version = bpy.app.version
print(f"Blender version: {version}")

if version >= (4, 2, 0):
    # Append the path to the sys.path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from argparse import Namespace
from render.render_utils.bpy_config import enable_gpus
from render.render_utils.bpy_config.render_frame import render_still, render_still_without_compositor
from render.render_utils.bpy_config.render_animation import render_animation, render_animation_without_compositor
from render.render_utils.bpy_config.arg_parser_scene import create_parser
from render.render_utils.bpy_config.scene_configurator import set_scene_name, set_layer_name, set_camera, set_resolution, set_aspect_ratio, set_output_settings, configure_compositor_nodes
from render.render_utils.bpy_config.set_scene_data_by_engine import set_cycles_config, set_eevee_config
from render.render_utils.bpy_config.metadata_configurator import set_metadata


def main():
    parser = create_parser()

    # Get all the arguments after "--"
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]

    bpy.app.driver_namespace['argv'] = argv
    
    args: Namespace = parser.parse_args(bpy.app.driver_namespace['argv'])


    # If gpu is enabled, enable it
    if args.use_gpu == True:
        # Activate GPU
        enable_gpus.enable_gpus("CUDA", True)
    else:
        print("Not using GPU")

    if args.use_compositor == True:
        print("use_compositor:", args.use_compositor)
        # Call function to configure compositor nodes
        configure_compositor_nodes()
    else:
        print("use_compositor:", args.use_compositor)
        print("Not using compositor")
        bpy.context.scene.render.use_compositing = False

    if args.use_stamp_metadata == True:
        print("use_stamp_metadata:", args.use_stamp_metadata)
        set_metadata()
    else:
        print("use_stamp_metadata:", args.use_stamp_metadata)
        print("Not using metadata")
        bpy.context.scene.render.use_stamp = False
  
    # If is_render_auto is True, render automatically the frame
    if args.is_render_auto == True and args.render_type == "frame" and args.use_compositor == True:
        print("Rendering frame automatically")
        # Get the scene name
        scene_name = args.scene_name
        print(f"Tipo de scene_name: {type(scene_name)}")
        # Call function to render the frame
        render_still(args.active_frame)
    elif args.is_render_auto == True and args.render_type == "frame" and args.use_compositor == False:
        print("Rendering frame automatically without compositor")
        # Call function to render the frame
        render_still_without_compositor(args.scene_name, args.layer_name, args.active_frame)
    elif args.is_render_auto == True and args.render_type == "animation" and args.use_compositor == True:
        print("Rendering animation automatically")
        # Call function to render the animation
        render_animation(args.start_frame, args.end_frame, args.frame_step)
    elif args.is_render_auto == True and args.render_type == "animation" and args.use_compositor == False:
        print("Rendering animation automatically without compositor")
        # Call function to render the animation
        render_animation_without_compositor(args.scene_name, args.layer_name, args.start_frame, args.end_frame, args.frame_step)



    # If is_render_auto is False, set the scene data and render the frame or animation
    if args.is_render_auto == False: 
        print("Rendering manually with custom settings and scene data")
        if args.scene_name:
            print("scene_name:", args.scene_name)
            set_scene_name(args.scene_name)
        if args.layer_name:
            print("layer_name:", args.layer_name)
            set_layer_name(args.layer_name)
        if args.camera_name:
            print("camera_name:", args.camera_name)
            set_camera(args.camera_name)
        if args.resolution_width and args.resolution_height and args.resolution_percentage:
            print("resolution_width:", args.resolution_width)
            print("resolution_height:", args.resolution_height)
            print("resolution_percentage:", args.resolution_percentage)
            set_resolution(args.resolution_width, args.resolution_height, args.resolution_percentage)
        if args.aspect_ratio_width and args.aspect_ratio_height:
            print("aspect_ratio_width:", args.aspect_ratio_width)
            print("aspect_ratio_height:", args.aspect_ratio_height)
            set_aspect_ratio(args.aspect_ratio_width, args.aspect_ratio_height)
        if args.color_depth and args.color_mode and args.compression and args.output_format:
            print("color_depth:", args.color_depth)
            print("color_mode:", args.color_mode)
            print("compression:", args.compression)
            set_output_settings(args.color_depth, args.color_mode, args.compression, args.output_format)

        # Configure scene data by engine
        if args.engine == "CYCLES":
            print("engine:", args.engine)

            # set cycles engine
            bpy.context.scene.render.engine = 'CYCLES'
            engine = bpy.context.scene.render.engine
            print(f"Engine: {engine}")

            # Call function to configure cycles config
            set_cycles_config(args.use_gpu,
                              args.denoise, 
                              args.dn_alg, 
                              args.denoise_pass, 
                              args.denoise_prefilter, 
                              args.noise_threshold, 
                              args.caustics_fg, 
                              args.caustics_reflective, 
                              args.caustics_refractive,
                              args.clamping_direct,
                              args.clamping_indirect, 
                              args.max_bounces_diffuse, 
                              args.max_bounces_glossy, 
                              args.max_bounces_total, 
                              args.max_bounces_transmission, 
                              args.max_bounces_transparent, 
                              args.max_bounces_volume, 
                              args.samples)
            if args.render_type == "frame" and args.use_compositor == True:
                render_still(args.active_frame)
            elif args.render_type == "frame" and args.use_compositor == False:
                render_still_without_compositor(args.scene_name, args.layer_name, args.active_frame)
            elif args.render_type == "animation" and args.use_compositor == True:
                render_animation(args.start_frame, args.end_frame, args.frame_step)
            elif args.render_type == "animation" and args.use_compositor == False:
                render_animation_without_compositor(args.scene_name, args.layer_name, args.start_frame, args.end_frame, args.frame_step)
            
        if args.engine == "BLENDER_EEVEE":
            print("engine:", args.engine)

             # If version >= 4.2.0 then bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'

            if version >= (4, 2, 0):
                bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
                engine = bpy.context.scene.render.engine
                print(f"Engine: {engine}")
            else:
                bpy.context.scene.render.engine = 'BLENDER_EEVEE'
                engine = bpy.context.scene.render.engine
                print(f"Engine Legacy: {engine}")

            if args.render_type == "frame" and args.use_compositor == True:
                render_still(args.active_frame)
            elif args.render_type == "frame" and args.use_compositor == False:
                render_still_without_compositor(args.scene_name, args.layer_name, args.active_frame)
            elif args.render_type == "animation" and args.use_compositor == True:
                render_animation(args.start_frame, args.end_frame, args.frame_step)
            elif args.render_type == "animation" and args.use_compositor == False:
                render_animation_without_compositor(args.scene_name, args.layer_name, args.start_frame, args.end_frame, args.frame_step)

    else:
        print("is_render_auto:", args.is_render_auto)
        print("No need to set scene data")
    

if __name__ == '__main__':
    main()