import * as cdk from 'aws-cdk-lib';


export interface BrenderStudioStackProps extends cdk.StackProps {
  blenderVersionsList: string;
  isPrivate: boolean;
  maxvCpus: {
    onDemandCPU: string;
    spotCPU: string;
    onDemandGPU: string;
    spotGPU: string;
  }
  useG6Instances: boolean;
  spotBidPercentage: {
    spotCPU: string;
    spotGPU: string;
  }
}
