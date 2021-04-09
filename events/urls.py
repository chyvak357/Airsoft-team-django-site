from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeEvents.as_view(), name='events_home'),
    path('user-events/', HomeEvents.as_view(), name='user_events_list'),
    path('event/<int:pk>/', ViewEvents.as_view(), name='view_events'),

    path('event/<int:pk>/user-table',  EventUsersList.as_view(), name='view_event_users'),

    path('event/register/<int:pk_event>/reg', register_event, name='events_register'),  # регистрация игрока на игру
    path('event/register/<int:pk_event>/cancel', register_cancel_visit, name='events_cancelVisit'),  # Отметить неявку на игру. В get должен быть id пользователя

    # Для получения данных
    path('event/<int:pk>/users-list', EventUsersListTest.as_view(), name='view_event_users_data')  # Список пользователь на меро

    # path('event/test', test, name='test_page'),

]