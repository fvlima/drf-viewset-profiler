from django.conf.urls import include, url

api_urlpatterns = [url(r"^api/", include("testapp.routes", namespace="testapp"))]

urlpatterns = api_urlpatterns
