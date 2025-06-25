import os
from app.services.icon_generator import generate_3state_icon

def test_generate_3state_icon():
    result = generate_3state_icon(
        "D:/Rainmeter/Icons/test_icon.png",
        "TestApp",
        "results")
    assert os.path.exists(result)
