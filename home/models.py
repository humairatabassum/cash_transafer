from django.db import models
from datetime import datetime
import os

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=1024)
    phoneNumber = models.CharField(max_length=15)
    balance = models.IntegerField(default=0)
    accountNo = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users_model'

    def isExists(self):
        if Users.objects.filter(email=self.email):
            return True
        return False


class Transactions(models.Model):
    sender = models.CharField(max_length=50)
    receiver = models.CharField(max_length=50)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'transactions_model'
