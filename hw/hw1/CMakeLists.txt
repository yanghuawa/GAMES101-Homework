cmake_minimum_required(VERSION 3.16)
project(hw1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(OpenCV REQUIRED)

# Eigen 在 MSYS2 的 include/eigen3 下，源码里写的是 <eigen3/Eigen/Eigen>
include_directories("C:/msys64/mingw64/include")
include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(hw1
    main.cpp
    rasterizer.cpp
    rasterizer.hpp
    Triangle.cpp
    Triangle.hpp
)

target_link_libraries(hw1 ${OpenCV_LIBS})
