export CC=clang
export CXX=clang++
export AR=ar
export NM=nm
export RUSTC_BOOTSTRAP=1

mkdir -p third_party/node/linux/node-linux-x64/bin/
ln -sv /usr/bin/node third_party/node/linux/node-linux-x64/bin/node

RUSTC_VERSION="$(rustc --version)"
CLANG_VERSION="$(clang --version | sed -n 's/clang version //p' | cut -d. -f1)"
GNFLAGS=(
    'google_api_key="AIzaSyBGpe01okUSW2GQDIgLovY23Mj1RKzzOOY"'
    'google_default_client_id="1006183841565.apps.googleusercontent.com"'
    'google_default_client_secret="XN6oYWBv7O7w_heXB8TVuldr"'
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
    'fieldtrial_testing_like_official_build=true'
    'ffmpeg_branding="Chrome"'
    'proprietary_codecs=true'
    'link_pulseaudio=true'
    'use_cups=true'
    'use_gnome_keyring=false'
    'use_gold=false'
    'use_sysroot=false'
    'enable_hangout_services_extension=true'
    'enable_widevine=true'
    'enable_nacl=false'
    'use_vaapi=true'
    'use_custom_libcxx=false'
    'use_cfi_icall=false'
    'use_ozone=true'
    'use_qt=true'
    'use_system_libwayland_server=true'
    'use_system_wayland_scanner=true'
    'use_system_libffi=true'
    'use_thin_lto=false'
    'is_cfi=false'
    'ozone_platform_wayland=true'
    'ozone_platform_x11=true'
    'ozone_auto_platforms=true'
    "rustc_version=\"$RUSTC_VERSION\""
    'rust_sysroot_absolute="/usr"'
)

# LLD 17 on loongarch64 does not work
# comment this out on amd64
GNFLAGS+=('use_lld=false')

gn gen ./out/Release \
    --args="${GNFLAGS[*]}" \
    --script-executable=/usr/bin/python3

ninja \
    --verbose \
    -C ./out/Release \
    chrome chrome_sandbox chromedriver
