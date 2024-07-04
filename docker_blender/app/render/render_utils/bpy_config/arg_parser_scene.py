from argparse import ArgumentParser

def create_parser():
    parser = ArgumentParser()

    def str_to_bool(s: str) -> bool:
        if s == "True":
            return True
        elif s == "False":
            return False
        else:
            raise ValueError("Cannot convert string to bool")

    parser.add_argument("-render_type", help="Type of render", required=True, type=str)
    parser.add_argument("-active_frame",  help="Active frame to render", required=False, type=int)
    parser.add_argument("-S", "--scene_name", help="Scene to render", required=False, type=str)
    parser.add_argument("-L", "--layer_name", help="Layer to render", required=False, type=str)
    parser.add_argument("-C", "--camera_name", help="Camera to render", required=False, type=str)
    parser.add_argument("-E", "--engine", help="Engine", required=False, type=str)
    # render config global
    parser.add_argument("-is_render_auto", help="Is render auto", required=False, type=str_to_bool)
    parser.add_argument("-project_name", help="Project name", required=False, type=str)
    parser.add_argument("-output_path", help="Output path", required=False, type=str)
    parser.add_argument("-use_gpu", help="Use GPU", required=False, type=str_to_bool)
    parser.add_argument("-use_compositor", help="Use compositor", required=False, type=str_to_bool)
    parser.add_argument("-use_sequencer", help="Use sequencer", required=False, type=str_to_bool)
    parser.add_argument("-use_stamp_metadata", help="Use stamp metadata", required=False, type=str_to_bool)
    parser.add_argument("-start_frame", help="Start frame", required=False, type=int)
    parser.add_argument("-end_frame", help="End frame", required=False, type=int)
    parser.add_argument("-frame_step", help="Frame step", required=False, type=float)
    # render info
    parser.add_argument("-ar_h", "--aspect_ratio_height", help="Aspect ratio height", required=False, type=float)
    parser.add_argument("-ar_w", "--aspect_ratio_width", help="Aspect ratio width", required=False, type=float)
    parser.add_argument("-res_h", "--resolution_height", help="Resolution height", required=False, type=int)
    parser.add_argument("-res_w", "--resolution_width", help="Resolution width", required=False, type=int)
    parser.add_argument("-res_p", "--resolution_percentage", help="Resolution percentage", required=False, type=int)
    parser.add_argument("-color_depth", help="Color depth", required=False, type=str)
    parser.add_argument("-color_mode", help="Color mode", required=False, type=str)
    parser.add_argument("-compression", help="Compression", required=False, type=int)
    parser.add_argument("-output_format", help="Output format", required=False, type=str)
    parser.add_argument("-fps", help="FPS", required=False, type=int) # review type
    # cycles
    parser.add_argument("-dn_alg", help="Denoise algorithm", required=False, type=str)
    parser.add_argument("-dn", "--denoise", help="Use denoise", required=False, type=str_to_bool)
    parser.add_argument("-dn_pass", "--denoise_pass", help="Denoise pass", required=False, type=str)
    parser.add_argument("-dn_prefilter", "--denoise_prefilter", help="Denoise prefilter", required=False, type=str)
    parser.add_argument("-noise_threshold", help="Noise threshold", required=False, type=float)
    parser.add_argument("-caustics_fg", help="Caustics filter glossy", required=False, type=int)
    parser.add_argument("-caustics_reflective", help="Caustics reflective", required=False, type=str_to_bool)
    parser.add_argument("-caustics_refractive", help="Caustics refractive", required=False, type=str_to_bool)
    parser.add_argument("-clamping_direct", help="Clamping direct", required=False, type=int)
    parser.add_argument("-clamping_indirect", help="Clamping indirect", required=False, type=int)
    parser.add_argument("-max_bounces_diffuse", help="Max bounces diffuse", required=False, type=int)
    parser.add_argument("-max_bounces_glossy", help="Max bounces glossy", required=False, type=int)
    parser.add_argument("-max_bounces_total", help="Max bounces total", required=False, type=int)
    parser.add_argument("-max_bounces_transmission", help="Max bounces transmission", required=False, type=int)
    parser.add_argument("-max_bounces_transparent", help="Max bounces transparent", required=False, type=int)
    parser.add_argument("-max_bounces_volume", help="Max bounces volume", required=False, type=int)
    parser.add_argument("-samples", help="Samples", required=False, type=int)
    ## eevee
    parser.add_argument("-taa_samples", help="TAA samples", required=False, type=int)
    parser.add_argument("-cube_size", help="Cube size", required=False, type=str)
    parser.add_argument("-cascade_size", help="Cascade size", required=False, type=str)
    parser.add_argument("-high_bitdepth", help="High bitdepth", required=False, type=str_to_bool)
    parser.add_argument("-soft_shadows", help="Soft shadows", required=False, type=str_to_bool)

    return parser
