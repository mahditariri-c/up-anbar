[app]
title = Up Anbar
package.name = upanbar
package.domain = org.mahditariri
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,ttf,otf,txt,json,md
source.include_patterns = fonts/*.ttf,fonts/*.otf

version = 10.0

requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow

orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.minapi = 24
android.api = 33
android.targetapi = 33
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.accept_sdk_license = True
android.permissions = WRITE_EXTERNAL_STORAGE
android.ndk = 25b
