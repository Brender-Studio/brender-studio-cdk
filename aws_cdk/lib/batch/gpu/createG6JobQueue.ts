import { RemovalPolicy } from 'aws-cdk-lib';
import { JobQueue } from 'aws-cdk-lib/aws-batch';
import { Construct } from 'constructs';
import { v4 as uuidv4 } from 'uuid';

export function createG6JobQueues(scope: Construct, computeEnvOnDemandG6: any, computeEnvSpotG6: any) {
    const jobQueueSpotG6 = new JobQueue(scope, 'JobQueueSpotGPUG6-' + uuidv4(), {
        computeEnvironments: [{ computeEnvironment: computeEnvSpotG6, order: 1 }],
        jobQueueName: 'JobQueueSpotGPUG6-' + uuidv4(),
        priority: 10,
    });
    jobQueueSpotG6.applyRemovalPolicy(RemovalPolicy.DESTROY);

    const jobQueueOnDemandG6 = new JobQueue(scope, 'JobQueueOnDemandGPUG6-' + uuidv4(), {
        computeEnvironments: [{ computeEnvironment: computeEnvOnDemandG6, order: 1 }],
        priority: 10,
        jobQueueName: 'JobQueueOnDemandGPUG6-' + uuidv4(),
    });
    jobQueueOnDemandG6.applyRemovalPolicy(RemovalPolicy.DESTROY);
}
