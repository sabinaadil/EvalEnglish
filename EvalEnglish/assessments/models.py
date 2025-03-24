from django.db import models
import uuid
from courses.models import Module, Course
from users.models import User
from common.models import Document

class QuestionType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Question Type"
        verbose_name_plural = "Question Types"

    def __str__(self):
        return self.name

class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question_text = models.TextField()
    question_type = models.ForeignKey(
        'QuestionType',
        on_delete=models.SET_NULL,
        null=True,
        related_name='questions'
    )
    question_file_url = models.ManyToManyField(
        Document,
        related_name='question_documents',
        blank=True
    )
    time_limit = models.PositiveIntegerField()
    max_attempts = models.PositiveIntegerField()
    max_score = models.PositiveIntegerField()
    correct_answer = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ['created_at']

    def __str__(self):
        return f"Question: {self.question_text[:50]}"

class AnswerOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answer_options'
    )
    answer_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Answer Option"
        verbose_name_plural = "Answer Options"

    def __str__(self):
        return f"{self.answer_text} (Correct: {self.is_correct})"

class UserAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='user_answers'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    answer_text = models.TextField(blank=True, null=True)
    answer_file_url = models.ManyToManyField(
        Document,
        related_name='user_answer_documents',
        blank=True
    )
    attempt_number = models.PositiveIntegerField()
    time_spent = models.PositiveIntegerField()
    is_correct = models.BooleanField(default=False)
    teacher_score = models.FloatField(blank=True, null=True)
    model_score = models.FloatField(blank=True, null=True)
    final_score = models.FloatField(blank=True, null=True)
    score = models.FloatField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_late = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User Answer"
        verbose_name_plural = "User Answers"
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Answer by {self.user.email} for Question {self.question.id}"

class ModuleAssessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='assessments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='module_assessments'
    )
    score = models.PositiveIntegerField()
    max_score = models.PositiveIntegerField()
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Module Assessment"
        verbose_name_plural = "Module Assessments"
        unique_together = ('module', 'user')
        ordering = ['-completed_at']

    def __str__(self):
        return f"Assessment for {self.module.title} by {self.user.email}"

class CourseAssessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='assessments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='course_assessments'
    )
    total_score = models.PositiveIntegerField(default=0)
    max_score = models.PositiveIntegerField(default=0)
    time_spent = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(blank=True, null=True)
    module_assessments = models.ManyToManyField(
        ModuleAssessment,
        related_name='course_assessments'
    )

    class Meta:
        verbose_name = "Course Assessment"
        verbose_name_plural = "Course Assessments"
        unique_together = ('course', 'user')
        ordering = ['-completed_at']

    def __str__(self):
        return f"Assessment for {self.course.name} by {self.user.email}"