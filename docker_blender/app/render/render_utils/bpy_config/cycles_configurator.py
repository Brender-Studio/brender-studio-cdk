import bpy

def configure_cycles_denoise(use_gpu, use_denoise, dn_alg, dn_pass, dn_prefilter, noise_threshold):
    for device in bpy.context.preferences.addons["cycles"].preferences.devices:
            print(f"Device: {device.name}, Type: {device.type}, Use: {device.use}")

    bpy.context.scene.render.engine = "CYCLES"

    # Use denoising 
    bpy.context.scene.cycles.use_denoising = use_denoise
    # Denoise passes (albedo, normal, ...)
    bpy.context.scene.cycles.denoising_data_passes = dn_pass
    # Denoise prefilter type 
    bpy.context.scene.cycles.denoising_prefilter_type = dn_prefilter
    # Denoise prefilter (0.0 - 1.0)
    bpy.context.scene.cycles.denoising_diffuse_direct_threshold = noise_threshold

    if use_denoise == True:
        print("Denoising enabled")

        if dn_alg == "OPTIX" and use_gpu:
            bpy.context.scene.cycles.denoiser = 'OPTIX'
            print("Denoiser set to:", bpy.context.scene.cycles.denoiser)
        else:
            print("Using OPENIMAGEDENOISE as denoiser.")
            bpy.context.scene.cycles.denoiser = 'OPENIMAGEDENOISE'
            print("Denoiser set to:", bpy.context.scene.cycles.denoiser)
    else:
        print("Denoising disabled")
        bpy.context.scene.cycles.use_denoising = False


# Caustics
def configure_cycles_caustics(caustics_fg, caustics_reflective, caustics_refractive):
    print("Setting caustics")
    # Caustics
    bpy.context.scene.cycles.blur_glossy = caustics_fg # REVIEW
    bpy.context.scene.cycles.caustics_reflective = caustics_reflective
    bpy.context.scene.cycles.caustics_refractive = caustics_refractive
        
# Clamping
def configure_cycles_clamping(clamping_direct, clamping_indirect):
    print("Setting clamping")
    # Clamping
    bpy.context.scene.cycles.sample_clamp_direct = clamping_direct
    bpy.context.scene.cycles.sample_clamp_indirect = clamping_indirect
        
# Bounces
def configure_cycles_bounces(max_bounces_diffuse, max_bounces_glossy, max_bounces, max_bounces_transmission, max_bounces_transparent, max_bounces_volume):
    print("Setting bounces")
    # Bounces
    bpy.context.scene.cycles.max_bounces = max_bounces
    bpy.context.scene.cycles.diffuse_bounces = max_bounces_diffuse
    bpy.context.scene.cycles.glossy_bounces = max_bounces_glossy
    bpy.context.scene.cycles.transmission_bounces = max_bounces_transmission
    bpy.context.scene.cycles.transparent_max_bounces = max_bounces_transparent
    bpy.context.scene.cycles.volume_bounces = max_bounces_volume
