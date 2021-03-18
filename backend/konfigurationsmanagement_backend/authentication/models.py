from django.db import models
from django.contrib.auth.models import User

class DashboardEntry(models.Model):
    type_id = models.IntegerField()
    message = models.TextField()
    timestamp = models.DateField()
    editor = models.ForeignKey(User, on_delete=models.CASCADE)

    def as_json(self):
        return {
            'dashboard_entry_id': self.id,
            'type_id': self.type_id,
            'message': self.message,
            'timestamp': self.timestamp,
            'editor': self.editor.additionaluserinformation.as_json()
        }

    def as_json_without_time(self):
        return {
            'dashboard_entry_id': self.id,
            'type_id': self.type_id,
            'message': self.message,
            'editor': self.editor.additionaluserinformation.as_json()
        }


class Role(models.TextChoices):
    USER = 'USER'
    ADMIN = 'ADMIN'


class AdditionalUserInformation(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(choices=Role.choices, default=Role.USER, max_length=30)
    socket_id = models.CharField('socket_id', unique=False, max_length=30, default="no_socket")
    dashboard = models.ManyToManyField(DashboardEntry, symmetrical=False)

    def as_json(self):
        return {
            'user_id': self.user.id,
            'username': self.user.username,
            'role': self.role
        }

    def as_json_detail(self):
        return {
            'user_id': self.user.id,
            'username': self.user.username,
            'role': self.role,
            'socket_id': self.socket_id
        }
