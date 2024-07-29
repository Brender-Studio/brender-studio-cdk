import bpy
import sys
import os
from argparse import Namespace

version = bpy.app.version
print(f"Blender version: {version}")

if version >= (4, 2, 0):
    print("Python path:", sys.path)
    sys.path.append('/app') 

from storage_actions.job_3.animation_ops.animation_parser import create_parser

def main():
    print("bpy script playblast")
    parser = create_parser()

    argv = sys.argv
    argv = argv[argv.index("--") + 1:]

    bpy.app.driver_namespace['argv'] = argv

    args: Namespace = parser.parse_args(bpy.app.driver_namespace['argv'])

    video_codec = 'H264'  # 'NONE', 'DNXHD', 'DV', 'FFV1', 'FLASH', 'H264', 'HUFFYUV', 'MPEG1', 'MPEG2', 'MPEG4', 'PNG', 'QTRLE', 'THEORA', 'WEBM', 'AV1')
    output_quality = 'LOW'  # 'HIGH', 'MEDIUM', 'LOW'
    encoding_speed = 'GOOD'  # 'GOOD', 'REALTIME', 'BEST'
    autosplit = False 

    print("args:", args)
    res_x = args.resolution_x
    res_y = args.resolution_y

    scene = bpy.context.scene
    scene.render.resolution_x = res_x
    scene.render.resolution_y = res_y

    scene.render.fps = args.fps
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = video_codec
    scene.render.ffmpeg.constant_rate_factor = output_quality
    scene.render.ffmpeg.ffmpeg_preset = encoding_speed
    scene.render.ffmpeg.use_autosplit = autosplit

    # Color management settings
    scene.view_settings.view_transform = 'Standard'
    scene.view_settings.look = 'None'

    output_folder = os.path.join(args.efs_project_path, 'output')
    print("Output folder:", output_folder)
    playblast_path = args.efs_project_path
    print("Playblast path:", playblast_path)

    # create a new video sequence
    seq = bpy.context.scene.sequence_editor_create()

    # Find all images in the output folder
    image_extensions = ('.png', '.jpg', '.jpeg', '.exr', '.tif', '.tiff', '.bmp', '.tga', '.cin', '.dpx', '.hdr', '.webp')
    images = []

    for root, _, files in os.walk(output_folder):
        # Exclude images from the compositor directory
        if any('compositor' in part.lower() for part in root.split(os.path.sep)):
            continue  # Skip the current directory
        for file in files:
            if file.lower().endswith(image_extensions):
                images.append(os.path.join(root, file))

    # Sort the images by name
    images.sort()

    # Add images to the video sequence
    for index, image in enumerate(images):
        seq.sequences.new_image(name=os.path.basename(image), filepath=image, channel=1, frame_start=index+1)

    # Set the start and end frames
    scene.frame_start = 1
    scene.frame_end = len(images)

    output_filepath = os.path.join(playblast_path, 'bs_playblast_')
    bpy.context.scene.render.filepath = output_filepath

    bpy.ops.render.render(animation=True, write_still=True)

if __name__ == "__main__":
    main()
