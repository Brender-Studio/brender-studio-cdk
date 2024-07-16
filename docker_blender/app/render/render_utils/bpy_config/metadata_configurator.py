import bpy

def set_metadata():
    # Metadata stamp (burn-in )
    bpy.context.scene.render.use_stamp = True

    # Metadata stamp options
    bpy.context.scene.render.use_stamp_date = True
    bpy.context.scene.render.use_stamp_time = True
    bpy.context.scene.render.use_stamp_render_time = True
    bpy.context.scene.render.use_stamp_frame = True
    bpy.context.scene.render.use_stamp_frame_range = True
    bpy.context.scene.render.use_stamp_memory = True
    bpy.context.scene.render.use_stamp_hostname = False
    bpy.context.scene.render.use_stamp_camera = True
    bpy.context.scene.render.use_stamp_lens = True
    bpy.context.scene.render.use_stamp_scene = True
    bpy.context.scene.render.use_stamp_marker = True
    bpy.context.scene.render.use_stamp_note = True
    bpy.context.scene.render.use_stamp_sequencer_strip = True
    bpy.context.scene.render.use_stamp_filename = True
    bpy.context.scene.render.stamp_background = (0, 0, 0, 0.8)


    # Note stamp metadata
    note_stamp_metadata()


def note_stamp_metadata():
    bpy.context.scene.render.stamp_note_text = "Brender Studio"

