from django.db import models

class Task(models.Model):
    """
    A Task model that stores task information and status.
    Think of this as a single row in a spreadsheet.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', 'New'),
            ('accepted', 'Accepted')
        ],
        default='new'
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """This makes the task show nicely in admin panel"""
        return f"{self.title} - {self.status}"
    
    class Meta:
        ordering = ['-created_at']  # Newest first