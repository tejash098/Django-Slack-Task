
# Slack App Setup Instructions
---

## 1. Introduction

### What is a Slack App?

A **Slack App** is an application that connects external software with Slack.
It helps other applications communicate with Slack by sending messages, receiving button clicks, and opening forms.

In this project, our **Django application** connects with Slack using a Slack App.

### Why is a Slack App Required?

Our Django project manages tasks. We want Slack to:

* Send task notifications to Slack channels
* Handle button clicks like Accept or Comment
* Open a modal form when the user clicks Comment

To do all this, Slack needs a Slack App that can talk to Django.

---

## 2. Creating a Slack App

### Step 1: Open Slack API Website

1. Open a browser
2. Go to: [https://api.slack.com/apps](https://api.slack.com/apps)
3. Click **Create New App**

---

### Step 2: Choose App Creation Method

1. A popup will appear
2. Select **From scratch**

We choose this option because we are building everything manually.

---

### Step 3: Basic App Details

Fill in the following details:

**App Name**

```
Django Tasks
```

**Workspace**

* Select our Slack workspace
*  We must have permission to install apps

Click **Create App**

After this,  we will be redirected to the app dashboard.

---

## 3. Enable Required Slack Features

### Feature 1: Incoming Webhooks

Incoming Webhooks allow Django to send messages to Slack.

#### Steps

1. In the left sidebar, click **Incoming Webhooks**
2. Turn **Activate Incoming Webhooks** ON
3. Scroll down and click **Add New Webhook to Workspace**
4. Select a Slack channel
5. Click **Allow**

 We will now see a webhook URL like this:

```
https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXX
```

Save this URL.
It will be used in Django settings.

---

### Feature 2: Interactivity and Shortcuts

This feature allows Slack to send button click data back to Django.

#### Steps

1. Click **Interactivity and Shortcuts**
2. Enable **Interactivity**
3. In **Request URL**, enter a temporary URL:

```
https://example.com/slack/actions/
```

4. Click **Save Changes**

This is only a placeholder. We will update it after setting up ngrok.

---

## 4. ngrok Setup (Required for Localhost)

### Why ngrok is Needed

Django runs on:

```
http://localhost:8000
```

Slack cannot access localhost.
ngrok creates a public URL that forwards requests to our local Django server.

---

### Installing ngrok

1. Download ngrok from [https://ngrok.com/download](https://ngrok.com/download)
2. Create a free ngrok account
3. Copy our authentication token from the dashboard

---

### Authenticate ngrok

Run the following command:

```bash
ngrok authtoken YOUR_AUTH_TOKEN
```

---

### Start ngrok

```bash
ngrok http 8000
```

 We will see output like:

```
Forwarding https://abc123.ngrok-free.dev -> http://localhost:8000
```

Copy the **https URL**.

---

### Update Slack Request URL

1. Go back to Slack App dashboard
2. Open **Interactivity and Shortcuts**
3. Replace the old URL with:

```
https://YOUR-NGROK-URL.ngrok-free.dev/slack/actions/
```

Example:

```
https://abc123.ngrok-free.dev/slack/actions/
```

Click **Save Changes**

Note:
Every time ngrok restarts, the URL changes and must be updated in Slack.

---

## 5. OAuth Scopes and Permissions

### What are Scopes?

Scopes define what our Slack App is allowed to do.

---

### Add Required Scopes

1. Click **OAuth and Permissions**
2. Scroll to **Bot Token Scopes**
3. Add the following scopes:

**chat:write**
Used to send messages and open modals

**incoming-webhook**
Used to send webhook messages

After adding scopes, reinstall the app.

---

## 6. Install App to Workspace

1. Go to **OAuth and Permissions**
2. Click **Install to Workspace**
3. Click **Allow**

After installation,  we will see a token like:

```
xoxb-xxxxxxxxxx-xxxxxxxxxx-xxxxxxxxxx
```

Save this token.
It will be used in Django.

---

## 7. Credentials Required for Django

 We should now have:

### Webhook URL

Used for sending messages to Slack

### Bot User OAuth Token

Used for Slack API requests

Add both to `settings_local.py`:

```python
SLACK_WEBHOOK_URL = "our-webhook-url"
SLACK_BOT_TOKEN = "xoxb-our-token"
```

---
