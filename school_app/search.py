from tkinter import Label

import django_filters
from django import forms
from django_filters import CharFilter

from school_app.models import Student


class StudentFilter(django_filters.FilterSet):
    student_class = CharFilter(label="" , lookup_expr="icontains" ,widget=forms.TextInput(attrs={'placeholder':'search','class':'form-control'}))
    class Meta:
        model = Student
        fields = ('student_class',)