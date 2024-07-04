import { ISecurityGroup, IVpc, SecurityGroup } from "aws-cdk-lib/aws-ec2";
import { Construct } from "constructs";

interface SGProps {
    name: string,
    vpc: IVpc
}

export function createSecurityGroup(scope: Construct, props: SGProps): ISecurityGroup {

    const { name, vpc } = props;

    const vpcSg = new SecurityGroup(scope, name, {
        vpc: vpc,
        description: 'AWS Batch sg',
        allowAllOutbound: true,
    })

    return vpcSg
}