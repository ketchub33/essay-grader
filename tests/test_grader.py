import pytest
from src.grader import EssayGrader

@pytest.fixture
def grader():
    return EssayGrader()

def test_empty_essay(grader):
    result = grader.grade("")
    assert result["score"] == 0

def test_short_essay_score(grader):
    text = "Cat sat on a mat."
    result = grader.grade(text)
    # Короткое эссе должно получить низкий балл за объем
    assert result["final_score"] < 50 

def test_good_essay_metrics(grader):
    text = "Automated grading systems in education leverage Natural Language Processing " \
           "to assess student performance. These tools provide instant feedback, allowing " \
           "students to improve their writing skills iteratively. However, AI should " \
           "assist teachers, not replace them."
    result = grader.grade(text)
    assert result["final_score"] > 50
    assert "metrics" in result
    assert result["metrics"]["word_count"] > 30