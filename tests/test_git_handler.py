from src.app.git_handler import remove_double_spaces


def test_remove_double_spaces():
    assert remove_double_spaces("Hello  world") == "Hello world"
    assert remove_double_spaces("No  double   spaces  here") == "No double spaces here"
    assert remove_double_spaces("Already clean") == "Already clean"
