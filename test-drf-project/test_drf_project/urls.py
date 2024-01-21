from django.urls import include, re_path

api_urlpatterns = [re_path(r"^api/", include("testapp.routes", namespace="testapp"))]

urlpatterns = api_urlpatterns
