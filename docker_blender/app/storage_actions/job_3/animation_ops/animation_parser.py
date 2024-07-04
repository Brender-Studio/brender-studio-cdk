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

    parser.add_argument("-animation_preview_full_resolution", type=str_to_bool)
    parser.add_argument("-fps", type=int)
    parser.add_argument("-resolution_x", type=int)
    parser.add_argument("-resolution_y", type=int)
    parser.add_argument("-output_quality", type=str)
    parser.add_argument("-encoding_speed", type=str)
    parser.add_argument("-autosplit", type=str_to_bool)
    parser.add_argument("-ffmpeg_format", type=str)
    parser.add_argument("-efs_project_path", type=str)

    return parser