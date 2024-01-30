from django.contrib import admin
from .models import Question, Choice, Submission


# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "lesson", "title", "created_at")


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("question", "content", "is_correct")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "question", "display_grade_submission")

    def display_grade_submission(self, obj):
        return obj.grade_submission()

    display_grade_submission.short_description = "Grade Submission"
