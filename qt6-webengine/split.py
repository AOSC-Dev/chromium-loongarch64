version = "6.6.3"
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
    elif path.startswith("qtwebengine/src/3rdparty/chromium/third_party/devtools-frontend/"):
        clazz = "rollup"
    elif path.startswith("qtwebengine/src/3rdparty/chromium/v8/src/regexp/"):
        clazz = "loongarch64-regexp-backport"
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
