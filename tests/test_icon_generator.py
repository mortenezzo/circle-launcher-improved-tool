import os
from pathlib import Path
from app.services.icon_generator import generate_3state_icon

def test_generate_3state_icon():
    rainmeter_path = Path(os.getenv("RAINMETER_SKINS_PATH", "tests"))
    result = generate_3state_icon("tests/test_icon.png", "TestApp", rainmeter_path)
    assert os.path.exists(result)
