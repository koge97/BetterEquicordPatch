import os
import getpass
import platform

os.chdir(os.path.dirname(__file__))
def clear():
    os.system("cls")

clear()
print("[BetterEquicordPatch Installer (Windows)]")
branch = input("Enter the branch of Discord to be patched by Equicord (stable, ptb, canary): ")
if branch not in ["stable", "ptb", "canary"]:
    input("This branch of Discord doesn't exist. ")
    exit()
openasar = input("Patch this branch of Discord with OpenAsar (y/N)? ").lower().strip() == "y"
use_autopatch = input("Patch this branch of Discord through updates (y/N)? ").lower().strip() == "y"
send_success_notifications = input("Send notifications on success (y/N)? ").lower().strip() == "y"

clear()
print("[Installing BetterEquicordPatch]")
print(f"Installing with preferences: branch='{branch}', openasar={openasar}, use_autopatch={use_autopatch}, send_success_notifications={send_success_notifications}")
print("\nRunning pre-install checks...", end=" ", flush=True)
os.makedirs(f"C:/Users/{getpass.getuser()}/AppData/Local/betterequicordpatch/", exist_ok=True)
if platform.system() != "Windows":
    print("failed")
    input("This operating system is not supported by this installer. ")
    exit()
for dir in ["./autopatch/" if use_autopatch else "./installer/"]:
    if not os.path.exists(dir):
        print("failed")
        input(f"The directory '{dir}' is missing. ")
        exit()
print("done")

branch_suffixes = {
    "stable": "",
    "ptb": "PTB",
    "canary": "Canary"
}
os.chdir("./installer/")
print("Building EquicordInstaller.exe...", end=" ", flush=True)
os.system("go mod tidy")
os.system("set CGO_ENABLED=0")
os.system("set GOOS=windows")
os.system("set GOARCH=amd64")
os.system(f"go build -ldflags=\"-H=windowsgui -X main.branch={branch} -X main.patchOpenAsar={str(openasar).lower()} -X main.sendSuccessNotifications='{str(send_success_notifications).lower()}'\" --tags cli")
if os.path.exists(f"C:/Users/{getpass.getuser()}/AppData/Local/betterequicordpatch/equicordinstaller.exe"):
    os.remove(f"C:/Users/{getpass.getuser()}/AppData/Local/betterequicordpatch/equicordinstaller.exe")
os.rename("equicordinstaller.exe", f"C:/Users/{getpass.getuser()}/AppData/Local/betterequicordpatch/equicordinstaller.exe")
print("done")

if use_autopatch:
    print("Building auto-patch binary...", end=" ", flush=True)
    os.system("go mod tidy")
    os.system(f"go build -ldflags=\"-H=windowsgui -X main.branch={branch_suffixes[branch]}\" --tags avp_win -o autoequicordpatch.exe")
    # uncomment this line and comment the line above to see autopatcher output
    # os.system(f"go build -ldflags=\"-X main.branch={branch_suffixes[branch]}\" --tags avp_win -o autoequicordpatch.exe")
    os.system("taskkill /f /im autoequicordpatch.exe >NUL 2>&1")
    if os.path.exists(f"C:/Users/{getpass.getuser()}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/autoequicordpatch.exe"):
        os.remove(f"C:/Users/{getpass.getuser()}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/autoequicordpatch.exe")
    os.rename("autoequicordpatch.exe", f"C:/Users/{getpass.getuser()}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/autoequicordpatch.exe")
    print("done")

input("\nSuccessfully installed BetterEquicordPatch! ")