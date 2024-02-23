from django.contrib import admin
from .models import Event, Comment
# Register your models here.


class EventAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'approved'
    ]

    class Meta:
        model = Event


admin.site.register(Event, EventAdmin)
admin.site.register(Comment)
