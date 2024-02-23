from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_secretary = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    is_head = models.BooleanField(default=False)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        first_name = self.user.first_name
        last_name = self.user.last_name
        return first_name + ' ' + last_name


class Secretary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        first_name = self.user.first_name
        last_name = self.user.last_name
        return first_name + ' ' + last_name


class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        first_name = self.user.first_name
        last_name = self.user.last_name
        return first_name + ' ' + last_name


class Head(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        first_name = self.user.first_name
        last_name = self.user.last_name
        return first_name + ' ' + last_name



