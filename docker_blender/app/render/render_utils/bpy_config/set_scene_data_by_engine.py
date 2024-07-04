import bpy
from .cycles_configurator import configure_cycles_denoise, configure_cycles_bounces, configure_cycles_caustics, configure_cycles_clamping


def set_cycles_config(use_gpu, use_denoise, dn_alg, dn_pass, dn_prefilter, noise_threshold, caustics_fg, caustics_reflective, caustics_refractive, clamping_direct, clamping_indirect, max_bounces_diffuse, max_bounces_glossy, max_bounces_total, max_bounces_transmission, max_bounces_transparent, max_bounces_volume, samples):
    
    print("Setting cycles config")
    for arg_name, arg_value in locals().items():
        if arg_name != "self" and arg_name != "__class__":
            print(f"{arg_name}: {arg_value}")

    # set samples
    bpy.context.scene.cycles.samples = samples

    configure_cycles_denoise(use_gpu, use_denoise, dn_alg, dn_pass, dn_prefilter, noise_threshold)
    configure_cycles_bounces(max_bounces_diffuse, max_bounces_glossy, max_bounces_total, max_bounces_transmission, max_bounces_transparent, max_bounces_volume)
    configure_cycles_caustics(caustics_fg, caustics_reflective, caustics_refractive)
    configure_cycles_clamping(clamping_direct, clamping_indirect)

def set_eevee_config(taa_samples, cube_size, cascade_size, high_bitdepth, soft_shadows):
    print("Setting eevee config")
    for arg_name, arg_value in locals().items():
        if arg_name != "self" and arg_name != "__class__":
            print(f"{arg_name}: {arg_value}")

    # set taa samples
    bpy.context.scene.eevee.taa_render_samples = taa_samples
    # set shadows
    bpy.context.scene.eevee.shadow_cube_size = cube_size
    bpy.context.scene.eevee.shadow_cascade_size = cascade_size
    bpy.context.scene.eevee.use_shadow_high_bitdepth = high_bitdepth
    bpy.context.scene.eevee.use_soft_shadows = soft_shadows