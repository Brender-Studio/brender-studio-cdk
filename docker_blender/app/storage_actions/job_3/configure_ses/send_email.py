import boto3
import json
from datetime import datetime, timedelta
from configure_ses.presigned_urls import generate_presigned_urls
from configure_ses.batch_details import get_batch_job_info
from configure_ses.get_ec2_details import get_ec2_instance_details

def convert_bytes_to_mb(bytes_size):
    """
    Convierte el tamaño de bytes a megabytes (MB)
    """
    mb_size = bytes_size / (1024 * 1024)
    return mb_size

def convert_bytes_to_gb(bytes_size):
    """
    Convierte el tamaño de bytes a gigabytes (GB)
    """
    gb_size = bytes_size / (1024 * 1024 * 1024)
    return gb_size

def total_seconds(time_str):
    """
    Convierte una cadena de tiempo en formato HH:MM:SS a segundos totales
    """
    if ':' in time_str:
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s
    else:
        return int(time_str) * 60  # Si es un número en minutos, convertir a segundos totales

def format_runtime(seconds):
    """
    Formatea la cantidad de segundos en el formato HH:MM:SS
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def format_expiration_datetime(expiration_datetime):
    """
    Formatea la fecha y hora de expiración en el formato deseado
    """
    # Definir los nombres de los meses en inglés
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    # Obtener el día, mes, año y hora de la fecha de expiración
    day = expiration_datetime.day
    month = months[expiration_datetime.month - 1]
    year = expiration_datetime.year
    hour = expiration_datetime.hour
    minute = expiration_datetime.minute
    
    # Formatear la fecha y hora en el formato deseado
    formatted_datetime = f"{day} {month}, {year} at {hour:02d}:{minute:02d}"
    
    return formatted_datetime

def send_render_ok_email(job_id, ses_config, render_details, zip_size, job_array_size, region):
    """
    Send an email with the specified SES configuration and render details
    """
    try:
        ses = boto3.client('ses', region_name=ses_config['region'])
        source_email = ses_config['source_email']
        destination_email = ses_config['destination_email']
        render_ok_template_name = ses_config['render_ok_template_name']

        # Render details
        project_name = render_details['project_name']
        resolution = render_details['resolution']
        scene_name = render_details['scene_name']
        layer_name = render_details['layer_name']
        camera_name = render_details['camera_name']
        samples = render_details['samples']
        engine = render_details['engine']
        render_type = render_details['render_type']
        active_frame = render_details['active_frame']
        frame_range = render_details['frame_range']
        job_array_size = render_details['job_array_size']

        thumbnail_presigned_url, output_zip_presigned_url = generate_presigned_urls(region)
        print(f"Thumbnail presigned url: {thumbnail_presigned_url}")

        runtime, _ = get_batch_job_info(job_id, region, render_details, job_array_size)

        if runtime is None:
            runtime = "N/A"
        print(f"Runtime minutes: {runtime}")


        ec2_instance_details = get_ec2_instance_details(job_id, region, job_array_size)
        print(f"EC2 Instance Details: {ec2_instance_details}")

        # Verificar si ec2_instance_details es None y asignar valores predeterminados
        if ec2_instance_details is None:
            instance_type = 'N/A'
            instance_lifecycle = 'N/A'
        else:
            # extraer el tipo de instancia, familia, si es spot o on-demand
            instance_type = ec2_instance_details.get('InstanceType', 'N/A')
            instance_lifecycle = ec2_instance_details.get('InstanceLifecycle', 'N/A')

        print(f"Instance Type: {instance_type}")
        print(f"Instance Lifecycle: {instance_lifecycle}")

        ## Rendering time calculated: array job x runtime
        if int(job_array_size) > 0:
            total_seconds_runtime = total_seconds(runtime) * int(job_array_size)  # Convertir a segundos totales
            total_runtime_formatted = format_runtime(total_seconds_runtime)
        else:
            total_runtime_formatted = runtime 

        if zip_size > 1024 * 1024 * 1024:  # Si el tamaño es mayor a 1 GB
            object_size_str = f"{convert_bytes_to_gb(zip_size):.2f} GB"
        else:
            object_size_str = f"{convert_bytes_to_mb(zip_size):.2f} MB"

        expiration_datetime = datetime.now() + timedelta(hours=12)

        # Definir los parámetros de la plantilla
        template_data = {
            'project_name': project_name,
            'resolution': resolution,
            'scene_name': scene_name,
            'layer_name': layer_name,
            'camera_name': camera_name,
            'samples': samples,
            'engine': engine,
            'render_type': render_type,
            'thumbnail_url': thumbnail_presigned_url,
            # 'alternate_download_url': output_zip_presigned_url,
            'brender_download_url': output_zip_presigned_url,
            'execution_time': runtime,
            'object_size': object_size_str,
            'current_year': str(datetime.now().year),
            'expiration_time': format_expiration_datetime(expiration_datetime),
            'active_frame': active_frame,
            'frame_range': frame_range,
            'job_array_size': job_array_size,
            'queue_type': instance_lifecycle,
            'aprox_execution_time': total_runtime_formatted,
            'instance_type': instance_type,
            # url vantage: https://instances.vantage.sh/aws/ec2/g5.xlarge?region=ap-northeast-1&os=linux&cost_duration=hourly&reserved_term=Standard.noUpfront
            'instance_pricing_url': f"https://instances.vantage.sh/aws/ec2/{instance_type}?region={region}&os=linux&cost_duration=hourly&reserved_term=Standard.noUpfront"
        }

        # Enviar el correo electrónico utilizando la plantilla
        response = ses.send_templated_email(
            Source=source_email,
            Destination={'ToAddresses': [destination_email]},
            Template=render_ok_template_name,
            TemplateData=json.dumps(template_data)
        )

        print("Correo electrónico enviado con éxito!")
        print("ID de mensaje:", response['MessageId'])

        return response

    except Exception as e:
        # Capturar cualquier excepción y mostrar un mensaje de error
        print("Error al enviar el correo electrónico:", e)
        return None
