# Building from Source
If you want build BetterVencordPatch and/or its autopatcher without installing BetterVencordPatch, see the below guide.
Make sure not to put quotes around the arguments.

## Building the Installer
You can use these commands to build the installer (arguments explained below):
- Windows: `go build -ldflags="-H=windowsgui -X main.branch=BRANCH -X main.patchOpenAsar=USE_OPEN_ASAR -X main.sendSuccessNotifications=SEND_SUCCESS_NOTIFICATIONS" --tags cli`
- macOS: `go build -ldflags="-X main.branch=BRANCH -X main.patchOpenAsar=USE_OPEN_ASAR -X main.sendSuccessNotifications=SEND_SUCCESS_NOTIFICATIONS" --tags cli`

These arguments can be used to customize the Vencord installer:
- BRANCH: The Discord branch that BetterVencordPatch will patch
    - Type: string
    - Possible values: stable | ptb | canary
- USE_OPEN_ASAR: If the installer will patch OpenAsar
    - Type: boolean
    - Possible values: true | false
- SEND_SUCCESS_NOTIFICATIONS: If the installer will send a success notification on success
    - Type: boolean
    - Possible values: true | false

## Building the Auto-patcher
You can use these commands to build the auto-patcher (arguments explained below):
- Windows: `go build -ldflags="-H=windowsgui -X main.branch=BRANCH" --tags avp_win -o autovencordpatch.exe`
- macOS: `go build -ldflags="-X main.branch=BRANCH" --tags avp_macos -o autovencordpatch`

These arguments can be used to customize the auto-patcher:
- BRANCH: The branch of Discord that will be watched for updates
    - Type: string
    - Possible values: stable | ptb | canary