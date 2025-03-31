from django.db import models
from django.contrib.auth.models import User


class Summary(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='summaries')
    user_title = models.CharField(max_length=255)
    user_description = models.TextField(blank=True, null=True)
    youtube_url = models.URLField()
    video_title = models.CharField(max_length=255)
    summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Summary for {self.video_title} by {self.user.username}"
