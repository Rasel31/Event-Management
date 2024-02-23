from django.urls import path
from .views import home_view, EventDetail, EventList, EventPDFView, reply_event, event_create_view, MyEventList,\
    EventDelete, EventUpdateView, ArchivedEventList

app_name = 'swehome'

urlpatterns = [
    path('', home_view, name='home'),
    path('events/create-event/', event_create_view, name='event-create'),
    path('events/', EventList.as_view(), name='event-list'),
    path('events/archived-events/', ArchivedEventList.as_view(), name='archived-event-list'),
    path('events/my-event-list/', MyEventList.as_view(), name='my-event-list'),
    path('events/<slug:slug>/detail/', EventDetail.as_view(), name='event-detail'),
    path('events/<slug:slug>/update/', EventUpdateView.as_view(), name='event-update'),
    path('events/<slug:slug>/delete', EventDelete.as_view(), name='event-delete'),
    path('events/<slug:slug>/detail/reply/', reply_event, name='event-reply'),
    path('events/<slug:slug>/pdf-form/', EventPDFView.as_view(), name='event-form'),
]


