import boto3
import os
from django.conf import settings
from datetime import datetime

# 🔹 Replace with actual AWS values from Learner Lab
AWS_ACCESS_KEY = "ASIATUYJP7SUL6EMG2M2"
AWS_SECRET_KEY = "mwmgEaQVZtqYlo1ZnvKEZdnCNmYDKxz0Rpfe3XeY"
AWS_SESSION_TOKEN = "IQoJb3JpZ2luX2VjEKv//////////wEaCXVzLWVhc3QtMSJGMEQCIHz5ehIPIaeasHgrA9zWnkqkkSH6+f05eeiXtyyh33ZXAiAx6bMiDmaBGSjNvxkyGvs6ZE0Gnzt7bTXZv2b0c9SZgSqABAgUEAMaDDI1MDczODYzNzk5MiIMh+5ZPEkAjF9yDmx1Kt0DGVZikU2alSRvYiRjLOUSuIfFXtyBOC+tqRLb6ZkNhgp+pOmS5/MXhU9xSI58S70rJpioL6GvzVPSPdQkm/Tw6dy5sJZd+QfmnVf+UEdKbCH7TziyzjozqgtFI0S61zxJcHiE+RNYF1TZh+ed1umOXOzbTw54LdyLr2pLRWLIZ5z+v58wlZIGcbMfZ2+8lycWbIM7E0XOQcwjgwWvlY807ptqe2ZQF3+k1gZCupOAnEYqg/UtsFpQBv1/ob4fOYUPSP+qVJX+LFc/yHoo0Ut2frWMTBc9ivM4YSzmo3l8soJIzNKyukiKeBfjAoxnljfniHgAdBTTWJ1ZI4SUt4cin62typkquywvHtOLwmJR8dtGJp9uW2Pzmg7LuqlwKbWjD1a9JlXBQX7Q7fSCxg065cVsegv3O0ZWZGLw+EzFjRVrdjvhbjC/vtCej+SsGpYM32CoWiOFmVQRA7tblC1pKjGO/gRbXnF3spgonqCJZ5+McOBKxMWAITBzpwghZTLYKPC0pTrq8nQVjqIJkj6CvuePX4QDU2EdiRlyXzakvuolLBuz5kgzjaAXDei15+eiYhJ00zvE3esomGMUuVBDMgcMa2lCMPe5vUKgsKqfNnSUyrbEwWCPdXtyJa6NMJWWir8GOqcBPWrQu7SzvB1hLkbrn/afLfFsHVsbIej24Z8kkuVhrmpkBFmIV0Nu0TzTZmwttGKvXL7IMiyIxkdk1GRnnXFLXGONRBroISQ3n2jtU5mihIfZJDI0/jChQazUL6+jA6PRg4Bd4CzG3+U+/PYD8gxJSPVHh/jKqrLc9aylKDmLMUQ57QPxYOBNbV2tjd8b19QjqW3PVyq4ZEuqqHm6yDU2unQERN2Rmc8=" # Temporary session token

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
