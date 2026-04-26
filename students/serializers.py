from rest_framework import serializers
from .models import StudentRecord


class StudentRecordSerializer(serializers.ModelSerializer):
    grade = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = StudentRecord
        fields = ['id', 'owner', 'full_name', 'course', 'year_level', 'grade']

    def create(self, validated_data):
        grade = validated_data.pop('grade', None)
        instance = StudentRecord.objects.create(**validated_data)
        if grade:
            instance.grade = grade
            instance.save()
        return instance

    def update(self, instance, validated_data):
        grade = validated_data.pop('grade', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if grade:
            instance.grade = grade
        instance.save()
        return instance