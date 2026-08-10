from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from school_app.forms import StudentForm, StudentProfileForm
from school_app.models import LoginData, Student, Teacher, Attendance


@login_required(login_url="login_view")
def student_dashboard(request):

    if request.user.role != "STUDENT":
        return redirect("login_view")
    student = Student.objects.get(user=request.user)
    attendance = Attendance.objects.filter(student=student)

    total = attendance.count()
    present = attendance.filter(status="P").count()
    absent = attendance.filter(status="A").count()
    late = attendance.filter(status="L").count()

    if total == 0:
        attendance_percentage = 0
    else:
        attendance_percentage = int(((present + late) / total) * 100)

    teacher = Teacher.objects.filter(
        assigned_class=student.student_class
    ).first()


    return render(request, "student/student_dashboard2.html",
                  {
                      "student": student,
                      "teacher": teacher,
                      "attendance_percentage": attendance_percentage,
                      "present": present,
                      "absent": absent,
                      "late": late,
                  }
    )


def add_student(request,):

    if request.method == "POST":

        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            student_class = form.cleaned_data["student_class"]
            roll_no = form.cleaned_data["roll_no"]
            student_id = form.cleaned_data["student_id"]
            address = form.cleaned_data["address"]
            academic_year = form.cleaned_data["academic_year"]
            phone=form.cleaned_data["phone"]
            department = form.cleaned_data["department"]
            image = form.cleaned_data["image"]

            user = LoginData(
                username=username,
                role="STUDENT"
            )

            user.set_password(password)
            user.save()

            Student.objects.create(
                user=user,
                student_class=student_class,
                roll_no=roll_no,
                student_id=student_id,
                address=address,
                academic_year=academic_year,
                phone=phone,
                department=department,
                image=image,
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
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect("student_dashboard")
    else:
        form = StudentForm(instance=student)

    return render(request, "student/edit_student_profile.html", {"form": form,"student": student})


def student_attendance(request):
    student = Student.objects.get(user=request.user)
    attendance = Attendance.objects.filter(student=student).order_by("-date")
    total=attendance.count()
    present=attendance.filter(status="P").count()
    absent=attendance.filter(status="A").count()
    late=attendance.filter(status="L").count()
    if total==0:
        attendance_percentage=0
    else:
        attendance_percentage=int((present+late)/total*100)

    return render(request, "student/student_attendance.html",{"attendance_percentage":attendance_percentage,
                                                              "present":present,"absent":absent,"late":late,"attendance":attendance})




