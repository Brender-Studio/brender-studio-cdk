import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { createVpc } from './vpc/vpc';
import { createSecurityGroup } from './vpc/sg';
import { createBatchResources } from './batch/batchResources';
import { createVpcCloudwatchLogs } from './cloudwatch/vpc-logs';
import { Port } from 'aws-cdk-lib/aws-ec2';
import { createFileSystem } from './efs/fileSystem';
import { createAccessPoint } from './efs/accessPoint';
import { createS3Bucket } from './s3/s3Bucket';
import { createListContentsFn } from './functions/listEfsContentsFn/construct';
import { LambdaRestApi } from 'aws-cdk-lib/aws-apigateway';
import { BrenderStudioStackProps } from './stack-config/stackProps';
import { v4 as uuidv4 } from 'uuid';

export class BrenderStudioStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: BrenderStudioStackProps) {
    super(scope, id, props);

    const lambdaLocalMountPath = '/mnt/files';

    const ecrRepositoryName = new cdk.CfnParameter(this, 'ecrRepoName', {
      type: 'String',
      description: 'Name of the ECR repository',
    });


    // CONTEXT PROPS
    const blenderVersions = props?.blenderVersionsList;
    console.log('blenderVersions', blenderVersions)

    const privateStack = props?.isPrivate;

    const isPrivate = Boolean(privateStack);
    console.log('isPrivate', isPrivate)

    const useG6Instances = props?.useG6Instances;
    const useG6 = Boolean(useG6Instances);

    console.log('useG6Instances', useG6Instances)
    console.log('useG6', useG6)

    const maxvCpus = props?.maxvCpus;
    console.log('maxvCpus before passing to createBatchResources:', maxvCpus);

    const spotBidPercentage = props?.spotBidPercentage;
    console.log('spotBidPercentage', spotBidPercentage);

    if(!spotBidPercentage) {
      throw new Error('spotBidPercentage is required');
    }

    if(!maxvCpus) {
      throw new Error('maxvCpus is required');
    }



    const brenderBucketName = 'brender-bucket-s3-' + uuidv4();

    // COMMAND DEPLOY STACK
    // cdk deploy --context stackName=BRENDER-STACK-BATCH-REFACTOR-V5 --parameters ecrRepoName=blender-repo-ecr --context blenderVersions="4.1.1" --context isPrivate="true" --context maxvCpus="{\"onDemandCPU\": \"100\", \"spotCPU\": \"256\", \"onDemandGPU\": \"100\", \"spotGPU\": \"256\"}" --context spotBidPercentage="{\"spotCPU\": \"80\", \"spotGPU\": \"90\"}" --context useG6Instances="true" --region us-east-1

    const vpc = createVpc(this, {
      name: 'Vpc-' + uuidv4(),
      gatewayEndpointName: 'VpcEndpointGatewayS3-' + uuidv4(),
      isPrivate,
    })

    const vpcSecurityGroup = createSecurityGroup(this, {
      name: 'SecurityGroup-' + uuidv4(),
      vpc
    })

    const efs = createFileSystem(this, {
      name: 'Efs-' + uuidv4(),
      vpc: vpc,
      sg: vpcSecurityGroup,
    });

    const accessPoint = createAccessPoint(this, {
      name: 'S3AccesPoint-' + uuidv4(),
      efs: efs,
      // path: '/efs/lambda',
      path: '/projects',
    });

    if (!brenderBucketName) {
      throw new Error('brenderBucketName is required');
    }


    const s3Bucket = createS3Bucket(this, {
      name: brenderBucketName,
    });

    efs.connections.allowFrom(vpcSecurityGroup, Port.tcp(2049));


    const listEfsContentsFn = createListContentsFn(this, {
      name: 'ListEfsContentFunction-' + uuidv4(),
      lambdaLocalMountPath: lambdaLocalMountPath,
      vpc: vpc,
      accessPoint: accessPoint,
      efs: efs,
    });

    const api = new LambdaRestApi(this, 'ApiBatchEfsListContent-' + uuidv4(), {
      handler: listEfsContentsFn,
    });


    const logGroup = createVpcCloudwatchLogs(this, {
      vpc,
      logGroupName: 'FlowLogsGroup-' + uuidv4(),
      logRoleName: 'CloudwatchLogsRole-' + uuidv4()
    })

    if (!blenderVersions) {
      throw new Error('blenderVersions is required');
    }

    const batch = createBatchResources(this, {
      vpc,
      sg: vpcSecurityGroup,
      efs: efs,
      ecrRepositoryName: ecrRepositoryName.valueAsString,
      s3BucketName: s3Bucket.bucketName,
      blenderVersionsList: blenderVersions,
      isPrivate,
      maxvCpus,
      spotBidPercentage,
      useG6Instances: useG6,
    })
  }
}
