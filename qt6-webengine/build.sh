#!/bin/bash
mkdir cmake-build
cd cmake-build
cmake .. -G Ninja -DBUILD_qtquick3dphysics=OFF -DQT_BUILD_EXAMPLES=ON
ninja
