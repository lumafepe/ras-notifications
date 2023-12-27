from django.db import models
import uuid
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# Create your models here.


class CustomUserManager(models.Manager):
    def get_or_create_user(self, id:str):
        if self.filter(id=id).exists():
            return self.get(id=id)
        else:
            return self.create(id=id)
        
    def get_email(self, user_id):
        try:
            """
            #TODO:: change this
            # Assuming your user API endpoint is at 'Users/id/'
            response = requests.get(f'http://example.com/Users/{user_id}/')  # Replace 'example.com' with your actual domain
            response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)

            user_data = response.json()
            return user_data.get('email')
            """
            return "lumafepe@gmail.com"
        except requests.exceptions.RequestException as e:
            # Handle request errors (e.g., connection error, timeout)
            return None

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    objects = CustomUserManager()
    
class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
class CustomUserNotificationManager(models.Manager):
    def create_user_notification(self,users:list[str],title:str,subject:str,message:str):
        notification = Notification.objects.create(message=message)
        for user_id in users:
            # Send notification to the user's WebSocket group
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'user_{user_id}',
                {
                    'type': 'send_notification',
                    'data': {
                        "title":title,
                        "subject":subject,
                        "description":message,
                        "timestamp":int(notification.timestamp.timestamp())
                    }
                }
            )
        users = [ User.objects.get_or_create_user(user) for user in users ]
        for user in users:
            self.create(user=user,notification=notification)
        return notification

class UserNotification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    class Meta:
        unique_together = ('user', 'notification')
        
    objects = CustomUserNotificationManager()