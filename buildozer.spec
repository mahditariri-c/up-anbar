[app]
title = Up Anbar
package.name = upanbar
package.domain = org.mahditariri
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,ttf,otf,txt,json,md,so
source.include_patterns = fonts/*.ttf
version = 10.0
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,openpyxl,reportlab,arabic-reshaper,python-bidi,kivy_garden.graph
orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 36
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.minapi = 29
android.ndk = 29
android.accept_sdk_license = True
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, CAMERA