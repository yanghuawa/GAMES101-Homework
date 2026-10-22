cmake_minimum_required(VERSION 3.16)
project(hw0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Eigen 在 MSYS2 的 include/eigen3 下，源码里写的是 <eigen3/Eigen/Dense>
include_directories("C:/msys64/mingw64/include")

add_executable(hw0 main.cpp)
