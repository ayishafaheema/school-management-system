from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from school_app.forms import StudentForm, StudentProfileForm
from school_app.models import Student, Teacher, Attendance, Homework, HomeworkStatus
from school_app.search import StudentFilter
from school_app.services.attendance import student_attendance_history
from school_app.services.homework import get_student_homework
from school_app.services.student import create_student


@login_required(login_url="login_view")
def student_dashboard(request):

    if request.user.role != "STUDENT":
        return redirect("login_view")

    student = Student.objects.get(user=request.user)

    homework_data,pending_count = get_student_homework(student)

    attendance_percentage, total, present, absent, late = student_attendance_history(student)

    teacher = Teacher.objects.filter(
        assigned_class=student.student_class
    ).first()

    context = {
        "student":student,
        "teacher": teacher,
        "attendance_percentage":attendance_percentage,
        "present":present,
        "absent":absent,
        "late":late,
        "total":total,
        "homework_data":homework_data,
        "pending_count": pending_count,


    }

    return render(request,"student/student_dashboard2.html",context)

def add_student(request,):

    if request.method == "POST":

        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            student_created = create_student(
                form.cleaned_data
            )

            return redirect("admin_dashboard")

    else:
        form = StudentForm()

    return render(
        request,
        "student/add_student.html",
        {"form": form}
    )

def edit_student_profile(request):
    student = Student.objects.get(user=request.user)

    if request.method == "POST":
        form = StudentProfileForm(
            request.POST,
            request.FILES,
            instance=student
        )

        if form.is_valid():
            form.save()
            return redirect("student_dashboard")

    else:
        form = StudentProfileForm(instance=student)

    return render(
        request,
        "student/edit_student_profile.html",
        {
            "form": form,
            "student": student
        }
    )

@login_required(login_url="login_view")
def student_attendance(request):

    student = Student.objects.get(user=request.user)

    attendance_percentage, total, present, absent, late = (
        student_attendance_history(student)
    )

    attendance = Attendance.objects.filter(
        student=student
    ).order_by("-date")

    return render(
        request,
        "student/student_attendance.html",
        {
            "attendance_percentage": attendance_percentage,
            "present": present,
            "absent": absent,
            "late": late,
            "attendance": attendance,
        }
    )

@login_required(login_url="login_view")
def student_homework(request):
    if request.user.role != "STUDENT":
        return redirect("login_view")

    student = Student.objects.get(user=request.user)

    homework_data=get_student_homework(student)
    return render(request, "student/student_homework.html",{
        "homework_data":homework_data
    })


