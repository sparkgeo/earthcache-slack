import base64
import json
import os

import urllib.parse
import urllib
from urllib import request, parse

SLACK_BEARER_TOKEN = os.environ["SLACK_BEARER_TOKEN"]


def create_modal(body, bearer_token):
    """Create a modal in Slack"""

    req = request.Request(
        "https://slack.com/api/views.open", data=json.dumps(body).encode("utf-8")
    )
    req.add_header("Content-Type", "application/json; charset=utf-8")
    req.add_header("Authorization", f"Bearer {bearer_token}")
    request.urlopen(req)


def create_message(url, body):
    """Send a message to Slack"""

    req = request.Request(url, data=json.dumps(body).encode("utf-8"))
    req.add_header("Content-Type", "application/json; charset=utf-8")
    request.urlopen(req)


def lambda_handler(event, context):
    body_dict = urllib.parse.parse_qs(event.get("body"))

    payload_dict = {}
    if body_dict.get("payload"):
        payload_dict = json.loads(body_dict.get("payload")[0])

    if body_dict.get("command"):
        """If the request body contains key 'command', it is
        directly from the slash command."""

        trigger_id = body_dict.get("trigger_id")[0]
        response_url = body_dict.get("response_url")[0]

        body = {
            "trigger_id": trigger_id,
            "view": {
                "type": "modal",
                "callback_id": "shortcut_modal",
                "title": {"type": "plain_text", "text": "Slash Command Example"},
                "submit": {"type": "plain_text", "text": "Submit"},
                "close": {"type": "plain_text", "text": "Cancel"},
                "blocks": [
                    {
                        "type": "input",
                        "element": {"type": "plain_text_input", "multiline": True},
                        "label": {
                            "type": "plain_text",
                            "text": "Text Content",
                            "emoji": True,
                        },
                        "block_id": "content_text",
                    },
                ],
                "private_metadata": response_url,
            },
        }
        create_modal(body, SLACK_BEARER_TOKEN)

    elif body_dict.get("payload"):
        """Interaction payloads contain key 'payload'"""

        response_url = payload_dict["view"]["private_metadata"]

        if payload_dict.get("type") == "view_submission":
            """View submission payloads are sent on submit button click"""
            state = payload_dict["view"]["state"]["values"]
            text_content = state["content_text"][list(state["content_text"].keys())[0]][
                "value"
            ]

            payload = {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "plain_text",
                            "text": text_content,
                            "emoji": True,
                        },
                    }
                ],
                "response_type": "ephemeral",
            }

            create_message(response_url, payload)

    return {"statusCode": 200}
