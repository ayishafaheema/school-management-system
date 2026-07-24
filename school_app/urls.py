from django.urls import path

from school_app import views, teacherView, studentView

urlpatterns = [
    path('', views.home, name='home'),
    path('student_dashboard', studentView.student_dashboard, name='student_dashboard'),
    path('login_view', views.login_view, name='login_view'),
    path('teacher_dashboard', teacherView.teacher_dashboard, name='teacher_dashboard'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('add_teacher',teacherView.add_teacher, name='teacher_add'),
    path('add_student',studentView.add_student, name='student_add'),

]