from django.urls import path
from .views import *

urlpatterns = [
    # path('register/', register, name='register'),
    # path('login/', user_login, name='login'),
    # path('logout/', user_logout, name='logout'),

    path('', test, name='test'),
    # path('', HomeNews.as_view(), name='home'),


]