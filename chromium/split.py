#!/usr/bin/env python3

from pathlib import Path

from format import normalize_diff_lines

version = Path("VERSION").read_text(encoding="utf-8").strip()
main_patch = Path(f"chromium-{version}.diff")

patches = []
cur = []
for line in main_patch.read_text(encoding="utf-8").splitlines(keepends=True):
    if line.startswith("diff "):
        if cur:
            patches.append(normalize_diff_lines(cur))
        cur = []
    cur.append(line)
if cur:
    patches.append(normalize_diff_lines(cur))


def patch_path(patch):
    for line in patch:
        if line.startswith("--- a/"):
            return line.split("\t", 1)[0][len("--- a/") :]
        if line.startswith("+++ b/"):
            return line.split("\t", 1)[0][len("+++ b/") :]
    raise ValueError("patch has no normalized file header")


def classify(path):
    # https://src.fedoraproject.org/rpms/chromium/tree/rawhide
    if path in ["components/media_router/common/providers/cast/channel/enum_table.h"]:
        # https://src.fedoraproject.org/rpms/chromium/blob/rawhide/f/chromium-130-hardware_destructive_interference_size.patch
        return "1001-Fedora-chromium-130-hardware_destructive_interference_size"
    if path in ["build/nocompile.gni", "build/rust/rust_bindgen.gni"]:
        return "3001-fix-invalid-substition-type"
    if path in ["build/config/clang/BUILD.gn", "build/config/clang/clang.gni"]:
        return "3002-fix-clang-builtins-path"
    if path.startswith("third_party/swiftshader/"):
        return "4001-loongarch64-swiftshader"
    if path.startswith("sandbox/"):
        return "4002-loongarch64-sandbox"
    if path.startswith("third_party/crashpad/"):
        return "4003-loongarch64-crashpad"
    if path.startswith("third_party/dav1d/"):
        return "4004-loongarch64-dav1d"
    if path.startswith("third_party/ffmpeg/") or path.startswith("media/ffmpeg/scripts/"):
        return "4005-loongarch64-ffmpeg"
    if path in [
        "build/rust/rust_target.gni",
        "build/rust/gni_impl/rust_target.gni",
    ]:
        return "4006-loongarch64-medium-cmodel"
    if path.startswith("gpu/"):
        return "4007-loongarch64-gpu"
    if path.startswith("third_party/xnnpack/"):
        return "4008-loongarch64-xnnpack"
    if path.startswith("v8/"):
        return "4010-loongarch64-v8-backports"
    return "4009-loongarch64"


classes = {}
for patch in sorted(patches):
    path = patch_path(patch)
    clazz = classify(path)
    classes.setdefault(clazz, []).append(patch)
    print(path)

for clazz, class_patches in classes.items():
    with open(f"chromium-{version}.{clazz}.diff", "w", encoding="utf-8") as f:
        for patch in class_patches:
            f.write("".join(patch))

with main_patch.open("w", encoding="utf-8") as f:
    for patch in sorted(patches):
        f.write("".join(patch))
