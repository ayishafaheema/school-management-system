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

# get student with homework status for teacher dashboard
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


# get student with homework and status for student dasgbiard
def get_student_homework(student):

    homeworks = Homework.objects.filter(
        assigned_class=student.student_class
    )
    homework_data = []
    pending_count=0
    for homework in homeworks:
        status = HomeworkStatus.objects.filter(
            homework=homework,
            student=student,
        ).first()
        if not status or status.status != "Y":
            pending_count += 1

        homework_data.append({
            "homework": homework,
            "status": status,
        })
    return homework_data,pending_count

def get_teacher_homework_stats(teacher):

    students = Student.objects.filter(
        student_class=teacher.assigned_class
    )

    homeworks = Homework.objects.filter(
        teacher=teacher
    )

    total_students =(students).count()
    total_homeworks = (homeworks).count()

    total_submitted = HomeworkStatus.objects.filter(
        homework__in=homeworks,
        status="Y",
    ).count()

    total_expected=(total_homeworks)*total_students
    total_pending=total_expected-total_submitted

    return total_students,total_homeworks,total_submitted,total_pending