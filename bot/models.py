from django.db import models


class FAQ(models.Model):
    Question=models.CharField(max_length=300)
    Answer=models.CharField(max_length=300)

    def __str__(self):
        return self.Question


class ChatReplyLog(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    session_key = models.CharField(max_length=64, blank=True)
    user_message = models.TextField(blank=True)
    bot_reply = models.TextField()
    match_source = models.CharField(max_length=30, default='fallback')
    confidence = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.match_source} ({self.confidence:.2f})"
