from rest_framework import serializers
from .models import StudentRecord

class StudentRecordSerializer(serializers.ModelSerializer):
    class meta:
        model = StudentRecord
        fields = '__all__'
