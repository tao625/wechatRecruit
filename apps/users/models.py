from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        db_table = 'auth_user'



    def __str__(self):
        return self.username
