# Basic Slack Slash Command CDK Template

This is a basic AWS CDK template for creating a simple Slack slash command backend.

The app in this template will display a modal window containing a text box. When submitted, the contents of the text box will be displayed within the Slack channel as an ephemeral message.

## Setup

1. Create a [Slack slash command](https://api.slack.com/interactivity/slash-commands). The `Request Url` will be created through CDK (you will have to edit the request url in the slash command UI manually, later). This template also makes use of Interactivity (a modal window), which you can enable and set to the same url, later.
2. Set environment variables like those found in `.envrc_template`. Notably, `SLACK_BEARER_TOKEN` corresponds to the `Bot User OAuth Token` found in the app UI, once installed to your Slack workspace.
3. Synth (`cdk synth`) and deploy (`cdk deploy`) the CDK stack within this repo, which creates an API Gateway, and two Lambda Functions. There is a high probability you will also have to add several permissions to the IAM Role(s).
4. Once the stack has been created, edit the slash command request url and interactivity request url to match the created API Gateway endpoint.

## Usage

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

- `cdk ls` list all stacks in the app
- `cdk synth` emits the synthesized CloudFormation template
- `cdk deploy` deploy this stack to your default AWS account/region
- `cdk diff` compare deployed stack with current state
- `cdk docs` open CDK documentation

Enjoy!
