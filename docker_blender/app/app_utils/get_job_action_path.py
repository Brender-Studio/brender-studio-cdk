def get_job_action_path(job_action):
    script_paths = {
        "copy_efs": "/app/storage_actions/job_1/s3_to_efs.py",
        "upload_render_output": "/app/storage_actions/job_3/efs_to_s3.py",
        "remove_efs": "/app/storage_actions/job_4/remove_all_efs.py",
        "render": "/app/render/render_config.py",
        "custom_render_python": "/app/render_python/render_python.py"
    }
    return script_paths.get(job_action, None)