import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Task

@csrf_exempt  # Slack doesn't send CSRF tokens
@require_POST  # Only accept POST requests
def slack_actions(request):
    """
    This function handles ALL button clicks from Slack.
    
    When someone clicks a button in Slack, Slack sends data here.
    We check what button was clicked and respond accordingly.
    """
    
    try:
        # Slack sends data in a field called 'payload'
        payload_str = request.POST.get('payload')
        
        if not payload_str:
            print("❌ No payload received")
            return JsonResponse({'error': 'No payload'}, status=400)
        
        # Convert from text to Python dictionary
        payload = json.loads(payload_str)
        
        # Debug: Print what we received
        print(f"📥 Received payload type: {payload.get('type')}")
        
        # Check what type of interaction this is
        payload_type = payload.get('type')
        
        # Handle button clicks
        if payload_type == 'block_actions':
            return handle_button_click(payload)
        
        # Handle modal submissions (for comments)
        elif payload_type == 'view_submission':
            return handle_modal_submission(payload)
        
        # Unknown type
        print(f"⚠️ Unknown payload type: {payload_type}")
        return JsonResponse({'status': 'ok'})
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
    except Exception as e:
        print(f"❌ Error in slack_actions: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


def handle_button_click(payload):
    """
    Called when someone clicks Accept or Comment button.
    """
    
    try:
        # Get the first action (button clicked)
        action = payload['actions'][0]
        action_id = action['action_id']
        task_id = action['value']
        
        # Get the user who clicked
        user = payload['user']['username']
        
        print(f"👤 User {user} clicked {action_id} for task {task_id}")
        
        # Get the task from database
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            print(f"❌ Task {task_id} not found")
            return JsonResponse({
                'response_type': 'ephemeral',
                'text': '❌ Task not found!'
            })
        
        # Handle "Accept" button
        if action_id == 'accept_task':
            task.status = 'accepted'
            task.save()
            
            print(f"✅ Task {task_id} accepted by {user}")
            
            # Return updated message
            return JsonResponse({
                'replace_original': True,
                'blocks': [
                    {
                        'type': 'section',
                        'text': {
                            'type': 'mrkdwn',
                            'text': f'✅ *Task Accepted!*\n\n*Title:* {task.title}\n*Description:* {task.description or "No description"}\n*Accepted by:* @{user}'
                        }
                    }
                ]
            })
        
        # Handle "Comment" button - open a modal
        elif action_id == 'comment_task':
            print(f"💬 Opening comment modal for task {task_id}")
            
            # Get the trigger_id from payload (needed to open modals)
            trigger_id = payload.get('trigger_id')
            
            if not trigger_id:
                print("❌ No trigger_id in payload - cannot open modal")
                return JsonResponse({
                    'response_type': 'ephemeral',
                    'text': '❌ Could not open modal (no trigger_id)'
                })
            
            # Open modal using Slack API
            from django.conf import settings
            import requests
            
            modal_view = {
                'type': 'modal',
                'callback_id': 'comment_modal',
                'title': {
                    'type': 'plain_text',
                    'text': '💬 Add Comment'
                },
                'submit': {
                    'type': 'plain_text',
                    'text': 'Save Comment'
                },
                'close': {
                    'type': 'plain_text',
                    'text': 'Cancel'
                },
                'blocks': [
                    {
                        'type': 'section',
                        'text': {
                            'type': 'mrkdwn',
                            'text': f'*Task:* {task.title}'
                        }
                    },
                    {
                        'type': 'input',
                        'block_id': 'comment_block',
                        'element': {
                            'type': 'plain_text_input',
                            'action_id': 'comment_input',
                            'multiline': True,
                            'placeholder': {
                                'type': 'plain_text',
                                'text': 'Enter your comment here...'
                            }
                        },
                        'label': {
                            'type': 'plain_text',
                            'text': 'Comment'
                        }
                    }
                ],
                'private_metadata': str(task_id)
            }
            
            # Call Slack API to open modal
            try:
                response = requests.post(
                    'https://slack.com/api/views.open',
                    headers={
                        'Authorization': f'Bearer {settings.SLACK_BOT_TOKEN}',
                        'Content-Type': 'application/json'
                    },
                    json={
                        'trigger_id': trigger_id,
                        'view': modal_view
                    }
                )
                
                result = response.json()
                
                if result.get('ok'):
                    print(f"✅ Modal opened successfully")
                    return HttpResponse(status=200)  # Just return 200, modal is already open
                else:
                    print(f"❌ Slack API error: {result.get('error')}")
                    return JsonResponse({
                        'response_type': 'ephemeral',
                        'text': f'❌ Error opening modal: {result.get("error")}'
                    })
                    
            except Exception as e:
                print(f"❌ Exception opening modal: {e}")
                import traceback
                traceback.print_exc()
                return JsonResponse({
                    'response_type': 'ephemeral',
                    'text': f'❌ Error: {str(e)}'
                })
        
        # Unknown action
        print(f"⚠️ Unknown action: {action_id}")
        return JsonResponse({'status': 'ok'})
        
    except Exception as e:
        print(f"❌ Error in handle_button_click: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'response_type': 'ephemeral',
            'text': f'❌ Error: {str(e)}'
        })


def handle_modal_submission(payload):
    """
    Called when someone submits the comment modal.
    """
    
    try:
        # Get task ID from private_metadata
        task_id = payload['view']['private_metadata']
        
        # Extract the comment text
        values = payload['view']['state']['values']
        comment = values['comment_block']['comment_input']['value']
        
        # Get the user
        user = payload['user']['username']
        
        print(f"💬 Saving comment from {user} for task {task_id}")
        
        # Get and update task
        try:
            task = Task.objects.get(id=task_id)
            
            # Add comment with username
            task.comment = f"Comment by @{user}:\n{comment}"
            task.save()
            
            print(f"✅ Comment saved for task {task_id}")
            
            # Close the modal
            return JsonResponse({
                'response_action': 'clear'
            })
            
        except Task.DoesNotExist:
            print(f"❌ Task {task_id} not found")
            return JsonResponse({
                'response_action': 'errors',
                'errors': {
                    'comment_block': 'Task not found'
                }
            })
            
    except Exception as e:
        print(f"❌ Error in handle_modal_submission: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'response_action': 'errors',
            'errors': {
                'comment_block': str(e)
            }
        })


@csrf_exempt
def health_check(request):
    """
    Visit this URL to verify Django is running.
    """
    return JsonResponse({
        'status': 'ok',
        'message': 'Django + Slack integration is running!'
    })