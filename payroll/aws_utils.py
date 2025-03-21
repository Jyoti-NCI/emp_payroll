import boto3
import os
from django.conf import settings
from datetime import datetime

# 🔹 Replace with actual AWS values from Learner Lab
AWS_ACCESS_KEY = "ASIATUYJP7SUJQB7GVU6"
AWS_SECRET_KEY = "i18XBOmV8B071uc8UgRMeVIbiWUl3NZOiapq8Nfz"
AWS_SESSION_TOKEN = "IQoJb3JpZ2luX2VjEEwaCXVzLWVhc3QtMSJIMEYCIQDSGvFy88gDT+L9es23/fz2vQmvrP23PaGFiSGPMModPwIhAMpsCsM369qd++5iTWLPEh58Q+Miy48msJxqI12VdfMWKokECKX//////////wEQAxoMMjUwNzM4NjM3OTkyIgzW2Egkqo7Vk4yxnN8q3QNXpg021Sn6pzUJZmwgoMFU0s2T14ikxxr0VAXaCY/MYzlwdnnaLlbcuIq03pIJs8Hm0pz4bJPxYBf4tfLzG0aB2vXLXG0xpbAeZMA6nlfYjSQTWDiTqld1OTl/DLWtLMFa/jLky8q7o9uv9bgG/kTQwn27LBhEhwLGi7Y/HifbidOTDngVBEpOB0QYiT4/OFEiI2RetCJre67cedDmwUrnJ5LrqLSbTqE0H3PvB9p65TsEGmq3D74ewp1Ikj32sLeiwAu9ifMowv/H1E5XjRBf+dtXNls3eiXYFjnoD276gSF0/t8FnzdNM/OLuGG6zAmYzVDqTMlzrJqt0dzJ/N3V5yx9e/5rLOiyKXpZcEL2SzHwIyV0nJ04zVOBunuc0BwQo5o7NflJgTFXLAu+/MKWtUEyPzBS9yZcN/705e+NH9U+Q+mnCmMAgAm2DZobLu6a0zcVFnbZ7r+GtgLc5Ga3pmobOdTgG6DESo6e0ZMeIGgZbF3dX4G3uECKAVQWyy5ex+So5W1ZORJl0ZyEJCLmdjoidH/GlLRX7nSDJ1X5M0vZ9iZ5nOheku1cNl9cGYUjyHAoYJhnh0wyl4r3Boxn4tWe3DW/OOmFIhpxkfDCVTeyWux5KZwzprpDKwMw8J31vgY6pQFRnoh/Nw0R0aNyjgdAhgdzz0vr726vr0F0IJmJ3CDdcBXyZba63TTxQiuvzAY0c/qA5w+LK8KSNBHbznzQHnaER9gDxlidE8WNVOjckiIduK1w4dMr8wU2v137emeKLPzScdOF/IiNmPKjj2T/9myd+N3MfjvORjfWS0eEP76V78Y5VoJmI+m+G6hCZWspCjb0IGBnTSmPcFpS+Up/WoL7m9mx7kA="  # Temporary session token

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
