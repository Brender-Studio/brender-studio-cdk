import { RemovalPolicy } from 'aws-cdk-lib';
import { ManagedEc2EcsComputeEnvironment, AllocationStrategy } from 'aws-cdk-lib/aws-batch';
import { ISecurityGroup, ISubnet, IVpc, SubnetSelection } from 'aws-cdk-lib/aws-ec2';
import { ManagedPolicy, Role, ServicePrincipal } from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';
import { v4 as uuidv4 } from 'uuid';

export function createCpuComputeEnvironments(
    scope: Construct,
    vpc: IVpc,
    sg: ISecurityGroup,
    allSubnets: ISubnet[],
    s3Policy: ManagedPolicy,
    batchPolicy: ManagedPolicy,
    parsedMaxvCpus: { onDemandCPU: number, spotCPU: number },
    parsedSpotBidPercentage: { spotCPU: number }
) {
    // Environment On-Demand CPU
    const computeEnvOnDemandCPU = new ManagedEc2EcsComputeEnvironment(scope, 'ComputeEnvOnDemandCPU-' + uuidv4(), {
        useOptimalInstanceClasses: true,
        instanceRole: new Role(scope, 'ComputeEnvironmentRoleOnDemandCPU', {
            assumedBy: new ServicePrincipal('ec2.amazonaws.com'),
            managedPolicies: [ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonEC2ContainerServiceforEC2Role'), s3Policy, batchPolicy],
        }),
        vpc,
        vpcSubnets: { subnets: allSubnets },
        computeEnvironmentName: 'ComputeEnvOnDemandCPU-' + uuidv4(),
        securityGroups: [sg],
        minvCpus: 0,
        maxvCpus: parsedMaxvCpus.onDemandCPU,
        enabled: true,
    });
    computeEnvOnDemandCPU.applyRemovalPolicy(RemovalPolicy.DESTROY);

    // Environment Spot CPU
    const computeEnvSpotCPU = new ManagedEc2EcsComputeEnvironment(scope, 'ComputeEnvSpotCPU-' + uuidv4(), {
        useOptimalInstanceClasses: true,
        instanceRole: new Role(scope, 'ComputeEnvironmentRoleSpotCPU', {
            assumedBy: new ServicePrincipal('ec2.amazonaws.com'),
            managedPolicies: [ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonEC2ContainerServiceforEC2Role'), s3Policy, batchPolicy],
        }),
        vpc,
        vpcSubnets: { subnets: allSubnets },
        securityGroups: [sg],
        minvCpus: 0,
        maxvCpus: parsedMaxvCpus.spotCPU,
        enabled: true,
        computeEnvironmentName: 'ComputeEnvSpotCPU-' + uuidv4(),
        spot: true,
        spotBidPercentage: parsedSpotBidPercentage.spotCPU,
        allocationStrategy: AllocationStrategy.SPOT_CAPACITY_OPTIMIZED,
    });
    computeEnvSpotCPU.applyRemovalPolicy(RemovalPolicy.DESTROY);

    return { computeEnvOnDemandCPU, computeEnvSpotCPU };
}
