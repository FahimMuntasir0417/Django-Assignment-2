from django.contrib import admin

# Register your models here.

from .models import Event, RSVP, Category

admin.site.register(Event)
admin.site.register(RSVP)
admin.site.register(Category)