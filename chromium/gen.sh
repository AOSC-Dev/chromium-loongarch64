#!/bin/sh
pushd ../../chromium-132.0.6834.83
diff '--color=auto' -p -X ../chromium-loongarch64/chromium/exclude -N -u -r a b > ../chromium-loongarch64/chromium/chromium-132.0.6834.83.diff
popd
bash strip-datetime.sh
