#!/bin/sh
pushd ../../chromium-131.0.6778.85
diff '--color=auto' -p -X ../chromium-loongarch64/chromium/exclude -N -u -r a b > ../chromium-loongarch64/chromium/chromium-131.0.6778.85.diff
popd
bash strip-datetime.sh
