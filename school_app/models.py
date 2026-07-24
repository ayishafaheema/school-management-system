from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class LoginData(AbstractUser):
    ROLE_CHOICES = [
    ("ADMIN","Admin"),
    ("TEACHER","Teacher"),
    ("STUDENT","Student"),
    ]
    role=models.CharField(choices=ROLE_CHOICES,max_length=50)

class Teacher(models.Model):
    user=models.OneToOneField(LoginData,on_delete=models.CASCADE)
    department=models.CharField(max_length=50)
    qualification=models.CharField(max_length=50)
    image = models.ImageField(upload_to="teachers/", blank=True, null=True)



    def __str__(self):
        return self.user.username


class Student(models.Model):
    user=models.OneToOneField(LoginData,on_delete=models.CASCADE)
    student_class=models.CharField(max_length=50)
    roll_no=models.CharField(max_length=50)
    image = models.ImageField(upload_to="students/", blank=True, null=True)

    def __str__(self):
        return self.user.username

