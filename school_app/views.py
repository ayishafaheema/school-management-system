from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    return render(request, 'home.html')


@login_required(login_url="login_view")
def admin_dashboard(request):

    if not (request.user.is_superuser or request.user.role == "ADMIN"):
        return redirect("login_view")

    return render(request, "admin/admin_dashboard.html")
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





