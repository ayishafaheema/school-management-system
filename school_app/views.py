from datetime import date
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from school_app.models import Student, Teacher, CLASS_CHOICES, Result, Exam
from school_app.services.attendance import get_attendance_on_date, calculate_attendance_percentage, \
    get_attendance_summary,get_weekly_attendance_data
from school_app.services.search import admin_search


# Create your views here.
def home(request):
    return render(request, 'home.html')


@login_required(login_url="login_view")
def admin_dashboard(request):

    if not (request.user.is_superuser or request.user.role == "ADMIN"):
        return redirect("login_view")

    students = Student.objects.all()
    teachers = Teacher.objects.all()

    today = date.today()

    today_attendance=get_attendance_on_date(students, today)
    student_count = students.count()
    attendance_summary = get_attendance_summary(today_attendance)

    present = attendance_summary["present"]
    absent = attendance_summary["absent"]
    late = attendance_summary["late"]

    marked_today = present + absent + late
    not_marked = student_count - marked_today

    attendance_percentage = calculate_attendance_percentage(present,student_count)

    graph_labels, graph_data = get_weekly_attendance_data(students,today)

    filtered_students, filtered_teachers = admin_search(request,students,teachers)

    return render(request, "admin/admin_dashboard2.html", {
        "students": students,
        "teachers": teachers,

        "student_count": student_count,
        "teacher_count": teachers.count(),

        "attendance_percentage": attendance_percentage,

        "present": present,
        "absent": absent,
        "late": late,

        "marked_today": marked_today,
        "not_marked": not_marked,

        "graph_labels": graph_labels,
        "graph_data": graph_data,

        "filtered_students":filtered_students,
        "filtered_teachers":filtered_teachers,



    })



def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.is_superuser:
                return redirect("admin_dashboard")

            elif user.role == "TEACHER":
                return redirect("teacher_dashboard")

            elif user.role == "STUDENT":
                return redirect("student_dashboard")

        else:

            return render(
                request,
                "log_in.html",
                {
                    "error": "Invalid Username or Password"
                }
            )

    return render(request, "log_in.html")

# @login_required(login_url="login_view")
# def view_all_students(request):
#
#     if request.user.role != "ADMIN":
#         return redirect("login_view")
#
#     students = Student.objects.all()
#
#     return render(
#         request,
#         "admin/view_all_students.html",
#         {
#             "students": students,
#         },
#     )

@login_required(login_url="login_view")
def view_all_students(request):

    print("USER:", request.user)
    print("ROLE:", request.user.role)

    if request.user.role != "ADMIN":
        return redirect("login_view")

    students = Student.objects.all()

    return render(
        request,
        "admin/view_all_students.html",
        {
            "students": students,
        },
    )


@login_required(login_url="login_view")
def view_all_teachers(request):

    if request.user.role != "ADMIN":
        return redirect("login_view")

    teachers = Teacher.objects.all()

    return render(
        request,
        "admin/view_all_teachers.html",
        {
            "teachers": teachers,
        },
    )

@login_required(login_url="login_view")
def class_wise_attendance(request):

    if not request.user.is_superuser and request.user.role != "ADMIN":
        return redirect("login_view")

    today = date.today()
    class_attendance = []
    for class_value, class_label in CLASS_CHOICES:
        students = Student.objects.filter(
            student_class=class_value
        )

        today_attendance = get_attendance_on_date(students, today)

        total_students=students.count()
        attendance_summary = get_attendance_summary(today_attendance)

        present = attendance_summary["present"]
        absent = attendance_summary["absent"]

        attendance_percentage = calculate_attendance_percentage(
            present,
            total_students
        )
        class_attendance.append({
                "class": class_label,
                "total": total_students,
                "present": present,
                "absent": absent,
                "percentage": attendance_percentage})

    return render(request, "admin/class_wise_attendance.html",{

        "class_attendance": class_attendance,
        "today": today,

    })


@login_required(login_url="login_view")
def admin_exam_results_view(request):

    if request.user.role != "ADMIN":
        return redirect("login_view")

    exams = Exam.objects.all().order_by("exam_date")

    for exam in exams:

        result_exists = Result.objects.filter(
            exam=exam
        ).exists()

        if result_exists:
            exam.result_status = "Published"
        else:
            exam.result_status = "Pending"

    return render(
        request,
        "admin/admin_exam_results.html",
        {
            "exams": exams,
        }
    )