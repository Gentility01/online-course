from django.urls import path
from . import views

urlpatterns = [
    path("ask-question/<int:lesson_id>/", views.student_askquestion,
         name="student_askquestion"),
    
    path("lesson-question/course/<int:course_id>/lesson/<int:lesson_id>", 
      views.lesson_questions, name="lesson_questions"),

    path("set-choices/<int:lesson_id>/", views.set_question_choices, name="set_questionchoices"),
    path("lesson-questions/<int:lesson_id>/", views.lesson_question_lists, name="lesson_question_lists"),
    path('lesson/<int:lesson_id>/question/<int:question_id>/', views.review_and_submit_question, name='review_and_submit_question'),
    path("course-list", views.enrolled_student_course_list, name="enrolled_studentcourselist"),
]