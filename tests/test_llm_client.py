from src.app.llm_client import verify_changes


def test_verify_changes_no_input():
    assert verify_changes("") == "No changes detected from staged (git)."
