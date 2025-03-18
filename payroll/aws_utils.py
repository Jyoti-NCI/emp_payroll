import boto3
import os
from django.conf import settings
from datetime import datetime

# 🔹 Replace with actual AWS values from Learner Lab
AWS_ACCESS_KEY = "ASIATUYJP7SUCNJ7OIMH"
AWS_SECRET_KEY = "AUK8OYNI3Nh403Xu+/RpZTQ7mXOudq6QXUSEfyWJ"
AWS_SESSION_TOKEN = "IQoJb3JpZ2luX2VjEHsaCXVzLWVhc3QtMSJGMEQCIG0DpnUK0bYHwbRbJYplnWC+3cjdlNfv3pvdmA/dQhoMAiAyL4jXEKBEFqCSEsY/r633X5PAZfmLFRNmYybPAm15MSqJBAjD//////////8BEAMaDDI1MDczODYzNzk5MiIM9+BNPy7KD/PERkRkKt0DDvpH5j73iwxOQg0Z2K38B2elW/70u8gXr8xRJkMzxotAHHjRsGCb6clskSr9cP1Xe2G4QxJ6ZnMIt+oKFuRU1ZVqBrEnQtiSCfPob0rHfoLwofuB+2EW67Owesox1KGvMdTl3y9zq9okKqh6e8bWfgQycjF7KeOq8BICWOh4w3B/Um+ZAaDwrIfp6SMzTxD7gn/kQDh79zS1zgJxH/3R3DBr4wFeJJr5uITGwjXiKDIxX7ny/RqRkmpd2cT9zd7BtyMXcN2mkGtcqoU8YljlkagDeVPSQst5zOnHMtm7s/cKwSqegZnyFNrUfTpU3pDfZ0zLvOtin4KLNM/LAX5MIHhrmdW/4jht+fTmvhAbD6tQpuRFnEtWX2GEt6CI99LEnTArlB+yC5CldS3m9gAkOMy9+ojF++OaYTleTUzDcRI1/KbM/qrJqjdDWKIUUWD+Xij9MUPYVmY9NNh0+TIxbjY4tK8h3LyG0VoU/YGD2ct1L3zgW99IBeXF5m2v3m8N7SE2Q2PvfFpMxzbdedoR4nws6AQsiWeslMwG0YwyUuz4hLNE/vA+BhATVLPOxnHelsZpkqvQZNNbkSxzF0ix/NIrbPU2//frU87g5dapuocRN+/9ITyHJEGpksLpMLOax74GOqcBI0zTDoprGseRyvPjGVXP6pWEci5vye2Usun6UMW4t9nbv3dUX3AQZrsjC8Pf++tSJWLI3kohXlOqQciB0zPJq1/6KeOMLYCAAwyEjhaQQEgpXZKxXiF8sCWzJNcAkaM/PDiV0Yst5tNDIh+mZ7p3uQ9dB/9xP4wnYycZ4gp0WQyfPGhI7hjQacssa9CqTCzS/n8x+bSW/WH1d3TPsngiHANi+tkFACo="  # Temporary session token

AWS_S3_BUCKET = "x24104558cppbucket"
AWS_SNS_TOPIC_ARN = "arn:aws:sns:eu-west-1:250738637992:EmployeeUpdates"
AWS_CLOUDWATCH_LOG_GROUP = "EmployeeActivityLogs"
AWS_CLOUDWATCH_LOG_STREAM = "GeneralLogs"

# 🔹 Configure AWS Clients with manual credentials
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    aws_session_token=AWS_SESSION_TOKEN,  # Temporary session token
)

sns_client = boto3.client(
    "sns",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
)

cloudwatch_client = boto3.client(
    "logs",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
)
# Initialize AWS Clients
s3_client = boto3.client("s3")
sns_client = boto3.client("sns")
cloudwatch_client = boto3.client("logs")

def upload_image_to_s3(image_file):
    """
    Uploads an image file to an S3 bucket and returns the public URL.
    """
    if image_file:
        file_name = f"employee_images/{image_file.name}"
        try:
            s3_client.upload_fileobj(image_file, AWS_S3_BUCKET, file_name)
            # ✅ Return the full S3 URL
            s3_url = f"https://{AWS_S3_BUCKET}.s3.amazonaws.com/{file_name}"
            return s3_url
        except Exception as e:
            print("S3 Upload Error:", str(e))
            return None
    return None

def send_sns_notification(message):
    """
    Sends an SNS notification with the given message.
    """
    try:
        sns_client.publish(TopicArn=AWS_SNS_TOPIC_ARN, Message=message, Subject="Employee Update Notification")
    except Exception as e:
        print("SNS Error:", str(e))

def log_to_cloudwatch(message):
    """
    Logs an activity message to AWS CloudWatch.
    """
    try:
        # Ensure Log Group exists
        cloudwatch_client.create_log_group(logGroupName=AWS_CLOUDWATCH_LOG_GROUP)
    except cloudwatch_client.exceptions.ResourceAlreadyExistsException:
        pass  

    try:
        # Ensure Log Stream exists
        cloudwatch_client.create_log_stream(logGroupName=AWS_CLOUDWATCH_LOG_GROUP, logStreamName=AWS_CLOUDWATCH_LOG_STREAM)
    except cloudwatch_client.exceptions.ResourceAlreadyExistsException:
        pass  

    timestamp = int(datetime.utcnow().timestamp() * 1000)
    cloudwatch_client.put_log_events(
        logGroupName=AWS_CLOUDWATCH_LOG_GROUP,
        logStreamName=AWS_CLOUDWATCH_LOG_STREAM,
        logEvents=[{"timestamp": timestamp, "message": message}]
    )
