from django.urls import path
from .views import *

urlpatterns = [
    path("", WakeUp.as_view(), name="api_entrypoint"),
    path("test", TestData.as_view(), name="api_entrypoint"),
    path("allowlist", AllowList.as_view(), name="api_allowList"),
    path("data", GetData.as_view(), name="api_getdata"),
]
