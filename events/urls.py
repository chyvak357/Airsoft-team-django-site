from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeEvents.as_view(), name='events_home'),
    path('user-events/', HomeEvents.as_view(), name='user_events_list'),
    path('event/<int:pk>/', ViewEvents.as_view(), name='view_events'),
    path('event/<int:pk>/user-table',  EventUsersList.as_view(), name='view_event_users'),
    path('event/register/<int:pk_event>/reg', register_event, name='events_register'),
    path('event/register/<int:pk_event>/<int:pk_reg>/cancel', register_cancel, name='events_cancel'),

]