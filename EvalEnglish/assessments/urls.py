from django.urls import path
from .api import (QuestionTypeListAPIView, QuestionAPIView, ModuleQuestionsListAPIView, QuestionSingleAPIView,
                  AnswerOptionAPIView, QuestionAnswerOptionsAPIView, AnswerOptionSingleAPIView, StudentAnswersReviewAPIView, UserAnswerCreateAPIView,
                  QuestionUserAnswersAPIView, UserAnswerSingleAPIView, GradeUserAnswerAPIView, ModuleAssessmentAPIView,
                  ModuleAssessmentCreateAPIView, ModuleAssessmentListAPIView, ModuleAssessmentSingleAPIView,
                  CourseAssessmentAPIView)

urlpatterns = [
    path('question-types/', QuestionTypeListAPIView.as_view(), name='question-types'),

    # question
    path('question/', QuestionAPIView.as_view(), name='question-create'),
    path('module/<uuid:module_id>/questions/', ModuleQuestionsListAPIView.as_view(), name='module-questions'),
    path('question/<uuid:question_id>/', QuestionSingleAPIView.as_view(), name='question-detail'),

    # answer option
    path('answer-option/', AnswerOptionAPIView.as_view(), name='answer-option-create'),
    path('question/<uuid:question_id>/options/', QuestionAnswerOptionsAPIView.as_view(), name='question-options'),
    path('answer-option/<uuid:option_id>/', AnswerOptionSingleAPIView.as_view(), name='answer-option-detail'),

    # user answer
    path('answer/', UserAnswerCreateAPIView.as_view(), name='submit-answer'),
    path('question/<uuid:question_id>/my-answers/', QuestionUserAnswersAPIView.as_view(), name='my-question-answers'),
    path('answer/<uuid:answer_id>/', UserAnswerSingleAPIView.as_view(), name='answer-detail'),
    path('user-answers/<uuid:answer_id>/grade/', GradeUserAnswerAPIView.as_view(), name='grade-user-answer'),
    path('student-answers/<uuid:student_id>/', StudentAnswersReviewAPIView.as_view(), name='student-answers-review'),

    # module assessment
    path('module/<uuid:module_id>/assessment/', ModuleAssessmentAPIView.as_view(), name='module-assessment'),
    path('module-assessment/', ModuleAssessmentCreateAPIView.as_view(), name='module-assessment-create'),
    path('my/module-assessments/', ModuleAssessmentListAPIView.as_view(), name='my-module-assessments'),
    path('module-assessment/<uuid:assessment_id>/', ModuleAssessmentSingleAPIView.as_view(), name='module-assessment-detail'),

    # course assessment
    path('course/<uuid:course_id>/assessment/', CourseAssessmentAPIView.as_view(), name='course-assessment'),

]