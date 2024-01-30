from django.db import models
from ckeditor.fields import RichTextField
from courses.models import Course


# Create your models here.
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="created_courses"
    )
    content = RichTextField()

    def __str__(self):
        return self.title
