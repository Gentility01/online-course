from django.db import models
from ckeditor.fields import RichTextField
from users.models import Instructor, Learner
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=100, null=False)
    image = models.ImageField(upload_to="course_images/")
    description = RichTextField()
    pub_date = models.DateField(null=True)
    instructors = models.ManyToManyField(Instructor)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="Enrollment", related_name="enrolled_courses"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_courses",
        default=None,
    )
    total_enrollment = models.IntegerField(default=0)
    is_enrolled = False

    def __str__(self):
        return f"Name: {self.name}"


class Enrollment(models.Model):
    ENROLLMENT_MODE_CHOICES = [
        ("free", "Free"),
        ("paid", "Paid"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    mode = models.CharField(
        max_length=10, choices=ENROLLMENT_MODE_CHOICES, default="free"
    )
    rating = models.IntegerField(
        null=True, blank=True, validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.name} on {self.enrollment_date} ({self.mode} mode) - Rating: {self.rating}"
