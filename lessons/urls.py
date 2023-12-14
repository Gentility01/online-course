from django.urls import path
from . import views




urlpatterns = [
    path('create-lesson/<int:course_id>/', views.create_lesson, name='create_lesson'),
    path("lesson-success", views.lesson_success, name="lesson_success"),
    path('lesson-edit/<int:course_id>/<int:lesson_id>/', views.edit_lesson, name='edit_lesson'),
    path("lesson-list/<int:instructor_id>/", views.instructors_lessons_list, name="instructors_lessons_list"),
    path("courses/<int:course_id>/lesson/<int:lesson_id>/", views.enrolled_course_lesson_details, name="enrolledcourse_details"),
]