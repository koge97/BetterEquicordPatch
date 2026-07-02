import os
import json
import shutil
import zipfile
import getpass
import platform
import requests
from sys import exit

os.chdir(os.path.dirname(__file__))
def clear():
    os.system("cls" if platform.system() == "Windows" else "clear;clear")

clear()
print("[BetterEquicordPatch Installer]")
print("This installer will download the latest files from GitHub.")
print("")
autopatch = input("Automatically patch Discord with Equicord through updates (y/N)? ").lower().strip() == "y"
openasar = input("Patch OpenAsar (y/N)? ").lower().strip() == "y"

releases = requests.get("https://api.github.com/repos/introvertednoob/bettervencordpatch/releases")
if not releases.ok:
    print("\nCouldn't fetch releases. Exiting...")
    exit()

paths = {
    "Windows": [
        f"C:/Users/{getpass.getuser()}/AppData/Local/BetterEquicordPatch/equicordinstaller.exe",
        f"C:/Users/{getpass.getuser()}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/autoequicordpatch.exe",
    ],
    "Darwin": [
        f"/Applications/EquicordInstaller.app",
        f"/Applications/EquicordInstaller.app/Contents/Resources/autoequicordpatch",
    ],
}

if platform.system() == "Windows":
    os.system("taskkill /f /im autoequicordpatch.exe >NUL 2>&1")
    os.makedirs(f"C:/Users/{getpass.getuser()}/AppData/Local/BetterEquicordPatch/", exist_ok=True)

clear()
print("[Downloading and moving required files...]")
rel = json.loads(releases.text)
for asset in rel[0]["assets"]:
    if platform.system() == "Darwin":
        if f"EquicordInstaller-{"no_" if not openasar else ""}openasar.app.zip" == asset["name"]:
            open("EquicordInstaller.app.zip", "wb").write(requests.get(asset["browser_download_url"]).content)
            if os.path.exists("/Applications/EquicordInstaller.app"):
                shutil.rmtree("/Applications/EquicordInstaller.app")
            with zipfile.ZipFile("EquicordInstaller.app.zip", 'r') as zip_ref:
                zip_ref.extractall("/Applications/")
            shutil.move(f"/Applications/EquicordInstaller-{"no_" if not openasar else ""}openasar.app", "/Applications/EquicordInstaller.app")
            os.system("chmod +x /Applications/EquicordInstaller.app/Contents/MacOS/equicordinstaller")
            os.remove("EquicordInstaller.app.zip")
            print(f"Successfully downloaded BetterEquicordPatch")
    elif platform.system() == "Windows":
        if f"EquicordInstaller-{"no_" if not openasar else ""}openasar.exe" == asset["name"]:
            open(f"C:/Users/{getpass.getuser()}/AppData/Local/BetterEquicordPatch/equicordinstaller.exe", "wb").write(requests.get(asset["browser_download_url"]).content)
            print(f"Successfully downloaded BetterEquicordPatch")
        elif f"autoequicordpatch.exe" == asset["name"] and autopatch:
            open(f"C:/Users/{getpass.getuser()}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/autoequicordpatch.exe", "wb").write(requests.get(asset["browser_download_url"]).content)
            print(f"Successfully installed autopatch component")

if platform.system() == "Darwin":
    for asset in rel[0]["assets"]:
        if asset["name"] == "org.aaron.autoequicordpatch.plist":
            open(f"/Users/{getpass.getuser()}/Library/LaunchAgents/org.aaron.autoequicordpatch.plist", "wb").write(requests.get(asset["browser_download_url"]).content)
            print(f"Successfully installed autopatch launchd plist (macOS)")
        elif asset["name"] == "autoequicordpatch" and autopatch:
            open(f"/Applications/EquicordInstaller.app/Contents/Resources/autoequicordpatch", "wb").write(requests.get(asset["browser_download_url"]).content)
            os.system("chmod +x /Applications/EquicordInstaller.app/Contents/Resources/autoequicordpatch")
            print(f"Successfully installed autopatch component")
    os.system("open /Applications/EquicordInstaller.app")

print("\nSuccessfully installed BetterEquicordPatch!")
input("If you're on Windows and installed the auto-patcher, make sure to restart your computer so the auto-patcher can run. ")
exit()
