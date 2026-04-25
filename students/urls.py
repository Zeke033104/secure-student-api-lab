from rest_framework.routers import DefaultRouter
from .views import StudentRecordViewSet

router = DefaultRouter()
router.register(r'students', StudentRecordViewSet)

urlpatterns = router.urls