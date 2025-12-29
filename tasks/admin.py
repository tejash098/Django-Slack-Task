from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        from .utils import send_task_to_slack
        if not change:
            send_task_to_slack(obj)