# AWS Lambda Layer Creation with AWS CDK

This project sets up an AWS Lambda function that dynamically installs Python packages specified at runtime. The installed packages are packaged into a Lambda Layer and uploaded to an S3 bucket. The project is built using AWS CDK with TypeScript, and it provides the infrastructure setup necessary for managing Lambda and S3 using AWS CloudFormation.

## Project Structure

```
.
├── .npmignore
├── README.md
├── bin
│   └── create-lambda-layer.ts
├── cdk.json
├── jest.config.js
├── lambda
│   └── create_layer.py
├── lib
│   └── create-lambda-layer-stack.ts
├── package.json
├── test
│   └── create-lambda-layer.test.ts
└── tsconfig.json
```

## Lambda Function (`create_layer.py`)

The Lambda function dynamically installs Python packages specified in the event payload. It packages the installed libraries into a zip file and uploads it to an S3 bucket. It also publishes the uploaded zip as a new Lambda Layer. The expected event payload structure is as follows:

```json
{
  "packages": ["requests", "numpy"],
  "layer_name": "your-layer-name",  // optional: specify layer name
  "description": "your-layer-description"  // optional: specify description
}
```

The function installs the specified packages, compresses them into a zip file, and uploads it to the S3 bucket defined by the environment variable `BUCKET_NAME`. The function then publishes the zip file as a new Lambda Layer. The layer name and description can optionally be specified in the event payload.

### Example Output

If the Lambda function runs successfully, it will return an output similar to the following:

```json
{
  "statusCode": 200,
  "body": "{\"message\": \"Successfully uploaded layer.zip to createlambdalayerstack-lambdalayerbucket3217ab23-cr22zh1gux72\", \"layerVersionArn\": \"arn:aws:lambda:ap-northeast-1:211125380625:layer:gtfsrt:1\"}"
}
```

## Environment Variables

The Lambda function uses the following environment variables:

- **`BUCKET_NAME`**: The name of the S3 bucket used to store the Lambda layer zip file.

## Usage

### Prerequisites

- An AWS account
- AWS CLI configured
- Node.js and npm installed

### Getting Started

1. Clone the repository and install dependencies:

   ```bash
   git clone https://github.com/your-repo/create-lambda-layer
   cd create-lambda-layer
   npm install
   ```

2. Synthesize the CloudFormation template:

   ```bash
   npx cdk synth
   ```

3. Deploy the CDK stack:

   ```bash
   npx cdk deploy
   ```

### Invoking the Lambda Function

The Lambda function can be invoked using the following event payload:

```json
{
  "packages": ["requests", "numpy"]
}
```

This installs the `requests` and `numpy` packages, uploads them to the S3 bucket, and creates a Lambda Layer. The function's output will include the ARN of the newly created layer.

## Cleanup

To clean up all resources created by this project, run the following command:

```bash
npx cdk destroy
```

This command deletes the Lambda function, S3 bucket, and any other resources associated with the stack.