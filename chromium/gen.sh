#!/bin/sh
pushd ../../chromium-124.0.6367.118
diff '--color=auto' -p -X ../chromium-loongarch64/chromium/exclude -N -u -r a b > ../chromium-loongarch64/chromium/chromium-124.0.6367.118.diff
popd
bash strip-datetime.sh
