[app]
title = My Flash App
package.name = flashapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.2.1,pyjnius
android.permissions = CAMERA, FLASHLIGHT
android.api = 31
android.minapi = 21
android.accept_sdk_license = True
