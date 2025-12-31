# Development Guide

1. Export the full version string (e.g. `export VERSION=142.0.7444.134`).
2. Download the Chromium tarball

   `wget https://commondatastorage.googleapis.com/chromium-browser-official/chromium-${VERSION}.tar.xz`

3. Extract two identical working copies

   ```
   mkdir a b
   tar -xf chromium-${VERSION}.tar.xz -C a --strip-components=1
   tar -xf chromium-${VERSION}.tar.xz -C b --strip-components=1
   ```

4. Apply and update all patches in the `b` tree.
5. For XNNPACK, regenerate `third_party/xnnpack/BUILD.gn` (see below).
6. Create the patch

   `diff -purN -X exclude a b > chromium-${VERSION}.diff`

7. Post-process

   ```
   python3 format.py chromium-${VERSION}.diff
   python3 split.py
   ```

# Regenerating XNNPACK’s BUILD.gn

1. Start a container with Bazel 8.5.0, e.g.
   `docker run -it --rm -v $(pwd):/src gcr.io/bazel-public/bazel:8.5.0 bash`

2. Inside the container

   ```
   cd /src/third_party/xnnpack
   BAZEL_PATH_OVERRIDE=/usr/local/bin/bazel python3 generate_build_gn.py
   ```

3. If `git cl format` fails, format the file manually:

   `../../buildtools/linux64/gn format BUILD.gn`

