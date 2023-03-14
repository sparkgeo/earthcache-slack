# SkyWatch EarthCache Slack Webhook CDK Template

This is an [AWS CDK](https://aws.amazon.com/cdk/) template for creating a service that receives outgoing subscription messages from [SkyWatch EarthCache](https://skywatch.com/earthcache/) and sends block-formatted messages to a [Slack](https://slack.com/) incoming webhook app.

## Setup and Usage

1. Create a [Slack webhook app](https://api.slack.com/messaging/webhooks). You will create a `Webhook URL` and install the app to a channel in your Slack workspace.
2. Set environment variables like those found in `.envrc_template`:
  - SKYWATCH_API_KEY = your SkyWatch EarthCache API key
  - SLACK_WEBHOOK_URL = Slack webhook URL created above, starting with `/services/...`
3. Synth (`cdk synth`) and deploy (`cdk deploy`) the CDK stack within this repo, which creates an [API Gateway](https://aws.amazon.com/api-gateway/) and a [Lambda Function](https://aws.amazon.com/lambda/) in your authenticated AWS account.
4. Once the stack has been created, use the output API Gateway URL + Lambda Function name as the `callback_uri` when creating a subscription to SkyWatch EarthCache.
