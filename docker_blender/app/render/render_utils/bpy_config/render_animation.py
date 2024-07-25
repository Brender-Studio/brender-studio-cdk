import bpy
import os

output_path = os.environ.get('EFS_BLENDER_OUTPUT_FOLDER_PATH')
array_size = os.environ.get('AWS_BATCH_JOB_ARRAY_SIZE', '1')  
job_index = os.environ.get('AWS_BATCH_JOB_ARRAY_INDEX', '0')

def calculate_frame_chunk(array_size, job_index, start_frame, end_frame, frame_step):
    start_frame = int(start_frame)
    end_frame = int(end_frame)
    frame_step = int(frame_step)
    array_size = int(array_size)
    job_index = int(job_index)
    
    if array_size == 1:
        # If not running as an array job, render all frames
        return start_frame, end_frame, frame_step
    
    total_frames = end_frame - start_frame + 1
    frames_per_chunk = total_frames // array_size
    extra_frames = total_frames % array_size
    
    chunk_start = start_frame + job_index * frames_per_chunk + min(job_index, extra_frames)
    chunk_end = chunk_start + frames_per_chunk + (1 if job_index < extra_frames else 0) - 1 
    
    return chunk_start, chunk_end, frame_step

def render_animation(start_frame, end_frame, frame_step):
    start_frame, end_frame, frame_step = calculate_frame_chunk(array_size, job_index, start_frame, end_frame, frame_step)
    for frame in range(int(start_frame), int(end_frame) + 1, int(frame_step)): 
        bpy.context.scene.frame_set(frame)
        render_file_path = os.path.join(output_path, f"{frame:05d}")
        bpy.context.scene.render.filepath = render_file_path
        bpy.ops.render.render(write_still=True)