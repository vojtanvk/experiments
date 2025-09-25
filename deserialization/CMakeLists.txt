cmake_minimum_required(VERSION 3.22)

project(
  RTT_Metrics_Deserializer
  LANGUAGES C CXX ASM
  VERSION 1.0.0
  )

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_compile_options(-Wall -Wextra -Wpedantic)

add_executable(${PROJECT_NAME} main.cpp)

target_sources(${PROJECT_NAME} PRIVATE 
  main.cpp)

add_subdirectory(bitsery)
target_link_libraries(${PROJECT_NAME} PUBLIC Bitsery::bitsery)

add_subdirectory(accelerometer)
target_link_libraries(${PROJECT_NAME} PUBLIC accelerometer)

add_subdirectory(rtt_metrics)
target_link_libraries(${PROJECT_NAME} PUBLIC rtt_metrics)