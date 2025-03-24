import boto3
import os
from django.conf import settings
from datetime import datetime

# 🔹 Replace with actual AWS values from Learner Lab
AWS_ACCESS_KEY = "ASIATUYJP7SUGFXOQCU2"
AWS_SECRET_KEY = "KoFx8yftdkdDgCQemzCqKnU/kYxBrrUHuk+Y4TO4"
AWS_SESSION_TOKEN = "IQoJb3JpZ2luX2VjEJX//////////wEaCXVzLWVhc3QtMSJIMEYCIQCWygy1TVAh1Q7pN1fdCPXGR0oxDBpsg+Tz11Za4rYiDQIhANcNhA8Ab5FDvqDeISlAwHRyoSUe2o9z5IKIBCkbAFoVKokECO7//////////wEQAxoMMjUwNzM4NjM3OTkyIgxuuJZrUeBql1jMFJcq3QM5tpQ0VdXUlObGYRSAYHPRpp6Sm1yfDoFwIt3+JAyKUQNlYQeWzetn95jXPTyiWZ/psmiQ28JSy0P4zWrTDszKgV9nnAen/HfvoGdEXDeoykHVOCuaIRNHzBY0Wo8Hc/sHR9GtFV/lYrl1FIfe9MsG6w+SESmTQFwhEmyX7liJxKe+jPOxse1d9opmGivXtFwGyFqIJUiZ3tAX7hCw2pcMVmgHdZXbG+CVHJINWpaAoY9Pnzg8AU2Ztvo8sygrEM0MhyMgwuNmWv2ZK2qQukYB8suqZ66M70RM2NUazyDJUG/V2suQb1F1/6ZB2j3LVdy8kIyYfGB4so+ahFl39R2GtO5f1iw04MT181kaP7KblrulTNoPY6eSn8wj+XJIzt7kqlGsaB4Pq76JKRz4OnNE+BAbz+LA6b32T6qlTNnei14xTy6qN8/Xiae1I4tjv15Er89aGFIPNB6n2Fca7WWEBxjn/Xg8ulIlgu4FIFyVnXpWvjCgtUw2SLIihhsRmm8HpFZeTZRQGp2fJVEQRfzYe+GVgApUXq6Xf4aThaIgK2ZncqTNjf0xmxl3Vsq3zO8RCvMRuAyOJPthU/Vb5okMJNAN1Xko1+GyX/jecd3RppvKVyvyqQ+aR3FpqGowsqKFvwY6pQEoc2eR/Fg3DLHJxSUr9QgJe3N4eZWjdc8CK0U1NJ3+GWHVS58UolsS8dhjRr2D6cIE7WTjepXwaKnZSiJduNrz2fH9lnRFiYlI9GKxv5u5fURDr0gMUaa9LBtAqzckCirSnJP9bbGePI6IiOVgyKy9dGmX5sHvbzu4mE3YIn8NJYJKPnD4DxyU9/6r9AkZyzDcdcQaYakparWorjE6/uqlOeaECc4=" # Temporary session token

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
