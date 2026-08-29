from school_app.models import Student, LoginData


def create_student(cleaned_data):

    username =cleaned_data["username"]
    password = cleaned_data["password"]
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

    return True