import uuid
from django.db import models


class ChatRoom(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, db_index=True) #  Cookie'den gelecek UUID
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.session_id} - {self.timestamp}"


class ChatLog(models.Model):
    room = models.ForeignKey('chatwithme.ChatRoom', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20)


class MeetingModel(models.Model):
    meeting_id = models.UUIDField(default=uuid.uuid4, db_index=True)
    title = models.CharField(max_length=255)
    notes = models.TextField(max_length=1000, blank=True, default='')
    email = models.EmailField()
    date = models.DateTimeField()
