from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeEvents.as_view(), name='events_home'),
    path('event/<int:pk>/', ViewEvents.as_view(), name='view_events'),

    # path('news', HomeNews.as_view(), name='news_home'),
    # path('category/<int:category_id>/', NewsByCategory.as_view(), name='category'),
    # path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    # path('news/add-news/', CreateNews.as_view(), name='add_news'),
    # path('about', about_page, name='about_page'),

]