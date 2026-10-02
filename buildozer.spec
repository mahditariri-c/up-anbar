[app]

title = Up Anbar

package.name = upanbar

package.domain = org.mahditariri

source.dir = .

source.include_exts = py,kv,png,jpg,jpeg,ttf,otf,txt,json,md

version = 9.0.0

requirements = python3,kivy,kivymd,openpyxl,reportlab,arabic-reshaper,python-bidi,kivy_garden.graph

orientation = portrait

fullscreen = 0

icon.filename = %(source.dir)s/icon.png

android.api = 36
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.minapi = 24
android.ndk = 29
android.build_tools_version = 35.0.0
android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
