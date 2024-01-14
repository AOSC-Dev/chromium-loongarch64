# chromium-loongarch64

Attempt to port chromium to loongarch64.

Status: working! Although debug build can trigger raw_ptr bugs.

Based on:

- [loongson/electron](https://github.com/loongson/electron/)
- [prcups/qt6-webengine-loongarchlinux](https://github.com/prcups/qt6-webengine-loongarchlinux/)
- various patches from linux distributions for building chromium with gcc
- llvm 16 files are generated by running `third_party/swiftshader/third_party/llvm-16.0/scripts/update.py`
