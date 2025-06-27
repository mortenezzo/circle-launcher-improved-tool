import os
from io import TextIOWrapper

from app.utils.clsid_helper import get_path_from_folder_clsid


def append_launcher_to_variables(exe_path: str, app_name: str, circle_launcher_path: str) -> None:
    variables_file = os.path.join(circle_launcher_path, "@Resources", "Variables.inc")
    normalized_exe_path = os.path.normpath(exe_path)
    replaced = False

    with open(variables_file, 'r', encoding="UTF-8") as f:
        content = f.readlines()

    with open(variables_file, 'w', encoding="UTF-8") as f:
        for line in content:
            if line.startswith(f"{app_name}="):
                replaced = True
                f.write(f"{app_name}=[\"{normalized_exe_path}\"]\n")
                continue
            else:
                f.write(line)
        if not replaced:
            f.write(f"{app_name}=[\"{normalized_exe_path}\"]\n")

def append_launcher_to_variables_using_system_app(app_name: str,app: dict,  circle_launcher_path: str) -> None:
    """
    Append a launcher to the Circle Launcher Variables.inc file.
    :param app_name: The name of the application.
    :param app: A dictionary containing the application details.
    :param circle_launcher_path: The path to the Circle Launcher directory.
    """
    variables_file = os.path.join(circle_launcher_path, "@Resources", "Variables.inc")
    replaced = False

    with open(variables_file, 'r', encoding="UTF-8") as f:
        content = f.readlines()

    with open(variables_file, 'w', encoding="UTF-8") as f:
        for line in content:
            if line.startswith(f"{app_name}="):
                replaced = True
                set_line(f, app_name, app)
            else:
                f.write(line)
        if not replaced:
            set_line(f, app_name, app)

def set_line(f: TextIOWrapper, name: str, app: dict) -> None:
    """
    Set a line in the file with the application details.
    :param f: The file object to write to.
    :param name: The line to write.
    :param app: A dictionary containing the application details.
    """
    app_id = app['AppID']
    if app['Type'] == 'UWP':
        f.write(f"{name}=[Shell:AppsFolder\\{app_id}]\n")
    elif app['Type'] == 'Win32':
        if app_id.startswith('{'):
            if app_id.endswith('}'):
                f.write(f"{name}=[Shell:::{app_id}]")
            else:
                clsid = app_id.split('\\')[0]
                rest_of_path = '\\'.join(app_id.split('\\')[1:])
                path = get_path_from_folder_clsid(clsid)
                f.write(f"{name}=[\"{path}\\{rest_of_path}\"]\n")
        else:
            f.write(f"{name}=[\"{app_id}\"]\n")