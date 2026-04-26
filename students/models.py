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