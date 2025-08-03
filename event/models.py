from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1, related_name='organized_events')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, through='RSVP', related_name='events_attending')
    image = models.ImageField(upload_to='event_images/', default='default-event.jpg')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_upcoming(self):
        return self.date >= timezone.now().date()

    def __str__(self):
        return self.title

class RSVP(models.Model):
    class Status(models.TextChoices):
        GOING = 'going', 'Going'
        NOT_GOING = 'not_going', 'Not Going'
        MAYBE = 'maybe', 'Maybe'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.GOING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.status})"