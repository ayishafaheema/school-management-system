from school_app.models import Student, LoginData
from django.core.mail import send_mail


def create_student(cleaned_data):

    username =cleaned_data["username"]
    password = cleaned_data["password"]
    email = cleaned_data["email"]
    student_class = cleaned_data["student_class"]
    roll_no = cleaned_data["roll_no"]
    student_id = cleaned_data["student_id"]
    address = cleaned_data["address"]
    academic_year = cleaned_data["academic_year"]
    phone = cleaned_data["phone"]
    department = cleaned_data["department"]
    image = cleaned_data["image"]

    user = LoginData(
        username=username,
        email=email,
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
    send_mail(
        subject="Your Student Account",
        message=f"""
    Hello {username},

    Your student account has been created.

    Username: {username}
    Password: {password}

    You can use these credentials to log in to the School Management System.

    Thank you,
    School Admin
    """,
        from_email=None,
        recipient_list=[email],
    )
    return True