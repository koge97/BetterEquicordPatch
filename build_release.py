import os
import shutil

os.chdir(os.path.dirname(__file__))
def clear():
    for i in range(2):
        os.system("clear")

def run_sh(sh):
    for cmd in sh.split("\n"):
        os.system(f"{cmd}")

def build(openasar, op):
    global branch
    global send_success_notifications

    suffix = ".app" if op == "Darwin" else ".exe"
    branch = "stable"
    send_success_notifications = True

    build_vi = f"""
    go mod tidy
    CGO_ENABLED=0{" GOOS=windows GOARCH=amd64 " if op == "Windows" else " "}go build -ldflags=\"{"-H=windowsgui " if op == "Windows" else ""}-X main.branch={branch} -X main.patchOpenAsar={str(openasar).lower()} -X main.sendSuccessNotifications={str(send_success_notifications).lower()}\" --tags cli
    """
    build_vi_darwin = """
    mkdir -p EquicordInstaller.app/Contents/MacOS
    mkdir -p EquicordInstaller.app/Contents/Resources
    cp macos/Info.plist EquicordInstaller.app/Contents/Info.plist
    mv EquicordInstaller EquicordInstaller.app/Contents/MacOS/EquicordInstaller
    cp macos/icon.icns EquicordInstaller.app/Contents/Resources/icon.icns
    rm -rf ../EquicordInstaller.app
    """
    run_sh(build_vi)
    if op == "Darwin":
        run_sh(build_vi_darwin)
    os.system(f"mv EquicordInstaller{suffix} ../binaries/EquicordInstaller-{"no_" if not openasar else ""}openasar{suffix}")

clear()
if os.path.exists("./binaries/"):
    shutil.rmtree("./binaries")
os.mkdir("./binaries/")

os.chdir("./installer/")
build_avp = f"""
go mod tidy
CGO_ENABLED=0 go build -o autoequicordpatch --tags avp_macos
CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build -ldflags=\"-H=windowsgui\" -o autoequicordpatch.exe --tags avp_win
"""
run_sh(build_avp)
os.rename("./autoequicordpatch", "../binaries/autoequicordpatch")
os.rename("./autoequicordpatch.exe", "../binaries/autoequicordpatch.exe")

for op in ["Windows", "Darwin"]:
    for openasar in [False, True]:
        build(openasar, op)
os.system("cp ../autopatch/org.aaron.autoequicordpatch.plist ../binaries/org.aaron.autoequicordpatch.plist")