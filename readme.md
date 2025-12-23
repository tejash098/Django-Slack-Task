# Django + Slack Two-Way Integration

A simple Django app that demonstrates two-way communication with Slack. Create tasks in Django, send them to Slack, and let users interact with them directly from Slack!

**Prerequisites**

- Python 3.10+ (3.11 recommended)
- Git
- A Slack workspace where you can create an app
- ngrok (for local Slack event delivery)

**Quick glossary**

- Django: Python web framework running the app.
- Webhook: An HTTP endpoint Slack uses to send events.
- ngrok: Tool to expose your local server to the internet (used for Slack callbacks).

---

## Setup (Beginner-friendly)

Follow the steps below. Commands use Windows examples first, then macOS/Linux variations where they differ.

1. Clone repository

```bash
git clone <your-repo-url>
cd taskproject
```

2. Create and activate Python virtual environment

Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

Windows (cmd.exe):

```cmd
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Configure local settings and secrets

Create a file `taskproject/settings_local.py` (this file should NOT be checked into source control). Example minimal contents:

```python
# taskproject/settings_local.py
SECRET_KEY = 'replace-with-a-secure-secret'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Slack configuration (see Slack setup steps below)
SLACK_SIGNING_SECRET = 'your-signing-secret'
SLACK_BOT_TOKEN = 'xoxb-...'
SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/xxxxx/xxxxx/xxxxx'

```

Add `taskproject/settings_local.py` to `.gitignore` if it's not already there.

5. Run migrations and create an admin user

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

6. Start the Django development server

```bash
python manage.py runserver 8000
```

If you see `Starting development server at http://127.0.0.1:8000/` you're good to go.

---

## Expose your local server with ngrok (for Slack callbacks)

1. Download ngrok from https://ngrok.com and install it.
2. Start a tunnel to port 8000:

```bash
ngrok http 8000
```

3. Copy the HTTPS forwarding URL (example `https://abc123.ngrok.io`).

Keep ngrok running while you test Slack interactions.

---

## Slack App Setup (step-by-step)

1. Create a Slack app at https://api.slack.com/apps (choose a workspace you can manage).
2. Under "OAuth & Permissions" add the following Bot Token Scopes (at minimum):

- `chat:write` — send messages as the app
- `commands` — (if you later add slash commands)

3. Install the app to your workspace and copy the Bot User OAuth Token (starts with `xoxb-`).
4. Under "Basic Information" or the App credentials, note the Signing Secret.
5. Under "Interactivity & Shortcuts" enable Interactivity and set the Request URL to:

```
<your-ngrok-url>/slack/actions/
```

Example: `https://abc123.ngrok.io/slack/actions/`

6. (Optional) If the project uses slash commands or events, wire those up in the Slack app config to the appropriate endpoints (see code comments in `tasks/views.py`).

7. Ensure `SLACK_SIGNING_SECRET`, `SLACK_BOT_TOKEN`, and `SLACK_WEBHOOK_URL` (if used) are present in `taskproject/settings_local.py` or in your environment.

---

## Project structure (key files)

```
taskproject/              # Django project
├─ settings.py             # Base settings
├─ settings_local.py*      # Local secrets (create this)
tasks/                    # App that models tasks and Slack handlers
├─ models.py               # Task model
├─ views.py                # Slack action endpoints
├─ utils.py                # Slack helper functions
├─ admin.py                # Admin configuration
manage.py                 # Django CLI
requirements.txt          # Python dependencies
db.sqlite3                # SQLite database (local)
```
---

## Running tests and verification

Run unit tests (if any):

```bash
python manage.py test
```

Manual verification steps:

1. Start Django server and ngrok as above.
2. Create a task in Django admin (`http://127.0.0.1:8000/admin`).
3. Confirm a Slack message appears in the configured channel.
4. Click a button in Slack and confirm the change shows up in Django.

---

## Useful commands reference

```bash
# Run development server
python manage.py runserver 8000

# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Run tests
python manage.py test
```
---