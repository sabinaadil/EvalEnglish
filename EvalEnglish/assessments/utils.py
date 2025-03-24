def update_user_answer_after_review(user_answer):
    teacher_score = user_answer.teacher_score
    model_score = user_answer.model_score or None

    if teacher_score is not None and model_score is not None:
        final_score = teacher_score * 0.7 + model_score * 0.3
        user_answer.final_score = final_score

        user_answer.score = round(user_answer.question.max_score * final_score, 2)

        user_answer.is_correct = final_score >= 0.5
    elif model_score is None:
        user_answer.final_score = teacher_score
        user_answer.score = teacher_score
        user_answer.is_correct = teacher_score >= 0.5

    user_answer.save()


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
import nltk
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, pos_tag

lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return 'a'  # adjective
    elif tag.startswith('V'):
        return 'v'  # verb
    elif tag.startswith('N'):
        return 'n'  # noun
    elif tag.startswith('R'):
        return 'r'  # adverb
    else:
        return 'n'  # default

def preprocess_text(text):
    corrected = str(TextBlob(text).correct())

    tokens = word_tokenize(corrected.lower())
    tagged = pos_tag(tokens)

    lemmatized = [lemmatizer.lemmatize(word, get_wordnet_pos(pos)) for word, pos in tagged]
    return ' '.join(lemmatized)

def evaluate_text_answer(student_answer: str, correct_answer: str) -> float:
    """
    Расширенная оценка текста студента по сравнению с правильным ответом.
    Возвращает значение от 0.0 до 1.0 (схожесть).
    """

    processed_student = preprocess_text(student_answer)
    processed_correct = preprocess_text(correct_answer)

    vectorizer = TfidfVectorizer().fit([processed_student, processed_correct])
    tfidf_matrix = vectorizer.transform([processed_student, processed_correct])

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    return round(float(similarity), 4)


from PyPDF2 import PdfReader
from docx import Document as DocxReader


def extract_text_from_file(file_path: str) -> str:
    if file_path.endswith('.pdf'):
        reader = PdfReader(file_path)
        return ' '.join(page.extract_text() or '' for page in reader.pages)

    elif file_path.endswith('.docx'):
        doc = DocxReader(file_path)
        return '\n'.join(p.text for p in doc.paragraphs)

    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    else:
        return ""