import { RemovalPolicy } from 'aws-cdk-lib';
import { JobQueue } from 'aws-cdk-lib/aws-batch';
import { Construct } from 'constructs';
import { v4 as uuidv4 } from 'uuid';

export function createG5JobQueues(scope: Construct, computeEnvOnDemandG5: any, computeEnvSpotG5: any) {
    const jobQueueSpotG5 = new JobQueue(scope, 'JobQueueSpotGPU-' + uuidv4(), {
        computeEnvironments: [{ computeEnvironment: computeEnvSpotG5, order: 1 }],
        jobQueueName: 'JobQueueSpotGPU-' + uuidv4(),
        priority: 10,
    });
    jobQueueSpotG5.applyRemovalPolicy(RemovalPolicy.DESTROY);

    const jobQueueOnDemandG5 = new JobQueue(scope, 'JobQueueOnDemandGPU-' + uuidv4(), {
        computeEnvironments: [{ computeEnvironment: computeEnvOnDemandG5, order: 1 }],
        priority: 10,
        jobQueueName: 'JobQueueOnDemandGPU-' + uuidv4(),
    });
    jobQueueOnDemandG5.applyRemovalPolicy(RemovalPolicy.DESTROY);
}
