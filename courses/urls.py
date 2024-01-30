from django.urls import path
from . import views

urlpatterns = [
    path("create-course", views.create_course, name="create_course"),
    path("courses/<int:course_id>/", views.course_detail, name="course_detail"),
    path("edit-course/<int:course_id>/", views.edit_course, name="edit_course"),
    path("enroll-course/<int:course_id>/", views.enroll_course, name="enroll_course"),
    path(
        "enrolledcourse-details/<int:course_id>/",
        views.enrolledcourse_details,
        name="enrolledcourse_details",
    ),
    path("all-courses", views.get_all_courses, name="all_courses"),
]
