import { RemovalPolicy } from "aws-cdk-lib";
import { FlowLog, FlowLogDestination, FlowLogResourceType, IVpc } from "aws-cdk-lib/aws-ec2";
import { Role, ServicePrincipal } from "aws-cdk-lib/aws-iam";
import { LogGroup } from "aws-cdk-lib/aws-logs";
import { Construct } from "constructs";

interface VpcLogsProps {
    vpc: IVpc,
    logGroupName: string,
    logRoleName: string,
}

export function createVpcCloudwatchLogs(scope: Construct, props: VpcLogsProps) {

    const { vpc, logGroupName, logRoleName } = props;

    const logGroup = new LogGroup(scope, logGroupName);

    const role = new Role(scope, logRoleName, {
        assumedBy: new ServicePrincipal('vpc-flow-logs.amazonaws.com'),
    });

    const vpcFlowLogs = new FlowLog(scope, 'FlowLog', {
        resourceType: FlowLogResourceType.fromVpc(vpc),
        destination: FlowLogDestination.toCloudWatchLogs(logGroup, role),
    });

    vpcFlowLogs.applyRemovalPolicy(RemovalPolicy.DESTROY)

    return vpcFlowLogs;
}