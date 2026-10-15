
from school_app.models import Student, Teacher
from school_app.search import StudentFilter, TeacherFilter


def admin_search(request,students , teachers):

    studentFilter = StudentFilter(request.GET, queryset=students)

    teacherFilter = TeacherFilter(request.GET, queryset=teachers)

    filtered_students  = studentFilter.qs
    filtered_teachers  = teacherFilter.qs
    return filtered_students , filtered_teachers