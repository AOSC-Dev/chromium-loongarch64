version = "120.0.6099.216"
with open(f"chromium-{version}.diff", "r") as f:
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
        if path in [
            "base/allocator/partition_allocator/src/partition_alloc/partition_alloc_base/strings/safe_sprintf.h",
            "third_party/blink/renderer/core/paint/fragment_data_iterator.h",
        ]:
            clazz = "Fedora-chromium-120-nullptr_t-without-namespace-std.patch"
        elif path in ["third_party/blink/renderer/core/BUILD.gn"]:
            clazz = "Fedora-chromium-117-mnemonic-error.patch"
        elif path in ["build/config/compiler/BUILD.gn"]:
            clazz = "Fedora-chromium-120-split-threshold-for-reg-with-hint.patch"
        elif path in [
            "third_party/material_color_utilities/src/cpp/palettes/tones.cc",
            "third_party/ruy/src/ruy/profiler/instrumentation.h",
        ]:
            clazz = "Fedora-chromium-120-missing-header-files.patch"
        elif path in [
            "build/nocompile.gni",
            "third_party/libvpx/BUILD.gn",
            "third_party/blink/renderer/platform/BUILD.gn",
            "third_party/blink/renderer/platform/graphics/gpu/webgl_image_conversion.cc",
        ]:
            clazz = "clang"
        elif path in [
            "third_party/webrtc/rtc_base/string_encode.h",
            "third_party/webrtc/api/stats/rtc_stats.h",
            "third_party/swiftshader/third_party/llvm-16.0/llvm/lib/Transforms/IPO/AttributorAttributes.cpp",
            "third_party/ruy/src/ruy/profiler/instrumentation.h",
            "third_party/ruy/src/ruy/profiler/instrumentation.cc",
            "third_party/protobuf/src/google/protobuf/repeated_ptr_field.h",
            "third_party/perfetto/include/perfetto/base/status.h",
            "third_party/material_color_utilities/src/cpp/palettes/tones.cc",
            "third_party/blink/renderer/core/typed_arrays/dom_typed_array.h",
            "third_party/blink/renderer/core/typed_arrays/dom_typed_array.cc",
            "third_party/blink/renderer/core/frame/local_frame_client.h",
            "third_party/blink/renderer/core/frame/local_frame.h",
            "third_party/blink/renderer/bindings/core/v8/native_value_traits_buffer_sources.cc",
            "third_party/blink/public/web/web_local_frame_client.h",
            "third_party/blink/common/interest_group/auction_config_mojom_traits.cc",
        ]:
            clazz = "gcc"
        elif path.startswith("third_party/swiftshader/"):
            clazz = "swiftshader"
        else:
            clazz = "loongarch64"

        if clazz not in classes:
            classes[clazz] = []
        classes[clazz].append(patch)
        print(path)

    for clazz in classes:
        with open(f"chromium-{version}.{clazz}.diff", "w") as f:
            for patch in classes[clazz]:
                print("".join(patch), end="", file=f)
