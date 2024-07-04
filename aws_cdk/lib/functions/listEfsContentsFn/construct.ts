import { IVpc } from "aws-cdk-lib/aws-ec2";
import { IAccessPoint, IFileSystem } from "aws-cdk-lib/aws-efs";
import { Runtime, Tracing, FileSystem as lfs } from "aws-cdk-lib/aws-lambda";
import { NodejsFunction } from "aws-cdk-lib/aws-lambda-nodejs";
import { Construct } from "constructs";
import path = require("path");

interface ListContentsFnProps {
    name: string;
    lambdaLocalMountPath: string;
    vpc: IVpc;
    accessPoint: IAccessPoint;
    efs: IFileSystem;
}

export const createListContentsFn = (scope: Construct, props: ListContentsFnProps) => {

    const { name, lambdaLocalMountPath, vpc, accessPoint, efs } = props;

    const listContentsFn = new NodejsFunction(scope, name, {
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
    });

    efs.connections.allowDefaultPortFrom(listContentsFn);

    return listContentsFn;
}