import boto3
from datetime import datetime, timedelta, timezone

def get_batch_job_info(job_id, region, render_details, job_array_size):
    try:
        # Crear cliente de AWS Batch
        batch_client = boto3.client('batch', region_name=region)

        # Render type Animation or Still
        render_type = render_details['render_type']
        print(f"Render Type: {render_type}")

        if int(job_array_size) > 1:
            job_id = f"{job_id}:0"
        else:
            job_id = job_id

        # Obtener detalles del trabajo
        response = batch_client.describe_jobs(jobs=[job_id])

        # Verificar si se recibió una respuesta válida
        if 'jobs' not in response or len(response['jobs']) == 0:
            raise ValueError(f"No se encontraron detalles para el trabajo con ID {job_id}")

        # Extraer información sobre el trabajo de AWS Batch
        job_info = response['jobs'][0]

        # Inicializar variables para el tiempo de inicio y finalización
        start_time_ms = None
        end_time_ms = None

        # Verificar si se proporcionaron las claves necesarias para calcular el tiempo de ejecución
        if 'startedAt' in job_info and 'stoppedAt' in job_info:
            start_time_ms = job_info['startedAt']
            end_time_ms = job_info['stoppedAt']
        elif 'createdAt' in job_info:
            created_at_ms = job_info['createdAt']
            current_time_ms = datetime.now().timestamp() * 1000
            start_time_ms = created_at_ms
            end_time_ms = current_time_ms
        else:
            raise ValueError("La respuesta de AWS Batch no contiene la información necesaria")

        # Calcular tiempo de ejecución si se proporcionaron los tiempos de inicio y finalización
        if start_time_ms is not None and end_time_ms is not None:
            runtime_formatted = calculate_runtime(start_time_ms, end_time_ms)
        else:
            runtime_formatted = "Tiempo de ejecución no disponible"

        # Obtener información de estado del trabajo
        status_info = get_status_info(job_info)

        return runtime_formatted, status_info
    
    except Exception as e:
        print(f"Ocurrió un error al obtener detalles del trabajo: {e}")
        return None, None

def calculate_runtime(start_time_ms, end_time_ms):
    # Convertir de milisegundos a segundos
    start_time_seconds = start_time_ms / 1000
    end_time_seconds = end_time_ms / 1000

    # Convertir a objetos datetime en UTC
    start_datetime = datetime.fromtimestamp(start_time_seconds, tz=timezone.utc)
    end_datetime = datetime.fromtimestamp(end_time_seconds, tz=timezone.utc)

    # Calcular tiempo de ejecución
    runtime_seconds = (end_datetime - start_datetime).total_seconds()

    # Obtener horas, minutos y segundos
    hours, remainder = divmod(runtime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Formatear el tiempo de ejecución como HH:MM:SS
    runtime_formatted = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

    return runtime_formatted

def get_status_info(job_info):
    try:
        # Obtener información de estado del trabajo
        reason = job_info['attempts'][0]['container']['reason']
        log_stream_name = job_info['attempts'][0]['container']['logStreamName']
        status_info = {
            "reason": reason,
            "log_stream_name": log_stream_name
        } 

        # si no hay información de estado, devolver un mensaje predeterminado
        if reason is None:
            status_info['reason'] = "Information not available for this job."
        if log_stream_name is None:
            status_info['log_stream_name'] = "Name not available for this job."


        return status_info
    except Exception as e:
        print(f"Ocurrió un error al obtener la información de estado del trabajo: {e}")
        return None