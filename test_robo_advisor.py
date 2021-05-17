# This is the testing function that is written by me
from robo_advisor import is_yes

def test_is_yes():
    user_input = "no"
    result = is_yes(user_input)
    assert result == False


