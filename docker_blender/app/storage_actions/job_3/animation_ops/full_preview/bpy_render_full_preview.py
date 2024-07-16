import bpy
import sys
import os
from argparse import Namespace
from storage_actions.job_3.animation_ops.animation_parser import create_parser


def main():
    print("bpy script playblast")
    parser = create_parser()
    
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]

    bpy.app.driver_namespace['argv'] = argv
    

    args: Namespace = parser.parse_args(bpy.app.driver_namespace['argv'])

    video_codec = 'H264'  # 'NONE', 'DNXHD', 'DV', 'FFV1', 'FLASH', 'H264', 'HUFFYUV', 'MPEG1', 'MPEG2', 'MPEG4', 'PNG', 'QTRLE', 'THEORA', 'WEBM', 'AV1')
    output_quality = args.output_quality  # 'HIGH', 'MEDIUM', 'LOW'
    encoding_speed = args.encoding_speed  # 'GOOD', 'REALTIME', 'BEST'
    autosplit = args.autosplit

    print("args:", args)
    res_x = args.resolution_x
    res_y = args.resolution_y

    scene = bpy.context.scene
    scene.render.resolution_x = res_x
    scene.render.resolution_y = res_y

    scene.render.fps = args.fps
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = args.ffmpeg_format # 'MPEG4'
    scene.render.ffmpeg.codec = video_codec
    scene.render.ffmpeg.constant_rate_factor = output_quality
    scene.render.ffmpeg.ffmpeg_preset = encoding_speed
    scene.render.ffmpeg.use_autosplit = autosplit

    # color management
    scene.view_settings.view_transform = 'Standard'
    scene.view_settings.look = 'None'

    output_folder = os.path.join(args.efs_project_path, 'output')
    print("Output folder:", output_folder)
    full_preview_path = args.efs_project_path
    print("Playblast path:", full_preview_path)

    seq = bpy.context.scene.sequence_editor_create()
    images = sorted([f for f in os.listdir(output_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.exr', '.tif', '.tiff', '.bmp', '.tga', '.cin', '.dpx', '.hdr', '.webp'))])

    for index, image in enumerate(images):
        filepath = os.path.join(output_folder, image)
        seq_strip = seq.sequences.new_image(name=image, filepath=filepath, channel=1, frame_start=index+1)

    scene.frame_start = 1
    scene.frame_end = len(images)
    
    # Name of the output file
    output_filepath = os.path.join(full_preview_path, 'bs_full_resolution_')
    bpy.context.scene.render.filepath = output_filepath

    bpy.ops.render.render(animation=True, write_still=True)

if __name__ == "__main__":
    main()