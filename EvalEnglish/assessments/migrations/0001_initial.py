# Generated by Django 5.1.4 on 2025-01-12 17:41

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Question Type',
                'verbose_name_plural': 'Question Types',
            },
        ),
        migrations.CreateModel(
            name='ModuleAssessment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('score', models.PositiveIntegerField()),
                ('max_score', models.PositiveIntegerField()),
                ('completed_at', models.DateTimeField(auto_now_add=True)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessments', to='courses.module')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='module_assessments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Module Assessment',
                'verbose_name_plural': 'Module Assessments',
                'ordering': ['-completed_at'],
                'unique_together': {('module', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('question_text', models.TextField()),
                ('question_file_url', models.CharField(blank=True, max_length=255, null=True)),
                ('time_limit', models.PositiveIntegerField()),
                ('max_attempts', models.PositiveIntegerField()),
                ('max_score', models.PositiveIntegerField()),
                ('correct_answer', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='courses.module')),
                ('question_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='questions', to='assessments.questiontype')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='AnswerOption',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('answer_text', models.CharField(max_length=255)),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_options', to='assessments.question')),
            ],
            options={
                'verbose_name': 'Answer Option',
                'verbose_name_plural': 'Answer Options',
            },
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('answer_text', models.TextField(blank=True, null=True)),
                ('answer_file_url', models.CharField(blank=True, max_length=255, null=True)),
                ('attempt_number', models.PositiveIntegerField()),
                ('time_spent', models.PositiveIntegerField()),
                ('is_correct', models.BooleanField(default=False)),
                ('teacher_score', models.FloatField(blank=True, null=True)),
                ('model_score', models.FloatField(blank=True, null=True)),
                ('final_score', models.FloatField(blank=True, null=True)),
                ('score', models.PositiveIntegerField(default=0)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('is_late', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to='assessments.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Answer',
                'verbose_name_plural': 'User Answers',
                'ordering': ['-submitted_at'],
            },
        ),
        migrations.CreateModel(
            name='CourseAssessment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('total_score', models.PositiveIntegerField(default=0)),
                ('max_score', models.PositiveIntegerField(default=0)),
                ('time_spent', models.PositiveIntegerField(default=0)),
                ('completed_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessments', to='courses.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_assessments', to=settings.AUTH_USER_MODEL)),
                ('module_assessments', models.ManyToManyField(related_name='course_assessments', to='assessments.moduleassessment')),
            ],
            options={
                'verbose_name': 'Course Assessment',
                'verbose_name_plural': 'Course Assessments',
                'ordering': ['-completed_at'],
                'unique_together': {('course', 'user')},
            },
        ),
    ]
