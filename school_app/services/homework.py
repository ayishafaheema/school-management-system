from datetime import  date

from school_app.models import Homework, Teacher, Student, HomeworkStatus


def create_homework_service(cleaned_data, teacher):

    subject = cleaned_data["subject"]
    title = cleaned_data["title"]
    description = cleaned_data["description"]
    due_date = cleaned_data["due_date"]

    assigned_class = teacher.assigned_class
    assigned_date = date.today()

    created_homework=Homework.objects.create(
        teacher=teacher,
        assigned_class=assigned_class,
        subject=subject,
        title=title,
        description=description,
        assigned_date=assigned_date,
        due_date = due_date

    )

    return created_homework

def homework_status_service(homework, student, status):
    HomeworkStatus.objects.update_or_create(
        homework=homework,
        student=student,
        defaults={
            "status": status
        }
    )

def get_students_with_homework_status(homework):
    students = Student.objects.filter(
        student_class=homework.assigned_class
    )

    for student in students:
        homework_status = HomeworkStatus.objects.filter(
            homework=homework,
            student=student
        ).first()

        if homework_status:
            student.homework_status = homework_status.status
        else:
            student.homework_status = "N"

    return students