import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as iam from 'aws-cdk-lib/aws-iam';

export class CreateLambdaLayerStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Get the current AWS account and region
    const account = cdk.Stack.of(this).account;
    const region = cdk.Stack.of(this).region;

    // Create an S3 bucket to store the Lambda layer
    const bucket = new s3.Bucket(this, 'LambdaLayerBucket', {
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });

    // Create a Lambda function to create and upload the Lambda layer
    const lambdaFunction = new lambda.Function(this, 'CreateAndUploadLayerLambda', {
      runtime: lambda.Runtime.PYTHON_3_12,
      handler: 'create_layer.lambda_handler',
      code: lambda.Code.fromAsset('lambda'),
      timeout: cdk.Duration.minutes(15),
      environment: {
        BUCKET_NAME: bucket.bucketName,
      },
      architecture: lambda.Architecture.ARM_64,
      memorySize: 1024,
    });

    // Add permission to the Lambda function to publish the layer for the specific account and region
    lambdaFunction.addToRolePolicy(new iam.PolicyStatement({
      actions: ['lambda:PublishLayerVersion'],
      resources: [`arn:aws:lambda:${region}:${account}:layer:*`],
    }));

    // Add permission to the Lambda function to write to the bucket
    bucket.grantPut(lambdaFunction);

    // Add permission to the Lambda function to read (GetObject) from the bucket
    bucket.grantRead(lambdaFunction);
  }
}
