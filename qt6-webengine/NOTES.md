Build qt6 with webengine:

```
make cmake-build
cd cmake-build
cmake .. -G Ninja -DBUILD_qtquick3dphysics=OFF
ninja
```
