from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StudentRecordViewSet, PaymentRecordViewSet, login_view


router = DefaultRouter()
router.register(r'students', StudentRecordViewSet)
router.register(r'payments', PaymentRecordViewSet, basename='payment')

urlpatterns = [
    path('login/', login_view, name='login'),
] + router.urls