import os
from PIL import Image, ImageDraw, ImageFont

def create_placeholder_image(output_path, width=300, height=100, text="Preview Not Available"):
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Optional: Set a custom font if available
    try:
        font = ImageFont.truetype("arial.ttf", 72)
    except IOError:
        font = ImageFont.load_default()

    textwidth, textheight = draw.textsize(text, font)
    x = (width - textwidth) / 2
    y = (height - textheight) / 2
    draw.text((x, y), text, fill=(0, 0, 0), font=font)

    image.save(output_path)
    return output_path

def convert_to_png(image_path):
    try:
        from wand.image import Image as WandImage
        output_path = os.path.splitext(image_path)[0] + '.png'
        with WandImage(filename=image_path) as img:
            img.format = 'png'
            img.save(filename=output_path)
        return output_path
    except Exception:
        # If the conversion fails, return None
        return None

def generate_thumbnail(render_output_path, thumbnail_output_path):
    print("Creating thumbnail...")
    image_path = None
    for root, dirs, files in os.walk(render_output_path):
        for file in files:
            if file.lower().endswith(('.bmp', '.iris', '.png', '.jpg', '.jpeg', '.jp2', '.tga', '.dpx', '.exr', '.hdr', '.tif', 'tiff', '.webp', '.cin')):
                image_path = os.path.join(root, file)
                break
        if image_path:
            break
    if not image_path:
        raise FileNotFoundError(f"No image found in {render_output_path}")

    # Determine if a placeholder image should be created
    if image_path.lower().endswith(('.exr', '.hdr')):
        print(f"Generating placeholder image for {image_path}")
        placeholder_path = os.path.join(thumbnail_output_path, '_thumbnail.png')
        return create_placeholder_image(placeholder_path)

    try:
        png_path = convert_to_png(image_path)
        if png_path is None:
            raise Exception("Failed to convert image.")
        image = Image.open(png_path)
        os.remove(png_path)
    except Exception as e:
        print(f"Error: {e}")
        # Create a placeholder image if conversion fails
        placeholder_path = os.path.join(thumbnail_output_path, '_thumbnail.png')
        return create_placeholder_image(placeholder_path)

    width, height = image.size
    new_width = 500
    new_height = int((height / width) * new_width)

    thumbnail = image.resize((new_width, new_height))
    thumbnail_path = os.path.join(thumbnail_output_path, '_thumbnail.png')
    thumbnail.save(thumbnail_path)
    print(f"Thumbnail created: {thumbnail_path}")
    return thumbnail_path
