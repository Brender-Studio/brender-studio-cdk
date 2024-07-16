import shutil
import os

def output_to_zip(render_output_path):
    # Compress the /output folder into /output/output.zip 
    print("Creating output.zip...")
    zip_path = shutil.make_archive(render_output_path, 'zip', render_output_path)
    print(f"output.zip created: {zip_path}")
    
    # Get the size of the output.zip file
    zip_size = os.path.getsize(zip_path)
    print(f"Size of output.zip: {zip_size} bytes")

    return zip_path, zip_size