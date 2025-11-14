import os
from pathlib import Path
import subprocess
import sys
import shutil
from win32com.client import Dispatch

def print_status(msg):
    print(f"[+] {msg}")

def main():
    # Paths
    extensions_folder = Path(os.getenv("LOCALAPPDATA")) / "spicetify" / "Extensions"
    startup_folder = Path(os.getenv("APPDATA")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"

    # Ensure folders exist
    extensions_folder.mkdir(parents=True, exist_ok=True)
    startup_folder.mkdir(parents=True, exist_ok=True)
    print_status(f"Spicetify Extensions folder: {extensions_folder}")
    print_status(f"Startup folder: {startup_folder}")

    # Install required Python modules
    print_status("Installing Python modules: flask, requests, flask_cors")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "requests", "flask_cors"])

    # Copy scripts directly into Extensions
    scripts_src = Path(__file__).parent / "scripts"
    py_script = scripts_src / "SPOTIFY_DOWNLOAD.py"
    js_script = scripts_src / "SPOTIFY_DOWNLOAD.js"

    if py_script.exists():
        shutil.copy(py_script, extensions_folder)
        print_status(f"Copied {py_script.name} to {extensions_folder}")
    else:
        print_status(f"Python script not found: {py_script}")

    if js_script.exists():
        shutil.copy(js_script, extensions_folder)
        print_status(f"Copied {js_script.name} to {extensions_folder}")
    else:
        print_status(f"JS script not found: {js_script}")

    # Create startup shortcut
    shortcut_path = startup_folder / "SpotifyDownloader.lnk"
    target = sys.executable  # pythonw.exe
    arguments = str(extensions_folder / "SPOTIFY_DOWNLOAD.py")

    print_status(f"Creating startup shortcut: {shortcut_path}")
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(str(shortcut_path))
    shortcut.Targetpath = target
    shortcut.Arguments = f'"{arguments}"'
    shortcut.WorkingDirectory = str(extensions_folder)
    shortcut.WindowStyle = 7  # Minimized
    shortcut.save()
    print_status("Shortcut created successfully")

    # Start the shortcut immediately
    print_status("Starting Spotify Downloader...")
    subprocess.Popen(['cmd', '/c', 'start', '', str(shortcut_path)], shell=True)

    # Apply Spicetify
    print_status("Applying Spicetify...")
    try:
        subprocess.run(["spicetify", "apply"], check=True)
        print_status("Spicetify applied successfully")
        print_status("May Require A System Restart To Function Properly.")
    except Exception as e:
        print_status(f"Failed to apply Spicetify: {e}")

if __name__ == "__main__":
    main()
