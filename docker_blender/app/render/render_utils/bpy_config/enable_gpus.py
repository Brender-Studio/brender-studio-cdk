import bpy

def enable_gpus(device_type, use_cpus):
    preferences = bpy.context.preferences
    cycles_preferences = preferences.addons["cycles"].preferences
    cycles_preferences.refresh_devices()
    devices = cycles_preferences.devices

    if not devices:
            raise RuntimeError("Unsupported device type")

    activated_gpus = []
    for device in devices:
            if device.type == "CPU":
                device.use = use_cpus
                print('activated cpu', device.name)
            else:
                device.use = True
                activated_gpus.append(device.name)
                print('activated gpu', device.name)

    cycles_preferences.compute_device_type = device_type

    for scene in bpy.data.scenes:
            scene.cycles.device = "GPU"
        #     scene.cycles.use_denoising = True

    return activated_gpus