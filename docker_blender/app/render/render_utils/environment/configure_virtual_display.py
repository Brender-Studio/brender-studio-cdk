import os

def configure_virtual_display(json_blender_render):
    print("CONFIGURE_VIRTUAL_DISPLAY")

    if json_blender_render is None:
        return

    engine = json_blender_render.get('render_config', {}).get('engine', '')

    if engine == "BLENDER_EEVEE":
        os.system('Xvfb :1 -screen 0 1280x720x16 &')
        os.environ['DISPLAY'] = ':1'
        print("Blender EEVEE engine selected")
    else:
        print("Blender CYCLES engine selected")