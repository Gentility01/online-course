from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)


class Instructor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class Learner(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    occupation = models.CharField(null=False, max_length=20)
    social_link = models.URLField(max_length=200)

    def __str__(self):
        return f"{self.user.username}, {self.occupation}"
