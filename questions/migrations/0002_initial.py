# Generated by Django 5.0 on 2023-12-14 12:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("lessons", "0001_initial"),
        ("questions", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="answer",
            name="instructor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="lesson",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="lessons.lesson"
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="choice",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="questions.question"
            ),
        ),
        migrations.AddField(
            model_name="answer",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="questions.question"
            ),
        ),
        migrations.AddField(
            model_name="submission",
            name="choices",
            field=models.ManyToManyField(to="questions.choice"),
        ),
        migrations.AddField(
            model_name="submission",
            name="question",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="questions.question",
            ),
        ),
        migrations.AddField(
            model_name="submission",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="grade",
            name="submission",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="questions.submission"
            ),
        ),
    ]
