# Django + Slack Two-Way Integration

A simple Django app that demonstrates two-way communication with Slack. Create tasks in Django, send them to Slack, and let users interact with them directly from Slack!

## Features

- 📤 Send task notifications to Slack
- ✅ Accept tasks with a button click
- 💬 Add comments via Slack modal
- 🔄 Real-time updates back to Django

## Setup Instructions

### 1. Clone and Setup Django

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

### 2. Configure Slack

1. Create Slack App at https://api.slack.com/apps
2. Enable "Incoming Webhooks" and add webhook to your workspace
3. Copy the Webhook URL
4. Enable "Interactivity & Shortcuts"
5. Add Bot Token Scopes: `chat:write`, `incoming-webhook`
6. Install app to workspace

### 3. Configure Django

Create `taskproject/settings_local.py`:

```python
SLACK_WEBHOOK_URL = "your-webhook-url-here"
```

**Important:** Add `settings_local.py` to `.gitignore`!

### 4. Setup ngrok

```bash
# Download from https://ngrok.com
# Start tunnel
ngrok http 8000
```

Copy the ngrok URL (e.g., `https://abc123.ngrok.io`)

### 5. Update Slack Interactivity URL

In your Slack app settings:
- Go to "Interactivity & Shortcuts"
- Set Request URL to: `https://your-ngrok-url.ngrok.io/slack/actions/`

### 6. Run the Application

```bash
# Terminal 1: Django server
python manage.py runserver

# Terminal 2: ngrok
ngrok http 8000
```

## Usage

1. Login to Django admin: `http://127.0.0.1:8000/admin`
2. Create a new task
3. Check your Slack channel for the notification
4. Click "Accept" or "Comment" buttons
5. Verify changes in Django admin

## Project Structure

```
django-slack-integration/
├── taskproject/          # Django project settings
├── tasks/               # Main app
│   ├── models.py        # Task model
│   ├── views.py         # Slack action handlers
│   ├── utils.py         # Slack utility functions
│   └── admin.py         # Admin configuration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Testing Checklist

- [ ] Create task in Django admin
- [ ] Slack message appears with buttons
- [ ] Accept button updates task status
- [ ] Comment button opens modal
- [ ] Comment saves to database

## Troubleshooting

**Message not appearing in Slack?**
- Check `SLACK_WEBHOOK_URL` in `settings_local.py`
- Verify the webhook is active in Slack app settings

**Buttons not responding?**
- Verify ngrok is running
- Check Slack app "Interactivity" URL is correct
- Look at Django console for errors

**Modal not opening?**
- Check Slack app has `chat:write` permission
- Verify the action_id matches in code

## Learn More

- [Slack API Documentation](https://api.slack.com/)
- [Django Documentation](https://docs.djangoproject.com/)
- [Block Kit Builder](https://api.slack.com/block-kit) - Design Slack messages

## Author

Built as an intern learning project to understand:
- REST APIs
- Webhooks
- Event-driven architecture
- Third-party integrations