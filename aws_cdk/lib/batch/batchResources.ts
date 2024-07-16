import * as cdk from 'aws-cdk-lib';
import { EcsEc2ContainerDefinition, EcsJobDefinition, EcsVolume } from "aws-cdk-lib/aws-batch";
import { ISecurityGroup, IVpc, SubnetType } from "aws-cdk-lib/aws-ec2";
import { Repository } from "aws-cdk-lib/aws-ecr";
import { ContainerImage } from "aws-cdk-lib/aws-ecs";
import { IFileSystem } from 'aws-cdk-lib/aws-efs';
import { ServicePrincipal } from "aws-cdk-lib/aws-iam";
import { Construct } from "constructs";
import { createS3Policy } from '../iam-roles/s3/createS3Policy';
import { v4 as uuidv4 } from 'uuid';
import { createBatchPolicy } from '../iam-roles/batch/createBatchPolicy';
import { createCpuComputeEnvironments } from './cpu/createCpuComputeEnv';
import { createCpuJobQueues } from './cpu/createCpuJobQueue';
import { createG5ComputeEnvironments } from './gpu/createG5ComputeEnv';
import { createG5JobQueues } from './gpu/createG5JobQueue';
import { createG6ComputeEnvironments } from './gpu/createG6ComputeEnv';
import { createG6JobQueues } from './gpu/createG6JobQueue';



interface BatchResourcesProps {
    vpc: IVpc,
    sg: ISecurityGroup,
    efs: IFileSystem;
    ecrRepositoryName: string,
    s3BucketName: string,
    blenderVersionsList: string,
    isPrivate: boolean,
    maxvCpus: {
        onDemandCPU: string;
        spotCPU: string;
        onDemandGPU: string;
        spotGPU: string;
    }
    useG6Instances: boolean;
    spotBidPercentage: {
        spotCPU: string;
        spotGPU: string;
    }
}

export function createBatchResources(scope: Construct, props: BatchResourcesProps) {
    const { vpc, sg, ecrRepositoryName, efs, s3BucketName, blenderVersionsList, isPrivate, maxvCpus, useG6Instances, spotBidPercentage } = props;

    console.log('maxvCpus inside createBatchResources:', maxvCpus);
    console.log('Type of maxvCpus: ', typeof maxvCpus);
    console.log('Max vCPUs: ', maxvCpus.onDemandCPU, maxvCpus.spotCPU, maxvCpus.onDemandGPU, maxvCpus.spotGPU)
    console.log('Type of spotBidPercentage: ', typeof spotBidPercentage);
    console.log('Spot Bid Percentage: ', spotBidPercentage.spotCPU, spotBidPercentage.spotGPU)

    // parse int values maxvCpus
    const parsedMaxvCpus = {
        onDemandCPU: parseInt(maxvCpus.onDemandCPU, 10),
        spotCPU: parseInt(maxvCpus.spotCPU, 10),
        onDemandGPU: parseInt(maxvCpus.onDemandGPU, 10),
        spotGPU: parseInt(maxvCpus.spotGPU, 10),
    };

    const parsedSpotBidPercentage = {
        spotCPU: parseInt(spotBidPercentage.spotCPU, 10),
        spotGPU: parseInt(spotBidPercentage.spotGPU, 10),
    };


    const ecrRepository = Repository.fromRepositoryName(scope, 'ECRRepository', ecrRepositoryName);
    ecrRepository.grantPull(new ServicePrincipal('batch.amazonaws.com'))


    const s3Policy = createS3Policy(scope, { s3BucketName })
    const batchPolicy = createBatchPolicy(scope);

    // Get all subnets
    const allSubnets = vpc.selectSubnets({
        subnetType: isPrivate ? SubnetType.PRIVATE_WITH_EGRESS : SubnetType.PUBLIC
    }).subnets;

    allSubnets.forEach(subnet => {
        console.log(`Subnet ${subnet.subnetId} en la zona de disponibilidad ${subnet.availabilityZone}`);
    });

    // Create CPU compute environments and job queues
    const { computeEnvOnDemandCPU, computeEnvSpotCPU } = createCpuComputeEnvironments(scope, vpc, sg, allSubnets, s3Policy, batchPolicy, parsedMaxvCpus, parsedSpotBidPercentage);
    createCpuJobQueues(scope, computeEnvOnDemandCPU, computeEnvSpotCPU);

    // Create GPU compute environments and job queues for G5
    const { computeEnvOnDemandG5, computeEnvSpotG5 } = createG5ComputeEnvironments(scope, vpc, sg, allSubnets, s3Policy, batchPolicy, parsedMaxvCpus, parsedSpotBidPercentage);
    createG5JobQueues(scope, computeEnvOnDemandG5, computeEnvSpotG5);

    // // Create GPU compute environments and job queues for G6
    if (useG6Instances) {
        const { computeEnvOnDemandG6, computeEnvSpotG6 } = createG6ComputeEnvironments(scope, vpc, sg, allSubnets, s3Policy, batchPolicy, parsedMaxvCpus, parsedSpotBidPercentage);
        createG6JobQueues(scope, computeEnvOnDemandG6, computeEnvSpotG6);
    }

    // Context param ex: "4.0.0,4.0.0,3.6.0" 

    let blenderList = blenderVersionsList.split(',').map(version => version.toLowerCase());
    console.log('blenderList: ', blenderList);

    blenderList.map((version, index) => {
        let versionBlender = version.replace(/\./g, '_');
        let jobDefinitionName = `JobDefinition_VERSION__${versionBlender}__${uuidv4()}`;
        let containerDefinitionName = `ContainerDefinition_VERSION__${versionBlender}__${uuidv4()}`;
        console.log('jobDefinitionName: ', jobDefinitionName);

        new EcsJobDefinition(scope, jobDefinitionName, {
            timeout: cdk.Duration.days(1),
            retryAttempts: 3,
            jobDefinitionName: jobDefinitionName,
            container: new EcsEc2ContainerDefinition(scope, containerDefinitionName, {
                image: ContainerImage.fromEcrRepository(ecrRepository, version),
                // Add max memory for the container
                memory: cdk.Size.gibibytes(768),
                cpu: 256, // review this value 
                volumes: [EcsVolume.efs({
                    name: 'efs-volume',
                    fileSystem: efs,
                    containerPath: '/mnt/efs',
                    rootDirectory: '/',
                    enableTransitEncryption: true,
                })],
            }),
        });
    });

}