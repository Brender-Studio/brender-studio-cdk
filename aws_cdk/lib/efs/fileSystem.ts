import { RemovalPolicy } from "aws-cdk-lib";
import { Port } from "aws-cdk-lib/aws-ec2";
import { FileSystem, IFileSystem } from "aws-cdk-lib/aws-efs";
import { AnyPrincipal, PolicyDocument, PolicyStatement } from "aws-cdk-lib/aws-iam";
import { Construct } from "constructs";

interface FileSystemProps {
    name: string;
    vpc: any;
    sg: any;
}

export function createFileSystem(scope: Construct, props: FileSystemProps): IFileSystem {

    const { name, vpc, sg } = props;

    const fileSystem = new FileSystem(scope, props.name, {
        vpc: vpc,
        fileSystemName: name,
        securityGroup: sg,
        removalPolicy: RemovalPolicy.DESTROY,
        encrypted: true,
        fileSystemPolicy: new PolicyDocument({
            statements: [
                new PolicyStatement({
                    actions: ['elasticfilesystem:ClientMount', 'elasticfilesystem:ClientWrite', 'elasticfilesystem:ClientRootAccess'],
                    resources: ['*'], // ARN of the EFS file system , TODO: change to specific ARN
                    principals: [new AnyPrincipal()],
                    conditions: {
                        Bool: {
                            'aws:SecureTransport': 'true',
                            'elasticfilesystem:AccessedViaMountTarget': 'true',
                        },
                    },
                }),
            ],
        }),
    });

    fileSystem.connections.allowFrom(sg, Port.tcp(2049), 'Allows inbound traffic from Security Group');


    return fileSystem;
}