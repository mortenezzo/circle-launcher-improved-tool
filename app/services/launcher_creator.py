import os

def create_launcher_ini(app_name: str, circle_launcher_path: str) -> str:
    """
    Create a launcher .ini file for the given application.

    :param app_name: Name of the application.
    :param circle_launcher_path: Path to the Circle Launcher directory.
    :return: Path to the created .ini file.
    """
    app_path = os.path.join(circle_launcher_path, app_name)
    ini_path = os.path.join(app_path, f"{app_name}.ini")

    if not os.path.exists(app_path):
        os.makedirs(app_path)

    if os.path.exists(ini_path):
        os.remove(ini_path)

    with open(ini_path, 'w', encoding="UTF-8") as f:
        f.write("[Rainmeter]\n")
        f.write("Update=1000\n")
        f.write(f"@include=#@#Variables.inc\n\n")
        f.write("\n")
        f.write("[Image]\n")
        f.write("Meter=Button\n")
        f.write(f"ButtonImage={app_name}\n")
        f.write("X=0\n")
        f.write("Y=0\n")
        f.write(f"LeftMouseUpAction=#{app_name}#\n")
        f.write(f"TooltipText={app_name}\n")

    return ini_path
