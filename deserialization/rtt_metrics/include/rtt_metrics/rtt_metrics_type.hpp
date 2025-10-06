#pragma once

#include <stdint.h>

namespace rtt_metrics {
    enum class MetricType : uint8_t {
        RawAcceleration = 1,
        RawAccelerationError = 2,
        cnt_ = 3
};
}
