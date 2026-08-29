from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from school_app.forms import TeacherForm, HomeworkForm
from school_app.models import LoginData, Teacher, Student, Homework, HomeworkStatus
from school_app.services import teacher
from school_app.services.attendance import get_attendance_on_date,is_attendance_completed,save_attendance
from school_app.services.homework import create_homework_service, homework_status_service, \
    get_students_with_homework_status
from school_app.services.teacher import create_teacher


@login_required(login_url="login_view")
def teacher_dashboard(request):

    if request.user.role != "TEACHER":
        return redirect("login_view")

    teacher = Teacher.objects.get(user=request.user)

    homeworks = Homework.objects.filter(
        teacher=teacher
    ).order_by("-assigned_date")[:2]

    students = Student.objects.filter(
        student_class=teacher.assigned_class
    )
    student_count = students.count()

    return render(
        request,
        "teacher/teacher_dashboard2.html",
        {
            "teacher": teacher,
            "students": students,
            "student_count": student_count,
            "homeworks": homeworks,

        },
    )

def add_teacher(request):

    if request.method == "POST":

        form = TeacherForm(request.POST, request.FILES)

        if form.is_valid():

            teacher_created = create_teacher(
                form.cleaned_data
            )

            if not teacher_created:
                form.add_error(
                    "assigned_class",
                    "This class is already assigned to another teacher."
                )
            else:
                return redirect("admin_dashboard")

    else:
        form = TeacherForm()

    return render(
        request,
        "teacher/add_teacher.html",
        {"form": form}
    )



@login_required(login_url="login_view")
def mark_attendance(request):

    if request.user.role != "TEACHER":
        return redirect("login_view")

    teacher = Teacher.objects.get(user=request.user)

    students = Student.objects.filter(
        student_class=teacher.assigned_class
    )

    today = date.today()

    # Check whether today's attendance is already completed
    attendance_completed = is_attendance_completed(
        students,
        today
    )

    today_attendance = get_attendance_on_date(
        students,
        today
    )
    # Save attendance only if it has not already been completed
    if request.method == "POST" and not attendance_completed:
        save_attendance(
            students,
            teacher,
            today,
            request.POST
        )

        return redirect("mark_attendance")

    return render(
        request,
        "teacher/mark_attendance.html",
        {
            "teacher": teacher,
            "students": students,
            "today": today,
            "attendance_completed": attendance_completed,
            "today_attendance": today_attendance,

        },
    )


@login_required(login_url="login_view")
def create_homework(request):
    if request.user.role != "TEACHER":
        return redirect("login_view")

    if request.method == "POST":
        form = HomeworkForm(request.POST)

        if form.is_valid():
            teacher = Teacher.objects.get(user=request.user)

            created_homework = create_homework_service(
                form.cleaned_data,
                teacher
            )

            return redirect("teacher_dashboard")
        else:
            print(form.errors)


    else:
        form = HomeworkForm()

    return render(request, "teacher/create_homework.html", {"form": form})

def view_all_homework(request):
    if request.user.role != "TEACHER":
        return redirect("login_view")

    teacher=Teacher.objects.get(user=request.user)
    homeworks = Homework.objects.filter(teacher=teacher).order_by("-assigned_date")

    return render(request, "teacher/view_all_homework.html", {"homeworks": homeworks})


@login_required(login_url="login_view")
def homework_details(request, homework_id):
    if request.user.role != "TEACHER":
        return redirect("login_view")
    teacher = Teacher.objects.get(
        user=request.user
    )
    homework = Homework.objects.get(
        id=homework_id,
        teacher=teacher
    )

    if request.method == "POST":
        student_id = request.POST.get("student_id")
        status = request.POST.get("status")
        student = Student.objects.get(
            id=student_id
        )

        homework_status_service(
            homework,
            student,
            status

        )
        return redirect("homework_details", homework_id=homework.id)

    students = get_students_with_homework_status(homework)


    return render(request, "teacher/homework_details.html", {"homework": homework,
                                                             "students": students})
