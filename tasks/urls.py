from django.urls import path
from . import views

urlpatterns = [
    path('slack/actions/', views.slack_actions, name='slack_actions'),
    path('health/', views.health_check, name='health_check'),
]