W3 Personal Sandbox Android wrapper. Open this folder in Android Studio and
build app-debug.apk. Web assets are packaged in app/src/main/assets/www.
The WebView only loads the built-in appassets.androidplatform.net path. File
selection uses Android's document picker; JSON export uses ACTION_CREATE_DOCUMENT.
No Termux server or INTERNET permission is required. Keep the same package ID
and signing key for updates; debug keys are not suitable for a public release.
