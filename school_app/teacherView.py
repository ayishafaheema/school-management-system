from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from school_app.forms import TeacherForm
from school_app.models import LoginData, Teacher, Student, Attendance


@login_required(login_url="login_view")
def teacher_dashboard(request):

    if request.user.role != "TEACHER":
        return redirect("login_view")

    teacher = Teacher.objects.get(user=request.user)

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
        },
    )

def add_teacher(request):
    if request.method == "POST":
        form = TeacherForm(request.POST, request.FILES)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            department = form.cleaned_data["department"]
            qualification = form.cleaned_data["qualification"]
            assigned_class = form.cleaned_data["assigned_class"]
            image = form.cleaned_data["image"]

            # Check if the class is already assigned
            if Teacher.objects.filter(assigned_class=assigned_class).exists():
                form.add_error(
                    "assigned_class",
                    "This class is already assigned to another teacher."
                )

            else:
                user = LoginData(
                    username=username,
                    role="TEACHER"
                )
                user.set_password(password)
                user.save()

                Teacher.objects.create(
                    user=user,
                    department=department,
                    qualification=qualification,
                    assigned_class=assigned_class,
                    image=image
                )


                return redirect("admin_dashboard")

    else:
        form = TeacherForm()

    return render(request, "teacher/add_teacher.html", {"form": form})





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
    attendance_count = Attendance.objects.filter(
        student__in=students,
        date=today,
    ).count()

    attendance_completed = attendance_count == students.count()
    today_attendance = Attendance.objects.select_related(
        "student",
        "student__user"
    ).filter(
        student__in=students,
        date=today
    )
    # Save attendance only if it has not already been completed
    if request.method == "POST" and not attendance_completed:

        for student in students:

            field_name = f"attendance_{student.id}"

            status = request.POST.get(field_name)

            Attendance.objects.create(
                student=student,
                teacher=teacher,
                date=today,
                status=status,
            )

            print(student.user.username, status)

        # Attendance has now been completed
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