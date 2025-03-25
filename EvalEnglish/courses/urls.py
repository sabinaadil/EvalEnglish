from django.urls import path
from .api import (CourseAPIView, CoursesListAPIView, CourseSingleAPIView, ModuleAPIView, ModulesListAPIView,
                  ModuleSingleAPIView, LessonAPIView, LessonsListAPIView, LessonSingleAPIView, EnrollCourseAPIView,
                  CourseParticipantsListAPIView, LeaveCourseAPIView, MyCoursesAPIView, CourseDetailAPIView)

urlpatterns = [
    # course
    path('course/', CourseAPIView.as_view(), name='course'),
    path('courses-list/', CoursesListAPIView.as_view(), name='course-list'),
    path('course/<uuid:course_id>/', CourseSingleAPIView.as_view(), name='course-single'),
    path('course-detail/<uuid:course_id>/', CourseDetailAPIView.as_view(), name='course-detail'),

    # module
    path('module/', ModuleAPIView.as_view(), name='module'),
    path('modules/<uuid:course_id>/', ModulesListAPIView.as_view(), name='module-list'),
    path('module/<uuid:module_id>/', ModuleSingleAPIView.as_view(), name='module-single'),

    # lesson
    path('lesson/', LessonAPIView.as_view(), name='lesson'),
    path('lessons/<uuid:module_id>/', LessonsListAPIView.as_view(), name='lesson-list'),
    path('lesson/<uuid:lesson_id>/', LessonSingleAPIView.as_view(), name='lesson-single'),

    # course_participants
    path('enroll/', EnrollCourseAPIView.as_view(), name='enroll-course'),
    path('course-participants/<uuid:course_id>/', CourseParticipantsListAPIView.as_view(), name='course-participants'),
    path('course/<uuid:course_id>/leave/', LeaveCourseAPIView.as_view(), name='course-leave'),
    path('my/courses/', MyCoursesAPIView.as_view(), name='my-courses'),
]
