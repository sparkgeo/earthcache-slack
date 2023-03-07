import boto3
import json
import logging
import os


WORKER_ARN = os.environ["WORKER_ARN"]

boto3_lambda_client = boto3.client("lambda")

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def respond(err, res=None):
    return {
        "statusCode": "400" if err else "200",
        "headers": {
            "Content-Type": "application/json",
        },
    }


def lambda_handler(event, context):
    boto3_lambda_client.invoke(
        FunctionName=WORKER_ARN,
        InvocationType="Event",
        LogType="None",
        Payload=json.dumps(event),
    )

    return respond(None, event)
