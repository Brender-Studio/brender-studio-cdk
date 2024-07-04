import boto3

def get_ec2_instance_details(job_id, region, job_array_size):
    # Inicializar los clientes de boto3
    batch_client = boto3.client('batch', region_name=region)
    ecs_client = boto3.client('ecs', region_name=region)
    ec2_client = boto3.client('ec2', region_name=region)

    try:
        # Construir el job_id correcto dependiendo de si es un array job o no
        if int(job_array_size) > 1:
            job_id = f"{job_id}:0"
        else:
            job_id = job_id

        # Paso 1: Obtener detalles del job
        job_details = batch_client.describe_jobs(jobs=[job_id])['jobs'][0]

        # Verificar si el trabajo tiene intentos (attempts)
        if not job_details['attempts']:
            raise Exception("El trabajo no tiene intentos, puede que no haya lanzado tareas ECS.")

        # Paso 2: Obtener el containerInstanceArn del job
        container_instance_arn = job_details['container']['containerInstanceArn']

        # Asegurarse de que hay un containerInstanceArn
        if not container_instance_arn:
            raise Exception("No se encontró containerInstanceArn para el job")

        # Paso 3: Extraer el nombre del clúster desde el containerInstanceArn
        cluster_name = container_instance_arn.split("/")[-2]

        # Paso 4: Obtener detalles de la instancia del contenedor
        container_instances = ecs_client.describe_container_instances(
            cluster=cluster_name,
            containerInstances=[container_instance_arn]
        )['containerInstances']

        # Asegurarse de que hay instancias del contenedor
        if not container_instances:
            raise Exception("No se encontraron instancias del contenedor")

        # Paso 5: Obtener el ID de la instancia EC2 desde la instancia del contenedor
        ec2_instance_id = container_instances[0]['ec2InstanceId']

        # Paso 6: Obtener detalles de la instancia EC2
        ec2_instances = ec2_client.describe_instances(InstanceIds=[ec2_instance_id])

        for reservation in ec2_instances['Reservations']:
            for instance in reservation['Instances']:
                # Obtener la familia y tipo de instancia EC2
                instance_type = instance['InstanceType']
                instance_family = instance_type.split('.')[0]

                # Obtener el ciclo de vida de la instancia (Spot u On-Demand)
                instance_lifecycle = instance.get('InstanceLifecycle')

                # Verificar explícitamente si es Spot
                if instance_lifecycle == 'spot':
                    instance_lifecycle = 'Spot'
                else:
                    # Verificar la especificación de la reserva de capacidad
                    reservation_spec = instance.get('CapacityReservationSpecification', {})
                    if reservation_spec.get('CapacityReservationPreference') == 'open':
                        instance_lifecycle = 'On-Demand'
                    elif reservation_spec.get('CapacityReservationPreference') == 'capacityReservation':
                        instance_lifecycle = 'Spot con reserva de capacidad'
                    else:
                        instance_lifecycle = 'On-Demand'

                # Retornar los detalles requeridos
                return {
                    'InstanceType': instance_type,
                    'InstanceFamily': instance_family,
                    'InstanceLifecycle': instance_lifecycle
                }

    except Exception as e:
        print(f"Error al obtener detalles de la instancia EC2: {str(e)}")
        return None