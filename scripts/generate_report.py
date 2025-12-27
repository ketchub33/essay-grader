import os
import csv
import sys

# Добавляем корень проекта в пути поиска, чтобы видеть папку src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.grader import EssayGrader
except ImportError:
    print("Ошибка: Не удалось найти модуль src. Проверьте структуру проекта.")
    sys.exit(1)

def main():
    grader = EssayGrader()
    # Согласно твоему скриншоту, папка называется 'data'
    input_dir = 'data'
    output_file = 'grading_report.csv'
    
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)

    # Получаем список всех .txt файлов в папке data
    files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    
    if not files:
        print(f"В папке {input_dir} нет .txt файлов. Создаю проверочный файл.")
        with open(os.path.join(input_dir, 'hello.txt'), 'w', encoding='utf-8') as f:
            f.write("Artificial intelligence is a great technology for the future.")
        files = ['hello.txt']

    results = []
    for filename in files:
        try:
            with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as f:
                text = f.read()
                # Вызываем метод grade из твоего класса
                report = grader.grade(text)
                results.append({
                    'filename': filename,
                    'score': report.get('final_score', 0),
                    'verdict': report.get('verdict', 'N/A')
                })
        except Exception as e:
            print(f"Не удалось обработать файл {filename}: {e}")

    # Записываем результат в CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['filename', 'score', 'verdict']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Отчет успешно создан! Обработано файлов: {len(files)}")

if __name__ == "__main__":
    main()
