import { Size } from "aws-cdk-lib";
import { IVpc } from "aws-cdk-lib/aws-ec2";
import { IAccessPoint, IFileSystem } from "aws-cdk-lib/aws-efs";
import { Runtime, Tracing, FileSystem as lfs } from "aws-cdk-lib/aws-lambda";
import { S3EventSource } from "aws-cdk-lib/aws-lambda-event-sources";
import { NodejsFunction } from "aws-cdk-lib/aws-lambda-nodejs";
import { Bucket, EventType, IBucket } from "aws-cdk-lib/aws-s3";
import { Construct } from "constructs";
import path = require("path");

interface CopyToEfsFnProps {
    name: string;
    lambdaLocalMountPath: string;
    vpc: IVpc;
    accessPoint: IAccessPoint;
    s3bucket: Bucket;
    efs: IFileSystem;
}

export const createCopyToEfsFn = (scope: Construct, props: CopyToEfsFnProps) => {

    const { name, lambdaLocalMountPath, vpc, accessPoint, s3bucket, efs } = props;


    const copyToEfsFn = new NodejsFunction(scope, name, {
        vpc,
        functionName: name,
        runtime: Runtime.NODEJS_18_X,
        handler: 'handler',
        entry: path.join(__dirname, './main.ts'),
        environment: {
            EFS_PATH: lambdaLocalMountPath,
        },
        filesystem: lfs.fromEfsAccessPoint(accessPoint, lambdaLocalMountPath),
        tracing: Tracing.ACTIVE,
        memorySize: 1024,
        ephemeralStorageSize: Size.gibibytes(10),
    });
    

    copyToEfsFn.addEventSource(new S3EventSource(s3bucket, {
        events: [EventType.OBJECT_CREATED],
        // filters: [{ prefix: 'data/' }],
    }))

    efs.connections.allowDefaultPortFrom(copyToEfsFn);

    return copyToEfsFn;

}