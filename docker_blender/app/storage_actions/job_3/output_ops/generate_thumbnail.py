import os
from PIL import Image
from wand.image import Image as WandImage


def convert_to_png(image_path):
    # Name of the output file
    output_path = os.path.splitext(image_path)[0] + '.png'
    # Open the image with Wand
    with WandImage(filename=image_path) as img:
        # Convert the image to PNG
        img.format = 'png'
        img.save(filename=output_path)

    return output_path


def generate_thumbnail(render_output_path, thumbnail_output_path):
    # Create a thumbnail of the first image found in the output folder and save it in the same folder as _thumbnail.png 
    print("Creating thumbnail...")
    # Find the first image in the render output folder
    image_path = None
    for root, dirs, files in os.walk(render_output_path):
        for file in files:
            if file.endswith(('.bmp', '.iris', '.png', '.jpg', '.jpeg', '.jp2', '.tga', '.dpx', '.exr', '.hdr', '.tif', 'tiff', '.webp', '.cin')):
                image_path = os.path.join(root, file)
                break
        if image_path:
            break
    if not image_path:
        raise FileNotFoundError(f"No image found in {render_output_path}")

    # Open the image 
    try:
        if image_path.lower().endswith(('.bmp', '.iris', '.jpg', '.jpeg', '.jp2', '.tga', '.dpx', '.exr', '.hdr', '.tif', 'tiff', '.webp', '.cin')):
            # Convert to PNG using ImageMagick (wand)
            png_path = convert_to_png(image_path)
            # Open the converted image
            image = Image.open(png_path)
            # Remove the converted image
            os.remove(png_path) 
        else:
            image = Image.open(image_path)
    except Exception as e:
        raise RuntimeError(f"Failed to open image: {e}")

    # Calculate the new dimensions
    width, height = image.size
    new_width = 500
    new_height = int((height / width) * new_width)

    # Create the thumbnail 
    thumbnail = image.resize((new_width, new_height))
    # Save the thumbnail
    thumbnail_path = os.path.join(thumbnail_output_path, '_thumbnail.png')
    thumbnail.save(thumbnail_path)
    print(f"Thumbnail created: {thumbnail_path}")
    return thumbnail_path
