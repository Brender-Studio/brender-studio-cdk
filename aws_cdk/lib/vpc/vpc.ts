import { RemovalPolicy } from "aws-cdk-lib";
import { GatewayVpcEndpointAwsService, IVpc, SubnetType, Vpc } from "aws-cdk-lib/aws-ec2";
import { Construct } from "constructs";

interface VpcProps {
    name: string;
    gatewayEndpointName: string;
    isPrivate: boolean;
}

export function createVpc(scope: Construct, props: VpcProps): IVpc {

    const { isPrivate, gatewayEndpointName, name } = props;

    const subnetConfiguration = [
        {
            cidrMask: 24,
            name: 'public-subnet-1',
            subnetType: SubnetType.PUBLIC,
        },
        {
            cidrMask: 24,
            name: 'public-subnet-2',
            subnetType: SubnetType.PUBLIC,
        },
        {
            cidrMask: 24,
            name: 'private-subnet-1',
            subnetType: SubnetType.PRIVATE_WITH_EGRESS,
        },
        {
            cidrMask: 24,
            name: 'private-subnet-2',
            subnetType: SubnetType.PRIVATE_WITH_EGRESS,
        },
    ];

    const natGateways = isPrivate ? 1 : 0; 

    const vpc = new Vpc(scope, name, {
        natGateways: natGateways,
        maxAzs: 99, 
        subnetConfiguration: subnetConfiguration,
    });

    // Gateway endpoint for S3 access from lambda efs
    const s3GatewayEndpoint = vpc.addGatewayEndpoint(gatewayEndpointName, {
        service: GatewayVpcEndpointAwsService.S3,
    });

    vpc.applyRemovalPolicy(RemovalPolicy.DESTROY);

    return vpc;
}
