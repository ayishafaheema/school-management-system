from datetime import date, timedelta
from inspect import ClassFoundException

from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from school_app.models import Student, Teacher, Attendance, CLASS_CHOICES  # Create your views here.
def home(request):
    return render(request, 'home.html')


@login_required(login_url="login_view")
def admin_dashboard(request):

    if not (request.user.is_superuser or request.user.role == "ADMIN"):
        return redirect("login_view")

    students = Student.objects.all()
    teachers = Teacher.objects.all()

    today = date.today()

    today_attendance = Attendance.objects.filter(
        student__in=students,
        date=today
    )

    student_count = students.count()

    present = today_attendance.filter(status="P").count()
    absent = today_attendance.filter(status="A").count()
    late = today_attendance.filter(status="L").count()

    marked_today = present + absent + late
    not_marked = student_count - marked_today

    if student_count == 0:
        attendance_percentage = 0
    else:
        attendance_percentage = int((present / student_count) * 100)

    graph_labels = []
    graph_data = []

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)

        graph_labels.append(day.strftime("%a"))
        day_attendance = Attendance.objects.filter(
            student__in=students,
            date=day
        )

        present_count = day_attendance.filter(status="P").count()
        late_count = day_attendance.filter(status="L").count()

        if student_count == 0:
            percentage = 0
        else:
            percentage = int(((present_count + late_count) / student_count) * 100)

        graph_data.append(percentage)
        print(graph_labels)
        print(graph_data)

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

        today_attendance = Attendance.objects.select_related(
            "student",
            "student__user"
        ).filter(
            student__in=students,
            date=today
        )
        total_students=students.count()
        students_presents=today_attendance.filter(status="P").count()
        students_absent=today_attendance.filter(status="A").count()

        if total_students == 0:
            attendance_percentage = 0
        else:
            attendance_percentage = int((students_presents/ total_students) * 100)

        class_attendance.append({
                "class": class_label,
                "total": total_students,
                "present": students_presents,
                "absent": students_absent,
                "percentage": attendance_percentage})

    return render(request, "admin/class_wise_attendance.html",{

        "class_attendance": class_attendance,
        "today": today,

    })

