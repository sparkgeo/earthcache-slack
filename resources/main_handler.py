import http.client
import json
import logging
import os


SKYWATCH_API_KEY = os.environ["SKYWATCH_API_KEY"]
SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def respond(err, res=None):
    return {
        "statusCode": "400" if err else "200",
        "headers": {
            "Content-Type": "application/json",
        },
    }


def assemble_download_link(name, url):
    return {
        "type": "section",
        "text": {"type": "mrkdwn", "text": name},
        "accessory": {
            "type": "button",
            "text": {"type": "plain_text", "text": "Download", "emoji": True},
            "value": url,
            "url": url,
        },
    }


def assemble_block(result):
    image_url = result["preview_url"]
    capture_time = result["capture_time"]
    name = result["metadata"]["name"]
    source = result["metadata"]["source"]
    cloud_cover = result["metadata"]["cloud_cover_percentage"]
    resolution_x = result["metadata"]["resolution_x"]
    resolution_y = result["metadata"]["resolution_y"]

    dl_links = []

    for k, v in result.items():
        if k.endswith("_url"):
            dl_links.append(assemble_download_link(k.replace("_url", "").upper(), v))
        elif k.endswith("_files"):
            for f in v:
                dl_links.append(
                    assemble_download_link(
                        f["name"].replace("_", " ").upper(), f["uri"]
                    )
                )

    block = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    f"*{name}*\n"
                    f"Source: {source}\n"
                    f"Capture time: {capture_time}\n"
                    f"Cloud cover: {cloud_cover}%\n"
                    f"Resolution: ({resolution_x}, {resolution_y})"
                ),
            },
            "accessory": {
                "type": "image",
                "image_url": image_url,
                "alt_text": "alt text for image",
            },
        }
    ]

    block += dl_links

    return block


def create_divider():
    return [{"type": "divider"}]


def lambda_handler(event, context):
    print("event", json.dumps(event))
    event = json.loads(event["body"])

    if event["event_name"] == "pipeline-complete-with-results":
        skywatch_endpoint = (
            f"/earthcache/interval_results?pipeline_id={event['data']['id']}"
        )

        skywatch_conn = http.client.HTTPSConnection("api.skywatch.co")
        skywatch_headers = {"x-api-key": SKYWATCH_API_KEY}
        skywatch_conn.request("GET", skywatch_endpoint, "", skywatch_headers)
        res = skywatch_conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))

        results = iter(data["data"][0]["results"])
        blocks = assemble_block(next(results))
        for result in results:
            blocks += create_divider()
            block = assemble_block(result)
            blocks += block

        slack_conn = http.client.HTTPSConnection("hooks.slack.com")
        slack_payload = json.dumps({"blocks": blocks})
        slack_headers = {"Content-Type": "application/json"}
        slack_conn.request("POST", SLACK_WEBHOOK_URL, slack_payload, slack_headers)
        slack_conn.getresponse()
    else:
        print("NO RESULTS")

    return respond(None, event)
