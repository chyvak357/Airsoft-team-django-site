from django.urls import path
from .views import *

urlpatterns = [
    # path('register/', register, name='register'),
    # path('login/', user_login, name='login'),
    # path('logout/', user_logout, name='logout'),

    # path('', test, name='test'),
    path('awards/', AwardsList.as_view(), name='awards_list'),
    path('awards/<int:pk>/', ViewAwards.as_view(), name='awards_detail'),
    path('awards/create_award/', CreateAwards.as_view(), name='awards_create'),

    path('roles/', RolesList.as_view(), name='roles_list'),
    path('roles/<int:pk>/', ViewRoles.as_view(), name='roles_detail'),
    # path('', HomeNews.as_view(), name='home'),

    path('positions/', PositionsList.as_view(), name='positions_list'),
    path('positions/<int:pk>/', ViewPositions.as_view(), name='positions_detail'),

]