import { RemovalPolicy } from 'aws-cdk-lib';
import { ManagedEc2EcsComputeEnvironment, AllocationStrategy } from 'aws-cdk-lib/aws-batch';
import { ISecurityGroup, IVpc, InstanceType, ISubnet } from 'aws-cdk-lib/aws-ec2';
import { ManagedPolicy, Role, ServicePrincipal } from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';
import { v4 as uuidv4 } from 'uuid';

export function createG5ComputeEnvironments(
    scope: Construct,
    vpc: IVpc,
    sg: ISecurityGroup,
    allSubnets: ISubnet[],
    s3Policy: ManagedPolicy,
    batchPolicy: ManagedPolicy,
    parsedMaxvCpus: { 
        onDemandGPU: number, 
        spotGPU: number
    },
    parsedSpotBidPercentage: { spotGPU: number }
) {
    // Environment On-Demand G5
    const computeEnvOnDemandG5 = new ManagedEc2EcsComputeEnvironment(scope, 'ComputeEnvOnDemandGPU-' + uuidv4(), {
        instanceRole: new Role(scope, 'ComputeEnvironmentRoleOnDemandGPU', {
            assumedBy: new ServicePrincipal('ec2.amazonaws.com'),
            managedPolicies: [ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonEC2ContainerServiceforEC2Role'), s3Policy, batchPolicy],
        }),
        vpc,
        vpcSubnets: { subnets: allSubnets },
        computeEnvironmentName: 'ComputeEnvOnDemandGPU-' + uuidv4(),
        securityGroups: [sg],
        minvCpus: 0,
        maxvCpus: parsedMaxvCpus.onDemandGPU,
        enabled: true,
        instanceTypes: [
            new InstanceType('g5')
        ],
    });
    computeEnvOnDemandG5.applyRemovalPolicy(RemovalPolicy.DESTROY);

    // Environment Spot G5
    const computeEnvSpotG5 = new ManagedEc2EcsComputeEnvironment(scope, 'ComputeEnvSpotGPU-' + uuidv4(), {
        instanceRole: new Role(scope, 'ComputeEnvironmentRoleSpotGPU', {
            assumedBy: new ServicePrincipal('ec2.amazonaws.com'),
            managedPolicies: [ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonEC2ContainerServiceforEC2Role'), s3Policy, batchPolicy],
        }),
        vpc,
        vpcSubnets: { subnets: allSubnets },
        securityGroups: [sg],
        minvCpus: 0,
        maxvCpus: parsedMaxvCpus.spotGPU,
        enabled: true,
        computeEnvironmentName: 'ComputeEnvSpotGPU-' + uuidv4(),
        spot: true,
        spotBidPercentage: parsedSpotBidPercentage.spotGPU,
        allocationStrategy: AllocationStrategy.SPOT_CAPACITY_OPTIMIZED,
        instanceTypes: [
            new InstanceType('g5')
        ],
    });
    computeEnvSpotG5.applyRemovalPolicy(RemovalPolicy.DESTROY);

    return { computeEnvOnDemandG5, computeEnvSpotG5 };
}
