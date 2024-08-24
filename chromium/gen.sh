#!/bin/sh
pushd ../../chromium-128.0.6613.84
diff '--color=auto' -p -X ../chromium-loongarch64/chromium/exclude -N -u -r a b > ../chromium-loongarch64/chromium/chromium-128.0.6613.84.diff
popd
bash strip-datetime.sh
