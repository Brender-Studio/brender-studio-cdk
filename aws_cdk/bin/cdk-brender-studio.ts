#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { BrenderStudioStack } from '../lib/cdk-brender-studio-stack';

const app = new cdk.App();
const stackName = app.node.tryGetContext('stackName');
const blenderVersionsList = app.node.tryGetContext('blenderVersions');
const isPrivate = app.node.tryGetContext('isPrivate') === 'true' ? true : false;
const maxvCpus = JSON.parse(app.node.tryGetContext('maxvCpus'));
const spotBidPercentage = JSON.parse(app.node.tryGetContext('spotBidPercentage'));
const useG6Instances = app.node.tryGetContext('useG6Instances') === 'true' ? true : false;

// Test the context values
const account = app.node.tryGetContext('account');
const region = app.node.tryGetContext('region');

const brenderStack = new BrenderStudioStack(app, 'BRENDER-STACK-V1', {
  stackName,
  blenderVersionsList,
  maxvCpus,
  isPrivate,
  spotBidPercentage,
  useG6Instances,
  description: 'This stack deploys all the essential resources to enable rendering Blender scenes in the cloud using AWS. It includes configurations for services such as AWS Batch, Amazon ECR, and Amazon EFS, providing a robust and scalable infrastructure for efficiently and reliably executing rendering jobs.',
  env: {
    account,
    region,
  },
});

cdk.Tags.of(brenderStack).add('StackName', stackName);