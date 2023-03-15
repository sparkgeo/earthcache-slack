import os
from aws_cdk import (
    core,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
)


class SlackAppStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        main_handler = lambda_.Function(
            self,
            "main-lambda-handler",
            function_name="earthcache-slack-lambda",
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.from_asset("resources"),
            handler="main_handler.lambda_handler",
            environment=dict(
                SKYWATCH_API_KEY=os.environ["SKYWATCH_API_KEY"],
                SLACK_WEBHOOK_URL=os.environ["SLACK_WEBHOOK_URL"],
            ),
        )

        api = apigateway.RestApi(
            self,
            "earthcache-slack-api",
            rest_api_name="EarthCache Slack API Service",
            description="This service receives webhooks messages from SkyWatch EarthCache and produces Slack messages.",
            default_cors_preflight_options={"allow_origins": ["*"]},
        )

        post_slack_integration = apigateway.LambdaIntegration(
            main_handler,
            request_templates={"application/json": '{ "statusCode": "200" }'},
        )

        api.root.add_method("POST", post_slack_integration)
