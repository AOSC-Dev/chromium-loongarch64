version = "6.8.1"
patches = []
with open(f"qt6-{version}.diff", "r") as f:
    cur = []
    for line in f:
        if line.startswith("diff "):
            if len(cur) > 0:
                patches.append(cur)
            cur = []
        cur.append(line)
    if len(cur) > 0:
        patches.append(cur)

classes = {"loongarch64": []}
for patch in sorted(patches):
    path = patch[1].split(" ")[1].split("\t")[0][2:]

    # classify
    if path.startswith("qtwebengine/src/3rdparty/chromium/third_party/ffmpeg/"):
        clazz = "loongarch64-ffmpeg"
    elif path.startswith("qtwebengine/src/3rdparty/chromium/sandbox/"):
        clazz = "loongarch64-sandbox"
    elif path.startswith("qtwebengine/src/3rdparty/chromium/third_party/crashpad/"):
        clazz = "loongarch64-crashpad"
    elif path.startswith(
        "qtwebengine/src/3rdparty/chromium/third_party/devtools-frontend/"
    ):
        clazz = "rollup"
    elif path.startswith(
        "qtwebengine/src/3rdparty/chromium/ui/gl"
    ):
        # https://gitweb.gentoo.org/repo/gentoo.git/commit/?id=cb122c4d819496c6384278d7817855e5740d1670
        clazz = "Gentoo-x11-header"
    elif path.startswith(
        "qtwebengine/src/3rdparty/chromium/third_party/libvpx/source/libvpx/vpx_dsp/loongarch/"
    ):
        # https://github.com/webmproject/libvpx/commit/391bb5604b85195468e73d576766252f6ce8e427
        clazz = "loongarch64-libvpx-lsx-backport"
    elif path.startswith(
        "qtwebengine/src/3rdparty/chromium/v8"
    ):
        # https://github.com/v8/v8/commit/1ec3c714bf75f01e3f4f6519bebb953eab93df39
        clazz = "loongarch64-v8-backport"
    elif path in [
        "qtwebengine/src/3rdparty/chromium/content/browser/BUILD.gn",
        "qtwebengine/src/3rdparty/chromium/extensions/browser/api/declarative_net_request/BUILD.gn",
        "qtwebengine/src/core/configure/BUILD.root.gn.in"
    ]:
        # https://gitweb.gentoo.org/repo/gentoo.git/tree/dev-qt/qtwebengine/files/qtwebengine-6.7.0-ninja1.12.patch
        clazz = "ninja-race-condition"
    else:
        clazz = "loongarch64"

    if clazz not in classes:
        classes[clazz] = []
    classes[clazz].append(patch)
    print(path)

for clazz in classes:
    with open(f"qt6-{version}.{clazz}.diff", "w") as f:
        for patch in classes[clazz]:
            print("".join(patch), end="", file=f)

with open(f"qt6-{version}.diff", "w") as f:
    for patch in sorted(patches):
        print("".join(patch), end="", file=f)
