add_library(rtt_metrics INTERFACE)

target_include_directories(rtt_metrics INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(rtt_metrics INTERFACE Bitsery::bitsery)
