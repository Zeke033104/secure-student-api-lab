from django.db import models
from django.contrib.auth.models import User
from .encryption import encrypt, decrypt
# Create your models here.

class StudentRecord(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    year_level = models.IntegerField()
    _grade = models.TextField(blank=True, null=True, db_column='grade')
    
    def __str__(self):
        return self.full_name
    
    @property
    def grade(self):
        """decrypt on read"""
        if self._grade:
            return decrypt(self._grade)
        return None
    
    @grade.setter
    def grade(self, value):
        """Encrypt the grade before saving to the database"""
        if value:
            self._grade = encrypt(str(value))
        else:
            self._grade = None
            
class PaymentRecord(models.Model):
    """"
    You are building a Secure Payment API that handles sensitive user information.
    The system must:
    Encrypt sensitive fields Hash passwords securely Prevent brute-force attacks Log security-related events
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=100)
    _card_number = models.TextField(db_column='encrypted_card_number')
    _amount = models.TextField(db_column='encrypted_amount')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment by {self.owner.username} on {self.created_at}"
    
    @property
    def amount(self):
        """Decrypt amount on read"""
        if self._amount:
            return decrypt(self._amount)
        return None
    
    @amount.setter
    def amount(self, value):
        """Encrypt the amount before saving to the database"""
        if value:
            self._amount = encrypt(str(value))
    