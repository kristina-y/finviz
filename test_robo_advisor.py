# This is the testing function that is written by me
from robo_advisor import is_yes
from robo_advisor import validate_timeframe

def test_is_yes():
    user_input = "no"
    result = is_yes(user_input)
    assert result == False

def test_validate_timeframe():
    result = validate_timeframe("hi")
    assert result == "1"
