#!/bin/sh
pushd ../../chromium-127.0.6533.72
diff '--color=auto' -p -X ../chromium-loongarch64/chromium/exclude -N -u -r a b > ../chromium-loongarch64/chromium/chromium-127.0.6533.72.diff
popd
bash strip-datetime.sh
