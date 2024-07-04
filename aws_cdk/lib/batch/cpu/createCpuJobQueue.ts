import { RemovalPolicy } from 'aws-cdk-lib';
import { JobQueue } from 'aws-cdk-lib/aws-batch';
import { Construct } from 'constructs';
import { v4 as uuidv4 } from 'uuid';


export function createCpuJobQueues(scope: Construct, computeEnvOnDemandCPU: any, computeEnvSpotCPU: any) {
    const jobQueueSpotCPU = new JobQueue(scope, 'JobQueueSpotCPU-' + uuidv4(), {
        computeEnvironments: [{ computeEnvironment: computeEnvSpotCPU, order: 1 }],
        jobQueueName: 'JobQueueSpotCPU-' + uuidv4(),
        priority: 10,
    });
    jobQueueSpotCPU.applyRemovalPolicy(RemovalPolicy.DESTROY);

    const jobQueueOnDemandCPU = new JobQueue(scope, 'JobQueueOnDemandCPU-' + uuidv4(), {
        computeEnvironments: [{ computeEnvironment: computeEnvOnDemandCPU, order: 1 }],
        priority: 10,
        jobQueueName: 'JobQueueOnDemandCPU-' + uuidv4(),
    });
    jobQueueOnDemandCPU.applyRemovalPolicy(RemovalPolicy.DESTROY);
}
