from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from school_app.forms import TeacherForm
from school_app.models import LoginData, Teacher

@login_required(login_url="login_view")
def teacher_dashboard(request):

    if request.user.role != "TEACHER":
        return redirect("login_view")

    return render(request, "teacher/teacher_dashboard.html")


def add_teacher(request):
    form = TeacherForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            department = form.cleaned_data["department"]
            qualification = form.cleaned_data["qualification"]

            user=LoginData(username=username,
                           role="TEACHER"
)
            user.set_password(password)
            user.save()

            Teacher.objects.create(
                user=user,
                department=department,
                qualification=qualification)
            return redirect("/admin_dashboard")

    return render(request, 'teacher/add_teacher.html', {'form': form})