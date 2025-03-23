def update_user_answer_after_review(user_answer):
    teacher_score = user_answer.teacher_score
    model_score = user_answer.model_score or None

    if teacher_score is not None and model_score is not None:
        final_score = (teacher_score + model_score) / 2
        user_answer.final_score = final_score

        user_answer.score = round(user_answer.question.max_score * final_score)

        user_answer.is_correct = final_score >= 0.5
    elif model_score is None:
        user_answer.final_score = teacher_score
        user_answer.score = teacher_score
        user_answer.is_correct = teacher_score >= 0.5

    user_answer.save()
