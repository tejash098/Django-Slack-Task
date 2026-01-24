import json
import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import Task


@csrf_exempt
@require_POST
def slack_actions(request):

    payload = json.loads(request.POST.get("payload","{}"))
    payload_type = payload.get("type")

    if payload_type == "block_actions":
        return handle_button_click(payload)

    elif payload_type == "view_submission":
        return handle_modal_submission(payload)

    return JsonResponse({"status":"ignored"})


def handle_button_click(payload):

    action = payload["actions"][0]
    task_id = action["value"]
    action_id = action["action_id"]
    user = payload["user"]["username"]

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"text":"Task not found"})

    if action_id == "accept_task":
        task.status = "accepted"
        task.save()
        requests.post(
            settings.SLACK_WEBHOOK_URL,
            json={
                "text": f"Task *{task.title}* has been accepted by @{user}."
            },
            timeout=5
        )

        return JsonResponse({
            "replace_original": True,
            "blocks":[{
                "type":"section",
                "text":{"type":"mrkdwn",
                "text":f"*Task Accepted*\n*{task.title}*\nAccepted by @{user}"}
            }]
        })

    if action_id == "comment_task":

        modal = {
            "type":"modal",
            "title":{"type":"plain_text","text":"Add Comment"},
            "submit":{"type":"plain_text","text":"Save"},
            "blocks":[
                {"type":"input",
                 "block_id":"comment_block",
                 "element":{"type":"plain_text_input","action_id":"comment_input","multiline":True},
                 "label":{"type":"plain_text","text":"Comment"}
                }],
            "private_metadata": task_id
        }

        requests.post(
            "https://slack.com/api/views.open",
            headers={"Authorization":f"Bearer {settings.SLACK_BOT_TOKEN}",
                     "Content-Type":"application/json"},
            json={"trigger_id":payload["trigger_id"],"view":modal}
        )

        return HttpResponse(status=200)

    return JsonResponse({"status":"ok"})


def handle_modal_submission(payload):

    task_id = payload["view"]["private_metadata"]
    values = payload["view"]["state"]["values"]
    comment = values["comment_block"]["comment_input"]["value"]
    user = payload["user"]["username"]

    task = Task.objects.get(id=task_id)
    task.comment = f"Comment by @{user}:\n{comment}"
    task.save()

    return JsonResponse({"response_action":"clear"})
