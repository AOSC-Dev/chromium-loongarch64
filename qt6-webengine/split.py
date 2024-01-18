version = "6.5.1"
with open(f"qt6-{version}.diff", "r") as f:
    cur = []
    patches = []
    for line in f:
        if line.startswith("diff "):
            if len(cur) > 0:
                patches.append(cur)
            cur = []
        cur.append(line)
    if len(cur) > 0:
        patches.append(cur)

    classes = {"loongarch64": []}
    for patch in patches:
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
