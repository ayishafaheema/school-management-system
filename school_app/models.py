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

CLASS_CHOICES = [
    ("1", "1st"),
    ("2", "2nd"),
    ("3", "3rd"),
    ("4", "4th"),
    ("5", "5th"),
    ("6", "6th"),
    ("7", "7th"),
    ("8", "8th"),
    ("9", "9th"),
    ("10", "10th"),
]

class Teacher(models.Model):
    user=models.OneToOneField(LoginData,on_delete=models.CASCADE)
    department=models.CharField(max_length=50)
    qualification=models.CharField(max_length=50)
    assigned_class=models.CharField(max_length=2,choices=CLASS_CHOICES,blank=True, null=True)
    image = models.ImageField(upload_to="teachers/", blank=True, null=True)



    def __str__(self):
        return self.user.username


class Student(models.Model):
    user=models.OneToOneField(LoginData,on_delete=models.CASCADE)

    student_class = models.CharField(
        max_length=2,
        choices=CLASS_CHOICES)
    roll_no=models.CharField(max_length=50)
    student_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    academic_year = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="students/", blank=True, null=True)


    def __str__(self):
        return self.user.username



STATUS_CHOICES = [
    ("P", "Present"),
    ("A", "Absent"),
    ("L", "Late"),
]


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "date"],
                name="unique_student_attendance_per_day"
            )
        ]

    def __str__(self):
        return f"{self.student.user.username} - {self.date}"

class Homework(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    assigned_class = models.CharField(
        max_length=2,
        choices=CLASS_CHOICES
    )
    subject=models.CharField(max_length=50)
    title=models.CharField(max_length=50)
    description = models.TextField()
    assigned_date = models.DateField()
    due_date = models.DateField()

HOMEWORK_STATUS_CHOICES =[
    ("Y","Submitted"),
    ("N","Not submitted"),
]
class HomeworkStatus(models.Model):

    homework=models.ForeignKey(Homework, on_delete=models.CASCADE)
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    status=models.CharField(
        max_length=1,
        choices=HOMEWORK_STATUS_CHOICES ,
        default="N"

    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["homework", "student"],
                name="unique_homework_status"
            )
        ]

