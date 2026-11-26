[app]
title = WirePro
package.name = wirepro
package.domain = com.innovative.wirepro
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = assets/*,images/*
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license_agreement = True
android.ant = auto
android.archs = arm64-v8a, armeabi-v7a
p4a.bootstrap = sdl2
p4a.whitelist = 

[app:ios]
ios.kivy_version = 2.3.0
