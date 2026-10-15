from school_app.forms import TeacherForm
from school_app.models import Teacher


from school_app.models import LoginData, Teacher


def create_teacher(cleaned_data):

    username = cleaned_data["username"]
    password = cleaned_data["password"]
    department = cleaned_data["department"]
    qualification = cleaned_data["qualification"]
    assigned_class = cleaned_data["assigned_class"]
    image = cleaned_data["image"]

    if Teacher.objects.filter(
        assigned_class=assigned_class
    ).exists():
        return False

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

    return True