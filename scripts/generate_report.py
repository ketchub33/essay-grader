import os
import csv
from src.grader import EssayGrader

def main():
    grader = EssayGrader()
    data_path = "data/essays_to_grade"
    os.makedirs(data_path, exist_ok=True)
    
    if not os.listdir(data_path):
        with open(f"{data_path}/test_student.txt", "w") as f:
            f.write("Artificial Intelligence is important for future development.")

    report_data = []
    print(f"Scanning {data_path}...")

    for filename in os.listdir(data_path):
        if filename.endswith(".txt"):
            with open(os.path.join(data_path, filename), "r") as f:
                res = grader.grade(f.read())
                report_data.append({
                    "file": filename,
                    "score": res["final_score"],
                    "verdict": res["verdict"],
                    "words": res["metrics"]["word_count"]
                })

    output_file = "grading_report.csv"
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "score", "verdict", "words"])
        writer.writeheader()
        writer.writerows(report_data)
    
    print(f"Report saved to {output_file}")

if __name__ == "__main__":
    main()