#!/bin/sh
pushd ../../chromium-129.0.6668.58
diff '--color=auto' -p -X ../chromium-loongarch64/chromium/exclude -N -u -r a b > ../chromium-loongarch64/chromium/chromium-129.0.6668.58.diff
popd
bash strip-datetime.sh
