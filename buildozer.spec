[app]
title = foodoptions
package.name = foodoptions
package.domain = com.foodoptions
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
version = 0.1
requirements = python3,kivy==1.10.1
orientation = all
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
#android.presplash_color = #1d3b3e
android.permissions = WRITE_EXTERNAL_STORAGE
android.api = 27
android.minapi = 21
android.sdk = 28
#private = False
android.ndk_path = /home/kivy/Android/android-ndk-r16b/
android.sdk_path = /home/kivy/Android/android-sdk-28/
android.arch = armeabi-v7a
p4a.source_dir = /home/kivy/Repos/python-for-android/
[buildozer]
log_level = 2
warn_on_root = 1
