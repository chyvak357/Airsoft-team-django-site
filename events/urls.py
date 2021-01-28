from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeEvents.as_view(), name='events_home'),
    path('event/<int:pk>/', ViewEvents.as_view(), name='view_events'),
    path('event/register/<int:pk>/', ViewUserEvent.as_view(), name='events_register'),

]