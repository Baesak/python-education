import pytest
from unittest.mock import Mock, patch, MagicMock
from to_test import time_of_day


@pytest.mark.parametrize("time", [0, 4, 5, 19])
@patch("to_test.datetime")
def test_night(mock_datetime, time):
    mock_datetime.now = MagicMock(return_value=Mock(hour=time))

    assert time_of_day() == "night"


@pytest.mark.parametrize("time", [6, 8, 11])
@patch("to_test.datetime")
def test_morning(mock_datetime, time):
    mock_datetime.now = MagicMock(return_value=Mock(hour=time))

    assert time_of_day() == "morning"


@pytest.mark.parametrize("time", [12, 15, 17])
@patch("to_test.datetime")
def test_afternoon(mock_datetime, time):
    mock_datetime.now = MagicMock(return_value=Mock(hour=time))

    assert time_of_day() == "afternoon"
