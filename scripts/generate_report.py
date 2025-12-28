import os
import csv
import sys

# Магия для GitHub: принудительно добавляем корень проекта в пути поиска
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

try:
    from src.grader import EssayGrader
except ImportError as e:
    print(f"Критическая ошибка импорта: {e}")
    print(f"Текущий путь поиска: {sys.path}")
    sys.exit(1)

def main():
    grader = EssayGrader()
    # На твоем скриншоте папка называется 'data'
    input_dir = os.path.join(BASE_DIR, 'data')
    output_file = os.path.join(BASE_DIR, 'grading_report.csv')
    
    os.makedirs(input_dir, exist_ok=True)
    files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    
    if not files:
        # Если папка пуста, создаем файл, чтобы Action не упал
        with open(os.path.join(input_dir, 'test.txt'), 'w', encoding='utf-8') as f:
            f.write("AI is transforming education by providing instant feedback.")
        files = ['test.txt']

    results = []
    for filename in files:
        try:
            with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as f:
                text = f.read()
                report = grader.grade(text)
                results.append({
                    'filename': filename, 
                    'score': report.get('final_score', 0), 
                    'verdict': report.get('verdict', 'N/A')
                })
        except Exception as e:
            print(f"Ошибка в файле {filename}: {e}")

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['filename', 'score', 'verdict'])
        writer.writeheader()
        writer.writerows(results)
    print("Отчет успешно создан!")

if __name__ == "__main__":
    main()
