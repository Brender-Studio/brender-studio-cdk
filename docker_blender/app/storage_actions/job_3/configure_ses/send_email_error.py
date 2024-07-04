import boto3
import json
from datetime import datetime, timedelta
from urllib.parse import quote_plus
from configure_ses.batch_details import get_batch_job_info

def send_render_error_email(ses_config, render_details, job_id, region, job_array_size):
    """
    Send an email with the specified SES configuration and render details if render fails
    """
    try:
        ses = boto3.client('ses', region_name=ses_config['region'])
        source_email = ses_config['source_email']
        destination_email = ses_config['destination_email']
        render_error_template_name = ses_config['render_error_template_name']

        # Render details
        project_name = render_details['project_name']
        resolution = render_details['resolution']
        scene_name = render_details['scene_name']
        layer_name = render_details['layer_name']
        camera_name = render_details['camera_name']
        samples = render_details['samples']
        engine = render_details['engine']
        render_type = render_details['render_type']

        runtime, status = get_batch_job_info(job_id, region, render_details, job_array_size)
        print(f"Runtime: {runtime}")
        print(f"Status: {status}")

        # Manejar el caso donde status es None
        if status is None:
            status_reason = "N/A"
            log_stream_name = "N/A"
        else:
            # Obtener la razón del estado
            status_reason = status.get('reason', "N/A")
            log_stream_name = status.get('log_stream_name', "N/A")

        # Transformar las barras diagonales en el formato adecuado para la URL, manejar el caso "N/A"
        if log_stream_name == "N/A":
            log_stream_name_encoded = "N/A"
            log_link = f"https://{ses_config['region']}.console.aws.amazon.com/cloudwatch/home?region={ses_config['region']}#logsV2:log-groups/log-group/%2Faws%2Fbatch%2Fjob"
        else:
            log_stream_name_encoded = quote_plus(log_stream_name)
            # Construir la URL con el log_stream_name codificado
            log_link = f"https://{ses_config['region']}.console.aws.amazon.com/cloudwatch/home?region={ses_config['region']}#logsV2:log-groups/log-group/%2Faws%2Fbatch%2Fjob/log-events/{log_stream_name_encoded}"

        # Definir los parámetros de la plantilla
        template_data = {
            'project_name': project_name,
            'reason_message': status_reason,
            'log_link': log_link,
            'resolution': resolution,
            'scene_name': scene_name,
            'layer_name': layer_name,
            'camera_name': camera_name,
            'samples': samples,
            'engine': engine,
            'render_type': render_type,
            'execution_time': runtime,
            'current_year': str(datetime.now().year),
        }

        print("template_data:", template_data)

        # Enviar el correo electrónico utilizando la plantilla
        response = ses.send_templated_email(
            Source=source_email,
            Destination={'ToAddresses': [destination_email]},
            Template=render_error_template_name,
            TemplateData=json.dumps(template_data)
        )

        print("Correo electrónico enviado con éxito!")
        print("ID de mensaje:", response['MessageId'])

        return response

    except Exception as e:
        # Capturar cualquier excepción y mostrar un mensaje de error
        print("Error al enviar el correo electrónico:", e)
        return None