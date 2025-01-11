export CC=/usr/lib/llvm-19/bin/clang
export CXX=/usr/lib/llvm-19/bin/clang++
export AR=ar
export NM=nm
export RUSTC_BOOTSTRAP=1

mkdir -p third_party/node/linux/node-linux-x64/bin/
ln -svf /usr/bin/node third_party/node/linux/node-linux-x64/bin/node

RUSTC_VERSION="$(rustc --version)"
CLANG_VERSION="$(clang --version | sed -n 's/clang version //p' | cut -d. -f1)"
GNFLAGS=(
    'google_api_key="AIzaSyBGpe01okUSW2GQDIgLovY23Mj1RKzzOOY"'
    'custom_toolchain="//build/toolchain/linux/unbundle:default"'
    'host_toolchain="//build/toolchain/linux/unbundle:default"'
    'is_clang=true'
    'clang_base_path="/usr"'
    'clang_use_chrome_plugins=false'
    "clang_version=\"$CLANG_VERSION\""
    'chrome_pgo_phase=0'
    'is_debug=false'
    'is_official_build=true'
    'fatal_linker_warnings=false'
    'treat_warnings_as_errors=false'
    'disable_fieldtrial_testing_config=true'
    'ffmpeg_branding="Chrome"'
    'proprietary_codecs=true'
    'link_pulseaudio=true'
    'use_cups=true'
    'use_sysroot=false'
    'enable_hangout_services_extension=true'
    'enable_widevine=true'
    'enable_nacl=false'
    'use_vaapi=true'
    'use_cfi_icall=false'
    'use_ozone=true'
    'use_qt=true'
    'use_system_libffi=true'
    'is_cfi=false'
    'ozone_platform_wayland=true'
    'ozone_platform_x11=true'
    'ozone_auto_platforms=true'
    "rustc_version=\"$RUSTC_VERSION\""
    'rust_sysroot_absolute="/usr"'
    'rust_bindgen_root="/usr"'
    'use_lld=true'
    'symbol_level=0'
    'v8_symbol_level=0'
)

gn gen ./out/Release \
    --args="${GNFLAGS[*]}" \
    --script-executable=/usr/bin/python3

ninja \
    --verbose \
    -C ./out/Release \
    chrome chrome_sandbox chromedriver
