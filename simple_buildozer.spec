[app]
title = Seabattle
package.name = seabattle
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,jpeg,wav,mp3,json,txt
version = 1.0
requirements = python3,kivy
orientation = landscape
fullscreen = 1

[buildozer]
log_level = 2

[android]
api = 31
minapi = 21
ndk = 23c
archs = arm64-v8a
android.permissions = INTERNET
android.private_storage = True
android.accept_sdk_license = True
