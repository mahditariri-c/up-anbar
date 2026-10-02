[app]

title = Up Anbar

package.name = upanbar

package.domain = org.mahditariri

source.dir = .

source.include_exts = py,kv,png,jpg,jpeg,ttf,otf,txt,json,md

version = 9.0.0

requirements = python3,kivy==2.3.1,kivymd==1.2.0,openpyxl,reportlab,arabic-reshaper,python-bidi,kivy_garden.graph

orientation = portrait

fullscreen = 0

icon.filename = %(source.dir)s/icon.png


# Android

android.api = 35

android.minapi = 24

android.ndk = 25b

android.archs = arm64-v8a

android.allow_backup = True

android.accept_sdk_license = True


[buildozer]

log_level = 2

warn_on_root = 1
