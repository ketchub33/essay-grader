import os
import csv
from src.grader import EssayGrader

def main():
    grader = EssayGrader()
    input_dir = 'data/essays_to_grade'
    output_file = 'grading_report.csv'
    
    # 1. Проверяем, существует ли папка, если нет - создаем
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        print(f"Created missing directory: {input_dir}")

    # 2. Ищем файлы
    files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    
    if not files:
        print("No .txt files found to grade! Creating a sample file...")
        with open(os.path.join(input_dir, 'sample.txt'), 'w', encoding='utf-8') as f:
            f.write("This is a sample text for grading. Artificial intelligence is evolving fast.")
        files = ['sample.txt']

    # 3. Оцениваем
    results = []
    for filename in files:
        path = os.path.join(input_dir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
            report = grader.grade(text)
            results.append({
                'filename': filename,
                'score': report['final_score'],
                'verdict': report['verdict']
            })

    # 4. Пишем отчет
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['filename', 'score', 'verdict'])
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Successfully generated {output_file} for {len(files)} files.")

if __name__ == "__main__":
    main()
