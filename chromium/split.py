version = "125.0.6422.60"
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
    if path in ["build/config/compiler/BUILD.gn"]:
        # https://src.fedoraproject.org/rpms/chromium/blob/rawhide/f/chromium-120-split-threshold-for-reg-with-hint.patch
        clazz = "1000-Fedora-chromium-120-split-threshold-for-reg-with-hint"
    elif path in ["optional"]:
        # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/fixes/absl-optional.patch?ref_type=heads
        clazz = "2000-Debian-fixes-absl-optional"
    elif path in [
        "base/allocator/partition_allocator/src/partition_alloc/starscan/stats_collector.h"
    ]:
        # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/fixes/stats-collector.patch
        clazz = "2001-Debian-fixes-stats-collector"
    elif (
        path.startswith("third_party/blink/renderer/")
        or path in ["tools/privacy_budget/font_indexer/font_indexer.cc"]
    ) and path not in [
        "third_party/blink/renderer/platform/BUILD.gn",
        "third_party/blink/renderer/platform/graphics/gpu/webgl_image_conversion.cc",
        "third_party/blink/renderer/platform/graphics/cpu/loongarch64/webgl_image_conversion_lsx.h",
        "third_party/blink/renderer/bindings/core/v8/script_streamer.cc",
        "third_party/blink/renderer/modules/webgpu/gpu_adapter_info.h",
    ]:
        # https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1067886
        # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/fixes/bad-font-gc0000.patch
        # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/fixes/bad-font-gc000.patch
        # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/fixes/bad-font-gc00.patch
        # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/fixes/bad-font-gc0.patch
        # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/fixes/bad-font-gc1.patch
        # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/fixes/bad-font-gc11.patch
        # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/fixes/bad-font-gc2.patch
        # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/fixes/bad-font-gc3.patch
        clazz = "2002-Debian-fixes-blink"
    elif path in [
        "chrome/browser/devtools/BUILD.gn"
    ]:
        # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/upstream/ninja.patch
        clazz = "2003-Debian-upstream-ninja"
    elif path in [
        "chrome/browser/ui/tabs/tab_strip_model.h"
    ]:
        # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/upstream/tabstrip-include.patch
        clazz = "2004-Debian-upstream-tabstrip-include"
    elif path in [
        "components/services/app_service/public/cpp/app_types.h",
    ]:
        # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/upstream/appservice-include.patch
        clazz = "2005-Debian-upstream-appservice-include"
    elif path in [
        "chrome/browser/lens/lens_overlay/lens_overlay_url_builder.h"
    ]:
        # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/upstream/lens-include.patch
        clazz = "2006-Debian-upstream-lens-optional"
    elif path in [
        "mojo/public/cpp/bindings/lib/bindings_internal.h"
    ]:
        # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/upstream/mojo-bindings-include.patch
        clazz = "2007-Debian-upstream-mojo-bindings-include"
    elif path in [
        "chrome/browser/sync/test/integration/product_specifications_helper.cc",
        "components/commerce/core/product_specifications/product_specifications_service.cc",
        "components/commerce/core/product_specifications/product_specifications_service.h",
        "components/commerce/core/product_specifications/product_specifications_service_unittest.cc",
        "components/commerce/core/product_specifications/product_specifications_set.cc",
        "components/commerce/core/product_specifications/product_specifications_set.h",
        "components/commerce/core/product_specifications/product_specifications_sync_bridge.cc",
        "components/commerce/core/product_specifications/product_specifications_sync_bridge.h",
        "components/commerce/core/product_specifications/product_specifications_sync_bridge_unittest.cc",
        "components/commerce/core/shopping_service.cc",
        "components/commerce/core/shopping_service.h",
        "mojo/public/cpp/base/proto_wrapper.cc"
    ]:
        # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/upstream/no-vector-consts.patch
        clazz = "2008-Debian-upstream-no-vector-consts"
    elif path in [
        "third_party/ruy/src/ruy/profiler/instrumentation.h"
    ]:
        # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/upstream/ruy-include.patch
        clazz = "2009-Debian-upstream-ruy-include"
    elif path in [
        "third_party/vulkan-deps/vulkan-utility-libraries/src/include/vulkan/utility/vk_small_containers.hpp"
    ]:
        # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/upstream/vulkan-include.patch
        clazz = "2010-Debian-upstream-vulkan-include"
    elif path in ["tools/v8_context_snapshot/BUILD.gn", "chrome/BUILD.gn"]:
        # https://issues.chromium.org/issues/40945821
        clazz = "3001-rust-ld-bfd"
    elif path in ["third_party/devtools-frontend/src/scripts/build/rollup.config.js"]:
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
        "third_party/angle/src/libANGLE/renderer/vulkan/FramebufferVk.cpp",
    ]:
        # https://issues.chromium.org/issues/41455655#comment473
        # https://chromium.googlesource.com/angle/angle.git/+/2f934a47e9709cac9ce04d312b7aa496948bced6%5E%21/#F0
        clazz = "3007-replace-powf-with-pow"
    elif path in [
        "content/browser/BUILD.gn",
        "chrome/browser/safe_browsing/BUILD.gn"
    ]:
        # https://bugs.gentoo.org/930112
        # https://bugs.gentoo.org/930107
        # https://gitweb.gentoo.org/repo/gentoo.git/tree/dev-qt/qtwebengine/files/qtwebengine-6.7.0-ninja1.12.patch
        clazz = "3008-fix-ninja-race-condition"
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
