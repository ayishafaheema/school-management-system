from django import forms

from school_app.models import Teacher, Student, Homework


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
            "assigned_class",
            "image"
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
            "roll_no",
            "student_id",
            "address",
            "academic_year",
            "phone",
            "department",
            "image",

        ]

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["phone", "address", "image"]

class HomeworkForm(forms.ModelForm):

    class Meta:
        model = Homework
        fields = [
            "subject",
            "title",
            "description",
            "due_date",
        ]
        widgets = {
            "due_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            )
        }