import { RemovalPolicy } from "aws-cdk-lib";
import { BlockPublicAccess, Bucket, BucketEncryption } from "aws-cdk-lib/aws-s3";
import { Construct } from "constructs";

interface s3BucketProps {
    name: string;
}

export function createS3Bucket(scope: Construct, props: s3BucketProps): Bucket {
    const { name } = props;
    

    const bucket = new Bucket(scope, name, {
        bucketName: name,
        removalPolicy: RemovalPolicy.DESTROY,
        encryption: BucketEncryption.S3_MANAGED,
        blockPublicAccess: BlockPublicAccess.BLOCK_ALL,
        autoDeleteObjects: true,
    
    });

    return bucket;
}