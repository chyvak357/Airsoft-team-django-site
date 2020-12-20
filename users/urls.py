from django.urls import path
from .views import *

urlpatterns = [
    # TODO сделать потом разделение на просмотр профиля для текущего пользователя и просто авторизованного
    path('register/', register, name='register'),
    path('edit/', edit_profile, name='edit_profile'),
    path('profile/', edit_profile, name='profile'),
    # path('profile_auth/', edit_profile, name='profile'),

    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

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