from pathlib import Path


def test_project_structure():
    assert Path("app/streamlit_app.py").exists()
    assert Path("src/data.py").exists()
    assert Path("src/metrics.py").exists()
