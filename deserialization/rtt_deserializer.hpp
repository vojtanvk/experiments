#pragma once

#include <bitsery/adapter/buffer.h>
#include <bitsery/traits/vector.h>

#include <cstdint>
#include <rtt_metrics/rtt_metrics_type.hpp>
#include <rtt_metrics/accel_metrics.hpp>
#include <accelerometer/common_structs.hpp>
#include <vector>

namespace rtt_metrics {
    using Buffer = std::vector<uint8_t>;
    using InputAdapter = bitsery::InputBufferAdapter<Buffer>;
}

void deserialize_packet(const uint8_t* data, const size_t data_size, std::vector<uint8_t> &out);

accelerometer::RawAcceleration deserialize_raw_acceleration(const std::vector<uint8_t> data);