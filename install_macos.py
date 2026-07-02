import os
import platform

os.chdir(os.path.dirname(__file__))
def clear():
    for i in range(2):
        os.system("clear")

def run_sh(sh):
    for cmd in sh.split("\n"):
        os.system(f"{cmd}")

clear()
print("[BetterEquicordPatch Installer (macOS)]")
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
if platform.system() != "Darwin":
    print("failed")
    input("This operating system is not supported by this installer. ")
    exit()
for dir in ["./autopatch/" if use_autopatch else "./installer/", "./installer/"]:
    if not os.path.exists(dir):
        print("failed")
        input(f"The directory '{dir}' is missing. ")
        exit()
print("done")

os.chdir("./installer/")
build_vi = f"""
go mod tidy
CGO_ENABLED=0 go build -ldflags=\"-X main.branch={branch} -X main.patchOpenAsar={str(openasar).lower()} -X main.sendSuccessNotifications={str(send_success_notifications).lower()}\" --tags cli
mkdir -p EquicordInstaller.app/Contents/MacOS
mkdir -p EquicordInstaller.app/Contents/Resources
cp macos/Info.plist EquicordInstaller.app/Contents/Info.plist
mv EquicordInstaller EquicordInstaller.app/Contents/MacOS/EquicordInstaller
cp macos/icon.icns EquicordInstaller.app/Contents/Resources/icon.icns
rm -rf ../EquicordInstaller.app
mv EquicordInstaller.app ../EquicordInstaller.app
"""
print("Building EquicordInstaller.app...", end=" ", flush=True)
run_sh(build_vi)
print("done")

if use_autopatch:
    print("Building auto-patch binary...", end=" ", flush=True)
    build_avp = f"""
    go mod tidy
    CGO_ENABLED=0 go build -ldflags=\"-X main.branch={branch}\" --tags avp_macos -o autoequicordpatch
    chmod +x autoequicordpatch
    mv autoequicordpatch ../EquicordInstaller.app/Contents/Resources/autoequicordpatch
    """
    run_sh(build_avp)
    print("done")

os.chdir("../")
mv_to_applications = """
rm -rf /Applications/EquicordInstaller.app
mv EquicordInstaller.app /Applications/EquicordInstaller.app
"""
run_sh(mv_to_applications)

if use_autopatch:
    print("Running auto-patch install scripts...", end=" ", flush=True)
    install = """
    cp autopatch/org.koge97.autoequicordpatch.plist ~/Library/LaunchAgents/org.koge97.autoequicordpatch.plist
    launchctl unload ~/Library/LaunchAgents/org.koge97.autoequicordpatch.plist > /dev/null 2>&1
    launchctl load ~/Library/LaunchAgents/org.koge97.autoequicordpatch.plist > /dev/null 2>&1
    open /Applications/EquicordInstaller.app
    """
    run_sh(install)
    print("done")

input("\nSuccessfully installed BetterEquicordPatch! ")
