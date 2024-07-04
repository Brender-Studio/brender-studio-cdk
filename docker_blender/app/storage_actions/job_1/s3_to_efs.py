import os
import boto3
import tarfile


bucket_name = os.environ['BUCKET_NAME']
bucket_key = os.environ['BUCKET_KEY']
efs_path = os.environ['EFS_BLENDER_FOLDER_PATH']


print(bucket_name)
print(bucket_key)
print(efs_path)

print(f"Copying project folder from S3: {bucket_name}/{bucket_key}")


s3_client = boto3.client('s3')

try:
    # Listar los objetos en el bucket/key
    response = s3_client.list_objects(Bucket=bucket_name, Prefix=bucket_key)

    # Obtener la lista de objetos
    objects = response.get('Contents', [])

    # Copiar cada objeto a la carpeta de destino de manera recursiva
    for obj in objects:
        obj_key = obj['Key']
        dest_path = os.path.join(efs_path, obj_key)

        print(f"Copying {obj_key} to {dest_path}")

        # Ruta de la carpeta de destino para la extracción
        extract_folder = os.path.splitext(os.path.basename(dest_path))[0]

        # Crear la ruta completa para la extracción
        extract_path = os.path.join(efs_path, os.path.dirname(obj_key))

        # Si la carpeta de extracción no existe, créala
        os.makedirs(extract_path, exist_ok=True)

        # Descargar el archivo desde S3
        s3_client.download_file(bucket_name, obj_key, dest_path)

        # Verificar si el archivo es un .tar.gz válido
        if obj_key.endswith('.tar.gz'):
            try:
                # Intentar abrir el archivo como un archivo tar.gz
                with tarfile.open(dest_path, mode="r:gz") as tar:
                    # Si no hay errores al abrirlo, proceder con la extracción
                    print(f"Extracting {obj_key} to {extract_path}")
                    tar.extractall(path=extract_path)
            except tarfile.ReadError:
                # Si hay errores al abrir el archivo, mostrar un mensaje de error
                print(f"Error: {obj_key} is not a valid tar.gz file")
        elif obj_key.endswith('.blend'):
            # Si el archivo es un .blend, copiarlo directamente
            print(f"{obj_key} is a .blend file, copying directly")
            os.rename(dest_path, os.path.join(extract_path, os.path.basename(dest_path)))
            print(f"{obj_key} copied to {extract_path}")
        else:
            print(f"{obj_key} is not a .tar.gz or .blend file, ignoring")
       

    print(f"Project folder copied to {efs_path}")
except Exception as e:
    print(f"Error: {e}")