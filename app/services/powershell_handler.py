import json
import shutil
import subprocess

def get_available_shell():
    """
    Get the available shell on the system.
    Returns:
        str: The name of the available shell.
    """
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if not shell:
        raise FileNotFoundError("No PowerShell or PowerShell Core found on the system.")
    return shell

def get_system_apps():
    """
    Get a list of system applications using PowerShell.
    Returns: A list of dictionaries containing the application type, name, and AppID.
    """
    shell_path = get_available_shell()
    command = [
        shell_path,
        "-NoProfile",
        "-Command",
        "Get-StartApps | ForEach-Object { if ($_.AppID -like '*Microsoft.*') { [PSCustomObject]@{ Type='UWP'; Name=$_.Name; AppID=$_.AppID } } else { [PSCustomObject]@{ Type='Win32'; Name=$_.Name; AppID=$_.AppID } } } | ConvertTo-Json"
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True)
        apps = json.loads(result.stdout.strip())
        return apps
    except subprocess.CalledProcessError as e:
        print(f"Error executing PowerShell command: {e}")
        return {}
    except FileNotFoundError as e:
        print(f"PowerShell executable not found: {e}")
        return {}