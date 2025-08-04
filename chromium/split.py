version = open("VERSION", "r", encoding="utf-8").read().strip()
patches = []
with open(f"chromium-{version}.diff", "r") as f:
    cur = []
    for line in f:
        if line.startswith("diff "):
            if len(cur) > 0:
                patches.append(cur)
            cur = []
        cur.append(line)
    if len(cur) > 0:
        patches.append(cur)

classes = {}
for patch in sorted(patches):
    path = patch[1].split(" ")[1].split("\t")[0][2:]

    # classify
    # https://src.fedoraproject.org/rpms/chromium/tree/rawhide
    if path in ["components/media_router/common/providers/cast/channel/enum_table.h"]:
        # https://src.fedoraproject.org/rpms/chromium/blob/rawhide/f/chromium-130-hardware_destructive_interference_size.patch
        clazz = "1001-Fedora-chromium-130-hardware_destructive_interference_size"
    elif path.startswith("third_party/swiftshader/third_party/llvm-16.0/llvm/include/llvm/Support/"):
        # https://salsa.debian.org/chromium-team/chromium/-/blob/d5eaa49a959d8fbaf5ba1fd6274636526efd9914/debian/patches/fixes/swiftshader-llvm.patch
        clazz = "2001-Debian-swiftshader-llvm"
    elif path in ["third_party/blink/renderer/build/scripts/gperf.py"]:
        # https://salsa.debian.org/chromium-team/chromium/-/commit/b67bb761d36f82c531ecb95fd45b93210080a466
        clazz = "2002-Debian-gperf-3.2"
    elif path in ["build/nocompile.gni", "build/rust/rust_bindgen.gni"]:
        clazz = "3001-fix-invalid-substition-type"
    elif path in [
        "build/config/clang/BUILD.gn",
    ]:
        clazz = "3002-fix-clang-builtins-path"
    elif path.startswith("third_party/swiftshader/"):
        clazz = "4001-loongarch64-swiftshader"
    elif path.startswith("sandbox/"):
        clazz = "4002-loongarch64-sandbox"
    elif path.startswith("third_party/crashpad/"):
        clazz = "4003-loongarch64-crashpad"
    elif path.startswith("third_party/dav1d/"):
        clazz = "4004-loongarch64-dav1d"
    elif path.startswith("third_party/ffmpeg/"):
        clazz = "4005-loongarch64-ffmpeg"
    elif path in [
        "build/rust/rust_target.gni",
    ]:
        clazz = "4006-loongarch64-medium-cmodel"
    elif path.startswith("gpu/"):
        clazz = "4007-loongarch64-gpu"
    elif path.startswith("third_party/xnnpack/"):
        clazz = "4008-loongarch64-xnnpack"
    else:
        clazz = "4009-loongarch64"

    if clazz not in classes:
        classes[clazz] = []
    classes[clazz].append(patch)
    print(path)

for clazz in classes:
    with open(f"chromium-{version}.{clazz}.diff", "w") as f:
        for patch in classes[clazz]:
            print("".join(patch), end="", file=f)

with open(f"chromium-{version}.diff", "w") as f:
    for patch in sorted(patches):
        print("".join(patch), end="", file=f)
