from apps.common.routers import BaseRouter
from apps.files.api.views_v1 import ImageViewSet

router = BaseRouter()

router.register(r"images", ImageViewSet, basename="image")

urlpatterns = router.urls
