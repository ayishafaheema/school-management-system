from django import forms

from school_app.models import Teacher, Student


class TeacherForm(forms.ModelForm):
    username=forms.CharField(max_length=150)
    password=forms.CharField(
        widget=forms.PasswordInput()
    )
    class Meta:
        model = Teacher
        fields = [
            "username",
            "password",
            "department",
            "qualification",
        ]

class StudentForm(forms.ModelForm):
    username=forms.CharField(max_length=150)
    password=forms.CharField(
        widget=forms.PasswordInput()
    )
    class Meta:
        model = Student
        fields = [
            "username",
            "password",
            "student_class",
            "roll_no"

        ]