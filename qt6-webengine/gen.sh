CWD=$PWD
cd ../../qt-6.6.2
diff '--color=auto' -p -X ../chromium-loongarch64/qt6-webengine/exclude -N -u -r a b > $CWD/qt6-6.6.2.diff
