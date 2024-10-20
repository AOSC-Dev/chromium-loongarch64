#!/bin/sh
pushd ../../chromium-130.0.6723.58
diff '--color=auto' -p -X ../chromium-loongarch64/chromium/exclude -N -u -r a b > ../chromium-loongarch64/chromium/chromium-130.0.6723.58.diff
popd
bash strip-datetime.sh
