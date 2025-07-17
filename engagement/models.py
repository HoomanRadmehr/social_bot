from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):

    PLATFORM_CHOICES = [
        ('twitter', 'Twitter'),
        ('telegram', 'Telegram'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('linkedin', 'LinkedIn'),
        ('tiktok', 'TikTok'),
    ]

    username = models.CharField(max_length=100, unique=True)
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    follower_count = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profiles")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} on {self.platform}"

class Alert(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    milestone = models.IntegerField()
    triggered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FollowerCountSnapshot(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='snapshots')
    follower_count = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']