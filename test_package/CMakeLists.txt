cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

find_package(DBus1 REQUIRED)

include_directories(${DBus1_INCLUDE_DIRS})

add_executable(example example.cpp)
target_link_libraries(example ${DBus1_LIBRARIES})
