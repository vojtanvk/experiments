#pragma once

#include <accelerometer/common_structs.hpp>

/// bitsery includes
#include <bitsery/bitsery.h>
#include <bitsery/adapter/buffer.h>
#include <bitsery/traits/string.h>
#include <bitsery/traits/vector.h>
#include <bitsery/traits/array.h>

namespace accelerometer {
    template <typename S>
    void serialize(S& s, const RawAcceleration & acceleration) {
        s.value2b(acceleration.val[0]);
        s.value2b(acceleration.val[1]);
        s.value2b(acceleration.val[2]);
    }
}