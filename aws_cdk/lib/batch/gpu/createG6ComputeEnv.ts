import { RemovalPolicy } from 'aws-cdk-lib';
import { ManagedEc2EcsComputeEnvironment, AllocationStrategy } from 'aws-cdk-lib/aws-batch';
import { ISecurityGroup, IVpc, SubnetSelection, InstanceType, ISubnet } from 'aws-cdk-lib/aws-ec2';
import { ManagedPolicy, Role, ServicePrincipal } from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';
import { v4 as uuidv4 } from 'uuid';

export function createG6ComputeEnvironments(
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
    // Environment On-Demand G6
    const computeEnvOnDemandG6 = new ManagedEc2EcsComputeEnvironment(scope, 'ComputeEnvOnDemandGPUG6-' + uuidv4(), {
        instanceRole: new Role(scope, 'ComputeEnvironmentRoleOnDemandG6', {
            assumedBy: new ServicePrincipal('ec2.amazonaws.com'),
            managedPolicies: [ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonEC2ContainerServiceforEC2Role'), s3Policy, batchPolicy],
        }),
        vpc,
        vpcSubnets: { subnets: allSubnets },
        computeEnvironmentName: 'ComputeEnvOnDemandGPUG6-' + uuidv4(),
        securityGroups: [sg],
        minvCpus: 0,
        maxvCpus: parsedMaxvCpus.onDemandGPU,
        enabled: true,
        instanceTypes: [new InstanceType('g6'),],
    });
    computeEnvOnDemandG6.applyRemovalPolicy(RemovalPolicy.DESTROY);

    // Environment Spot G6
    const computeEnvSpotG6 = new ManagedEc2EcsComputeEnvironment(scope, 'ComputeEnvSpotGPUG6-' + uuidv4(), {
        instanceRole: new Role(scope, 'ComputeEnvironmentRoleSpotG6', {
            assumedBy: new ServicePrincipal('ec2.amazonaws.com'),
            managedPolicies: [ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonEC2ContainerServiceforEC2Role'), s3Policy, batchPolicy],
        }),
        vpc,
        vpcSubnets: { subnets: allSubnets },
        securityGroups: [sg],
        minvCpus: 0,
        maxvCpus: parsedMaxvCpus.spotGPU,
        enabled: true,
        computeEnvironmentName: 'ComputeEnvSpotGPUG6-' + uuidv4(),
        spot: true,
        spotBidPercentage: parsedSpotBidPercentage.spotGPU,
        allocationStrategy: AllocationStrategy.SPOT_CAPACITY_OPTIMIZED,
        instanceTypes: [new InstanceType('g6'),],
    });
    computeEnvSpotG6.applyRemovalPolicy(RemovalPolicy.DESTROY);

    return { computeEnvOnDemandG6, computeEnvSpotG6 };
}
