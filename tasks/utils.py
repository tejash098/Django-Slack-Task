import requests
from django.conf import settings

def send_task_to_slack(task):
    """
    Sends a task notification to Slack with interactive buttons.
    
    Think of this as composing a rich message with buttons,
    similar to an email with action buttons.
    """
    
    # This is the structure Slack expects (called Block Kit)
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",  # Markdown formatting
                    "text": f"*🆕 New Task Created*\n\n*Title:* {task.title}\n*Description:* {task.description or 'No description'}"
                }
            },
            {
                "type": "divider"  # A horizontal line
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
                        "style": "primary",  # Makes it blue
                        "value": str(task.id),  # Task ID for reference
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
        response = requests.post(
            settings.SLACK_WEBHOOK_URL,
            json=payload,
            timeout=5
        )
        
        if response.status_code == 200:
            print(f"✅ Task sent to Slack: {task.title}")
        else:
            print(f"❌ Slack error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Failed to send to Slack: {str(e)}")