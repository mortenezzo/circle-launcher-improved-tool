import os
from pathlib import Path

def create_launcher_ini(app_name: str, rainmeter_path: Path) -> str:
    """
    Create a launcher .ini file for the given application.

    :param app_name: Name of the application.
    :param rainmeter_path: Path to the Rainmeter skins directory.
    :return: Path to the created .ini file.
    """
    app_path = rainmeter_path.joinpath(app_name)
    ini_path = os.path.join(app_path, f"{app_name}.ini")


    with open(ini_path, 'w', encoding="UTF-8") as f:
        f.write("""[Rainmeter]
        Update=1000
        @include=#@#Variables.inc
        
        [Image]
        Meter=Button
        ButtonImage={app_name}
        X=0
        Y=0
        LeftMouseUpAction=#"{app_name}"#
        """)

    return ini_path
