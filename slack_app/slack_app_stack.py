import os
from aws_cdk import (
    core,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    aws_iam as iam,
)


class SlackAppStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        worker_handler = lambda_.Function(
            self,
            "worker-lambda-handler",
            function_name="slack-worker-lambda",
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.from_asset("resources"),
            handler="worker_handler.lambda_handler",
            environment=dict(
                SLACK_BEARER_TOKEN=os.environ["SLACK_BEARER_TOKEN"],
            ),
        )

        main_handler = lambda_.Function(
            self,
            "main-lambda-handler",
            function_name="slack-main-lambda",
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.from_asset("resources"),
            handler="main_handler.lambda_handler",
            environment=dict(
                WORKER_ARN=worker_handler.function_arn,
            ),
        )

        main_handler.add_to_role_policy(
            statement=iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["lambda:InvokeFunction"],
                resources=[worker_handler.function_arn],
            )
        )

        api = apigateway.RestApi(
            self,
            "slack-app-api",
            rest_api_name="Slack App API Service",
            description="This service serves accepts Slack slash command requests and responds with modals/messages.",
            default_cors_preflight_options={"allow_origins": ["*"]},
        )

        post_slack_integration = apigateway.LambdaIntegration(
            main_handler,
            request_templates={"application/json": '{ "statusCode": "200" }'},
        )

        api.root.add_method("POST", post_slack_integration)
