[app]

title = Hesaplayici
package.name = hesaplayici
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

[buildozer]
log_level = 2
warn_on_root = 1

android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.orientation = portrait
android.fullscreen = 0
android.arch = arm64-v8a
p4a.bootstrap = sdl2
p4a.requirements = python3,kivy,kivymd
