cmake_minimum_required(VERSION 3.22)

project(
  RTTMetricsDeserializer
  LANGUAGES C CXX ASM
  VERSION 1.0.0
  )

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_compile_options(-Wall -Wextra -Wpedantic)

# find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

add_subdirectory(pybind11)
pybind11_add_module(${PROJECT_NAME} main.cpp)
# target_link_libraries(${PROJECT_NAME} PUBLIC pybind11 pybind11::module pybind11::embed)

# Library providing serialization/deserialization using Bitsery
add_subdirectory(bitsery)
target_link_libraries(${PROJECT_NAME} PUBLIC Bitsery::bitsery)

# Library defining accelerometer data structures
add_subdirectory(accelerometer)
target_link_libraries(${PROJECT_NAME} PUBLIC accelerometer)

# Library providing serialization/deserialization API RTT metrics data
add_subdirectory(rtt_metrics)
target_link_libraries(${PROJECT_NAME} PUBLIC rtt_metrics)

add_subdirectory(cobs)
target_link_libraries(${PROJECT_NAME} PUBLIC cobs)

target_sources(${PROJECT_NAME} PRIVATE rtt_deserializer.cpp)