import { ManagedPolicy, PolicyStatement } from "aws-cdk-lib/aws-iam";
import { Construct } from "constructs";



interface s3PolicyProps {
    s3BucketName: string
}



export function createS3Policy(scope: Construct, props: s3PolicyProps) {
    const { s3BucketName } = props;

    const s3Policy = new ManagedPolicy(scope, 'S3Policy', {
        statements: [
            new PolicyStatement({
                actions: [
                    's3:GetObject',
                    's3:PutObject',
                    's3:DeleteObject',
                    's3:ListBucket'
                ],
                resources: [
                    `arn:aws:s3:::${s3BucketName}/*`,
                    `arn:aws:s3:::${s3BucketName}`,
                ],
            }),
        ],
    });
    return s3Policy
}