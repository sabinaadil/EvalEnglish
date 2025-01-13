from .models import UserAnswer

def evaluate_answer(user_answer):
    question = user_answer.question
    if question.question_type.name in ['quiz', 'boolean']:
        if question.correct_answer.strip().lower() == user_answer.answer_text.strip().lower():
            user_answer.is_correct = True
            user_answer.score = question.max_score
        else:
            user_answer.is_correct = False
            user_answer.score = 0
        user_answer.save()

def evaluate_free_text_answer(user_answer, model_score=None, teacher_score=None):
    if model_score is not None:
        user_answer.model_score = model_score
    if teacher_score is not None:
        user_answer.teacher_score = teacher_score

    if user_answer.model_score is not None and user_answer.teacher_score is not None:
        user_answer.final_score = round(0.7 * teacher_score + 0.3 * model_score, 2)
        user_answer.score = round(user_answer.final_score)
        user_answer.is_correct = user_answer.final_score >= 50
    user_answer.save()
