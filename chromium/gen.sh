#!/bin/sh
VERSION=$(cat VERSION)
pushd ../../chromium-${VERSION}
diff '--color=auto' -p -X ../chromium-loongarch64/chromium/exclude -N -u -r a b > ../chromium-loongarch64/chromium/chromium-${VERSION}.diff
popd
bash strip-datetime.sh
python3 split.py
