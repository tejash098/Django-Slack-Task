import requests
from django.conf import settings

def send_task_to_slack(task):
    # This is the structure Slack expects (called Block Kit)
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*New Task Created*\n\n*Title:* {task.title}\n*Description:* {task.description or 'No description'}"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "✅ Accept"
                        },
                        "style": "primary", 
                        "value": str(task.id), 
                        "action_id": "accept_task"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "💬 Comment"
                        },
                        "value": str(task.id),
                        "action_id": "comment_task"
                    }
                ]
            }
        ]
    }
    
    try:
        requests.post(
            settings.SLACK_WEBHOOK_URL,
            json=payload,
            timeout=5
        )
            
    except Exception as e:
        print(f"Failed to send to Slack: {str(e)}")