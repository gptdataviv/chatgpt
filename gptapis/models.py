from django.db import models

# Create your models here.

class RequestsData(models.Model):
    request_time = models.DateTimeField(auto_now_add=True)
    request_data = models.TextField()
    response_data = models.TextField()

class ChatData(models.Model):
    chat_id = models.IntegerField(auto_now_add=True)
    user_id = models.IntegerField()
    chat_data = models.TextField()
    updated_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request ID: {self.id}"