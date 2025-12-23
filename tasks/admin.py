from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    This controls how tasks appear in Django admin panel.
    It's like customizing how data shows in Excel.
    """
    list_display = ['title', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at']
    
    # This will trigger Slack notification when task is saved
    def save_model(self, request, obj, form, change):
        """Called when you save a task in admin"""
        super().save_model(request, obj, form, change)
        # We'll add Slack notification here later
        from .utils import send_task_to_slack
        if not change:  # Only for new tasks
            send_task_to_slack(obj)