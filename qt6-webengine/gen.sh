#!/bin/sh
VERSION=$(cat VERSION)
CWD=$PWD
pushd ../../qt-${VERSION}
diff '--color=auto' -p -X ../chromium-loongarch64/qt6-webengine/exclude -N -u -r a b > $CWD/qt6-${VERSION}.diff
popd
bash ../chromium/strip-datetime.sh
python3 split.py
