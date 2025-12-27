import re
from textblob import TextBlob
from src.utils import count_words, calculate_readability

class EssayGrader:
    def __init__(self):
        self.criteria = {
            "length": 30,      # Вес критерия объема
            "vocabulary": 30,  # Вес критерия словарного запаса
            "readability": 20, # Вес сложности текста
            "subjectivity": 20 # Вес личного мнения (анализ тональности)
        }

    def grade(self, text):
        if not text.strip():
            return {"final_score": 0, "feedback": "Empty text provided."}

        # Для анализа тональности используем TextBlob
        blob = TextBlob(text)
        
        # Регулярка для поиска слов (поддерживает и RU, и EN)
        all_words = re.findall(r'[a-zA-Zа-яА-ЯёЁ]+', text.lower())
        word_count = len(all_words)
        unique_words_count = len(set(all_words))
        
        # 1. Оценка объема (цель: > 150 слов)
        score_length = min(100, (word_count / 150) * 100)
        
        # 2. Словарный запас (цель: > 40% уникальных слов)
        diversity_ratio = unique_words_count / word_count if word_count > 0 else 0
        score_vocab = min(100, (diversity_ratio / 0.4) * 100)
        
        # 3. Читаемость (цель: уровень 8-12)
        ari = calculate_readability(text)
        score_readability = 100 if 8 <= ari <= 14 else 70
        
        # 4. Субъективность
        # TextBlob выдает 0.0 для русского, поэтому сделаем заглушку 0.5 (нейтрально),
        # если это русский текст, чтобы не занижать балл.
        is_russian = bool(re.search(r'[а-яА-Я]', text))
        if is_russian:
            subj = 0.5  # Для русского принимаем за среднее значение
        else:
            subj = blob.sentiment.subjectivity
            
        score_subj = min(100, (subj / 0.5) * 100)

        # Финальный расчет по твоим весам
        final_score = (
            score_length * 0.3 +
            score_vocab * 0.3 +
            score_readability * 0.2 +
            score_subj * 0.2
        )

        return {
            "final_score": round(final_score, 1),
            "metrics": {
                "word_count": word_count,
                "readability_index": ari,
                "vocabulary_diversity": round(diversity_ratio, 2),
                "subjectivity": round(subj, 2)
            },
            "verdict": self._get_verdict(final_score)
        }

    def _get_verdict(self, score):
        if score >= 90: return "Excellent"
        if score >= 75: return "Good"
        if score >= 60: return "Satisfactory"
        return "Needs Improvement"

if __name__ == "__main__":
    # Быстрый тест (EN и RU)
    grader = EssayGrader()
    
    print("English test:")
    print(grader.grade("This is a very simple essay. It is not very long."))
    
    print("\nRussian test:")
    print(grader.grade("Это короткое эссе. Оно написано на русском языке для проверки системы."))