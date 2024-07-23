# Brender Studio Docker Images

## Description

Brender Studio utilizes specialized Docker images that include Blender and all necessary dependencies for rendering. These images also contain the required logic to manage AWS Batch jobs. A key feature is that a single image can handle all types of jobs, greatly simplifying management and maintenance.

## AWS Batch Workflow

Brender Studio primarily uses AWS Batch to handle rendering projects. Each rendering job triggers three sequential jobs:

1. **Copy Project Files**: The first job copies Blender project files from Amazon S3 to the Elastic File System (EFS).
2. **Rendering**: The second job renders the Blender scene using the files stored in EFS.
3. **Upload and Notification**: The third job uploads the rendered images from EFS back to Amazon S3 and sends an email notification via Amazon SES to inform the user that rendering has completed.

Additionally, there's an auxiliary job responsible for mounting EFS and cleaning all its content, although this is not considered a primary job.

## Project Organization

The entry point of the Docker image is a script called `app.py`. This script orchestrates the job according to a JSON sent to the job container. This JSON contains job data sent from the Brender Studio frontend.

All logic is written in Python for simplicity and consistency, as Blender's API (bpy) is also in Python.

## Code Structure

The code is designed to be as modular as possible, branching according to received parameters:

```
app.py
├── render (render job)
├── render_python (custom Python render job)
└── storage actions
    ├── job_1 (s3_to_efs.py)
    ├── job_3 (efs_to_s3.py)
    └── job_4 (auxiliary job to delete EFS content)
```

## Dockerfile

The Dockerfile is based on an NVIDIA CUDA image and performs the following main actions:

1. Installs necessary dependencies.
2. Downloads and installs Blender.
3. Configures required environment variables.
4. Copies the application code to the container.
5. Sets the entry point to `app.py`.

## Execution

The `app.py` script determines the type of job to execute based on the `JOB_ACTION_TYPE` environment variable. It uses a `get_job_action_path` function to map the job type to the corresponding script:

```python
def get_job_action_path(job_action):
    script_paths = {
        "copy_efs": "/app/storage_actions/job_1/s3_to_efs.py",
        "upload_render_output": "/app/storage_actions/job_3/efs_to_s3.py",
        "remove_efs": "/app/storage_actions/job_4/remove_all_efs.py",
        "render": "/app/render/render_config.py",
        "custom_render_python": "/app/render_python/render_python.py"
    }
    return script_paths.get(job_action, None)
```

## Environment Variables

The main environment variables used are:

- `EFS_BLENDER_FOLDER_PATH`: Path to the projects directory in EFS.
- `BLENDER_EXECUTABLE`: Path to the Blender executable.
- `JOB_ACTION_TYPE`: Type of job to execute.

## Development Considerations

We recommend local testing with devcontainers. You can use the Visual Studio Code extension "Remote - Containers" to run the development container.

In this repository [brender-studio-devcontainer](https://github.com/Brender-Studio/brender-studio-devcontainer), you'll find an example of how to set up a devcontainer for working with Brender Studio.

The devcontainer attempts to replicate the production environment as faithfully as possible, facilitating development and debugging of issues.
