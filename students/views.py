import logging
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import  authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import StudentRecord
from .serializers import StudentRecordSerializer
from .permissions import IsAdminOrFaculty


logger = logging.getLogger('students_security')

class LoginRateThrottle(AnonRateThrottle):
    """Max 5 login attempts per minute per IP ."""
    rate = '5/min'


@api_view(['POST'])
@throttle_classes([LoginRateThrottle])
def login_view(request):
    
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        logger.info(f"Successful login for user: {username}")
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        logger.warning(f"Failed login attempt for username: {username}")
        return Response(
                {'detail': 'Invalid credentials.'},
                status=status.HTTP_401_UNAUTHORIZED
         )
        

class StudentRecordViewSet(ModelViewSet):
    queryset = StudentRecord.objects.all()
    serializer_class = StudentRecordSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name__in=['Admin', 'Faculty']).exists():
            return StudentRecord.objects.all()
        return StudentRecord.objects.filter(owner=user)

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAdminUser]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAdminOrFaculty]
        else:
            permission_classes = [IsAuthenticated]
            
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        logger.info(f"Creating student record by user: {self.request.user.username}")
        serializer.save()
        
    def perform_destroy(self, instance):
        logger.warning(f"Student record deleted by: {self.request.user} - record:{instance}")
        instance.delete()