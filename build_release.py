import os
import shutil

os.chdir(os.path.dirname(__file__))
def clear():
    for i in range(2):
        os.system("clear")

def run_sh(sh):
    for cmd in sh.split("\n"):
        os.system(f"{cmd}")

def build(openasar, op, arch="amd64"):
    global branch
    global send_success_notifications

    suffix = ".app" if op == "Darwin" else ".exe"
    branch = "stable"
    send_success_notifications = True

    goos_goarch = f" GOOS=windows GOARCH={arch} " if op == "Windows" else f" GOOS=darwin GOARCH={arch} "
    build_vi = f"""
    go mod tidy
    CGO_ENABLED=0{goos_goarch}go build -ldflags=\"{"-H=windowsgui " if op == "Windows" else ""}-X main.branch={branch} -X main.patchOpenAsar={str(openasar).lower()} -X main.sendSuccessNotifications={str(send_success_notifications).lower()}\" -o EquicordInstaller{suffix if op == "Windows" else ""} --tags cli
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
    arch_tag = "-arm64" if arch == "arm64" else ""
    os.system(f"mv EquicordInstaller{suffix} ../binaries/EquicordInstaller-{"no_" if not openasar else ""}openasar{arch_tag}{suffix}")

clear()
if os.path.exists("./binaries/"):
    shutil.rmtree("./binaries")
os.mkdir("./binaries/")

os.chdir("./installer/")
build_avp = f"""
go mod tidy
CGO_ENABLED=0 GOOS=darwin GOARCH=amd64 go build -o autoequicordpatch --tags avp_macos
CGO_ENABLED=0 GOOS=darwin GOARCH=arm64 go build -o autoequicordpatch-arm64 --tags avp_macos
CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build -ldflags=\"-H=windowsgui\" -o autoequicordpatch.exe --tags avp_win
CGO_ENABLED=0 GOOS=windows GOARCH=arm64 go build -ldflags=\"-H=windowsgui\" -o autoequicordpatch-arm64.exe --tags avp_win
"""
run_sh(build_avp)
os.rename("./autoequicordpatch", "../binaries/autoequicordpatch")
os.rename("./autoequicordpatch-arm64", "../binaries/autoequicordpatch-arm64")
os.rename("./autoequicordpatch.exe", "../binaries/autoequicordpatch.exe")
os.rename("./autoequicordpatch-arm64.exe", "../binaries/autoequicordpatch-arm64.exe")

for op in ["Windows", "Darwin"]:
    for openasar in [False, True]:
        build(openasar, op)
        build(openasar, op, arch="arm64")
os.system("cp ../autopatch/org.koge97.autoequicordpatch.plist ../binaries/org.koge97.autoequicordpatch.plist")