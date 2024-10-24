import os
import subprocess
import zipfile
import boto3
import json

s3 = boto3.client("s3")
lambda_client = boto3.client("lambda")

def lambda_handler(event, context):
  # Get BUCKET_NAME from environment variable
  bucket_name = os.environ.get("BUCKET_NAME")
  key_name = "layer.zip"
  temp_dir = "/tmp/package_dir"
  python_dir = os.path.join(temp_dir, "python")
  site_packages_dir = os.path.join(python_dir, "lib", "python3.12", "site-packages")
  zip_file_path = "/tmp/layer.zip"

  # Get the list of packages from the event
  packages = event.get("packages", [])
  if not packages:
    return {
      "statusCode": 400,
      "body": json.dumps("No packages specified in the event"),
    }

  # Create necessary directories for Lambda Layer
  os.makedirs(site_packages_dir, exist_ok=True)

  # Install specified packages to the appropriate site-packages directory
  try:
    for package in packages:
      subprocess.check_call(["pip", "install", package, "-t", site_packages_dir])
  except Exception as e:
    return {
      "statusCode": 500,
      "body": json.dumps(f"Error during pip install: {str(e)}"),
    }

  # Create a zip file
  try:
    with zipfile.ZipFile(zip_file_path, "w") as zipf:
      for root, dirs, files in os.walk(temp_dir):
        for file in files:
          file_path = os.path.join(root, file)
          arcname = os.path.relpath(file_path, temp_dir)
          zipf.write(file_path, arcname)
  except Exception as e:
    return {
      "statusCode": 500,
      "body": json.dumps(f"Error creating zip file: {str(e)}"),
    }

  # Upload the zip file to S3
  try:
    s3.upload_file(zip_file_path, bucket_name, key_name)
  except Exception as e:
    return {
      "statusCode": 500,
      "body": json.dumps(f"Error uploading file to S3: {str(e)}"),
    }

  # Publish the uploaded zip as a new Lambda Layer
  try:
    layer_response = lambda_client.publish_layer_version(
      LayerName=event.get("layer_name", "custom_layer"),
      Content={
        "S3Bucket": bucket_name,
        "S3Key": key_name,
      },
      CompatibleRuntimes=["python3.12"],  # 対応するランタイムを指定
      Description=event.get("description", "Custom Lambda Layer created by Lambda function"),
    )
    return {
      "statusCode": 200,
      "body": json.dumps(
        {
          "message": f"Successfully uploaded {key_name} to {bucket_name}",
          "layerVersionArn": layer_response["LayerVersionArn"],
        }
      ),
    }
  except Exception as e:
    return {
      "statusCode": 500,
      "body": json.dumps(f"Error creating Lambda Layer: {str(e)}"),
    }
