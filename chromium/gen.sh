#!/bin/sh
cd ../../chromium-123.0.6312.58
diff '--color=auto' -p -X ../chromium-loongarch64/chromium/exclude -N -u -r a b > ../chromium-loongarch64/chromium/chromium-123.0.6312.58.diff
bash strip-datetime.sh
