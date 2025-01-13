from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import CourseAssessment

@receiver(m2m_changed, sender=CourseAssessment.module_assessments.through)
def update_course_assessment(sender, instance, **kwargs):
    total_score = 0
    max_score = 0
    time_spent = 0

    for module_assessment in instance.module_assessments.all():
        total_score += module_assessment.score
        max_score += module_assessment.max_score
        time_spent += module_assessment.time_spent

    instance.total_score = total_score
    instance.max_score = max_score
    instance.time_spent = time_spent
    instance.save()
