import { RemovalPolicy } from "aws-cdk-lib";
import { AccessPoint, IAccessPoint } from "aws-cdk-lib/aws-efs";
import { Construct } from "constructs";


interface AccessPointProps {
    name: string;
    efs: any;
    path: string;
}

export function createAccessPoint(scope: Construct, props: AccessPointProps): IAccessPoint {

    const accessPoint = new AccessPoint(scope, props.name, {
        fileSystem: props.efs,
        path: props.path,
        createAcl: {
            ownerGid: '1001',
            ownerUid: '1001',
            permissions: '750',
        },
        posixUser: {
            gid: '1001',
            uid: '1001',
        },
    });

    accessPoint.applyRemovalPolicy(RemovalPolicy.DESTROY);

    return accessPoint;
}