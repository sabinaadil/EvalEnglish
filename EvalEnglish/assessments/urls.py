from django.urls import path
from .api import (QuestionTypeListAPIView, QuestionAPIView, ModuleQuestionsListAPIView, QuestionSingleAPIView,
                  AnswerOptionAPIView, QuestionAnswerOptionsAPIView, AnswerOptionSingleAPIView, UserAnswerCreateAPIView,
                  QuestionUserAnswersAPIView, UserAnswerSingleAPIView, GradeUserAnswerAPIView)

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

]