from django.contrib import admin
from .models import CustomUser, Learner, Instructor

# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "username", "email"]


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ["user", "full_time", "total_learners"]


@admin.register(Learner)
class LearnerAdmin(admin.ModelAdmin):
    list_display = ["user", "occupation", "social_link"]
