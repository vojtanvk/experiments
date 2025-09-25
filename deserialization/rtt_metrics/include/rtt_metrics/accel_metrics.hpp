#pragma once

#include <accelerometer/common_structs.hpp>

#include <utility>

// bitsery includes
#include <bitsery/bitsery.h>
#include <bitsery/adapter/buffer.h>
#include <bitsery/traits/array.h>
#include <bitsery/brief_syntax/array.h>
#include <bitsery/brief_syntax/variant.h>

namespace accelerometer {
using Buffer = std::array<uint8_t, 6>;
using OutputAdapter = bitsery::OutputBufferAdapter<Buffer>;

template <typename S>
void serialize(S &s, RawAcceleration &data) {
    s.value2b(data.val[0]);
    s.value2b(data.val[1]);
    s.value2b(data.val[2]);
}

template <typename S>
void serialize(S &s, Error &error) {
    s.value1b(std::to_underlying(error));
}

} // namespace accelerometer

namespace rtt_metrics {
void log_accelerometer(int16_t x, int16_t y, int16_t z);
void log_accelerometer_error(accelerometer::Error error);
} // namespace rtt_metrics
