import os
from PIL import Image
from wand.image import Image as WandImage


def convert_to_png(image_path):
    # Nombre del archivo de salida
    output_path = os.path.splitext(image_path)[0] + '.png'
    # Abrir la imagen con wand
    with WandImage(filename=image_path) as img:
        # Convertir a PNG
        img.format = 'png'
        img.save(filename=output_path)

    return output_path


def generate_thumbnail(render_output_path, thumbnail_output_path):
    # Crear thumbnail de la primera imagen que haya en output, guardarlo en la misma ruta de files (efs project path env) como: _thumbnail.png
    print("Creating thumbnail...")
    # Encontrar la primera imagen en la carpeta de output
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

    # Abrir la imagen y crear el thumbnail
    try:
        if image_path.lower().endswith(('.bmp', '.iris', '.jpg', '.jpeg', '.jp2', '.tga', '.dpx', '.exr', '.hdr', '.tif', 'tiff', '.webp', '.cin')):
            # Convertir a PNG utilizando ImageMagick (wand)
            png_path = convert_to_png(image_path)
            # Abrir la imagen convertida
            image = Image.open(png_path)
            # Eliminar la imagen convertida
            os.remove(png_path) 
        else:
            image = Image.open(image_path)
    except Exception as e:
        raise RuntimeError(f"Failed to open image: {e}")

    # Calcular las nuevas dimensiones manteniendo el aspect ratio
    width, height = image.size
    new_width = 500
    new_height = int((height / width) * new_width)

    # Redimensionar la imagen con las nuevas dimensiones
    thumbnail = image.resize((new_width, new_height))
    # Guardar el thumbnail
    thumbnail_path = os.path.join(thumbnail_output_path, '_thumbnail.png')
    thumbnail.save(thumbnail_path)
    print(f"Thumbnail created: {thumbnail_path}")
    return thumbnail_path
