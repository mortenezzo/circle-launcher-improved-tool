import os

def append_launcher_to_variables(exe_path: str, app_name: str, circle_launcher_path: str) -> None:
    variables_file = os.path.join(circle_launcher_path, "@Resources", "Variables.inc")
    normalized_exe_path = os.path.normpath(exe_path)

    with open(variables_file, 'r', encoding="UTF-8") as f:
        content = f.readlines()

    with open(variables_file, 'w', encoding="UTF-8") as f:
        for line in content:
            if line.startswith(f"{app_name}="):
                f.write(f"{app_name}=[\"{normalized_exe_path}\"]\n")
                continue
            else:
                f.write(line)