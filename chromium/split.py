version = "122.0.6261.57"
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
        # https://src.fedoraproject.org/rpms/chromium/tree/rawhide
        if path in [
            "base/allocator/partition_allocator/src/partition_alloc/partition_alloc_base/strings/safe_sprintf.h",
            "third_party/blink/renderer/core/paint/fragment_data_iterator.h",
        ]:
            clazz = "Fedora-chromium-120-nullptr_t-without-namespace-std"
        elif path in ["third_party/blink/renderer/core/BUILD.gn"]:
            clazz = "Fedora-chromium-117-mnemonic-error"
        elif path in ["build/config/compiler/BUILD.gn"]:
            clazz = "Fedora-chromium-120-split-threshold-for-reg-with-hint"
        elif path in [
            "base/check_op.h",
            "base/containers/flat_map.h",
            "base/debug/profiler.h",
            "base/memory/ref_counted.h",
            "chrome/browser/privacy_budget/encountered_surface_tracker.h",
            "chrome/browser/webauthn/authenticator_request_dialog_model.h",
            "chrome/test/chromedriver/chrome/web_view_impl.cc",
            "components/autofill/core/browser/autofill_ablation_study.h",
            "components/crash/core/app/crash_reporter_client.h",
            "components/feature_engagement/internal/event_storage_validator.h",
            "components/feature_engagement/internal/never_event_storage_validator.h",
            "components/omnibox/browser/on_device_head_model.h",
            "components/password_manager/core/browser/generation/password_generator.h",
            "components/payments/content/utility/fingerprint_parser.h",
            "gin/time_clamper.h",
            "gpu/config/gpu_feature_info.h",
            "net/base/net_export.h",
            "pdf/document_attachment_info.h",
            "sandbox/linux/syscall_broker/broker_file_permission.h",
            "services/device/public/cpp/generic_sensor/sensor_reading.h",
            "skia/ext/skcolorspace_trfn.cc",
            "third_party/abseil-cpp/absl/strings/string_view.h",
            "third_party/angle/include/GLSLANG/ShaderVars.h",
            "third_party/blink/public/common/bluetooth/web_bluetooth_device_id.h",
            "third_party/dawn/src/tint/lang/spirv/reader/ast_parser/namer.h",
            "third_party/ipcz/src/ipcz/router_link.h",
            "third_party/material_color_utilities/src/cpp/palettes/tones.cc",
            "third_party/openscreen/src/discovery/dnssd/public/dns_sd_txt_record.h",
            "third_party/pdfium/constants/annotation_flags.h",
            "third_party/ruy/src/ruy/profiler/instrumentation.h",
            "third_party/swiftshader/src/System/LRUCache.hpp",
            "third_party/swiftshader/third_party/llvm-10.0/llvm/lib/Support/Unix/Signals.inc",
            "third_party/tflite/src/tensorflow/lite/kernels/internal/spectrogram.h",
            "third_party/vulkan-deps/vulkan-validation-layers/src/layers/external/vma/vk_mem_alloc.h",
            "third_party/webrtc/audio/utility/channel_mixer.cc",
            "third_party/webrtc/common_video/h264/sps_parser.h",
            "third_party/webrtc/modules/include/module_common_types_public.h",
            "third_party/webrtc/modules/video_coding/utility/ivf_file_reader.cc",
            "ui/base/prediction/kalman_filter.h",
            "ui/gfx/geometry/linear_gradient.h",
            "ui/gfx/linux/drm_util_linux.h",
        ]:
            clazz = "Fedora-chromium-120-missing-header-files"
        elif path in ["optional"]:
            # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/fixes/absl-optional.patch?ref_type=heads
            clazz = "Debian-fixes-absl-optional"
        elif path in ["mojo/public/cpp/bindings/type_converter.h"]:
            # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/fixes/std-to-address.patch?ref_type=heads
            clazz = "Debian-fixes-std-to-address"
        elif path.startswith("base/allocator/partition_allocator/src/partition_alloc"):
            # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/bookworm/undo-internal-alloc.patch?ref_type=heads
            clazz = "Debian-bookworm-undo-internal-alloc"
        elif path in ["components/data_sharing/public/data_sharing_network_loader.h"]:
            # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/upstream/uniqptr.patch?ref_type=heads
            clazz = "Debian-upstream-uniqptr"
        elif path in ["components/plus_addresses/plus_address_types.h"]:
            # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/upstream/optional.patch?ref_type=heads
            clazz = "Debian-upstream-optional"
        elif path in ["components/search_engines/util.h", "components/search_engines/search_engine_choice/search_engine_choice_service.h", "content/common/service_worker/race_network_request_write_buffer_manager.h"]:
            # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/fixes/optional.patch?ref_type=heads
            clazz = "Debian-fixes-optional"
        elif path in ["components/bookmarks/browser/uuid_index.h"]:
            # https://salsa.debian.org/chromium-team/chromium/-/blob/master/debian/patches/upstream/bookmarknode.patch?ref_type=heads
            clazz = "Debian-upstream-bookmarknode"
        elif path in ["build/config/linux/libffi/BUILD.gn"]:
            clazz = "AOSC"
        elif path in ["tools/v8_context_snapshot/BUILD.gn", "chrome/BUILD.gn"]:
            clazz = "rust-ld-bfd"
        elif path in [
            "third_party/devtools-frontend/src/scripts/build/rollup.config.js"
        ]:
            clazz = "rollup"
        elif path in ["build/nocompile.gni", "build/rust/rust_bindgen.gni"]:
            clazz = "fix-invalid-substition-type"
        elif path in [
            "build/config/clang/BUILD.gn",
        ]:
            clazz = "fix-clang-builtins-path"
        elif path in [
            "third_party/libvpx/BUILD.gn",
            "third_party/blink/renderer/platform/BUILD.gn",
            "third_party/blink/renderer/platform/graphics/gpu/webgl_image_conversion.cc",
            "third_party/libvpx/source/config/linux/loongarch/vpx_dsp_rtcd.h",
            "third_party/libvpx/source/config/linux/loongarch/vp8_rtcd.h",
        ]:
            clazz = "loongarch64-clang-no-lsx"
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
            clazz = "loongarch64-swiftshader"
        elif path.startswith("sandbox/"):
            clazz = "loongarch64-sandbox"
        elif path.startswith("third_party/crashpad/"):
            clazz = "loongarch64-crashpad"
        elif path.startswith("third_party/dav1d/"):
            clazz = "loongarch64-dav1d"
        elif path.startswith("third_party/ffmpeg/"):
            clazz = "loongarch64-ffmpeg"
        elif path in [
            "build/rust/rust_target.gni",
        ]:
            clazz = "loongarch64-medium-cmodel"
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
