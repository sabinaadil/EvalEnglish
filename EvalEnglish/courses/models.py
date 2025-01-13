from django.db import models
from django.utils import timezone
import uuid
from users.models import User
from common.models import Document

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Module(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='modules'
    )
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Module"
        verbose_name_plural = "Modules"
        ordering = ['order']

    def __str__(self):
        return f"{self.title} (Course: {self.course.name})"

class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    content_url = models.ManyToManyField(
        Document,
        related_name='lesson_documents',
        blank=True
    )
    order = models.PositiveIntegerField()
    deadline = models.DateTimeField(null=True, blank=True)
    time_limit = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
        ordering = ['order']

    def __str__(self):
        return f"{self.title} (Module: {self.module.title})"

class CourseParticipant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='participants'
    )
    participant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrolled_courses'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.FloatField(default=0.0)

    class Meta:
        verbose_name = "Course Participant"
        verbose_name_plural = "Course Participants"
        unique_together = ('course', 'participant')
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.participant.email} - {self.course.name}"