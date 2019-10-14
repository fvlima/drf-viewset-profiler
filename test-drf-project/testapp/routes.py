from rest_framework import routers

from .views import TestModelViewSet, TestViewSet

app_name = "testapp"

router = routers.DefaultRouter()
router.register(r"test-viewset", TestViewSet, basename="test-viewset")
router.register(r"test-model-viewset", TestModelViewSet, basename="test-model-viewset")

urlpatterns = router.urls
