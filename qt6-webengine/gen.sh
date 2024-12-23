CWD=$PWD
pushd ../../qt-6.8.1
diff '--color=auto' -p -X ../chromium-loongarch64/qt6-webengine/exclude -N -u -r a b > $CWD/qt6-6.8.1.diff
popd
bash ../chromium/strip-datetime.sh
