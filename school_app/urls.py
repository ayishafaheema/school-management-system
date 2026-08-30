from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from school_app import views, teacherView, studentView

urlpatterns = [
    path('', views.home, name='home'),
    path('login_view', views.login_view, name='login_view'),


    # student url
    path('student_dashboard', studentView.student_dashboard, name='student_dashboard'),
    path('add_student', studentView.add_student, name='student_add'),
    path("edit_student_profile/", studentView.edit_student_profile, name="edit_student_profile"),
    path("student_attendance", studentView.student_attendance, name='student_attendance'),
    path("student_homework",studentView.student_homework,name='student_homework'),


    # teacher url
    path('teacher_dashboard', teacherView.teacher_dashboard, name='teacher_dashboard'),
    path('add_teacher', teacherView.add_teacher, name='teacher_add'),
    path('mark_attendance', teacherView.mark_attendance, name='mark_attendance'),
    path('create_homework', teacherView.create_homework, name='create_homework'),
    path('homeworks',teacherView.view_all_homework,name='view_all_homework'),
    path("homework/<int:homework_id>/",teacherView.homework_details,name="homework_details"),
    path("teacher_attendance_history",teacherView.teacher_attendance_history_view,name="teacher_attendance_history"),

    # admin url
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('class_wise',views.class_wise_attendance,name='class_wise'),
    path("students",views.view_all_students,name='view_all_students'),
    path("teachers",views.view_all_teachers,name='view_all_teachers'),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)