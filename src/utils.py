import re

def count_sentences(text):
    # Учитываем русские и английские знаки препинания
    return len(re.split(r'[.!?]+', text)) - 1 if text else 0

def count_words(text):
    # Находим все слова (и латиницу, и кириллицу)
    return len(re.findall(r'[a-zA-Zа-яА-ЯёЁ]+', text))

def calculate_readability(text):
    words = count_words(text)
    sentences = count_sentences(text)
    # Считаем только буквы (без пробелов и знаков)
    characters = len(re.findall(r'[a-zA-Zа-яА-ЯёЁ]', text))
    
    if words == 0 or sentences == 0:
        return 0
    
    # Индекс ARI адаптированный
    score = 4.71 * (characters / words) + 0.5 * (words / sentences) - 21.43
    return max(0, round(score, 2))