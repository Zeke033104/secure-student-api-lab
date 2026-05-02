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
    
class PaymentRecordSerializer(serializers.ModelSerializer):
    card_number = serializers.CharField(write_only=True)
    amount = serializers.CharField(write_only=True)
    cardholder_name = serializers.CharField()
    
    class Meta:
        from .models import PaymentRecord
        model = PaymentRecord
        fields = ['id', 'owner', 'cardholder_name', 'card_number', 'amount', 'created_at']
        read_only_fields = ['created_at']
        
        def create(self, validated_data):
            from .models import PaymentRecord
            card_number = validated_data.pop('card_number')
            amount = validated_data.pop('amount')
            instance = PaymentRecord(**validated_data)
            instance.card_number = card_number
            instance.amount = amount
            instance.save()
            return instance
    