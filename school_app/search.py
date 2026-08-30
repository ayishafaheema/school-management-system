
import django_filters
from django import forms
from django.db.models import Q
from django_filters import CharFilter, widgets

from school_app.models import Student, Teacher


class StudentFilter(django_filters.FilterSet):
    q = CharFilter(label="" ,method="filter_students",widget=forms.TextInput(attrs={'placeholder':'search','class':'form-control'}))
    def filter_students(self,queryset,name, search):
        return queryset.filter(
            Q(user__username__icontains=search) |
            Q(student_class__icontains=search)
        )

    class Meta:
        model = Student
        fields = ("q",)

class TeacherFilter(django_filters.FilterSet):
    q=CharFilter(label="",method="filter_teachers",widget=forms.TextInput(attrs={'placeholder':'search','class':'form-control'}))
    def filter_teachers(self,queryset,name, search):
        return queryset.filter(
            Q(user__username__icontains=search) |
            Q(assigned_class__icontains=search)
        )

    class Meta:
        model = Teacher
        fields = ("q",)







    # studentFilter = StudentFilter(request.GET, queryset=students)

