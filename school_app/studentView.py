from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from school_app.forms import StudentForm
from school_app.models import LoginData, Student


@login_required(login_url="login_view")
def student_dashboard(request):

    if request.user.role != "STUDENT":
        return redirect("login_view")

    return render(request, "student/student_dashboard.html")


def add_student(request):

    if request.method == "POST":

        form = StudentForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            student_class = form.cleaned_data["student_class"]
            roll_no = form.cleaned_data["roll_no"]

            user = LoginData(
                username=username,
                role="STUDENT"
            )

            user.set_password(password)
            user.save()

            Student.objects.create(
                user=user,
                student_class=student_class,
                roll_no=roll_no
            )

            return redirect("admin_dashboard")

    else:
        form = StudentForm()

    return render(
        request,
        "student/add_student.html",
        {"form": form}
    )