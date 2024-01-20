# Generated by Django 5.0 on 2023-12-14 12:28

import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='title', max_length=200)),
                ('order', models.IntegerField(default=0)),
                ('content', ckeditor.fields.RichTextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_courses', to='courses.course')),
            ],
        ),
    ]