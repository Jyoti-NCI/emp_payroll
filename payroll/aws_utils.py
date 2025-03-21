import boto3
import os
from django.conf import settings
from datetime import datetime

# 🔹 Replace with actual AWS values from Learner Lab
AWS_ACCESS_KEY = "ASIATUYJP7SUNP44TBV4"
AWS_SECRET_KEY = "kpl4h2wGky8LfJQ+txtB/SVTRSYE2i4Jeq/eNWKU"
AWS_SESSION_TOKEN = "IQoJb3JpZ2luX2VjEE4aCXVzLWVhc3QtMSJHMEUCIQDK2JWnZWi9Lwjxi3aUX1zTvtce3fgm3tj+i6Xkda6qsQIgKnKbe9MT5PbbgC9dEsZD94T1KQVLwxdWyL4XbZfVZsMqiQQIp///////////ARADGgwyNTA3Mzg2Mzc5OTIiDNP5PbT+WBc+1OGRySrdAznO4ZPJ3xTQjJuaXOZ6wl3x+sgHITtKKrquVFPPqvZzib6rTWOll9vDhwsqgoWYO8qDwkknOrNhgHTipbG6wTDqBc1X64BlHdcHkdjSLy+tZvR6z4ezoal6oSCYqLjfJus681mwsY653bYqNHcJgwetoayOh6NktIR2EK73DzLKHKDW4KCXYuNLw9SNewNC5sjiFmLyLU02xmezGH0Nwu0FZlpPMy324S1Upef4sRKUG4bMHBpQLmBvskGu+ZSpLGb7ab2uMMAwqYgh2kGh078gjmoWcNJUiufB76aSGfo8TRZXChN5Ho8HTQO32w3KY5HkzuQSXjaEFfHj3tGU0+n33XzFoDpLaLKs+eSBnc43k3jgdHsATVCs1psQwISJw3K6cqMx+rDRL8vQhsNJ14nQpayUYLBDpgsZcqfhtEVrGvl1HP2EQZhqUALxM6P2G768Pl1y3VxlAqIVkDyn/zRraoVg6wy74P9W5xVPaDAYfxBLANYegn7Gc2p+AD1JrG9qEniofRNs6lDc5Z8/uBnoJ6r8vQkcWOH4GUa1D2aYRGdmnj/3k+gqi7EeEse0Ku5z0vRIVCy6jl8PTf/e7OgYyfa5ohMyyfQCQBXVk15vwaBp3RHIKjpVh8kXPjCS2PW+BjqmAau3A85pQGYnJBA823QMLZXKbXU6XvE1dS3hlFmGUTyqVx7qn+Fs7dPKroeBdZF2oSNmPhooZelJHcqbAT4nxeJMf13ojSiqFEq4H8Xvon9x+h3ZlkZ/ETeX6v+qiiREljlPpPf1oRT2bBeYrsI8o7Zi/GPeFWDWR44rKmbZ3LtgOJbABru586WbkB0u7P/UIACGrEVTTnjrY8pIMgLngroez9qi2+4=" # Temporary session token

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
"""s3_client = boto3.client("s3")
sns_client = boto3.client("sns")
cloudwatch_client = boto3.client("logs")"""

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
