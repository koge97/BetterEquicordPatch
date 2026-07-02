//go:build cli

/*
 * SPDX-License-Identifier: GPL-3.0
 * Vencord Installer, a cross platform gui/cli app for installing Vencord
 * Copyright (c) 2023 Vendicated and Vencord contributors
 */

package main

import (
	"image/color"
	"equicordinstaller/buildinfo"
)

const ReleaseUrl = "https://api.github.com/repos/Equicord/Equicord/releases/latest"
const ReleaseUrlFallback = ReleaseUrl
const InstallerReleaseUrl = "https://api.github.com/repos/koge97/BetterEquicordPatch/releases/latest"
const InstallerReleaseUrlFallback = InstallerReleaseUrl

var UserAgent = "EquicordInstaller/" + buildinfo.InstallerGitHash + " (https://github.com/koge97/BetterEquicordPatch)"

var (
	DiscordGreen  = color.RGBA{R: 0x2D, G: 0x7C, B: 0x46, A: 0xFF}
	DiscordRed    = color.RGBA{R: 0xEC, G: 0x41, B: 0x44, A: 0xFF}
	DiscordBlue   = color.RGBA{R: 0x58, G: 0x65, B: 0xF2, A: 0xFF}
	DiscordYellow = color.RGBA{R: 0xfe, G: 0xe7, B: 0x5c, A: 0xff}
)
