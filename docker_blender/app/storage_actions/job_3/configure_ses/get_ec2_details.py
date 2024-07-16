import boto3

def get_ec2_instance_details(job_id, region, job_array_size):
    batch_client = boto3.client('batch', region_name=region)
    ecs_client = boto3.client('ecs', region_name=region)
    ec2_client = boto3.client('ec2', region_name=region)

    try:
        # Build the job ID for the AWS Batch job
        if int(job_array_size) > 1:
            job_id = f"{job_id}:0"
        else:
            job_id = job_id

        # Step 1: Get job details from AWS Batch
        job_details = batch_client.describe_jobs(jobs=[job_id])['jobs'][0]

        # Verify if the job has attempts
        if not job_details['attempts']:
            raise Exception("Job attempts not found")

        # Step 2: Extract the container instance ARN from the job details
        container_instance_arn = job_details['container']['containerInstanceArn']

        # Verify if the container instance ARN is present
        if not container_instance_arn:
            raise Exception("Container instance ARN not found")

        # Step 3: Extract the cluster name from the container instance ARN
        cluster_name = container_instance_arn.split("/")[-2]

        # Step 4: Get container instance details from Amazon ECS
        container_instances = ecs_client.describe_container_instances(
            cluster=cluster_name,
            containerInstances=[container_instance_arn]
        )['containerInstances']

        # Verify if container instances are found
        if not container_instances:
            raise Exception("Container instances not found")

        # Step 5: Extract the EC2 instance ID from the container instance details
        ec2_instance_id = container_instances[0]['ec2InstanceId']

        # Step 6: Get EC2 instance details from Amazon EC2
        ec2_instances = ec2_client.describe_instances(InstanceIds=[ec2_instance_id])

        for reservation in ec2_instances['Reservations']:
            for instance in reservation['Instances']:
                # Get the instance type and family
                instance_type = instance['InstanceType']
                instance_family = instance_type.split('.')[0]

                # Get the instance lifecycle (On-Demand, Spot, or Spot with Capacity Reservation)
                instance_lifecycle = instance.get('InstanceLifecycle')

                # Check if the instance is a Spot instance
                if instance_lifecycle == 'spot':
                    instance_lifecycle = 'Spot'
                else:
                    # Check if the instance has a Capacity Reservation
                    reservation_spec = instance.get('CapacityReservationSpecification', {})
                    if reservation_spec.get('CapacityReservationPreference') == 'open':
                        instance_lifecycle = 'On-Demand'
                    elif reservation_spec.get('CapacityReservationPreference') == 'capacityReservation':
                        instance_lifecycle = 'Spot con reserva de capacidad'
                    else:
                        instance_lifecycle = 'On-Demand'

                return {
                    'InstanceType': instance_type,
                    'InstanceFamily': instance_family,
                    'InstanceLifecycle': instance_lifecycle
                }

    except Exception as e:
        print(f"Error getting EC2 details: {str(e)}")
        return None