CWD=$PWD
cd ../../../qt
diff '--color=auto' -p -X ../chromium/chromium-loongarch64/qt6-webengine/exclude -N -u -r a b > $CWD/qt6-6.5.1.diff
