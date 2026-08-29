from datetime import timedelta

from school_app.models import Attendance


def get_attendance_on_date(students, target_date):
    attendance = Attendance.objects.filter(
        student__in=students,
        date=target_date
    )

    return attendance

def calculate_attendance_percentage(students_present, total_students):
    if total_students == 0:
        return 0

    attendance_percentage = int(
        (students_present / total_students) * 100
    )

    return attendance_percentage

def get_attendance_summary(attendance):
    present = attendance.filter(status="P").count()
    absent = attendance.filter(status="A").count()
    late = attendance.filter(status="L").count()

    return {
        "present": present,
        "absent": absent,
        "late": late,
    }

def get_weekly_attendance_data(students, today):
    graph_labels = []
    graph_data = []

    student_count = students.count()

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)

        graph_labels.append(day.strftime("%a"))

        day_attendance = get_attendance_on_date(
            students,
            day
        )

        present_count = day_attendance.filter(
            status="P"
        ).count()

        late_count = day_attendance.filter(
            status="L"
        ).count()

        if student_count == 0:
            percentage = 0
        else:
            percentage = int(
                ((present_count + late_count) / student_count) * 100
            )

        graph_data.append(percentage)

    return graph_labels, graph_data


def is_attendance_completed(students, date):
    attendance_count = get_attendance_on_date(
        students,
        date
    ).count()

    return attendance_count == students.count()

def save_attendance(students, teacher, date, post_data):
    for student in students:
        field_name = f"attendance_{student.id}"
        status = post_data.get(field_name)

        Attendance.objects.create(
            student=student,
            teacher=teacher,
            date=date,
            status=status
        )

def student_attendance_history(student):
    attendance = Attendance.objects.filter(
        student=student
    ).order_by("-date")

    total = attendance.count()
    present = attendance.filter(status="P").count()
    absent = attendance.filter(status="A").count()
    late = attendance.filter(status="L").count()

    if total == 0:
        attendance_percentage = 0
    else:
        attendance_percentage = int(
            ((present + late) / total) * 100
        )

    return attendance_percentage, total, present, absent, late
