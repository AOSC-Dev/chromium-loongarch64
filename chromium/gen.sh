#!/bin/sh
pushd ../../chromium-126.0.6478.114
diff '--color=auto' -p -X ../chromium-loongarch64/chromium/exclude -N -u -r a b > ../chromium-loongarch64/chromium/chromium-126.0.6478.114.diff
popd
bash strip-datetime.sh
