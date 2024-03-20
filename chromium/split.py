version = "123.0.6312.58"
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
    if path in [
        "base/allocator/partition_allocator/src/partition_alloc/partition_alloc_base/strings/safe_sprintf.h",
        "third_party/blink/renderer/core/paint/fragment_data_iterator.h",
    ]:
        # https://src.fedoraproject.org/rpms/chromium/blob/rawhide/f/chromium-121-nullptr_t-without-namespace-std.patch
        clazz = "1000-Fedora-chromium-121-nullptr_t-without-namespace-std"
    elif path in ["build/config/compiler/BUILD.gn"]:
        # https://src.fedoraproject.org/rpms/chromium/blob/rawhide/f/chromium-120-split-threshold-for-reg-with-hint.patch
        clazz = "1001-Fedora-chromium-120-split-threshold-for-reg-with-hint"
    elif path in [
        "base/check_op.h",
        "base/containers/flat_map.h",
        "chrome/browser/webauthn/authenticator_request_dialog_model.h",
        "chrome/test/chromedriver/chrome/web_view_impl.cc",
        "components/feature_engagement/internal/never_event_storage_validator.h",
        "gin/time_clamper.h",
        "net/base/net_export.h",
        "third_party/abseil-cpp/absl/strings/string_view.h",
        "third_party/dawn/src/tint/lang/spirv/reader/ast_parser/namer.h",
        "third_party/material_color_utilities/src/cpp/palettes/tones.cc",
        "third_party/ruy/src/ruy/profiler/instrumentation.h",
        "third_party/swiftshader/third_party/llvm-10.0/llvm/lib/Support/Unix/Signals.inc",
        "third_party/vulkan-deps/vulkan-validation-layers/src/layers/external/vma/vk_mem_alloc.h",
        "third_party/webrtc/audio/utility/channel_mixer.cc",
        "third_party/webrtc/modules/include/module_common_types_public.h",
        "ui/gfx/linux/drm_util_linux.h",
    ]:
        clazz = "1002-Fedora-chromium-122-missing-header-files"
    elif path in ["optional"]:
        # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/fixes/absl-optional.patch?ref_type=heads
        clazz = "2000-Debian-fixes-absl-optional"
    elif path in ["mojo/public/cpp/bindings/type_converter.h"]:
        # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/upstream/std-to-address.patch?ref_type=heads
        clazz = "2001-Debian-upstream-std-to-address"
    elif path in ["base/allocator/partition_allocator/src/partition_alloc/starscan/stats_collector.h"]:
        # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/fixes/internalalloc.patch?ref_type=heads
        clazz = "2002-Debian-fixes-internalalloc"
    elif path in ["components/page_load_metrics/browser/observers/ad_metrics/aggregate_frame_data.h"]:
        # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/fixes/optional2.patch?ref_type=heads
        clazz = "2003-Debian-fixes-optional2"
    elif path in ["tools/v8_context_snapshot/BUILD.gn", "chrome/BUILD.gn"]:
        clazz = "3001-rust-ld-bfd"
    elif path in [
        "third_party/devtools-frontend/src/scripts/build/rollup.config.js"
    ]:
        clazz = "3002-rollup"
    elif path in ["build/nocompile.gni", "build/rust/rust_bindgen.gni"]:
        clazz = "3003-fix-invalid-substition-type"
    elif path in [
        "build/config/clang/BUILD.gn",
    ]:
        clazz = "3004-fix-clang-builtins-path"
    elif path in [
        "third_party/blink/renderer/core/layout/hit_test_request.h",
        "third_party/blink/renderer/platform/peerconnection/resolution_monitor.cc",
        "third_party/tflite/src/tensorflow/lite/kernels/internal/spectrogram.h",
        "third_party/webrtc/common_video/h264/sps_parser.h",
        "third_party/webrtc/modules/video_coding/utility/ivf_file_reader.cc",
    ]:
        clazz = "3005-fix-missing-header"
    elif path in [
        "chrome/browser/ui/webui/top_chrome/webui_contents_wrapper.h",
    ]:
        clazz = "3006-fix-static-assertion"
    elif path in [
        "third_party/libvpx/BUILD.gn",
        "third_party/blink/renderer/platform/BUILD.gn",
        "third_party/blink/renderer/platform/graphics/gpu/webgl_image_conversion.cc",
        "third_party/libvpx/source/config/linux/loongarch/vpx_dsp_rtcd.h",
        "third_party/libvpx/source/config/linux/loongarch/vp8_rtcd.h",
    ]:
        clazz = "4000-loongarch64-clang-no-lsx"
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
    else:
        clazz = "4007-loongarch64"

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