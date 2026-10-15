from school_app.models import Result, Teacher, Student


def save_exam_results(exam, students, post_data):

    for student in students:

        # English
        english_mark = post_data.get(
            f"english_mark_{student.id}"
        )
        english_absent = post_data.get(
            f"english_absent_{student.id}"
        )
        english_absent = english_absent == "on"

        # Science
        science_mark = post_data.get(
            f"science_mark_{student.id}"
        )
        science_absent = post_data.get(
            f"science_absent_{student.id}"
        )
        science_absent = science_absent == "on"

        # Mathematics
        mathematics_mark = post_data.get(
            f"mathematics_mark_{student.id}"
        )
        mathematics_absent = post_data.get(
            f"mathematics_absent_{student.id}"
        )
        mathematics_absent = mathematics_absent == "on"

        # Second Language
        second_language_mark = post_data.get(
            f"second_language_mark_{student.id}"
        )
        second_language_absent = post_data.get(
            f"second_language_absent_{student.id}"
        )
        second_language_absent = second_language_absent == "on"

        # Social Science
        social_science_mark = post_data.get(
            f"social_science_mark_{student.id}"
        )
        social_science_absent = post_data.get(
            f"social_science_absent_{student.id}"
        )
        social_science_absent = social_science_absent == "on"

        # Hindi
        hindi_mark = post_data.get(
            f"hindi_mark_{student.id}"
        )
        hindi_absent = post_data.get(
            f"hindi_absent_{student.id}"
        )
        hindi_absent = hindi_absent == "on"

        # Create or update result
        Result.objects.update_or_create(
            exam=exam,
            student=student,
            defaults={
                "english_mark": english_mark or None,
                "english_absent": english_absent,

                "science_mark": science_mark or None,
                "science_absent": science_absent,

                "mathematics_mark": mathematics_mark or None,
                "mathematics_absent": mathematics_absent,

                "second_language_mark": second_language_mark or None,
                "second_language_absent": second_language_absent,

                "social_science_mark": social_science_mark or None,
                "social_science_absent": social_science_absent,

                "hindi_mark": hindi_mark or None,
                "hindi_absent": hindi_absent,
            }
        )


def calculate_results(exam, students):
    student_results = []
    for student in students:
        result = Result.objects.filter(
            exam=exam,
            student=student
        ).first()

        if result is None:
            student_results.append({
                "student": student,
                "total": None,
                "percentage": None,
                "grade": None,
                "status": "Not Published",

            })
        elif (
                    result.english_mark is None
                    and result.science_mark is None
                    and result.mathematics_mark is None
                    and result.second_language_mark is None
                    and result.social_science_mark is None
                    and result.hindi_mark is None
            ):
            student_results.append({
                "student": student,
                "total": None,
                "percentage": None,
                "grade": None,
                "status": "Not Published",
            })



        else:

            english_mark = result.english_mark or 0
            science_mark = result.science_mark or 0
            mathematics_mark = result.mathematics_mark or 0
            second_language_mark = result.second_language_mark or 0
            social_science_mark = result.social_science_mark or 0
            hindi_mark = result.hindi_mark or 0
            total = (
                english_mark
                + science_mark
                + mathematics_mark
                + second_language_mark
                + social_science_mark
                + hindi_mark
            )
            percentage = (total / 600) * 100
            if percentage >= 95:
                grade= "A+"
            elif percentage >= 90:
                grade= "A"
            elif percentage >= 80:
                grade= "B+"
            elif percentage >= 70:
                grade= "B"
            elif percentage >= 60:
                grade= "C+"
            elif percentage >= 50:
                grade= "C"
            elif percentage >= 40:
                grade= "D+"
            elif percentage >= 35:
                grade= "D"
            else:
                grade= "F"

            if grade=="F":
                status="Failed"
            else:
                status="Passed"

            student_results.append({
                "student": student,
                "total": total,
                "percentage": percentage,
                "grade": grade,
                "status": status,
            })

    return student_results



def calculate_student_results(student, exams):
    student_results = []
    for exam in exams:
        result = Result.objects.filter(
            exam=exam,
            student=student
        ).first()
        if result is None:
            student_results.append({
                "exam": exam,
                "total": None,
                "percentage": None,
                "grade": None,
                "status": "Not Published",
            })
        else:
            english_mark = result.english_mark or 0
            science_mark = result.science_mark or 0
            mathematics_mark = result.mathematics_mark or 0
            second_language_mark = result.second_language_mark or 0
            social_science_mark = result.social_science_mark or 0
            hindi_mark = result.hindi_mark or 0
            total = (
                    english_mark
                    + science_mark
                    + mathematics_mark
                    + second_language_mark
                    + social_science_mark
                    + hindi_mark
            )
            percentage = (total / 600) * 100
            if percentage >= 95:
                grade = "A+"
            elif percentage >= 90:
                grade = "A"
            elif percentage >= 80:
                grade = "B+"
            elif percentage >= 70:
                grade = "B"
            elif percentage >= 60:
                grade = "C+"
            elif percentage >= 50:
                grade = "C"
            elif percentage >= 40:
                grade = "D+"
            elif percentage >= 35:
                grade = "D"
            else:
                grade = "F"

            if grade == "F":
                status = "Failed"
            else:
                status = "Passed"

            student_results.append({
                "exam": exam,
                "total": total,
                "percentage": percentage,
                "grade": grade,
                "status": status,
            })
    return student_results

def calculate_result_details(result):

    english_mark = result.english_mark or 0
    science_mark = result.science_mark or 0
    mathematics_mark = result.mathematics_mark or 0
    second_language_mark = result.second_language_mark or 0
    social_science_mark = result.social_science_mark or 0
    hindi_mark = result.hindi_mark or 0

    total = (
        english_mark
        + science_mark
        + mathematics_mark
        + second_language_mark
        + social_science_mark
        + hindi_mark
    )

    percentage = (total / 600) * 100

    if percentage >= 95:
        grade = "A+"
    elif percentage >= 90:
        grade = "A"
    elif percentage >= 80:
        grade = "B+"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C+"
    elif percentage >= 50:
        grade = "C"
    elif percentage >= 40:
        grade = "D+"
    elif percentage >= 35:
        grade = "D"
    else:
        grade = "F"

    if grade == "F":
        status = "Failed"
    else:
        status = "Passed"

    return {
        "total": total,
        "percentage": percentage,
        "grade": grade,
        "status": status,
    }






