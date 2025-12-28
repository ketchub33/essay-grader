import os
import csv
import sys


project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.grader import EssayGrader

def main():
    grader = EssayGrader()
    input_dir = os.path.join(project_root, 'data')
    output_file = os.path.join(project_root, 'grading_report.csv')
    

    os.makedirs(input_dir, exist_ok=True)

    files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    
    if not files:
        print("Нет файлов для проверки. Создаю тестовый файл...")
        with open(os.path.join(input_dir, 'test.txt'), 'w', encoding='utf-8') as f:
            f.write("Artificial intelligence is changing the world of education.")
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
    
    print(f"Отчет готов! Обработано файлов: {len(files)}")

if __name__ == "__main__":
    main()
