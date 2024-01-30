from django.db import models
from lessons.models import Lesson
from users.models import *
from django.conf import settings
from ckeditor.fields import RichTextField

# Create your models here.


class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}  title '{self.title}'  -> {self.content}"


class Answer(models.Model):
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.instructor.username} answered on {self.question.lesson.title} - '{self.question.title}'"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class Submission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, default=1
    )  # Add a default value here
    choices = models.ManyToManyField(Choice)
    score = models.IntegerField(default=0)

    def grade_submission(self):
        # Get the correct choices for the associated question
        correct_choices = Choice.objects.filter(question=self.question, is_correct=True)

        # Check if the selected choices match the correct choices
        is_correct = set(correct_choices) == set(self.choices.filter(is_correct=True))

        # Update the score based on correctness
        self.score = 10 if is_correct else 0
        self.save()

        return is_correct

    def get_total_score(cls):
        total_score = 0
        for submission in cls.objects.all():
            total_score += submission.score
        return total_score

    def __str__(self):
        return f"{self.user.username}'s submission for {self.question.title}"


class Grade(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField(blank=True, null=True)
