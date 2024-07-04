import sys
import os

# aws_batch_job_index = int(os.environ['AWS_BATCH_JOB_ARRAY_INDEX'])
# aws_batch_array_size = int(os.environ['AWS_BATCH_JOB_ARRAY_SIZE'])
output_path = os.environ['EFS_BLENDER_OUTPUT_FOLDER_PATH']


def calculate_active_frame(aws_batch_job_index, start_frame, frame_step):
    if aws_batch_job_index == 0:
        return start_frame 
    else:
        return start_frame + (aws_batch_job_index * frame_step)


def build_sys_args(render_config):
    sys_args = [
        "-render_type", render_config['type'],
        "-is_render_auto", str(render_config['is_render_auto']),
        "-dn", str(render_config['use_denoise']),
        "-use_gpu", str(render_config['use_gpu']),
        "-use_compositor", str(render_config['use_compositor']),
        "-use_sequencer", str(render_config['use_sequencer']),
        "-use_stamp_metadata", str(render_config['use_stamp_metadata']),
        "-E", render_config['engine'],
    ]
    return sys_args


def build_sys_args_by_render_type(json_blender_render):
    print("Building sys args by render type...")
    render_type = json_blender_render['render_config']['type']
    print("Render type:", render_type)


    render_config = json_blender_render['render_config']
    render_info = json_blender_render['render_config']['render_info']
    sys_args = build_sys_args(render_config)

    common_sys_args = [
        "-S", render_info['scene_name'],
        "-L", render_info['layer_name'],
        "-C", render_info['camera_name'],
        "-ar_h", str(render_info['aspect_ratio']['height']),
        "-ar_w", str(render_info['aspect_ratio']['width']),
        "-res_h", str(render_info['resolution']['height']),
        "-res_w", str(render_info['resolution']['width']),
        "-res_p", str(render_info['resolution']['percentage']),
        "-color_depth", render_info['output']['color']['color_depth'],
        "-color_mode", render_info['output']['color']['color_mode'],
        "-compression", str(render_info['output']['compression']),
        "-output_format", render_info['output']['output_format'],
        "-project_name", render_info['output']['project_name'],
        "-output_path", output_path,
    ]

    if render_config['engine'] == "CYCLES":
        cycles_sys_args = [
            "-dn_alg", render_info['cycles_config']['denoise_config']['algorithm'],
            "-dn_pass", render_info['cycles_config']['denoise_config']['denoise_pass'],
            "-dn_prefilter", render_info['cycles_config']['denoise_config']['denoise_prefilter'],
            "-noise_threshold", str(render_info['cycles_config']['denoise_config']['noise_threshold']),
            "-caustics_fg", str(render_info['cycles_config']['light_paths']['caustics']['filter_glossy']),
            "-caustics_reflective", str(render_info['cycles_config']['light_paths']['caustics']['reflective']),
            "-caustics_refractive", str(render_info['cycles_config']['light_paths']['caustics']['refractive']),
            "-clamping_direct", str(render_info['cycles_config']['light_paths']['clamping']['direct']),
            "-clamping_indirect", str(render_info['cycles_config']['light_paths']['clamping']['indirect']),
            "-max_bounces_diffuse", str(render_info['cycles_config']['light_paths']['max_bounces']['diffuse_bounces']),
            "-max_bounces_glossy", str(render_info['cycles_config']['light_paths']['max_bounces']['glossy_bounces']),
            "-max_bounces_total", str(render_info['cycles_config']['light_paths']['max_bounces']['total']),
            "-max_bounces_transmission", str(render_info['cycles_config']['light_paths']['max_bounces']['transmission_bounces']),
            "-max_bounces_transparent", str(render_info['cycles_config']['light_paths']['max_bounces']['transparent_max_bounces']),
            "-max_bounces_volume", str(render_info['cycles_config']['light_paths']['max_bounces']['volume_bounces']),
            "-samples", str(render_info['cycles_config']['samples']),
        ]

    # if render_config['engine'] == "BLENDER_EEVEE":
    #     eevee_sys_args = [
    #         "-taa_samples", str(render_info['eevee_config']['taa_samples']),
    #         "-cube_size", str(render_info['eevee_config']['shadows']['cube_size']),
    #         "-cascade_size", str(render_info['eevee_config']['shadows']['cascade_size']),
    #         "-high_bitdepth", str(render_info['eevee_config']['shadows']['high_bitdepth']),
    #         "-soft_shadows", str(render_info['eevee_config']['shadows']['soft_shadows']),
    #     ]


    if render_type == "frame":
        print("Frame render type detected")
        # Extend sys args with frame specific args
        sys_args.extend([
            "-active_frame", str(render_config['active_frame']),
        ])

        # Solo extender los sys args common si no es render auto
        if not render_config['is_render_auto']:
            sys_args.extend(common_sys_args)

        # Solo extender los sys args cycles si el engine es CYCLES y no es render auto
        if render_config['engine'] == "CYCLES" and not render_config['is_render_auto']:
            sys_args.extend(cycles_sys_args)

        # if render_config['engine'] == "BLENDER_EEVEE" and not render_config['is_render_auto']:
        #     sys_args.extend(eevee_sys_args)
      

    elif render_type == "animation":
        aws_batch_job_index = int(os.environ['AWS_BATCH_JOB_ARRAY_INDEX'])
        aws_batch_array_size = int(os.environ['AWS_BATCH_JOB_ARRAY_SIZE'])
        print("Animation render type detected")
        start_frame = int(render_config['start_frame'])
        end_frame = int(render_config['end_frame'])
        frame_step = int(render_config['frame_step'])

        # Llamar funcion para calcular el frame activo segun el array job de aws batch
        active_frame = calculate_active_frame(aws_batch_job_index, start_frame, frame_step)

        # Extend sys args with animation specific args
        sys_args.extend([
            "-fps", str(render_config['fps']),
            "-active_frame", str(active_frame),
            "-start_frame", str(start_frame),
            "-end_frame", str(end_frame),
            "-frame_step", str(frame_step),
        ])

        # Solo extender los sys args common si no es render auto
        if not render_config['is_render_auto']:
            sys_args.extend(common_sys_args)
        
        # Solo extender los sys args cycles si el engine es CYCLES y no es render auto
        if render_config['engine'] == "CYCLES" and not render_config['is_render_auto']:
            sys_args.extend(cycles_sys_args)

        # if render_config['engine'] == "BLENDER_EEVEE" and not render_config['is_render_auto']:
        #     sys_args.extend(eevee_sys_args)


    else:
        print("Error, render type not detected")
        sys.exit(1)

    return sys_args